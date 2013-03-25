# coding: utf8
#
#    Project: Time-Resolved EXAFS
#             http://www.edna-site.org
#
#    Copyright (C)      2013 European Synchrotron Radiation Facility
#                            Grenoble, France
#
#    Principal authors:      Olof Svensson (svensson@esrf.fr) 
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

__author__="<author>"
__license__ = "GPLv3+"
__copyright__ = "<copyright>"


import numpy

from EDPluginControl import EDPluginControl
from EDFactoryPluginStatic import EDFactoryPluginStatic
from EDUtilsArray import EDUtilsArray

from XSDataCommon import XSDataString
from XSDataCommon import XSDataInteger

from XSDataTRExafsv1_0 import XSDataInputTRExafs
from XSDataTRExafsv1_0 import XSDataResultTRExafs

EDFactoryPluginStatic.loadModule("XSDataJesfv1_0")
from XSDataJesfv1_0 import XSDataInputJesf

EDFactoryPluginStatic.loadModule("XSDataWriteNexusFilev1_0")
from XSDataWriteNexusFilev1_0 import XSDataNexusAxis
from XSDataWriteNexusFilev1_0 import XSDataNexusArrayGroup
from XSDataWriteNexusFilev1_0 import XSDataInputWriteNexusFile

class EDPluginControlTRExafsv1_0( EDPluginControl ):
    """
    [To be replaced with a description of EDPluginControlTemplatev10]
    """

    def __init__( self ):
        """
        """
        EDPluginControl.__init__(self)
        self.setXSDataInputClass(XSDataInputTRExafs)   
        self.strJesfPluginName = "EDPluginExecJesfv1_0"
        self.strWriteNexusFilePluginName = "EDPluginExecWriteNexusFilev1_0"
        self.edPluginExecJesf = None
        self.listEdPluginExecJesf = []
        
    def process(self, _edObject = None):
        EDPluginControl.process(self)
        self.DEBUG("EDPluginControlTRExafsv1_0.process")
        self.checkMandatoryParameters(self.dataInput, "Data Input is None")
        self.checkMandatoryParameters(self.dataInput.energy, "Data Input 'energy' is None")
        self.checkMandatoryParameters(self.dataInput.dataArray, "Data Input 'dataArray' is None")
        numpyDataArray = EDUtilsArray.xsDataToArray(self.dataInput.dataArray)
        numpyEnergyCalibrationArray = EDUtilsArray.xsDataToArray(self.dataInput.energy)
        # Launch Jesf
        listEdPluginExecJesf = self.launchJesfPlugins(numpyDataArray, numpyEnergyCalibrationArray)
        # Create result data arrays
        dictResultArrays = self.createResultArrays(listEdPluginExecJesf)
        

        
        
    def launchJesfPlugins(self, _numpyDataArray, _numpyEnergyCalibrationArray):
        listEdPluginExecJesf = []
        (iNoRows, iNoColumns) = _numpyDataArray.shape
        # Loop through all the columns of self.numpyInputArray
        for iColumn in range(iNoColumns):
            # Load the execution plugin
            edPluginExecJesf = self.loadPlugin(self.strJesfPluginName) 
#            edPluginExecJesf.connectSUCCESS(self.doSuccessExecTemplate)
#            edPluginExecJesf.connectFAILURE(self.doFailureExecTemplate)
            numpyArrayInputJesf = numpy.ndarray((iNoRows,2))
            numpyArrayInputJesf[:,0] = _numpyEnergyCalibrationArray
            numpyArrayInputJesf[:,1] = _numpyDataArray[:, iColumn]
            print numpyArrayInputJesf
            xsDataInputJesf = XSDataInputJesf()
            xsDataInputJesf.data = EDUtilsArray.arrayToXSData(numpyArrayInputJesf)
#            print xsDataInputJesf.marshal()
            edPluginExecJesf.dataInput = xsDataInputJesf
#            self.edPluginExecJesf.executeSynchronous()
            listEdPluginExecJesf.append([iColumn, edPluginExecJesf])
            edPluginExecJesf.execute()
        # Synchronize all jobs
        self.screen("Synchronizing Jesf jobs")
        for listPlugin in listEdPluginExecJesf:
            listPlugin[1].synchronize()
        return listEdPluginExecJesf

    def createResultArrays(self, _listEdPluginExecJesf):
        # Find the max dimensions for each result array
        dictArray = {}
        iNSpectra = len(_listEdPluginExecJesf)
        iMaxDimFort92 = 0
        iMaxDimFort95 = 0
        iMaxDimFort96 = 0
        iMaxDimFort97 = 0
        iMaxDimFort98 = 0
        iMaxDimFort99 = 0
        for listPlugin in _listEdPluginExecJesf:
            edPluginJesf = listPlugin[1]
            if not edPluginJesf.isFailure():
                xsDataResultJesf = edPluginJesf.dataOutput
                # Fort92
                if xsDataResultJesf.fort92 is not None:
                    xsDataArrayFort92 = xsDataResultJesf.fort92
                    iNelementsFort92 = xsDataArrayFort92.shape[0]
                    if iNelementsFort92 > iMaxDimFort92:
                        iMaxDimFort92 = iNelementsFort92
                # Fort95
                if xsDataResultJesf.fort95 is not None:
                    xsDataArrayFort95 = xsDataResultJesf.fort95
                    iNelementsFort95 = xsDataArrayFort95.shape[0]
                    if iNelementsFort95 > iMaxDimFort95:
                        iMaxDimFort95 = iNelementsFort95
                # Fort96
                if xsDataResultJesf.fort96 is not None:
                    xsDataArrayFort96 = xsDataResultJesf.fort96
                    iNelementsFort96 = xsDataArrayFort96.shape[0]
                    if iNelementsFort96 > iMaxDimFort96:
                        iMaxDimFort96 = iNelementsFort96
                # Fort97
                if xsDataResultJesf.fort97 is not None:
                    xsDataArrayFort97 = xsDataResultJesf.fort97
                    iNelementsFort97 = xsDataArrayFort97.shape[0]
                    if iNelementsFort97 > iMaxDimFort97:
                        iMaxDimFort97 = iNelementsFort97
                # Fort98
                if xsDataResultJesf.fort98 is not None:
                    xsDataArrayFort98 = xsDataResultJesf.fort98
                    iNelementsFort98 = xsDataArrayFort98.shape[0]
                    if iNelementsFort98 > iMaxDimFort98:
                        iMaxDimFort98 = iNelementsFort98
                # Fort99
                if xsDataResultJesf.fort99 is not None:
                    xsDataArrayFort99 = xsDataResultJesf.fort99
                    iNelementsFort99 = xsDataArrayFort99.shape[0]
                    if iNelementsFort99 > iMaxDimFort99:
                        iMaxDimFort99 = iNelementsFort99
        # Create data arrays
        if iMaxDimFort92 > 0:
            print "iMaxDimFort92: %d" % iMaxDimFort92
            numpyDataAxis1Fort92 = numpy.arange((iNSpectra))
            numpyDataAxis2Fort92 = numpy.zeros((iMaxDimFort92))            
            numpyDataArrayFort92 = numpy.zeros((iNSpectra,iMaxDimFort92))
        else:
            numpyDataArrayFort92 = None
        if iMaxDimFort95 > 0:
            print "iMaxDimFort95: %d" % iMaxDimFort95
            numpyDataAxis1Fort95 = numpy.zeros((iNSpectra))
            numpyDataAxis2Fort95 = numpy.zeros((iMaxDimFort95))            
            numpyDataArrayFort95 = numpy.zeros((iNSpectra,iMaxDimFort95))
        else:
            numpyDataArrayFort95 = None
        if iMaxDimFort96 > 0:
            print "iMaxDimFort96: %d" % iMaxDimFort96
            numpyDataAxis1Fort96 = numpy.zeros((iNSpectra))
            numpyDataAxis2Fort96 = numpy.zeros((iMaxDimFort96))            
            numpyDataArrayFort96 = numpy.zeros((iNSpectra,iMaxDimFort96))
        else:
            numpyDataArrayFort96 = None
        if iMaxDimFort97 > 0:
            print "iMaxDimFort97: %d" % iMaxDimFort97
            numpyDataAxis1Fort97 = numpy.zeros((iNSpectra))
            numpyDataAxis2Fort97 = numpy.zeros((iMaxDimFort97))            
            numpyDataArrayFort97 = numpy.zeros((iNSpectra,iMaxDimFort97))
        else:
            numpyDataArrayFort97 = None
        if iMaxDimFort98 > 0:
            print "iMaxDimFort98: %d" % iMaxDimFort98
            numpyDataAxis1Fort98 = numpy.zeros((iNSpectra))
            numpyDataAxis2Fort98 = numpy.zeros((iMaxDimFort98))            
            numpyDataArrayFort98 = numpy.zeros((iNSpectra,iMaxDimFort98))
        else:
            numpyDataArrayFort98 = None
        if iMaxDimFort99 > 0:
            print "iMaxDimFort99: %d" % iMaxDimFort99
            numpyDataAxis1Fort99 = numpy.zeros((iNSpectra))
            numpyDataAxis2Fort99 = numpy.zeros((iMaxDimFort99))            
            numpyDataArrayFort99 = numpy.zeros((iNSpectra,iMaxDimFort99))
        else:
            numpyDataArrayFort99 = None
        # Second loop through results
        for listPlugin in _listEdPluginExecJesf:
            iSpectra = listPlugin[0]
            edPluginJesf = listPlugin[1]
            if not edPluginJesf.isFailure():
                xsDataResultJesf = edPluginJesf.dataOutput
                # Fort92
                if xsDataResultJesf.fort92 is not None:
                    xsDataArrayFort92 = xsDataResultJesf.fort92
                    numpyArrayTmp = EDUtilsArray.xsDataToArray(xsDataArrayFort92)
                    iSizeNumpyArrayTmp = numpyArrayTmp.shape[0]
                    numpyDataAxis2Fort92[0:iSizeNumpyArrayTmp] = numpyArrayTmp[:,0]
                    numpyDataArrayFort92[iSpectra,0:iSizeNumpyArrayTmp] = numpyArrayTmp[:,1]
                    print numpyDataAxis2Fort92
                    print numpyDataArrayFort92
                # Fort95
                if xsDataResultJesf.fort95 is not None:
                    xsDataArrayFort95 = xsDataResultJesf.fort95
                    numpyArrayTmp = EDUtilsArray.xsDataToArray(xsDataArrayFort95)
                    iSizeNumpyArrayTmp = numpyArrayTmp.shape[0]
                    numpyDataArrayFort95[iSpectra,0:iSizeNumpyArrayTmp] = numpyArrayTmp[:,1]
                # Fort96
                if xsDataResultJesf.fort96 is not None:
                    xsDataArrayFort96 = xsDataResultJesf.fort96
                    numpyArrayTmp = EDUtilsArray.xsDataToArray(xsDataArrayFort96)
                    iSizeNumpyArrayTmp = numpyArrayTmp.shape[0]
                    numpyDataArrayFort96[iSpectra,0:iSizeNumpyArrayTmp] = numpyArrayTmp[:,1]
                # Fort97
                if xsDataResultJesf.fort97 is not None:
                    xsDataArrayFort97 = xsDataResultJesf.fort97
                    numpyArrayTmp = EDUtilsArray.xsDataToArray(xsDataArrayFort97)
                    iSizeNumpyArrayTmp = numpyArrayTmp.shape[0]
                    numpyDataArrayFort97[iSpectra,0:iSizeNumpyArrayTmp] = numpyArrayTmp[:,1]
                # Fort98
                if xsDataResultJesf.fort98 is not None:
                    xsDataArrayFort98 = xsDataResultJesf.fort98
                    numpyArrayTmp = EDUtilsArray.xsDataToArray(xsDataArrayFort98)
                    iSizeNumpyArrayTmp = numpyArrayTmp.shape[0]
                    numpyDataArrayFort98[iSpectra,0:iSizeNumpyArrayTmp] = numpyArrayTmp[:,1]
                # Fort99
                if xsDataResultJesf.fort99 is not None:
                    xsDataArrayFort99 = xsDataResultJesf.fort99
                    numpyArrayTmp = EDUtilsArray.xsDataToArray(xsDataArrayFort99)
                    iSizeNumpyArrayTmp = numpyArrayTmp.shape[0]
                    numpyDataArrayFort99[iSpectra,0:iSizeNumpyArrayTmp] = numpyArrayTmp[:,1]
        # Test to store data in nexus file
        xsDataInputWriteNexusFile = XSDataInputWriteNexusFile()
        xsDataInputWriteNexusFile.instrument = XSDataString("ID24")
        xsDataInputWriteNexusFile.outputFileName = XSDataString("id24_test.nxs")
        xsDataNexusArrayGroup = XSDataNexusArrayGroup()
        xsDataNexusArrayGroup.title = XSDataString("data")
        xsDataNexusArrayGroup.long_name = XSDataString("Raw Data")
        xsDataNexusArrayGroup.data = EDUtilsArray.arrayToXSData(numpyDataArrayFort92)
        xsDataNexusArrayGroup.signal = XSDataInteger(1)
        xsDataNexusAxisEnergy = XSDataNexusAxis()
        xsDataNexusAxisEnergy.title = XSDataString("Energy")
        xsDataNexusAxisEnergy.long_name = XSDataString("Energy [eV]")
        xsDataNexusAxisEnergy.primary = XSDataInteger(1)
        xsDataNexusAxisEnergy.axis = XSDataInteger(0)
        xsDataNexusAxisEnergy.units = XSDataString("eV")
        xsDataNexusAxisEnergy.axisData = EDUtilsArray.arrayToXSData(numpyDataAxis2Fort92)
        xsDataNexusArrayGroup.addAxis(xsDataNexusAxisEnergy)
        xsDataNexusAxisSpectra = XSDataNexusAxis()
        xsDataNexusAxisSpectra.title = XSDataString("Spectra")
        xsDataNexusAxisSpectra.long_name = XSDataString("Specta [number]")
        xsDataNexusAxisSpectra.primary = XSDataInteger(2)
        xsDataNexusAxisSpectra.axis = XSDataInteger(1)
        xsDataNexusAxisSpectra.units = XSDataString("number")
        xsDataNexusAxisSpectra.axisData = EDUtilsArray.arrayToXSData(numpyDataAxis1Fort92)
        xsDataNexusArrayGroup.addAxis(xsDataNexusAxisSpectra)
        xsDataInputWriteNexusFile.addNexusGroup(xsDataNexusArrayGroup)
#        print xsDataInputWriteNexusFile.marshal()
        edPluginExecWriteNexusData = self.loadPlugin(self.strWriteNexusFilePluginName)
        edPluginExecWriteNexusData.dataInput = xsDataInputWriteNexusFile
        edPluginExecWriteNexusData.executeSynchronous()
        dictArray["fort92"] = {"axis1" : numpyDataAxis1Fort92,
                               "axis2" : numpyDataAxis2Fort92,
                               "data"  : numpyDataArrayFort92}
#        import pprint
#        pprint.pprint(dictArray)
        dictArray["fort95"] = numpyDataArrayFort95
        dictArray["fort96"] = numpyDataArrayFort96
        dictArray["fort97"] = numpyDataArrayFort97
        dictArray["fort98"] = numpyDataArrayFort98
        dictArray["fort99"] = numpyDataArrayFort99
        return dictArray
    
    def postProcess(self, _edObject = None):
        EDPluginControl.postProcess(self)
        self.DEBUG("EDPluginControlTRExafsv1_0.postProcess")
        # Create some output data
        xsDataResult = XSDataResultTRExafs()
        self.setDataOutput(xsDataResult)
    

    def doSuccessExecTemplate(self,  _edPlugin = None):
        self.DEBUG("EDPluginControlTRExafsv1_0.doSuccessExecTemplate")
        self.retrieveSuccessMessages(_edPlugin, "EDPluginControlTRExafsv1_0.doSuccessExecTemplate")
        self.screen("Run "+_edPlugin.getBaseName()+" ended with success!")


    def doFailureExecTemplate(self,  _edPlugin = None):
        self.DEBUG("EDPluginControlTRExafsv1_0.doFailureExecTemplate")
        self.retrieveFailureMessages(_edPlugin, "EDPluginControlTRExafsv1_0.doFailureExecTemplate")
        self.screen("Run "+_edPlugin.getBaseName()+" ended with failure!")

