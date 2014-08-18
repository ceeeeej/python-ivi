"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2013-2014 Alex Forencich

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

from .. import ivi
from .. import scpi

class prodigitBaseDCLoad(scpi.dcload.Base):
    "Prodigit generic IVI electronic DC load driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(prodigitBaseDCLoad, self).__init__(*args, **kwargs)
        
        self._channel_count = 1

        self._channel_spec = [
            {
                'range': {
                    'P60V': (60.0, 30.0)
                },
                'ovp_max': 66.0,
                'ocp_max': 33.0,
                'voltage_max': 60.0,
                'current_max': 30.0
            }
        ]
        
        self._memory_size = 5
        
        self._identity_description = "Prodigit generic IVI electronic DC load driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Prodigit"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['3311C']

        ivi.add_property(self, 'channels.mode',
                        self._get_channel_mode,
                        self._set_channel_mode)
        ivi.add_property(self, 'channels.dynamic',
                        self._get_channel_dynamic,
                        self._set_channel_dynamic)
        ivi.add_property(self, 'channels.dynamic_slew',
                        self._get_channel_dynamic_slew,
                        self._set_channel_dynamic_slew)
        ivi.add_property(self, 'channels.range',
                        self._get_channel_range,
                        self._set_channel_range)
        #ivi.add_property(self, 'channels.current.low',
        #                self._get_channel_current_low,
        #                self._set_channel_current_low)
        #ivi.add_property(self, 'channels.current.high',
        #                self._get_channel_current_high,
        #                self._set_channel_current_high)

        self._init_channels()

    def _init_channels(self):
        try:
            super(prodigitBaseDCLoad, self)._init_channels()
        except AttributeError:
            pass

        self._channel_name = list()
        self._channel_mode = list()
        self._channel_dynamic = list()
        self._channel_dynamic_slew = list()
        self._channel_level = list()
        self._channel_range = list()
        self._channel_current_limit = list()
        self._channel_current_low = list()
        self._channel_current_high = list()
        self._channel_enabled = list()
        self._channel_ovp_enabled = list()
        self._channel_ovp_limit = list()
        self._channel_voltage_level = list()
        self._channel_voltage_max = list()
        self._channel_slew_rate = list()
        for i in range(self._channel_count):
            self._channel_name.append("output%d" % (i+1))
            self._channel_mode.append(0)
            self._channel_dynamic.append(False)
            self._channel_dynamic_slew.append(0)
            self._channel_level.append("low")
            self._channel_range.append(0)
            self._channel_current_limit.append(self._channel_spec[i-1]['current_max'])
            self._channel_current_limit.append(0)
            #self._channel_current_low.append(0)
            #self._channel_current_high.append(0)
            self._channel_enabled.append(False)
            self._channel_ovp_enabled.append(True)
            self._channel_ovp_limit.append(self._channel_spec[i-1]['ovp_max'])
            self._channel_voltage_level.append(0)
            self._channel_voltage_max.append(self._channel_spec[i-1]['voltage_max'])
            self._channel_slew_rate.append(0)

        self.channels._set_list(self._channel_name)


    
    
    

