"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from .lecroyBaseScope import *

ScreenshotImageFormatMapping = {
        'bmp': 'bmp',
        'bmp24': 'bmp',
        'bmp8': 'bmpcomp',
        'jpeg': 'jpeg',
        'png': 'png',
        'png24': 'png',
        'psd': 'psd',
        'tiff': 'tiff'}

class lecroyWRXIA(lecroyBaseScope):
    "LeCroy WaveRunner Xi-A / MXi-A series IVI oscilloscope driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(lecroyWRXIA, self).__init__(*args, **kwargs)

        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1e9

        self._identity_description = "LeCroy WaveRunner Xi-A / MXi-A series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['WR204MXI-A', 'WR204XI-A', 'WR104MXI-A', 'WR104XI-A', 'WR64MXI-A', 'WR64XI-A',
                                                      'WR62XI-A', 'WR44MXI-A', 'WR44XI-A']

        # To use some advanced commands of the WRXIA series, we setup the XStreamDSO as "app" using the VBS command
        #self._write("VBS \'app = CreateObject(\"LeCroy.XStreamDSO\")\'")
        self._init_channels()
        #self._channel_count = self._analog_channel_count + self._digital_channel_count
        #self.channels._set_list(self._channel_name)

    # Modified for LeCroy, WORKING ON WR104XI-A
    def _get_channel_label(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_label[index] = self._ask("VBS? \"Return=app.Acquisition.%s.LabelsText\"" % (self._channel_name[index])).strip('"')
        self._set_cache_valid(index=index)
        return self._channel_label[index]

    # Modified for LeCroy, WORKING ON WR104XI-A
    def _set_channel_label(self, index, value):
        value = str(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write("VBS \"app.Acquisition.%s.LabelsText = \"\"%s\"" % (self._channel_name[index], value))
            self._write("VBS \"app.Acquisition.%s.ViewLabels = \"True" % self._channel_name[index])
        self._channel_label[index] = value
        self._set_cache_valid(index=index)

    # Modified for LeCroy, WORKING ON WR104XI-A
    def _get_channel_invert(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_invert[index] = bool(self._ask("VBS? \"Return=app.Acquisition.%s.Invert\"" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_invert[index]

    # Modified for LeCroy, WORKING ON WR104XI-A
    def _set_channel_invert(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("VBS \"app.Acquisition.%s.Invert = %s\"" % (self._channel_name[index], value))
        self._channel_invert[index] = value
        self._set_cache_valid(index=index)
