# coding: utf8
# 
#    Project: bioSaxs
#             http://www.edna-site.org
#
#    File: "$Id$"
#
#    Copyright (C) ESRF
#
#    Principal author:       Jérôme Kieffer
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

__author__ = "Jérôme Kieffer"
__license__ = "GPLv3+"
__copyright__ = "ESRF"

import os, sys
from EDVerbose                           import EDVerbose
from EDAssert                            import EDAssert
from EDTestCasePluginExecute             import EDTestCasePluginExecute
from XSDataBioSaxsv1_0                   import  XSDataResultBioSaxsMetadatav1_0
from EDFactoryPluginStatic               import EDFactoryPluginStatic


# Needed for loading the plugin...
EDFactoryPluginStatic.loadModule("EDInstallNumpyv1_3")
EDFactoryPluginStatic.loadModule("EDInstallPILv1_1_7")
EDFactoryPluginStatic.loadModule("EDInstallFabio_v0_0_7")
import fabio


class EDTestCasePluginExecuteBioSaxsMetadatav1_1(EDTestCasePluginExecute):


    def __init__(self, _strTestName=None):
        EDTestCasePluginExecute.__init__(self, "EDPluginBioSaxsMetadatav1_1")
#        self.setConfigurationFile(os.path.join(self.getPluginTestsDataHome(),
#                                               "XSConfiguration_BioSaxsMetadata.xml"))
        self.setDataInputFile(os.path.join(self.getPluginTestsDataHome(), \
                                           "XSDataInputBioSaxsMetadata_reference.xml"))
        self.setReferenceDataOutputFile(os.path.join(self.getPluginTestsDataHome(), \
                                                     "XSDataResultBioSaxsMetadata_referencev1_1.xml"))

        self.outputImage = None

    def preProcess(self):
        """
        PreProcess of the execution test: download a set of images  from http://www.edna-site.org
        and remove any existing output file 
        """
        EDTestCasePluginExecute.preProcess(self)
        self.loadTestImage([ "bioSaxsRaw.edf", "bioSaxsMetadata.edf"])
        strExpectedOutput = self.readAndParseFile (self.getReferenceDataOutputFile())
        EDVerbose.DEBUG("strExpectedOutput:" + strExpectedOutput)
        xsDataResultReference = XSDataResultBioSaxsMetadatav1_0.parseString(strExpectedOutput)
        self.outputImage = xsDataResultReference.getOutputImage().getPath().value
        EDVerbose.DEBUG("Output file is %s" % self.outputImage)
        if not os.path.isdir(os.path.dirname(self.outputImage)):
            os.makedirs(os.path.dirname(self.outputImage))
        if os.path.isfile(self.outputImage):
            EDVerbose.DEBUG(" Output Image file exists %s, I will remove it" % self.outputImage)
            os.remove(self.outputImage)



    def testExecute(self):
        """
        """
        self.run()
        plugin = self.getPlugin()
 ################################################################################
# Compare XSDataResults
################################################################################

        strExpectedOutput = self.readAndParseFile (self.getReferenceDataOutputFile())
#        strObtainedOutput = self.readAndParseFile (self.m_edObtainedOutputDataFile)
        EDVerbose.DEBUG("Checking obtained result...")
        xsDataResultReference = XSDataResultBioSaxsMetadatav1_0.parseString(strExpectedOutput)
        xsDataResultObtained = plugin.getDataOutput()
        EDAssert.strAlmostEqual(xsDataResultReference.marshal(), xsDataResultObtained.marshal(), "XSDataResult output are the same", _strExcluded="bioSaxs")

################################################################################
# Compare dictionary
################################################################################
        edfRef = fabio.open(xsDataResultObtained.getOutputImage().getPath().value)
        edfObt = fabio.open(os.path.join(self.getTestsDataImagesHome(), "bioSaxsMetadata.edf"))
        keysRef = edfRef.header_keys
        keysObt = edfObt.header_keys
        keysRef.sort()
        keysObt.sort()

        for key in ["HeaderID", "Image", 'EDF_BinarySize', "EDF_DataBlockID", "EDF_HeaderSize", "filename", "RasterOrientation" ]:
            if key in keysObt: keysObt.remove(key)
            if key in keysRef: keysRef.remove(key)
#        print edfObt.header
        EDAssert.equal(keysRef, keysObt, _strComment="Same keys in the header dictionary")
        for key in keysRef:
            EDAssert.strAlmostEqual(edfRef.header[key], edfObt.header[key], _strComment="header value %s are the same" % key, _strExcluded="bioSaxs")


################################################################################
# Compare images 
################################################################################

        outputData = edfObt.data
        referenceData = edfRef.data
        EDAssert.arraySimilar(outputData, referenceData , _fAbsMaxDelta=0.1, _fScaledMaxDelta=0.05, _strComment="Images-data are the same")






    def process(self):
        """
        """
        self.addTestMethod(self.testExecute)




if __name__ == '__main__':

    edTestCasePluginExecuteBioSaxsMetadatav1_0 = EDTestCasePluginExecuteBioSaxsMetadatav1_1("EDTestCasePluginExecuteBioSaxsMetadatav1_1")
    edTestCasePluginExecuteBioSaxsMetadatav1_0.execute()
