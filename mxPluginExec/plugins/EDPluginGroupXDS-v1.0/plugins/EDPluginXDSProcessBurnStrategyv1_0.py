#
#    Project: mxPluginExec
#             http://www.edna-site.org
#
#    Copyright (C) 2012 ESRF, Grenoble, France
#
#    Principal authors: Sandor Brockhauser (brockhauser@embl-grenoble.fr)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    and the GNU Lesser General Public License  along with this program.  
#    If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Olof Svensson"
__contact__ = "svensson@esrf.fr"
__license__ = "LGPLv3+"
__copyright__ = "ESRF, Grenoble, France"
__date__ = "20121014"
__status__ = "alpha"


from EDPluginXDSv1_0 import EDPluginXDSv1_0

from XSDataXDSv1_0 import XSDataInputXDSProcessBurnStrategy

class EDPluginXDSProcessBurnStrategyv1_0(EDPluginXDSv1_0):


    def __init__(self):
        EDPluginXDSv1_0.__init__(self)
        self.setXSDataInputClass(XSDataInputXDSProcessBurnStrategy)


    def configure(self):
        EDPluginXDSv1_0.configure(self)
        self.DEBUG("EDPluginXDSIndexingv1_0.configure")
        self.addJob("XYCORR")
        self.addJob("INIT")
        self.addJob("COLSPOT")
        self.addJob("IDXREF")



