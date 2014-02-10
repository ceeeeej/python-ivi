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
from .. import dcpwr
from .. import scpi

TrackingType = set(['floating'])
TriggerSourceMapping = {
        'immediate': 'imm',
        'bus': 'bus'}

class chromaBaseDCPwr(scpi.dcpwr.Base, scpi.dcpwr.Trigger, scpi.dcpwr.SoftwareTrigger,
                scpi.dcpwr.Measurement):
    "Chroma ATE generic IVI DC power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(chromaBaseDCPwr, self).__init__(*args, **kwargs)
        
        self._output_count = 1

        self._output_spec = [
            {
                'range': {
                    'P600V': (600.0, 120.0)
                },
                'ovp_max': 660.0,
                'ocp_max': 120.0,
                'voltage_max': 600.0,
                'current_max': 120.0
            }
        ]
        
        self._memory_size = 10
        
        self._identity_description = "Chroma ATE generic IVI DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Chroma ATE"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['62006P-100-25', '62012P-80-60', '62012P-100-50', '62012P-600-8',
                                                      '62006P-30-80', '62006P-300-8', '62012P-40-120', '62024P-40-120',
                                                      '62024P-80-60', '62024P-100-50', '62024P-600-8', '62050P-100-100']
        
        ivi.add_method(self, 'memory.save',
                        self._memory_save)
        ivi.add_method(self, 'memory.recall',
                        self._memory_recall)
        
        self._init_outputs()
        
    
    def _memory_save(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*sav %d" % index)
    
    def _memory_recall(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*rcl %d" % index)
    
    
    

