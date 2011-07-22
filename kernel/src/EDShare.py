# -*- coding: utf8 -*-
#
#    Project: The EDNA Kernel
#             http://www.edna-site.org
#
#    File: "$Id:$"
#
#    Copyright (C) 2008-2009 European Synchrotron Radiation Facility
#                            Grenoble, France
#
#    Principal authors: Jérôme Kieffer (jerome.kieffer@esrf.fr)
# 
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
__authors__ = [ "Jérôme Kieffer" ]
__contact__ = "jerome.kieffer@esrf.fr"
__license__ = "LGPLv3+"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__date__ = "27/05/2011"

import os, tempfile

from EDLogging              import EDLogging
from EDFactoryPluginStatic  import EDFactoryPluginStatic
from EDUtilsPlatform        import EDUtilsPlatform
from EDSession              import EDSession


TEMPDIR = tempfile.gettempdir()

if os.name in ["posix", "nt"]:
    h5pyPath = os.path.join(os.environ["EDNA_HOME"], "libraries", "H5Py-1.3.0", EDUtilsPlatform.architecture)
    h5py = EDFactoryPluginStatic.preImport("h5py", _strPath=h5pyPath, _strForceVersion="1.8", _strMethodVersion="version.api_version")
#    h5py = None
    if h5py is None:
        BACKEND = "dict"
    else:
        BACKEND = "hdf5"
else:
    BACKEND = "dict"
if BACKEND == "dict":
    import pickle


class EDShare(EDLogging, EDSession):
    """
    This class implements methods to share (large) arrays between plugins.
    
    It is a Singleton  
    """
    _instance = None
    def __init__(self):
        EDLogging.__init__(self)
        #EDSession is a static class
        self._backend = BACKEND
        self._filename = None
        self._storage = None
        self._listKeys = []


    def __call__(self):
        """
        Makes this class a SINGLETON
        """
        return self

    def __getitem__(self, key):
        """
        getter for a key:
        """
        if self.isInitialized():
            self.synchronizeOn()
            if key in self._listKeys:
                try:
                    value = self._storage[key]
                except:
                    value = None
                    self.ERROR("EDShare (exception):  no such key %s" % key)
            else:
                value = None
                self.ERROR("EDShare: no such key %s" % key)
            self.synchronizeOff()
        else:
            self.WARNING("EDShare is uninitialized: initializing")
            self.initialize()
            value = None
        return value
    get = __getitem__


    def __setitem__(self, key, value):
        """
        setter for a key/value pair
        @type key: string
        @type value: int, float, or string ; one or many in lists or arrays (without mixing types)  
        """
        if self.isInitialized():
            self.synchronizeOn()
            if key in self._listKeys:
                self.ERROR("EDShare: Redefinition of elements is forbidden ")
            else:
                self._listKeys.append(key)
                self._storage[key] = value
            self.synchronizeOff()
        else:
            self.WARNING("EDShare is uninitialized: initializing")
            self.initialize()
    set = __setitem__


    def __contains__(self, key):
        return (key in self._listKeys)
    has_key = __contains__


    def isInitialized(self):
        return not((self._filename is None) and (self._storage is None))


    def initialize(self, directory=TEMPDIR, filename=None):
        """
        Initialize  EDShare to use this 
        """
        self.synchronizeOn()
        if filename is None:
            if self._backend == "hdf5":
                filename = "EDShare-%s.h5" % self.sessionId
            if self._backend == "dict":
                filename = "EDShare-%s.pickle" % self.sessionId
        absFilename = os.path.abspath(os.path.join(directory, filename))

        if not self.isInitialized():
            self._filename = absFilename
            if not os.path.isdir(directory):
                os.makedirs(directory)
            if (self._backend == "dict"):
                if os.path.isfile(self._filename):
                    self._storage = pickle.load(open(self._filename))
                    self._listKeys = self._storage.keys()
                    if not isinstance(self._storage, dict):
                        self.ERROR("I did not load a dictionary ... resetting")
                        self._storage = {}
                        self._listKeys = []
                else:
                    self._storage = {}
                    self._listKeys = []
            elif (self._backend == "hdf5"):
                self._storage = h5py.File(self._filename)
                self._storage.visititems(self._analyseHDF5)
            else:
                self.ERROR("unrecognized backend !!!")
        else:
            if  (absFilename != self._filename):
                self.ERROR("EDShare was already initialized with backend %s on %s" % (self._backend, self._storage))
        self.synchronizeOff()


    def flush(self):
        """
        Write the content of the cache on the disk
        """
        self.synchronizeOn()
        if self.isInitialized():
            if self._backend == "hdf5":
                self._storage.flush()
            elif (self._backend == "dict"):
                fileOut = open(self._filename, "w")
                self._storage = pickle.dump(self._storage, fileOut)
                fileOut.close()
            else:
                self.ERROR("EDShare: unrecognized backend !!!")
        else:
                self.ERROR("EDShare: Uninitialized !!!")
        self.synchronizeOff()


    def close(self, remove=False):
        """
        Method that closes the file and resets the cache.
        if remove: delete the input file as well. 
        
        Useful for testing mainly
        """
        self.flush()
        self.synchronizeOn()
        if self.isInitialized():
            if self._backend == "hdf5":
                self._storage.close()
            self._listKeys = []
            self._storage = None
            if remove:
                os.unlink(self._filename)
            self._filename = None
        else:
            self.ERROR("Closing a file that is uninitialized !!!")
        self.synchronizeOff()


    def _analyseHDF5(self, name, obj):
        """
        Part of the recursive analysis of an HDF5 tree to retrieve all datasets. 
        Populates self._listKeys
        
        @param name: name of the object itself (string)
        @param obj: the h5py object itself
        @return None
        """
        if isinstance(obj, h5py.Dataset):
            self._listKeys.append(name)


    def items(self):
        """
        Returns the list of 
        """
        return self._listKeys


    def get_backend(self):
        return self._backend
    backend = property(get_backend)


    def get_filename(self):
        return self._filename
    filename = property(get_filename)

EDShare = EDShare()

