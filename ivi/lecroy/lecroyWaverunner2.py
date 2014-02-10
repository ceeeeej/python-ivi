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
    'bmp8': 'bmp8bit',
    'png': 'png',
    'png24': 'png'}


class lecroyWaverunner2(lecroyBaseScope):
    "LeCroy WaveRunner-2 series IVI oscilloscope driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(lecroyWaverunner2, self).__init__(*args, **kwargs)

        self._analog_channel_name = list()
        self._analog_channel_count = 4
        # Commented out the following lines as I don't believe these scopes have any digital channel support
        # self._digital_channel_name = list()
        # self._digital_channel_count = 16
        # self._channel_count = self._analog_channel_count + self._digital_channel_count
        # Modified channel_count equation to only include analog channels
        self._channel_count = self._analog_channel_count
        self._bandwidth = 1e9
        # TODO: add all Waverunner-2 models below and .py files for each model
        self._identity_description = "LeCroy WaveRunner-2 IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['LT264']
