#!/usr/bin/env python

#
# Generated Mon Jan 21 03:45::43 2013 by EDGenerateDS.
#

import os, sys
from xml.dom import minidom
from xml.dom import Node


strEdnaHome = os.environ.get("EDNA_HOME", None)

dictLocation = { \
 "XSDataCommon": "kernel/datamodel", \
 "XSDataCommon": "kernel/datamodel", \
 "XSDataCommon": "kernel/datamodel", \
}

try:
    from XSDataCommon import XSData
    from XSDataCommon import XSDataInput
    from XSDataCommon import XSDataResult
except ImportError as error:
    if strEdnaHome is not None:
        for strXsdName in dictLocation:
            strXsdModule = strXsdName + ".py"
            strRootdir = os.path.dirname(os.path.abspath(os.path.join(strEdnaHome, dictLocation[strXsdName])))
            for strRoot, listDirs, listFiles in os.walk(strRootdir):
                if strXsdModule in listFiles:
                    sys.path.append(strRoot)
    else:
        raise error
from XSDataCommon import XSData
from XSDataCommon import XSDataInput
from XSDataCommon import XSDataResult




#
# Support/utility functions.
#

# Compabiltity between Python 2 and 3:
if sys.version.startswith('3'):
    unicode = str
    from io import StringIO
else:
    from StringIO import StringIO


def showIndent(outfile, level):
    for idx in range(level):
        outfile.write(unicode('    '))


def warnEmptyAttribute(_strName, _strTypeName):
    pass
    #if not _strTypeName in ["float", "double", "string", "boolean", "integer"]:
    #    print("Warning! Non-optional attribute %s of type %s is None!" % (_strName, _strTypeName))

class MixedContainer(object):
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:     # category == MixedContainer.CategoryComplex
            self.value.export(outfile, level, name)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write(unicode('<%s>%s</%s>' % (self.name, self.value, self.name)))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write(unicode('<%s>%d</%s>' % (self.name, self.value, self.name)))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write(unicode('<%s>%f</%s>' % (self.name, self.value, self.name)))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write(unicode('<%s>%g</%s>' % (self.name, self.value, self.name)))

#
# Data representation classes.
#



class XSDataSamplePosition(XSData):
    def __init__(self, omegaz=None, omegay=None, sampy=None, sampx=None, omega=None):
        XSData.__init__(self, )
        if omega is None:
            self._omega = None
        else:
            self._omega = float(omega)
        if sampx is None:
            self._sampx = None
        else:
            self._sampx = float(sampx)
        if sampy is None:
            self._sampy = None
        else:
            self._sampy = float(sampy)
        if omegay is None:
            self._omegay = None
        else:
            self._omegay = float(omegay)
        if omegaz is None:
            self._omegaz = None
        else:
            self._omegaz = float(omegaz)
    # Methods and properties for the 'omega' attribute
    def getOmega(self): return self._omega
    def setOmega(self, omega):
        if omega is None:
            self._omega = None
        else:
            self._omega = float(omega)
    def delOmega(self): self._omega = None
    omega = property(getOmega, setOmega, delOmega, "Property for omega")
    # Methods and properties for the 'sampx' attribute
    def getSampx(self): return self._sampx
    def setSampx(self, sampx):
        if sampx is None:
            self._sampx = None
        else:
            self._sampx = float(sampx)
    def delSampx(self): self._sampx = None
    sampx = property(getSampx, setSampx, delSampx, "Property for sampx")
    # Methods and properties for the 'sampy' attribute
    def getSampy(self): return self._sampy
    def setSampy(self, sampy):
        if sampy is None:
            self._sampy = None
        else:
            self._sampy = float(sampy)
    def delSampy(self): self._sampy = None
    sampy = property(getSampy, setSampy, delSampy, "Property for sampy")
    # Methods and properties for the 'omegay' attribute
    def getOmegay(self): return self._omegay
    def setOmegay(self, omegay):
        if omegay is None:
            self._omegay = None
        else:
            self._omegay = float(omegay)
    def delOmegay(self): self._omegay = None
    omegay = property(getOmegay, setOmegay, delOmegay, "Property for omegay")
    # Methods and properties for the 'omegaz' attribute
    def getOmegaz(self): return self._omegaz
    def setOmegaz(self, omegaz):
        if omegaz is None:
            self._omegaz = None
        else:
            self._omegaz = float(omegaz)
    def delOmegaz(self): self._omegaz = None
    omegaz = property(getOmegaz, setOmegaz, delOmegaz, "Property for omegaz")
    def export(self, outfile, level, name_='XSDataSamplePosition'):
        showIndent(outfile, level)
        outfile.write(unicode('<%s>\n' % name_))
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write(unicode('</%s>\n' % name_))
    def exportChildren(self, outfile, level, name_='XSDataSamplePosition'):
        XSData.exportChildren(self, outfile, level, name_)
        if self._omega is not None:
            showIndent(outfile, level)
            outfile.write(unicode('<omega>%e</omega>\n' % self._omega))
        if self._sampx is not None:
            showIndent(outfile, level)
            outfile.write(unicode('<sampx>%e</sampx>\n' % self._sampx))
        else:
            warnEmptyAttribute("sampx", "double")
        if self._sampy is not None:
            showIndent(outfile, level)
            outfile.write(unicode('<sampy>%e</sampy>\n' % self._sampy))
        else:
            warnEmptyAttribute("sampy", "double")
        if self._omegay is not None:
            showIndent(outfile, level)
            outfile.write(unicode('<omegay>%e</omegay>\n' % self._omegay))
        else:
            warnEmptyAttribute("omegay", "double")
        if self._omegaz is not None:
            showIndent(outfile, level)
            outfile.write(unicode('<omegaz>%e</omegaz>\n' % self._omegaz))
        else:
            warnEmptyAttribute("omegaz", "double")
    def build(self, node_):
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'omega':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    fval_ = float(sval_)
                except ValueError:
                    raise ValueError('requires float (or double) -- %s' % child_.toxml())
                self._omega = fval_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sampx':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    fval_ = float(sval_)
                except ValueError:
                    raise ValueError('requires float (or double) -- %s' % child_.toxml())
                self._sampx = fval_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sampy':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    fval_ = float(sval_)
                except ValueError:
                    raise ValueError('requires float (or double) -- %s' % child_.toxml())
                self._sampy = fval_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'omegay':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    fval_ = float(sval_)
                except ValueError:
                    raise ValueError('requires float (or double) -- %s' % child_.toxml())
                self._omegay = fval_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'omegaz':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    fval_ = float(sval_)
                except ValueError:
                    raise ValueError('requires float (or double) -- %s' % child_.toxml())
                self._omegaz = fval_
        XSData.buildChildren(self, child_, nodeName_)
    #Method for marshalling an object
    def marshal( self ):
        oStreamString = StringIO()
        oStreamString.write(unicode('<?xml version="1.0" ?>\n'))
        self.export( oStreamString, 0, name_="XSDataSamplePosition" )
        oStringXML = oStreamString.getvalue()
        oStreamString.close()
        return oStringXML
    #Only to export the entire XML tree to a file stream on disk
    def exportToFile( self, _outfileName ):
        outfile = open( _outfileName, "w" )
        outfile.write(unicode('<?xml version=\"1.0\" ?>\n'))
        self.export( outfile, 0, name_='XSDataSamplePosition' )
        outfile.close()
    #Deprecated method, replaced by exportToFile
    def outputFile( self, _outfileName ):
        print("WARNING: Method outputFile in class XSDataSamplePosition is deprecated, please use instead exportToFile!")
        self.exportToFile(_outfileName)
    #Method for making a copy in a new instance
    def copy( self ):
        return XSDataSamplePosition.parseString(self.marshal())
    #Static method for parsing a string
    def parseString( _inString ):
        doc = minidom.parseString(_inString)
        rootNode = doc.documentElement
        rootObj = XSDataSamplePosition()
        rootObj.build(rootNode)
        # Check that all minOccurs are obeyed by marshalling the created object
        oStreamString = StringIO()
        rootObj.export( oStreamString, 0, name_="XSDataSamplePosition" )
        oStreamString.close()
        return rootObj
    parseString = staticmethod( parseString )
    #Static method for parsing a file
    def parseFile( _inFilePath ):
        doc = minidom.parse(_inFilePath)
        rootNode = doc.documentElement
        rootObj = XSDataSamplePosition()
        rootObj.build(rootNode)
        return rootObj
    parseFile = staticmethod( parseFile )
# end class XSDataSamplePosition


class XSDataInputCalculateHelicalPositions(XSDataInput):
    def __init__(self, configuration=None, no_positions=None, beamsize_y=None, omega_stop=None, omega_start=None, pos2=None, pos1=None):
        XSDataInput.__init__(self, configuration)
        if pos1 is None:
            self._pos1 = None
        elif pos1.__class__.__name__ == "XSDataSamplePosition":
            self._pos1 = pos1
        else:
            strMessage = "ERROR! XSDataInputCalculateHelicalPositions constructor argument 'pos1' is not XSDataSamplePosition but %s" % self._pos1.__class__.__name__
            raise BaseException(strMessage)
        if pos2 is None:
            self._pos2 = None
        elif pos2.__class__.__name__ == "XSDataSamplePosition":
            self._pos2 = pos2
        else:
            strMessage = "ERROR! XSDataInputCalculateHelicalPositions constructor argument 'pos2' is not XSDataSamplePosition but %s" % self._pos2.__class__.__name__
            raise BaseException(strMessage)
        if omega_start is None:
            self._omega_start = None
        else:
            self._omega_start = float(omega_start)
        if omega_stop is None:
            self._omega_stop = None
        else:
            self._omega_stop = float(omega_stop)
        if beamsize_y is None:
            self._beamsize_y = None
        else:
            self._beamsize_y = float(beamsize_y)
        if no_positions is None:
            self._no_positions = None
        else:
            self._no_positions = int(no_positions)
    # Methods and properties for the 'pos1' attribute
    def getPos1(self): return self._pos1
    def setPos1(self, pos1):
        if pos1 is None:
            self._pos1 = None
        elif pos1.__class__.__name__ == "XSDataSamplePosition":
            self._pos1 = pos1
        else:
            strMessage = "ERROR! XSDataInputCalculateHelicalPositions.setPos1 argument is not XSDataSamplePosition but %s" % pos1.__class__.__name__
            raise BaseException(strMessage)
    def delPos1(self): self._pos1 = None
    pos1 = property(getPos1, setPos1, delPos1, "Property for pos1")
    # Methods and properties for the 'pos2' attribute
    def getPos2(self): return self._pos2
    def setPos2(self, pos2):
        if pos2 is None:
            self._pos2 = None
        elif pos2.__class__.__name__ == "XSDataSamplePosition":
            self._pos2 = pos2
        else:
            strMessage = "ERROR! XSDataInputCalculateHelicalPositions.setPos2 argument is not XSDataSamplePosition but %s" % pos2.__class__.__name__
            raise BaseException(strMessage)
    def delPos2(self): self._pos2 = None
    pos2 = property(getPos2, setPos2, delPos2, "Property for pos2")
    # Methods and properties for the 'omega_start' attribute
    def getOmega_start(self): return self._omega_start
    def setOmega_start(self, omega_start):
        if omega_start is None:
            self._omega_start = None
        else:
            self._omega_start = float(omega_start)
    def delOmega_start(self): self._omega_start = None
    omega_start = property(getOmega_start, setOmega_start, delOmega_start, "Property for omega_start")
    # Methods and properties for the 'omega_stop' attribute
    def getOmega_stop(self): return self._omega_stop
    def setOmega_stop(self, omega_stop):
        if omega_stop is None:
            self._omega_stop = None
        else:
            self._omega_stop = float(omega_stop)
    def delOmega_stop(self): self._omega_stop = None
    omega_stop = property(getOmega_stop, setOmega_stop, delOmega_stop, "Property for omega_stop")
    # Methods and properties for the 'beamsize_y' attribute
    def getBeamsize_y(self): return self._beamsize_y
    def setBeamsize_y(self, beamsize_y):
        if beamsize_y is None:
            self._beamsize_y = None
        else:
            self._beamsize_y = float(beamsize_y)
    def delBeamsize_y(self): self._beamsize_y = None
    beamsize_y = property(getBeamsize_y, setBeamsize_y, delBeamsize_y, "Property for beamsize_y")
    # Methods and properties for the 'no_positions' attribute
    def getNo_positions(self): return self._no_positions
    def setNo_positions(self, no_positions):
        if no_positions is None:
            self._no_positions = None
        else:
            self._no_positions = int(no_positions)
    def delNo_positions(self): self._no_positions = None
    no_positions = property(getNo_positions, setNo_positions, delNo_positions, "Property for no_positions")
    def export(self, outfile, level, name_='XSDataInputCalculateHelicalPositions'):
        showIndent(outfile, level)
        outfile.write(unicode('<%s>\n' % name_))
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write(unicode('</%s>\n' % name_))
    def exportChildren(self, outfile, level, name_='XSDataInputCalculateHelicalPositions'):
        XSDataInput.exportChildren(self, outfile, level, name_)
        if self._pos1 is not None:
            self.pos1.export(outfile, level, name_='pos1')
        else:
            warnEmptyAttribute("pos1", "XSDataSamplePosition")
        if self._pos2 is not None:
            self.pos2.export(outfile, level, name_='pos2')
        else:
            warnEmptyAttribute("pos2", "XSDataSamplePosition")
        if self._omega_start is not None:
            showIndent(outfile, level)
            outfile.write(unicode('<omega_start>%e</omega_start>\n' % self._omega_start))
        else:
            warnEmptyAttribute("omega_start", "double")
        if self._omega_stop is not None:
            showIndent(outfile, level)
            outfile.write(unicode('<omega_stop>%e</omega_stop>\n' % self._omega_stop))
        else:
            warnEmptyAttribute("omega_stop", "double")
        if self._beamsize_y is not None:
            showIndent(outfile, level)
            outfile.write(unicode('<beamsize_y>%e</beamsize_y>\n' % self._beamsize_y))
        if self._no_positions is not None:
            showIndent(outfile, level)
            outfile.write(unicode('<no_positions>%d</no_positions>\n' % self._no_positions))
    def build(self, node_):
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'pos1':
            obj_ = XSDataSamplePosition()
            obj_.build(child_)
            self.setPos1(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'pos2':
            obj_ = XSDataSamplePosition()
            obj_.build(child_)
            self.setPos2(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'omega_start':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    fval_ = float(sval_)
                except ValueError:
                    raise ValueError('requires float (or double) -- %s' % child_.toxml())
                self._omega_start = fval_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'omega_stop':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    fval_ = float(sval_)
                except ValueError:
                    raise ValueError('requires float (or double) -- %s' % child_.toxml())
                self._omega_stop = fval_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'beamsize_y':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    fval_ = float(sval_)
                except ValueError:
                    raise ValueError('requires float (or double) -- %s' % child_.toxml())
                self._beamsize_y = fval_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'no_positions':
            if child_.firstChild:
                sval_ = child_.firstChild.nodeValue
                try:
                    ival_ = int(sval_)
                except ValueError:
                    raise ValueError('requires integer -- %s' % child_.toxml())
                self._no_positions = ival_
        XSDataInput.buildChildren(self, child_, nodeName_)
    #Method for marshalling an object
    def marshal( self ):
        oStreamString = StringIO()
        oStreamString.write(unicode('<?xml version="1.0" ?>\n'))
        self.export( oStreamString, 0, name_="XSDataInputCalculateHelicalPositions" )
        oStringXML = oStreamString.getvalue()
        oStreamString.close()
        return oStringXML
    #Only to export the entire XML tree to a file stream on disk
    def exportToFile( self, _outfileName ):
        outfile = open( _outfileName, "w" )
        outfile.write(unicode('<?xml version=\"1.0\" ?>\n'))
        self.export( outfile, 0, name_='XSDataInputCalculateHelicalPositions' )
        outfile.close()
    #Deprecated method, replaced by exportToFile
    def outputFile( self, _outfileName ):
        print("WARNING: Method outputFile in class XSDataInputCalculateHelicalPositions is deprecated, please use instead exportToFile!")
        self.exportToFile(_outfileName)
    #Method for making a copy in a new instance
    def copy( self ):
        return XSDataInputCalculateHelicalPositions.parseString(self.marshal())
    #Static method for parsing a string
    def parseString( _inString ):
        doc = minidom.parseString(_inString)
        rootNode = doc.documentElement
        rootObj = XSDataInputCalculateHelicalPositions()
        rootObj.build(rootNode)
        # Check that all minOccurs are obeyed by marshalling the created object
        oStreamString = StringIO()
        rootObj.export( oStreamString, 0, name_="XSDataInputCalculateHelicalPositions" )
        oStreamString.close()
        return rootObj
    parseString = staticmethod( parseString )
    #Static method for parsing a file
    def parseFile( _inFilePath ):
        doc = minidom.parse(_inFilePath)
        rootNode = doc.documentElement
        rootObj = XSDataInputCalculateHelicalPositions()
        rootObj.build(rootNode)
        return rootObj
    parseFile = staticmethod( parseFile )
# end class XSDataInputCalculateHelicalPositions


class XSDataResultCalculateHelicalPositions(XSDataResult):
    def __init__(self, status=None, sample_position=None):
        XSDataResult.__init__(self, status)
        if sample_position is None:
            self._sample_position = []
        elif sample_position.__class__.__name__ == "list":
            self._sample_position = sample_position
        else:
            strMessage = "ERROR! XSDataResultCalculateHelicalPositions constructor argument 'sample_position' is not list but %s" % self._sample_position.__class__.__name__
            raise BaseException(strMessage)
    # Methods and properties for the 'sample_position' attribute
    def getSample_position(self): return self._sample_position
    def setSample_position(self, sample_position):
        if sample_position is None:
            self._sample_position = []
        elif sample_position.__class__.__name__ == "list":
            self._sample_position = sample_position
        else:
            strMessage = "ERROR! XSDataResultCalculateHelicalPositions.setSample_position argument is not list but %s" % sample_position.__class__.__name__
            raise BaseException(strMessage)
    def delSample_position(self): self._sample_position = None
    sample_position = property(getSample_position, setSample_position, delSample_position, "Property for sample_position")
    def addSample_position(self, value):
        if value is None:
            strMessage = "ERROR! XSDataResultCalculateHelicalPositions.addSample_position argument is None"
            raise BaseException(strMessage)            
        elif value.__class__.__name__ == "XSDataSamplePosition":
            self._sample_position.append(value)
        else:
            strMessage = "ERROR! XSDataResultCalculateHelicalPositions.addSample_position argument is not XSDataSamplePosition but %s" % value.__class__.__name__
            raise BaseException(strMessage)
    def insertSample_position(self, index, value):
        if index is None:
            strMessage = "ERROR! XSDataResultCalculateHelicalPositions.insertSample_position argument 'index' is None"
            raise BaseException(strMessage)            
        if value is None:
            strMessage = "ERROR! XSDataResultCalculateHelicalPositions.insertSample_position argument 'value' is None"
            raise BaseException(strMessage)            
        elif value.__class__.__name__ == "XSDataSamplePosition":
            self._sample_position[index] = value
        else:
            strMessage = "ERROR! XSDataResultCalculateHelicalPositions.addSample_position argument is not XSDataSamplePosition but %s" % value.__class__.__name__
            raise BaseException(strMessage)
    def export(self, outfile, level, name_='XSDataResultCalculateHelicalPositions'):
        showIndent(outfile, level)
        outfile.write(unicode('<%s>\n' % name_))
        self.exportChildren(outfile, level + 1, name_)
        showIndent(outfile, level)
        outfile.write(unicode('</%s>\n' % name_))
    def exportChildren(self, outfile, level, name_='XSDataResultCalculateHelicalPositions'):
        XSDataResult.exportChildren(self, outfile, level, name_)
        for sample_position_ in self.getSample_position():
            sample_position_.export(outfile, level, name_='sample_position')
    def build(self, node_):
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'sample_position':
            obj_ = XSDataSamplePosition()
            obj_.build(child_)
            self.sample_position.append(obj_)
        XSDataResult.buildChildren(self, child_, nodeName_)
    #Method for marshalling an object
    def marshal( self ):
        oStreamString = StringIO()
        oStreamString.write(unicode('<?xml version="1.0" ?>\n'))
        self.export( oStreamString, 0, name_="XSDataResultCalculateHelicalPositions" )
        oStringXML = oStreamString.getvalue()
        oStreamString.close()
        return oStringXML
    #Only to export the entire XML tree to a file stream on disk
    def exportToFile( self, _outfileName ):
        outfile = open( _outfileName, "w" )
        outfile.write(unicode('<?xml version=\"1.0\" ?>\n'))
        self.export( outfile, 0, name_='XSDataResultCalculateHelicalPositions' )
        outfile.close()
    #Deprecated method, replaced by exportToFile
    def outputFile( self, _outfileName ):
        print("WARNING: Method outputFile in class XSDataResultCalculateHelicalPositions is deprecated, please use instead exportToFile!")
        self.exportToFile(_outfileName)
    #Method for making a copy in a new instance
    def copy( self ):
        return XSDataResultCalculateHelicalPositions.parseString(self.marshal())
    #Static method for parsing a string
    def parseString( _inString ):
        doc = minidom.parseString(_inString)
        rootNode = doc.documentElement
        rootObj = XSDataResultCalculateHelicalPositions()
        rootObj.build(rootNode)
        # Check that all minOccurs are obeyed by marshalling the created object
        oStreamString = StringIO()
        rootObj.export( oStreamString, 0, name_="XSDataResultCalculateHelicalPositions" )
        oStreamString.close()
        return rootObj
    parseString = staticmethod( parseString )
    #Static method for parsing a file
    def parseFile( _inFilePath ):
        doc = minidom.parse(_inFilePath)
        rootNode = doc.documentElement
        rootObj = XSDataResultCalculateHelicalPositions()
        rootObj.build(rootNode)
        return rootObj
    parseFile = staticmethod( parseFile )
# end class XSDataResultCalculateHelicalPositions



# End of data representation classes.


