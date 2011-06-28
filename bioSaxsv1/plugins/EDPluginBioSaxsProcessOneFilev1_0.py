# coding: utf8
# 
#    Project: BioSaxs
#             http://www.edna-site.org
#
#    File: "$Id$"
#
#    Copyright (C) ESRF
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

"""
ReImplementation of the Reprocess script: Process one file  
( by ricardo.fernandes@esrf.fr)
"""

__author__ = "Jérôme Kieffer"
__license__ = "GPLv3+"
__copyright__ = "ESRF"

import os, sys
from EDVerbose              import EDVerbose
from EDPluginControl        import EDPluginControl
from EDUtilsPlatform        import EDUtilsPlatform
from EDFactoryPluginStatic  import EDFactoryPluginStatic
from XSDataBioSaxsv1_0      import XSDataInputBioSaxsProcessOneFilev1_0, XSDataResultBioSaxsProcessOneFilev1_0, \
                            XSDataString, XSDataFile, XSDataImage, XSDataInteger, \
                            XSDataInputBioSaxsNormalizev1_0, XSDataInputBioSaxsAzimutIntv1_0
from XSDataCommon           import XSDataStatus

class EDPluginBioSaxsProcessOneFilev1_0(EDPluginControl):
    """
    Control plugin that does what was in the Reprocess function in the original program 
    
    """

    def __init__(self):
        """
        """
        EDPluginControl.__init__(self)
        self.setXSDataInputClass(XSDataInputBioSaxsProcessOneFilev1_0)
        self.__strControlledPluginNormalize = "EDPluginBioSaxsNormalizev1_1"
        self.__strControlledPluginIntegrate = "EDPluginBioSaxsAzimutIntv1_1"
        self.__edPluginNormalize = None
        self.__edPluginIntegrate = None

        self.rawImageSize = XSDataInteger(1024)
        self.normalizedImage = None
        self.integratedCurve = None
        self.integratedImage = None
        self.strExecutiveSummary = ""

    def checkParameters(self):
        """
        Checks the mandatory parameters.
        """
        self.DEBUG("EDPluginBioSaxsProcessOneFilev1_0.checkParameters")
        self.checkMandatoryParameters(self.dataInput, "Data Input is None")
        self.checkMandatoryParameters(self.dataInput.rawImage, "No raw image provided")
        self.checkMandatoryParameters(self.dataInput.sample, "No sample information provided")
        self.checkMandatoryParameters(self.dataInput.experimentSetup, "No experimental setup provided")


    def preProcess(self, _edObject=None):
        EDPluginControl.preProcess(self)
        self.DEBUG("EDPluginBioSaxsProcessOneFilev1_0.preProcess")
        # Load the execution plugin
        self.__edPluginNormalize = self.loadPlugin(self.__strControlledPluginNormalize)
        self.__edPluginIntegrate = self.loadPlugin(self.__strControlledPluginIntegrate)
        if self.dataInput.rawImageSize is not None:
            self.rawImageSize = self.dataInput.rawImageSize

    def process(self, _edObject=None):
        EDPluginControl.process(self)
        self.DEBUG("EDPluginBioSaxsProcessOneFilev1_0.process")
        self.__edPluginNormalize.connectSUCCESS(self.doSuccessNormalize)
        self.__edPluginNormalize.connectFAILURE(self.doFailureNormalize)
        xsd = XSDataInputBioSaxsNormalizev1_0()
        xsd.rawImage = self.dataInput.rawImage
        xsd.normalizedImage = self.dataInput.normalizedImage
        xsd.rawImageSize = (self.rawImageSize)
        expe = self.dataInput.experimentSetup
        sample = self.dataInput.sample
        xsd.detector = expe.detector
        xsd.detectorDistance = expe.detectorDistance
        xsd.pixelSize_1 = expe.pixelSize_1
        xsd.pixelSize_2 = expe.pixelSize_2
        xsd.beamCenter_1 = expe.beamCenter_1
        xsd.beamCenter_2 = expe.beamCenter_2
        xsd.beamStopDiode = expe.beamStopDiode
        xsd.wavelength = expe.wavelength
        xsd.machineCurrent = expe.machineCurrent
        xsd.maskFile = expe.maskFile
        xsd.normalizationFactor = expe.normalizationFactor
        xsd.sampleConcentration = sample.sampleConcentration
        xsd.sampleComments = sample.sampleComments
        xsd.sampleCode = sample.sampleCode
        xsd.logFile = self.dataInput.logFile

        self.__edPluginNormalize.dataInput = xsd
        self.__edPluginNormalize.executeSynchronous()
        if self.isFailure():
            return

        self.__edPluginIntegrate.connectSUCCESS(self.doSuccessIntegrate)
        self.__edPluginIntegrate.connectFAILURE(self.doFailureIntegrate)
        xsd = XSDataInputBioSaxsAzimutIntv1_0()
        xsd.normalizedImage = self.dataInput.normalizedImage
        xsd.normalizedImageSize = (self.rawImageSize)
        xsd.integratedImage = self.dataInput.integratedImage
        xsd.integratedCurve = self.dataInput.integratedCurve

        xsd.detector = expe.detector
        xsd.detectorDistance = expe.detectorDistance
        xsd.pixelSize_1 = expe.pixelSize_1
        xsd.pixelSize_2 = expe.pixelSize_2
        xsd.beamCenter_1 = expe.beamCenter_1
        xsd.beamCenter_2 = expe.beamCenter_2
        xsd.beamStopDiode = expe.beamStopDiode
        xsd.wavelength = expe.wavelength
        xsd.machineCurrent = expe.machineCurrent
        xsd.maskFile = expe.maskFile
        xsd.normalizationFactor = expe.normalizationFactor
        xsd.sampleConcentration = sample.sampleConcentration
        xsd.sampleComments = sample.sampleComments
        xsd.sampleCode = sample.sampleCode
        xsd.logFile = self.dataInput.logFile

        self.__edPluginIntegrate.dataInput = xsd
        self.__edPluginIntegrate.executeSynchronous()


    def postProcess(self, _edObject=None):
        EDPluginControl.postProcess(self)
        self.DEBUG("EDPluginBioSaxsProcessOneFilev1_0.postProcess")
        # Create some output data
        xsDataResult = XSDataResultBioSaxsProcessOneFilev1_0()

        xsDataResult.normalizedImage = self.normalizedImage
        xsDataResult.integratedImage = self.integratedImage
        xsDataResult.integratedCurve = self.integratedCurve
        xsDataResult.status = XSDataStatus(executiveSummary=XSDataString(self.strExecutiveSummary))
        self.setDataOutput(xsDataResult)


    def doSuccessNormalize(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsProcessOneFilev1_0.doSuccessNormalize")
        self.retrieveSuccessMessages(_edPlugin, "EDPluginBioSaxsProcessOneFilev1_0.doSuccessNormalize")
        xsdOut = _edPlugin.dataOutput
        self.normalizedImage = xsdOut.normalizedImage
        self.strExecutiveSummary += os.linesep + xsdOut.processLog.value

    def doFailureNormalize(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsProcessOneFilev1_0.doFailureNormalize")
        self.retrieveFailureMessages(_edPlugin, "EDPluginBioSaxsProcessOneFilev1_0.doFailureNormalize")
        try:
            xsdOut = _edPlugin.dataOutput
            self.strExecutiveSummary += os.linesep + xsdOut.processLog.value
        except:
            pass
        self.setFailure()

    def doSuccessIntegrate(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsProcessOneFilev1_0.doSuccessIntegrate")
        self.retrieveSuccessMessages(_edPlugin, "EDPluginBioSaxsProcessOneFilev1_0.doSuccessIntegrate")
        xsdOut = _edPlugin.dataOutput
        self.integratedImage = xsdOut.integratedImage
        self.integratedCurve = xsdOut.integratedCurve
        self.strExecutiveSummary += os.linesep + xsdOut.processLog.value


    def doFailureIntegrate(self, _edPlugin=None):
        self.DEBUG("EDPluginBioSaxsProcessOneFilev1_0.doFailureIntegrate")
        self.retrieveFailureMessages(_edPlugin, "EDPluginBioSaxsProcessOneFilev1_0.doFailureIntegrate")
        try:
            xsdOut = _edPlugin.dataOutput
            self.strExecutiveSummary += os.linesep + xsdOut.processLog.value
            self.integratedImage = xsdOut.integratedImage
            self.integratedCurve = xsdOut.integratedCurve
        except:
            pass
        self.setFailure()