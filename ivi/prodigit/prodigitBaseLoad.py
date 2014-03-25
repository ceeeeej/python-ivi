"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

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

class prodigitBaseLoad(scpi.dcpwr.Base):
    "Prodigit series IVI DC electronic load driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '3310C')

        # don't do standard SCPI init routine
        self._do_scpi_init = False

        super(prodigitBaseLoad, self).__init__(*args, **kwargs)

        self._input_count = 1

        self._input_spec = [
            {
                'range': {
                    'P60V': (61.0, 60.0)
                },
                'ovp_max': 61.0,
                'voltage_max': 60.0,
                'current_max': 60.0
            }
        ]

        self._memory_size = 5

        self._output_trigger_delay = list()

        self._couple_tracking_enabled = False
        self._couple_tracking_type = 'floating'
        self._couple_trigger = False

        self._identity_description = "Prodigit DC electronic load driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Prodigit"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['3310C', '3311C', '3312C', '3314C', '3315C']

        ivi.add_property(self, 'outputs.dynamic',
                        self._get_output_dynamic,
                        self._set_output_dynamic)

        ivi.add_property(self, 'measurement.voltage',
                        self._measurement_voltage)
        ivi.add_property(self, 'measurement.current',
                        self._measurement_current)

        ivi.add_method(self, 'memory.save',
                        self._memory_save)
        ivi.add_method(self, 'memory.recall',
                        self._memory_recall)

        self._init_outputs()

    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(prodigitBaseLoad, self).initialize(resource, id_query, reset, **keywargs)

        # configure interface
        if self._interface is not None:
            if 'dsrdtr' in self._interface.__dict__:
                self._interface.dsrdtr = True
                self._interface.update_settings()

        # interface clear
        if not self._driver_operation_simulate:
            self._clear()

        # check ID
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)

        # reset
        if reset:
            self.utility_reset()


    def _measurement_voltage(self):
        if not self._driver_operation_simulate:
            return float(self._ask("measure:voltage?"))

    def _measurement_current(self):
        if not self._driver_operation_simulate:
            return float(self._ask("measure:current?"))

    def _memory_save(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("system:store %d" % index)

    def _memory_recall(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("system:recall %d" % index)


class Measurement(prodigitBaseLoad.Measurement):
    def _output_measure(self, type):
        if type not in dcpwr.MeasurementType:
            raise ivi.ValueNotSupportedException()
        if type == 'voltage':
            if not self._driver_operation_simulate:
                return float(self._ask("measure:voltage?"))
        elif type == 'current':
            if not self._driver_operation_simulate:
                return float(self._ask("measure:current?"))
        return 0


