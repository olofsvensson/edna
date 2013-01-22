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



import math

from EDPluginExec import EDPluginExec

from XSDataHelicalPositionsv1_0 import XSDataSamplePosition
from XSDataHelicalPositionsv1_0 import XSDataInputCalculateHelicalPositions
from XSDataHelicalPositionsv1_0 import XSDataResultCalculateHelicalPositions

class EDPluginExecHelicalPositionsv1_0(EDPluginExec ):
    """
    Calculates motor positions for helical data collections
    """
    

    def __init__(self ):
        EDPluginExec.__init__(self )
        self.setXSDataInputClass(XSDataInputCalculateHelicalPositions)


    def process(self, _edObject = None):
        EDPluginExec.process(self)
        self.DEBUG("EDPluginExecHelicalMotosPositionsv1_0.process")
        self.checkMandatoryParameters(self.dataInput,"Data Input is None")
        self.checkMandatoryParameters(self.dataInput.pos1,"pos1 Data Input is None")
        self.checkMandatoryParameters(self.dataInput.pos2,"pos2 Data Input is None")
        self.checkMandatoryParameters(self.dataInput.omega_start,"omega_start Input is None")
        self.checkMandatoryParameters(self.dataInput.omega_stop,"omega_stop Data Input is None")
        # Check if no positions have been given
        if self.dataInput.no_positions is None:
            self.checkMandatoryParameters(self.dataInput.beamsize_y,
                                          "beamsize_y and no_positions Data Input are None")
            fOmegay1 = self.dataInput.pos1.omegay
            fOmegay2 = self.dataInput.pos2.omegay
            fBeamsizeY = self.dataInput.beamsize_y
            iNoPositions = int(abs(fOmegay2 - fOmegay1) / fBeamsizeY) + 1
        else:
            iNoPositions = self.dataInput.no_positions
        # Calculate positions
        positions = []
        pos1 = self.dataInput.pos1
        pos2 = self.dataInput.pos2
        omega_start = self.dataInput.omega_start
        omega_stop  = self.dataInput.omega_stop
        omega_range = omega_start - omega_stop
        delta_omega =  math.fabs(omega_range / (iNoPositions -1))
        omegay_range = pos1.omegay - pos2.omegay
        #
        hp1_sampx  = (pos1.sampx - pos2.sampx) / omegay_range
        hp1_sampy  = (pos1.sampy - pos2.sampy) / omegay_range
        hp1_omegay =  omegay_range / omega_range
        hp1_omegaz = (pos1.omegaz - pos2.omegaz) / omegay_range
        #
        hp2_sampx  = (pos1.omegay * pos2.sampx - pos2.omegay * pos1.sampx) / omegay_range
        hp2_sampy  = (pos1.omegay * pos2.sampy - pos2.omegay * pos1.sampx) / omegay_range
        hp2_omegay = omega_start * pos2.omegay - omega_stop * pos1.omegay / omega_range 
        hp2_omegaz = pos1.omegay * pos2.omegaz - pos2.omegay * pos2.omegaz / omegay_range
        #
        fOmegaPos = omega_start
        xsDataResultCalculateHelicalPositions = XSDataResultCalculateHelicalPositions()
        for i in range(iNoPositions):
            newPosition = XSDataSamplePosition()
            newPosition.omega = fOmegaPos
            newPosition.omegay = hp1_omegay * fOmegaPos + hp2_omegay
            newPosition.omegaz = hp1_omegaz * fOmegaPos + hp2_omegaz
            newPosition.sampx  = hp1_sampx  * fOmegaPos + hp2_sampx
            newPosition.sampy  = hp1_sampy  * fOmegaPos + hp2_sampy
            fOmegaPos += delta_omega
            xsDataResultCalculateHelicalPositions.addSample_position(newPosition)
        self.setDataOutput(xsDataResultCalculateHelicalPositions)
