# coding: utf8
#
#    Project: Autoproc
#             http://www.edna-site.org
#
#    File: "$Id$"
#
#    Copyright (C) ESRF
#
#    Principal author: Thomas Boeglin
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

__author__="Thomas Boeglin"
__license__ = "GPLv3+"
__copyright__ = "ESRF"

import sys
import os.path

from EDPluginControl import EDPluginControl
from EDVerbose import EDVerbose

from XSDataCommon import XSDataFile, XSDataString

from XSDataAutoproc  import XSDataMinimalXdsIn, XSDataXdsOutputFile, XSDataRange

from xdscfgparser import parse_xds_file

class EDPluginControlRunXdsFastProc( EDPluginControl ):
    """
    Runx XDS 3 times like Max's autoproc does.
    1. First run is a vanilla run
    2. Second run set JOB to DEFPIX INTEGRATE CORRECT
    3. Third run set JOB to ALL, maxproc to 4 and maxjobs to 1
    4. Final run set JOB to DEFPIX INTEGRATE CORRECT and maxproc and
    maxjobs like the 3rd run
    """


    def __init__( self ):
        """
        """
        EDPluginControl.__init__(self)
        self.setXSDataInputClass(XSDataMinimalXdsIn)
        self.controlled_plugin_name = 'EDPluginExecMinimalXds'
        self.first_run = None
        self.second_run = None
        self.third_run = None

        # to hold a ref to the successful plugin
        self.successful_run = None

    def checkParameters(self):
        """
        Checks the mandatory parameters.
        """
        self.DEBUG("EDPluginControlRunXdsFastProc.checkParameters")
        self.checkMandatoryParameters(self.dataInput, "Data Input is None")
        self.checkMandatoryParameters(self.dataInput.input_file, "No XDS input file")


    def preProcess(self, _edObject = None):
        EDPluginControl.preProcess(self)
        self.DEBUG("EDPluginControlRunXdsFastProc.preProcess")
        # Load the execution plugin
        self.first_run = self.loadPlugin(self.controlled_plugin_name)

        cfg = parse_xds_file(self.dataInput.input_file.value)
        spot_range = cfg.get('SPOT_RANGE=')
        if spot_range is None:
            self.ERROR('no SPOT_RANGE parameter')
            self.setFailure()
        else:
            self.spot_range = spot_range

        # we will use this value to constrain the upper bound of
        # spot_range so it does not get past the last image number, so
        # we use a default value that cannot be a constraint in case
        # we cannot find it in the xds input file
        self.end_image_no = sys.maxint

        data_range = cfg.get('DATA_RANGE=')
        if data_range is not None:
            self.end_image_no = data_range[1]

    def process(self, _edObject = None):
        EDPluginControl.process(self)
        self.DEBUG("EDPluginControlRunXdsFastProc.process")
        # First run is vanilla without any modification
        params = XSDataMinimalXdsIn()
        params.input_file = self.dataInput.input_file
        self.first_run.dataInput = params
        self.first_run.executeSynchronous()

        EDVerbose.DEBUG('first run completed...')

        if self.first_run.dataOutput is not None and self.first_run.dataOutput.succeeded.value:
            EDVerbose.DEBUG('... and it worked')
            self.successful_run = self.first_run
        else:
            EDVerbose.DEBUG('... and it failed')


        if not self.successful_run:
            self.second_run = self.loadPlugin(self.controlled_plugin_name)
            params = XSDataMinimalXdsIn()
            params.input_file = self.dataInput.input_file
            params.jobs = 'DEFPIX INTEGRATE CORRECT'

            # increase all the spot ranges end by 20, constrained to
            # the data range upper limit
            spot_range = list()
            for srange in self.spot_range:
                range_begin = srange[0]
                range_end = srange[1] + 20
                if range_end > self.end_image_no:
                    range_end = self.end_image_no
                r = XSDataRange(begin=range_begin, end=range_end)
                spot_range.append(r)

            params.spot_range = spot_range

            self.second_run.dataInput = params
            self.second_run.executeSynchronous()

            EDVerbose.DEBUG('second run completed')
            if self.second_run.dataOutput is not None and self.second_run.dataOutput.succeeded.value:
                EDVerbose.DEBUG('... and it worked')
                self.successful_run = self.second_run
            else:
                EDVerbose.DEBUG('... and it failed')


        if not self.successful_run:
            self.third_run = self.loadPlugin(self.controlled_plugin_name)
            params = XSDataMinimalXdsIn()
            params.input_file = self.dataInput.input_file
            params.jobs = 'DEFPIX INTEGRATE CORRECT'
            spot_range = list()
            for srange in self.spot_range:
                range_begin = srange[0]
                range_end = srange[1] + 40
                if range_end > self.end_image_no:
                    range_end = self.end_image_no
                r = XSDataRange(begin=range_begin, end=range_end)
                spot_range.append(r)

            params.spot_range = spot_range

            self.third_run.dataInput = params
            self.third_run.executeSynchronous()

            EDVerbose.DEBUG('third run completed')
            if self.third_run.dataOutput is not None and self.third_run.dataOutput.succeeded.value:
                EDVerbose.DEBUG('... and it worked')
                self.successful_run = self.third_run
            else:
                EDVerbose.DEBUG('... and it failed')

        if not self.successful_run:
        # all runs failed so bail out ...
            self.setFailure()
        else:
            # use the xds parser plugin to parse the xds output file...
            parser = self.loadPlugin("EDPluginParseXdsOutput")
            wd = self.successful_run.getWorkingDirectory()
            parser_input = XSDataXdsOutputFile()
            correct_lp_path = XSDataFile()
            correct_lp_path.path = XSDataString(os.path.join(wd, 'CORRECT.LP'))
            parser_input.correct_lp = correct_lp_path
            gxparm_path = os.path.join(wd, 'GXPARM.XDS')
            if os.path.isfile(gxparm_path):
                gxparm = XSDataFile()
                gxparm.path = XSDataString(os.path.join(wd, 'GXPARM.XDS'))
                parser_input.gxparm = gxparm

            parser.dataInput = parser_input
            parser.executeSynchronous()

            if parser.isFailure():
                # that should not happen
                self.setFailure()
                return
            self.dataOutput = parser.dataOutput

    def postProcess(self, _edObject = None):
        EDPluginControl.postProcess(self)
        self.DEBUG("EDPluginControlRunXdsFastProc.postProcess")
        # XXX: maybe move the XDS output parsing there?
