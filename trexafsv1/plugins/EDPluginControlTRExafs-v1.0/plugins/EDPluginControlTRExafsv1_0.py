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
from EDUtilsFile import EDUtilsFile
from EDFactoryPluginStatic import EDFactoryPluginStatic
from EDUtilsArray import EDUtilsArray

from XSDataTRExafsv1_0 import XSDataInputTRExafs
from XSDataTRExafsv1_0 import XSDataResultTRExafs

EDFactoryPluginStatic.loadModule("XSDataJesfv1_0")
from XSDataJesfv1_0 import XSDataInputJesf

class EDPluginControlTRExafsv1_0( EDPluginControl ):
    """
    [To be replaced with a description of EDPluginControlTemplatev10]
    """

    def __init__( self ):
        """
        """
        EDPluginControl.__init__(self)
        self.setXSDataInputClass(XSDataInputTRExafs)   
        self.strControlledPluginName = "EDPluginExecJesfv1_0"
        self.edPluginExecJesf = None
        
    def process(self, _edObject = None):
        EDPluginControl.process(self)
        self.DEBUG("EDPluginControlTRExafsv1_0.process")
        self.checkMandatoryParameters(self.dataInput, "Data Input is None")
        self.checkMandatoryParameters(self.dataInput.energy, "Data Input 'energy' is None")
        self.checkMandatoryParameters(self.dataInput.dataArray, "Data Input 'dataArray' is None")
        numpyDataArray = EDUtilsArray.xsDataToArray(self.dataInput.dataArray)
        numpyEnergyCalibrationArray = EDUtilsArray.xsDataToArray(self.dataInput.energy)
        # Loop through all the columns of self.numpyInputArray
        (iNoRows, iNoColumns) = numpyDataArray.shape
        for iColumn in range(iNoColumns):
            # Load the execution plugin
            self.edPluginExecJesf = self.loadPlugin(self.strControlledPluginName) 
            self.edPluginExecJesf.connectSUCCESS(self.doSuccessExecTemplate)
            self.edPluginExecJesf.connectFAILURE(self.doFailureExecTemplate)
            numpyArrayInputJesf = numpy.ndarray((iNoRows,2))
            numpyArrayInputJesf[:,0] = numpyEnergyCalibrationArray
            numpyArrayInputJesf[:,1] = numpyDataArray[:, iColumn]
            xsDataInputJesf = XSDataInputJesf()
            xsDataInputJesf.data = EDUtilsArray.arrayToXSData(numpyArrayInputJesf)
            print xsDataInputJesf.marshal()
            self.edPluginExecJesf.dataInput = xsDataInputJesf
            self.edPluginExecJesf.executeSynchronous()

    
    def postProcess(self, _edObject = None):
        EDPluginControl.postProcess(self)
        self.DEBUG("EDPluginControlTRExafsv1_0.postProcess")
        # Create some output data
        xsDataResult = XSDataResultTRExafs()
        self.setDataOutput(xsDataResult)
    

    def doSuccessExecTemplate(self,  _edPlugin = None):
        self.DEBUG("EDPluginControlTRExafsv1_0.doSuccessExecTemplate")
        self.retrieveSuccessMessages(_edPlugin, "EDPluginControlTRExafsv1_0.doSuccessExecTemplate")


    def doFailureExecTemplate(self,  _edPlugin = None):
        self.DEBUG("EDPluginControlTRExafsv1_0.doFailureExecTemplate")
        self.retrieveFailureMessages(_edPlugin, "EDPluginControlTRExafsv1_0.doFailureExecTemplate")

