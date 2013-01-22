# coding: utf8
#
#    Project: Plugins for MxCuBE
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

__authors__ = "Olof Svensson"
__contact__ = "svensson@esrf.fr"
__license__ = "LGPLv3+"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__date__ = "20130121"
__status__ = "beta"


import os, numpy

from EDVerbose import EDVerbose
from EDTestCasePluginUnit import EDTestCasePluginUnit
from EDUtilsArray import EDUtilsArray

from XSDataHelicalPositionsv1_0 import XSDataInputCalculateHelicalPositions

class EDTestCasePluginUnitExecHelicalPositionsv1_0(EDTestCasePluginUnit):
    """
    Those are all units tests for the EDNA Exec plugin HelicalPositionsv1_0
    """

    def __init__(self, _strTestName = None):
        EDTestCasePluginUnit.__init__(self, "EDPluginExecHelicalPositionsv1_0")
              

    def testCheckParameters(self):
        xsDataInputCalculateHelicalPositions = \
            XSDataInputCalculateHelicalPositions.parseFile(
                os.path.join(self.getPluginTestsDataHome(),
                             "XSDataInputHelicalPositions_useCase1.xml"))
        edPluginExecHelicalPositions = self.createPlugin()
        edPluginExecHelicalPositions.setDataInput(xsDataInputCalculateHelicalPositions)
        edPluginExecHelicalPositions.checkParameters()
        
    
    def process(self):
        self.addTestMethod(self.testCheckParameters)

    
