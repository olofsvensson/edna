# coding: utf8
#
#    Project: BioSaxs
#             http://www.edna-site.org
#
#    File: "$Id$"
#
#    Copyright (C) 2011, ESRF Grenoble
#
#    Principal author:        Jérôme Kieffer
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import with_statement

__author__ = "Jérôme Kieffer"
__contact__ = "Jerome.kieffer@esrf.fr"
__license__ = "GPLv3+"
__copyright__ = "2011, ESRF Grenoble"
__date__ = "20110921"
__status__ = "Development"

import os, shutil
from EDPluginControl import EDPluginControl
from EDFactoryPluginStatic import EDFactoryPluginStatic
EDFactoryPluginStatic.loadModule("XSDataEdnaSaxs")
EDFactoryPluginStatic.loadModule("XSDataBioSaxsv1_0")
EDFactoryPluginStatic.loadModule("XSDataWaitFilev1_0")
from XSDataCommon       import XSDataString, XSDataStatus, XSDataFile, XSDataTime, XSDataInteger
from XSDataBioSaxsv1_0 import XSDataInputBioSaxsSmartMergev1_0
from XSDataBioSaxsv1_0 import XSDataResultBioSaxsSmartMergev1_0
from XSDataEdnaSaxs     import XSDataInputDatcmp, XSDataInputDataver, XSDataInputAutoRg
from XSDataWaitFilev1_0 import XSDataInputWaitMultiFile


class EDPluginBioSaxsSmartMergev1_1(EDPluginControl):
    """
    This plugin takes a set of input data files (1D SAXS) measure
    their differences (versus previous and versus first) and merge those which are equivalent
    v1.1 adds information from AutoRg
    
    Controled plugins:
     - Execplugins/WaitMultifile
     - EdnaSaxs/Atsas/DatCmp
     - EdnaSaxs/Atsas/DatAver
     - EdnaSaxs/Atsas/AutoRg
    """


    def __init__(self):
        """
        """
        EDPluginControl.__init__(self)
        self.__strControlledPluginDataver = "EDPluginExecDataverv1_0"
        self.__strControlledPluginDatcmp = "EDPluginExecDatcmpv1_0"
        self.__strControlledPluginWaitFile = "EDPluginWaitMultiFile"
        self.__strControlledPluginAutoRG = "EDPluginExecAutoRgv1_0"
        self.__edPluginExecDatcmp = None
        self.__edPluginExecDataver = None
        self.__edPluginExecWaitFile = None
        self.__edPluginExecAutoRg = None
        self.setXSDataInputClass(XSDataInputBioSaxsSmartMergev1_0)
        self.__edPluginExecDatCmp = None
        self.lstInput = []
        self.lstXsdInput = []
        self.absoluteFidelity = None
        self.relativeFidelity = None
        self.dictSimilarities = {} #key: 2-tuple of images, similarities
        self.lstSummary = []
        self.lstStrInput = []

    def checkParameters(self):
        """
        Checks the mandatory parameters.
        """
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.checkParameters")
        self.checkMandatoryParameters(self.dataInput, "Data Input is None")
        self.checkMandatoryParameters(self.dataInput.inputCurves, "Input curve list is empty")
        self.checkMandatoryParameters(self.dataInput.mergedCurve, "Output curve filename  is empty")


    def preProcess(self, _edObject=None):
        EDPluginControl.preProcess(self)
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.preProcess")
        # Load the execution plugin
        if self.dataInput.absoluteFidelity is not None:
            self.absoluteFidelity = self.dataInput.absoluteFidelity.value
        if self.dataInput.relativeFidelity is not None:
            self.relativeFidelity = self.dataInput.relativeFidelity.value
        self.lstInput = self.dataInput.inputCurves
        self.lstStrInput = [i.path.value for i in self.lstInput]
        self.__edPluginExecWaitFile = self.loadPlugin(self.__strControlledPluginWaitFile)


    def process(self, _edObject=None):
        EDPluginControl.process(self)
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.process")

        xsdwf = XSDataInputWaitMultiFile(timeOut=XSDataTime(30),
                                        expectedSize=XSDataInteger(10000),
                                        expectedFile=[XSDataFile(i.path) for i in self.lstInput])
        self.__edPluginExecWaitFile.setDataInput(xsdwf)
        self.__edPluginExecWaitFile.connectFAILURE(self.doFailureExecWait)
        self.__edPluginExecWaitFile.connectSUCCESS(self.doSuccessExecWait)
        self.__edPluginExecWaitFile.executeSynchronous()
        if self.isFailure():
            return
        if len(self.lstInput) == 1:
            shutil.copyfile(self.lstInput[0].path.value, self.dataInput.mergedCurve.path.value)
        else:
            lstFile = []
            if (self.absoluteFidelity is not None) or (self.relativeFidelity is not None):
                if self.absoluteFidelity is not None :
                    for oneFile in self.lstInput[1:]:
                        edPluginExecAbsoluteFidelity = self.loadPlugin(self.__strControlledPluginDatcmp)
                        xsd = XSDataInputDatcmp(inputCurve=[self.lstInput[0], oneFile])
                        edPluginExecAbsoluteFidelity.setDataInput(xsd)
                        edPluginExecAbsoluteFidelity.connectFAILURE(self.doFailureExecDatcmp)
                        edPluginExecAbsoluteFidelity.connectSUCCESS(self.doSuccessExecDatcmp)
                        edPluginExecAbsoluteFidelity.execute()
                if (self.relativeFidelity is not None) and (len(self.lstInput) > 2):
                    for idx, oneFile in enumerate(self.lstInput[2:]):
                        edPluginExecRelativeFidelity = self.loadPlugin(self.__strControlledPluginDatcmp)
                        xsd = XSDataInputDatcmp(inputCurve=[self.lstInput[idx + 1], oneFile])
                        edPluginExecRelativeFidelity.setDataInput(xsd)
                        edPluginExecRelativeFidelity.connectFAILURE(self.doFailureExecDatcmp)
                        edPluginExecRelativeFidelity.connectSUCCESS(self.doSuccessExecDatcmp)
                        edPluginExecRelativeFidelity.execute()
            self.synchronizePlugins()

            for idx, oneFile in enumerate(self.lstInput):
                if idx == 0:
                    lstFile.append(oneFile)
                elif (self.absoluteFidelity is not None) and (self.relativeFidelity is not None):
                    if (self.dictSimilarities[(0, idx)] >= self.absoluteFidelity) and (self.dictSimilarities[(idx - 1, idx)] >= self.relativeFidelity):
                        lstFile.append(oneFile)
                    else:
                        break
                elif (self.absoluteFidelity is not None) :
                    if (self.dictSimilarities[(0, idx)] >= self.absoluteFidelity):
                        lstFile.append(oneFile)
                    else:
                        break
                elif (self.relativeFidelity is not None) :
                    if (self.dictSimilarities[(idx - 1, idx)] >= self.relativeFidelity):
                        lstFile.append(oneFile)
                    else:
                        break
                else:
                    lstFile.append(oneFile)
            self.lstSummary.append("Merging files: " + " ".join([os.path.basename(i.path.value) for i in lstFile]))
            self.__edPluginExecDataver = self.loadPlugin(self.__strControlledPluginDataver)
            xsd = XSDataInputDataver(outputCurve=self.dataInput.mergedCurve,
                                    inputCurve=lstFile)
            self.__edPluginExecDataver.setDataInput(xsd)
            self.__edPluginExecDataver.connectSUCCESS(self.doSuccessExecDataver)
            self.__edPluginExecDataver.connectFAILURE(self.doFailureExecDataver)
            self.__edPluginExecDataver.executeSynchronous()

            if self.isFailure():
                retrun
            self.__edPluginExecAutoRg = self.loadPlugin(self.__strControlledPluginAutoRG)
            xsd = XSDataInputAutoRg(inputCurve=[self.dataInput.mergedCurve])
            self.__edPluginExecAutoRg.setDataInput(xsd)
            self.__edPluginExecAutoRg.connectSUCCESS(self.doSuccessExecAutoRg)
            self.__edPluginExecAutoRg.connectFAILURE(self.doFailureExecAutoRg)
            self.__edPluginExecAutoRg.executeSynchronous()


    def postProcess(self, _edObject=None):
        EDPluginControl.postProcess(self)
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.postProcess")
        # Create some output data
        xsDataResult = XSDataResultBioSaxsSmartMergev1_0()
        xsDataResult.mergedCurve = self.dataInput.mergedCurve
        executiveSummary = os.linesep.join(self.lstSummary)
        xsDataResult.status = XSDataStatus(executiveSummary=XSDataString(executiveSummary))
        self.setDataOutput(xsDataResult)
        self.DEBUG(executiveSummary)


    def doSuccessExecWait(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.doSuccessExecWait")
        self.retrieveSuccessMessages(_edPlugin, "EDPluginBioSaxsSmartMergev1_0.doSuccessExecWait")
        xsdo = _edPlugin.dataOutput
        if (xsdo.timedOut is not None) and  bool(xsdo.timedOut.value):
            strErr = "Error in waiting for all input files to arrive"
            self.ERROR(strErr)
            self.setFailure()


    def doFailureExecWait(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.doFailureExecWait")
        self.retrieveFailureMessages(_edPlugin, "EDPluginBioSaxsSmartMergev1_0.doFailureExecWait")
        strErr = "Error in waiting for all input files to arrive"
        self.ERROR(strErr)
        self.setFailure()


    def doSuccessExecDataver(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.doSuccessExecDataver")
        self.retrieveSuccessMessages(_edPlugin, "EDPluginBioSaxsSmartMergev1_0.doSuccessExecDataver")


    def doFailureExecDataver(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.doFailureExecDataver")
        self.retrieveFailureMessages(_edPlugin, "EDPluginBioSaxsSmartMergev1_0.doFailureExecDataver")
        strErr = "Error in Processing of Atsas 'dataver'"
        self.ERROR(strErr)
        self.setFailure()


    def doSuccessExecDatcmp(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.doSuccessExecDatcmp")
        self.retrieveSuccessMessages(_edPlugin, "EDPluginBioSaxsSmartMergev1_0.doSuccessExecDatcmp")
        with self.locked():
            xsdIn = _edPlugin.dataInput
            xsdOut = _edPlugin.getDataOutput()
            file0 = xsdIn.inputCurve[0].path.value
            file1 = xsdIn.inputCurve[1].path.value
            fidelity = xsdOut.fidelity.value
            self.dictSimilarities[(self.lstStrInput.index(file0), self.lstStrInput.index(file1))] = fidelity
            self.lstSummary.append("Fidelity between %s and %s is %s" % (os.path.basename(file0), os.path.basename(file1), fidelity))


    def doFailureExecDatcmp(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.doFailureExecDatcmp")
        self.retrieveFailureMessages(_edPlugin, "EDPluginBioSaxsSmartMergev1_0.doFailureExecDatcmp")
        self.setFailure()


    def doSuccessExecAutoRg(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.doSuccessExecAutoRg")
        self.retrieveSuccessMessages(_edPlugin, "EDPluginBioSaxsSmartMergev1_0.doSuccessExecAutoRg")
        xsdOut = _edPlugin.dataOutput
        if len(xsdOut.autoRgOut) > 0:
            res = _edPlugin.dataOutput.autoRgOut[0]
            self.lstSummary.append("AutoRg: Rg   =   %.4f +/- %.2f ( %.1f%%)" % (res.rg.value, res.rgStdev.value, 100. * res.rgStdev.value / res.rg.value))
            self.lstSummary.append("AutoRg: I(0) =   %.2f +/- %.4f" % (res.i0.value, res.i0Stdev.value))
            self.lstSummary.append("AutoRg: Points   %i to %i ( %i total)" % (res.firstPointUsed.value, res.lastPointUsed.value , 1 + res.lastPointUsed.value - res.firstPointUsed.value))
            self.lstSummary.append("AutoRg: Quality: %.1f%%" % (res.quality.value * 100.0))
            self.autoRg = res

    def doFailureExecAutoRg(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsSmartMergev1_0.doFailureExecAutoRg")
        self.retrieveFailureMessages(_edPlugin, "EDPluginBioSaxsSmartMergev1_0.doFailureExecAutoRg")
        strErr = "Error in Processing of Atsas 'AutoRg'"
        self.ERROR(strErr)
        self.setFailure()

