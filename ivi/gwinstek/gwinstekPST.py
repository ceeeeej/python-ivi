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
from .. import scpi

CurrentLimitBehaviors = set(['regulate', 0, 'trip', 1])
CurrentLimitBehaviorMapping = {
    0: 'regulate',
    1: 'trip',
    'regulate': 0,
    'trip': 1}
TrackingTypes = set(['independent', 0, 'parallel', 1, 'series', 2])
TrackingTypeMapping = {
    'independent': 0,
    'parallel': 1,
    'series': 2,
    0: 'independent',
    1: 'parallel',
    2: 'series'}


class gwinstekPST(scpi.dcpwr.Base, scpi.dcpwr.Trigger, scpi.dcpwr.SoftwareTrigger,
                  scpi.dcpwr.Measurement):
    "GW Instek PST series IVI DC power supply driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'PST')

        # don't do standard SCPI init routine
        self._do_scpi_init = False

        super(gwinstekPST, self).__init__(*args, **kwargs)

        self._output_count = 3

        self._output_spec = [
            {
                'range': {
                    'P32V': (33.0, 2.0)
                },
                'ovp_max': 33.0,
                'voltage_max': 32.0,
                'current_max': 2.0
            },
            {
                'range': {
                    'P6V': (7.0, 5.0)
                },
                'ovp_max': 7.0,
                'voltage_max': 6.0,
                'current_max': 5.0
            }
        ]

        self._memory_size = 5

        self._output_trigger_delay = list()

        self._couple_tracking_enabled = False
        self._couple_tracking_type = 'floating'
        self._couple_trigger = False

        self._identity_description = "GW Instek PST series IVI DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "GW Instek"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['PST-3201', 'PST-3202']

        ivi.add_property(self, 'couple.tracking.type',
                         self._get_couple_tracking_type,
                         self._set_couple_tracking_type)
        ivi.add_method(self, 'memory.save',
                       self._memory_save)
        ivi.add_method(self, 'memory.recall',
                       self._memory_recall)

        self._init_outputs()

    def initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        "Opens an I/O session to the instrument."

        super(gwinstekPST, self).initialize(resource, id_query, reset, **keywargs)

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

    def _init_outputs(self):
        try:
            super(gwinstekPST, self)._init_outputs()
        except AttributeError:
            pass

        self._output_name = list()
        self._output_current_limit = list()
        self._output_current_limit_behavior = list()
        self._output_enabled = list()
        self._output_ovp_enabled = list()
        self._output_ovp_limit = list()
        self._output_voltage_level = list()
        self._output_voltage_max = list()
        for i in range(self._output_count):
            self._output_name.append("output%d" % (i + 1))
            self._output_current_limit.append(self._output_spec[i - 1]['current_max'])
            #self._output_current_limit.append(0)
            self._output_current_limit_behavior.append('regulate')
            self._output_enabled.append(False)
            self._output_ovp_enabled.append(True)
            self._output_ovp_limit.append(self._output_spec[i - 1]['ovp_max'])
            #self._output_ovp_limit.append(0)
            self._output_voltage_level.append(0)
            self._output_voltage_max.append(self._output_spec[i - 1]['voltage_max'])
            #self._output_voltage_max.append(0)

        self.outputs._set_list(self._output_name)

    # Tested with PST-3202, working
    def _get_output_current_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_current_limit[index] = float(self._ask(":channel%s:current ?" % (index + 1)))
            self._set_cache_valid(index=index)
        return self._output_current_limit[index]

    # Tested with PST-3202, working
    def _set_output_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":channel%s:current %f" % (index + 1, value))
        self._output_current_limit[index] = value
        self._set_cache_valid(index=index)

    #TODO: test
    def _get_output_current_limit_behavior(self, index):
        """
        Gets the current limit behavior:
        * regulate
        * trip
        """
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            value = int(self._ask(":channel%s:protection:current ?" % (index + 1)))
            self._output_current_limit_behavior[index] = CurrentLimitBehaviorMapping[value]
            self._set_cache_valid(index=index)
        return self._output_current_limit_behavior[index]

    #TODO: test
    def _set_output_current_limit_behavior(self, index, value):
        """
        Set the current limit behavior:
        * regulate
        * trip
        """
        index = ivi.get_index(self._output_name, index)
        if value not in CurrentLimitBehaviorMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":channel%s:protection:current %d" % (index + 1, int(CurrentLimitBehaviorMapping[value])))
        self._output_current_limit_behavior[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False, index=k)
        self._set_cache_valid(index=index)

    # Tested with PST-3202, working
    def _get_output_enabled(self, index):
        """On the GW Instek PST series this function will return the status of all outputs!"""
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_enabled[index] = bool(int(self._ask(":output:state ?")))
            self._set_cache_valid(index=index)
        return self._output_enabled[index]

    # Tested with PST-3202, working
    def _set_output_enabled(self, index, value):
        """
        On the GW Instek PST series this function will turn on or off all of the outputs.
        The outputs are not individually controlled.
        """
        index = ivi.get_index(self._output_name, index)
        #value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":output:state %d" % int(value))
        self._output_enabled[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False, index=k)
        self._set_cache_valid(index=index)

    # Tested with PST-3202, working
    def _get_output_ovp_limit(self, index):
        """
        Return the currently set OVP limit for the specified channel.
        """
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_ovp_limit[index] = float(self._ask(":channel%s:protection:voltage ?" % (index + 1)))
            self._set_cache_valid(index=index)
        return self._output_ovp_limit[index]

    # Tested with PST-3202, working
    def _set_output_ovp_limit(self, index, value):
        """
        Sets the OVP limit for the specified channel.
        """
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['ovp_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":channel%s:protection:voltage %f" % (index + 1, value))
        self._output_ovp_limit[index] = value
        self._set_cache_valid(index=index)

    # Tested with PST-3202, working
    def _get_output_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_voltage_level[index] = float(self._ask(":channel%s:voltage ?" % (index + 1)))
            self._set_cache_valid(index=index)
        return self._output_voltage_level[index]

    # Tested with PST-3202, working
    def _set_output_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_voltage_max[index]:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":channel%s:voltage %f" % (index + 1, value))
        self._output_voltage_level[index] = value
        self._set_cache_valid(index=index)

    # Not implemented correctly, not sure what the point of these should be
    #def _output_query_voltage_level_max(self, index, voltage_level):
    #    """
    #    Returns the maximum voltage level for the specific output channel as defined by the 'output_spec'
    #    """
    #    index = ivi.get_index(self._output_name, index)
    #    if voltage_level < 0 or voltage_level > self._output_spec[index]['voltage_max']:
    #        raise ivi.OutOfRangeException()
    #    return self._output_spec[index]['voltage_max']
    #def _output_query_current_limit_max(self, index, current_limit):
    #    """
    #    Returns the maximum current limit for the specific output channel as defined by the 'output_spec'
    #    """
    #    index = ivi.get_index(self._output_name, index)
    #    if current_limit < 0 or current_limit > self._output_spec[index]['current_max']:
    #        raise ivi.OutOfRangeException()
    #    return self._output_spec[index]['current_max']

    # Tested with PST-3202, working
    def _output_measure(self, index, type):
        index = ivi.get_index(self._output_name, index)
        if type not in ['voltage', 'current']:
            raise ivi.ValueNotSupportedException()
        if type == 'voltage':
            if not self._driver_operation_simulate:
                return float(self._ask(":channel%s:measure:voltage ?" % (index + 1)))
        elif type == 'current':
            if not self._driver_operation_simulate:
                return float(self._ask(":channel%s:measure:current ?" % (index + 1)))
        return 0

    #TODO: test
    def _output_reset_output_protection(self):
        if not self._driver_operation_simulate:
            self._write(":output:protection:clear")

    # Tested with PST-3202, working
    def _get_couple_tracking_type(self):
        """
        Get the tracking type:
        * 0: independent (no tracking)
        * 1: series tracking for channels 1 and 2
        * 2: parallel tracking for channels 1 and 2
        """
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":output:couple:tracking ?")
            self._couple_tracking_type = TrackingTypeMapping[int(value)]
            self._set_cache_valid()
        return self._couple_tracking_type

    # Tested with PST-3202, working
    def _set_couple_tracking_type(self, value):
        """
        Set the tracking type:
        * 0: independent (no tracking)
        * 1: series tracking for channels 1 and 2
        * 2: parallel tracking for channels 1 and 2
        """
        value = str(value)
        if value not in TrackingTypeMapping:
            raise ivi.ValueNotSupportedException()
        self._write(":output:couple:tracking %d" % int(TrackingTypeMapping[value]))
        self._couple_tracking_type = value

    # Tested with PST-3202, working
    def _memory_save(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*sav %d" % index)

    # Tested with PST-3202, working
    def _memory_recall(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*rcl %d" % index)
