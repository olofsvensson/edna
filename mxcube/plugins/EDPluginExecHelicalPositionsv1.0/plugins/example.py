import os, sys

EDNA_HOME = os.path.join(os.path.dirname(os.getcwd()),"edna")
os.environ["EDNA_HOME"]=EDNA_HOME
sys.path.append(os.path.join(EDNA_HOME,"kernel","src"))

from EDFactoryPluginStatic import EDFactoryPluginStatic
EDFactoryPluginStatic.loadModule("XSDataHelicalPositionsv1_0")
from XSDataHelicalPositionsv1_0 import XSDataSamplePosition
from XSDataHelicalPositionsv1_0 import XSDataInputCalculateHelicalPositions

pos1 = XSDataSamplePosition()
pos1.sampx = 0.0
pos1.sampy = 0.0
pos1.omegay = 0.0
pos1.omegaz = 0.0

pos2 = XSDataSamplePosition()
pos2.sampx = 0.0
pos2.sampy = 0.0
pos2.omegay = 1.0
pos2.omegaz = 0.0

xsDataInput = XSDataInputCalculateHelicalPositions()
xsDataInput.pos1 = pos1
xsDataInput.pos2 = pos2
xsDataInput.beamsize_y = 0.1
xsDataInput.omega_start = 0.0
xsDataInput.omega_stop = 10.0

edPluginExecHelicalPositions = EDFactoryPluginStatic.loadPlugin("EDPluginExecHelicalPositionsv1_0")
edPluginExecHelicalPositions.dataInput = xsDataInput
edPluginExecHelicalPositions.process()
xsDataOutput = edPluginExecHelicalPositions.dataOutput
for sample_position in xsDataOutput.sample_position:
    print "omega: %10.2f, omegay: %10.2f" % (sample_position.omega, sample_position.omegay)