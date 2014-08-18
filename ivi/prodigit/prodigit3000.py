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

from .prodigitBaseDCLoad import *

ModeMapping = {
    0: "CC",
    1: "CR",
    2: "CV",
    3: "CP",
    "CC": 0,
    "CR": 1,
    "CV": 2,
    "CP": 3
}

BehaviorMapping = {
    "static": 0,
    "dynamic": 1
}

MeasurementType = ['current', 'voltage']

class prodigit3000(prodigitBaseDCLoad):
    """Prodigit 3000 series IVI electronic DC load driver"""

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(prodigit3000, self).__init__(*args, **kwargs)

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

        self._memory_size = 10

        self._identity_description = "Prodigit 3000 series IVI electronic DC load driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Prodigit"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['3311C']

        self._init_channels()


    ## Tested on Chroma 62012P-80-60; working
    #def _get_channel_current_limit(self, index):
    #    """
    #    This function fetches the current limit setting of the instrument.
    #    """
    #    index = ivi.get_index(self._channel_name, index)
    #    if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
    #        self._channel_current_limit[index] = self._ask("LIM:CURR:HIGH ?")
    #        self._set_cache_valid(index=index)
    #    return self._channel_current_limit[index]
#
    ## Tested on Chroma 62012P-80-60; working
    #def _set_channel_current_limit(self, index, value):
    #    """
    #    This function sets the current limit of the instrument.
    #    """
    #    index = ivi.get_index(self._channel_name, index)
    #    value = float(value)
    #    if value < 0 or value > self._channel_spec[index]['current_max']:
    #        raise ivi.OutOfRangeException()
    #    if not self._driver_operation_simulate:
    #        self._write("LIM:CURR:HIGH %.2f" % float(value))
    #    self._channel_current_limit[index] = value
    #    self._set_cache_valid(index=index)

    # Tested on Prodigit 3311C; working
    def _get_channel_enabled(self, index):
        """
        This function queries the output state of the instrument.
        * 0, False = OFF
        * 1, True = ON
        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_enabled[index] = bool(self._ask("STATE:LOAD?"))
            self._set_cache_valid(index=index)
        return self._channel_enabled[index]

    # Tested on Prodigit 3311C; working
    def _set_channel_enabled(self, index, value):
        """
        This function sets the output state of the instrument.
        * 0, False = OFF
        * 1, True = ON
        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write("STATE:LOAD %s" % int(value))
        self._channel_enabled[index] = bool(value)
        for k in range(self._channel_count):
            self._set_cache_valid(valid=False, index=k)
        self._set_cache_valid(index=index)

    ## Tested on Chroma 62012P-80-60; working
    #def _get_channel_voltage_limit(self, index):
    #    """
    #    This function fetches the voltage limit setting of the instrument.
    #    """
    #    index = ivi.get_index(self._channel_name, index)
    #    if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
    #        self._channel_voltage_level[index] = float(self._ask("SOUR:VOLT?"))
    #        self._set_cache_valid(index=index)
    #    return self._channel_voltage_level[index]
#
    ## Tested on Chroma 62012P-80-60; working
    #def _set_channel_voltage_limit(self, index, value):
    #    """
    #    This function sets the voltage limit setting of the instrument.
    #    """
    #    index = ivi.get_index(self._channel_name, index)
    #    value = float(value)
    #    if value < 0 or value > self._channel_voltage_max[index]:
    #        raise ivi.OutOfRangeException()
    #    if not self._driver_operation_simulate:
    #        self._write("SOUR:VOLT %.2f" % float((value)))
    #    self._channel_voltage_level[index] = value
    #    self._set_cache_valid(index=index)

    # Tested on Prodigit 3311C; working
    def _get_channel_mode(self, index):
        """
        This function gets the operating mode of the channel.
        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_mode[index] = ModeMapping[int(self._ask("STATE:MODE ?"))]
            self._set_cache_valid(index=index)
        return self._channel_mode[index]

    # Tested on Prodigit 3311C; working
    def _set_channel_mode(self, index, value):
        """
        This function sets the operating mode of the channel.
        * CC
        * CR
        * CV
        * CP
        """
        index = ivi.get_index(self._channel_name, index)
        if value not in ModeMapping:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("STATE:MODE %d" % int(ModeMapping[value]))
        self._channel_mode[index] = ModeMapping[value]
        self._set_cache_valid(index=index)

    # Tested on Prodigit 3311C; working
    def _get_channel_dynamic(self, index):
        """
        This function gets the status of the dynamic operating behavior of the channel.
        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_dynamic[index] = bool(int(self._ask("STATE:DYNAMIC ?")))
            self._set_cache_valid(index=index)
        return self._channel_dynamic[index]

    # Tested on Prodigit 3311C; working
    def _set_channel_dynamic(self, index, value):
        """
        This function sets the status of the dynamic operating behavior of the channel.
        """
        index = ivi.get_index(self._channel_name, index)
        if value not in [0, 1, False, True]:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("STATE:DYNAMIC %d" % int(value))
        self._channel_dynamic[index] = bool(value)
        self._set_cache_valid(index=index)

    # Tested on Prodigit 3311C; working
    def _get_channel_dynamic_slew(self, index):
        """
        This function gets the status of the dynamic operating behavior of the channel.
        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_dynamic_slew[index] = float(self._ask("SLEW ?"))
            self._set_cache_valid(index=index)
        return self._channel_dynamic_slew[index]

    # Tested on Prodigit 3311C; working
    def _set_channel_dynamic_slew(self, index, value):
        """
        This function sets the status of the dynamic operating behavior of the channel.
        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write("SLEW %f" % float(value))
        self._channel_dynamic_slew[index] = float(value)
        self._set_cache_valid(index=index)

    # TODO: test
    def _get_channel_cc_low(self, index):
        """
        This function gets the status of the dynamic operating behavior of the channel.
        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_cc_low[index] = float(self._ask("CC:LOW ?"))
            self._set_cache_valid(index=index)
        return self._channel_cc_low[index]

    # TODO: test
    def _set_channel_cc_low(self, index, value):
        """
        This function sets the status of the dynamic operating behavior of the channel.
        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write("CC:LOW %.3f" % float(value))
        self._channel_cc_low[index] = float(value)
        self._set_cache_valid(index=index)

    # TODO: test
    def _get_channel_cc_high(self, index):
        """

        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_cc_high[index] = float(self._ask("CC:HIGH ?"))
            self._set_cache_valid(index=index)
        return self._channel_cc_high[index]

    # TODO: test
    def _set_channel_cc_high(self, index, value):
        """

        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write("CC:HIGH %.3f" % float(value))
        self._channel_cc_high[index] = float(value)
        self._set_cache_valid(index=index)

    # TODO: test
    def _get_channel_level(self, index):
        index = ivi.get_index(self._channel_name, index)
        self._channel_level[index] = int(self._ask("LEVEL ?"))
        return self._channel_level[index]
    # TODO: test
    def _set_channel_level(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = int(value)
        #if value not in Levels:
        #    raise ivi.OutOfRangeException()
        self._write("LEVEL %d" % value)
        self._channel_level[index] = value

    # TODO: test
    def _get_channel_range(self, index):
        index = ivi.get_index(self._channel_name, index)
        self._channel_level[index] = str(self._ask("RANGE ?"))
        return self._channel_range[index]
    # TODO: test
    def _set_channel_range(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = int(value)
        #if value not in Levels:
        #    raise ivi.OutOfRangeException()
        self._write("RANGE %d" % value)
        self._channel_range[index] = value
