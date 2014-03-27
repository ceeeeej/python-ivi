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

import time
import struct

from .. import ivi
from .. import scope

AcquisitionTypeMapping = {
        'normal': 'norm',
        'peak_detect': 'peak',
        'high_resolution': 'hres',
        'average': 'aver'}
VerticalCoupling = set(['ac', 'dc', 'gnd'])
# Bandwidth Limits, OFF = none, ON = 20 MHz, 200MHZ = 200 MHz
BandwidthLimit = set(['OFF', 'ON', '200MHZ'])
TriggerTypeMapping = {
        'auto': 'auto',
        'norm': 'norm',
        'single': 'single',
        'stop': 'stop',}
TriggerCouplingMapping = {
        'ac': ('ac', 0, 0),
        'dc': ('dc', 0, 0),
        'hf_reject': ('dc', 0, 1),
        'lf_reject': ('lfr', 0, 0),
        'noise_reject': ('dc', 1, 0),
        'hf_reject_ac': ('ac', 0, 1),
        'noise_reject_ac': ('ac', 1, 0),
        'hf_noise_reject': ('dc', 1, 1),
        'hf_noise_reject_ac': ('ac', 1, 1),
        'lf_noise_reject': ('lfr', 1, 0)}
TVTriggerEventMapping = {'field1': 'fie1',
        'field2': 'fie2',
        'any_field': 'afi',
        'any_line': 'alin',
        'line_number': 'lfi1',
        'vertical': 'vert',
        'line_field1': 'lfi1',
        'line_field2': 'lfi2',
        'line': 'line',
        'line_alternate': 'lalt',
        'lvertical': 'lver'}
TVTriggerFormatMapping = {'generic': 'gen',
        'ntsc': 'ntsc',
        'pal': 'pal',
        'palm': 'palm',
        'secam': 'sec',
        'p480l60hz': 'p480',
        'p480': 'p480',
        'p720l60hz': 'p720',
        'p720': 'p720',
        'p1080l24hz': 'p1080',
        'p1080': 'p1080',
        'p1080l25hz': 'p1080l25hz',
        'p1080l50hz': 'p1080l50hz',
        'p1080l60hz': 'p1080l60hz',
        'i1080l50hz': 'i1080l50hz',
        'i1080': 'i1080l50hz',
        'i1080l60hz': 'i1080l60hz'}
PolarityMapping = {'positive': 'pos',
        'negative': 'neg'}
GlitchConditionMapping = {'less_than': 'less',
        'greater_than': 'gre'}
WidthConditionMapping = {'within': 'rang'}
SampleModeMapping = {'real_time': 'rtim',
        'equivalent_time': 'etim'}
SlopeMapping = {
        'positive': 'pos',
        'negative': 'neg',
        'either': 'eith',
        'alternating': 'alt'}
MeasurementFunctionMapping = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'voltage_rms': 'vrms display',
        'voltage_peak_to_peak': 'vpp',
        'voltage_max': 'vmax',
        'voltage_min': 'vmin',
        'voltage_high': 'vtop',
        'voltage_low': 'vbase',
        'voltage_average': 'vaverage display',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_positive': 'dutycycle',
        'amplitude': 'vamplitude',
        'voltage_cycle_rms': 'vrms cycle',
        'voltage_cycle_average': 'vaverage cycle',
        'overshoot': 'overshoot',
        'preshoot': 'preshoot',
        'ratio': 'vratio',
        'phase': 'phase',
        'delay': 'delay'}
MeasurementFunctionMappingDigital = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_positive': 'dutycycle'}
ScreenshotImageFormatMapping = {
        'bmp': 'bmp',
        'bmp24': 'bmp',
        'bmp8': 'bmpcomp',
        'jpeg': 'jpeg',
        'png': 'png',
        'png24': 'png',
        'psd': 'psd',
        'tiff': 'tiff'}
TimebaseModeMapping = {
        'main': 'main',
        'window': 'wind',
        'xy': 'xy',
        'roll': 'roll'}
TimebaseReferenceMapping = {
        'left': 'left',
        'center': 'cent',
        'right': 'righ'}

class lecroyBaseScope(ivi.Driver, scope.Base, scope.TVTrigger,
                scope.GlitchTrigger, scope.WidthTrigger, scope.AcLineTrigger,
                scope.WaveformMeasurement, scope.MinMaxWaveform,
                scope.ContinuousAcquisition, scope.AverageAcquisition,
                scope.SampleMode, scope.AutoSetup):
    "LeCroy generic IVI oscilloscope driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._channel_label = list()
        self._channel_probe_skew = list()
        self._channel_invert = list()
        self._channel_probe_id = list()
        self._channel_bw_limit = list()
        
        super(lecroyBaseScope, self).__init__(*args, **kwargs)
        
        self._memory_size = 5
        
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1e9
        
        self._horizontal_divisions = 10
        self._vertical_divisions = 8
        
        self._timebase_mode = 'main'
        self._timebase_reference = 'center'
        self._timebase_position = 0.0
        self._timebase_range = 1e-3
        self._timebase_scale = 100e-6
        self._timebase_window_position = 0.0
        self._timebase_window_range = 5e-6
        self._timebase_window_scale = 500e-9
        self._display_vectors = True
        self._display_labels = True
        # TODO: Check default setting for GRID? and use as display_grid setting
        self._display_grid = "single"
        
        self._identity_description = "LeCroy generic IVI oscilloscope driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "LeCroy"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['WR204MXI-A', 'WR204XI-A', 'WR104MXI-A', 'WR104XI-A', 'WR64MXI-A', 'WR64XI-A',
                                                      'WR62XI-A', 'WR44MXI-A', 'WR44XI-A']

        ivi.add_property(self, 'channels[].bw_limit',
                        self._get_channel_bw_limit,
                        self._set_channel_bw_limit,
                        None,
                        ivi.Doc("""
                        Commands an internal low-pass filter.  When the filter is on, the
                        bandwidth of the channel is limited to approximately 20 MHz.
                        """))
        ivi.add_property(self, 'channels[].invert',
                        self._get_channel_invert,
                        self._set_channel_invert,
                        None,
                        ivi.Doc("""
                        Selects whether or not to invert the channel.
                        """))
        ivi.add_property(self, 'channels[].label',
                        self._get_channel_label,
                        self._set_channel_label,
                        None,
                        ivi.Doc("""
                        Sets the channel label.  Setting a channel label also adds the label to
                        the nonvolatile label list. Setting the label will turn it's display on.
                        """))
        ivi.add_property(self, 'channels[].scale',
                        self._get_channel_scale,
                        self._set_channel_scale,
                        None,
                        ivi.Doc("""
                        Specifies the vertical scale, or units per division, of the channel.  Units
                        are volts.
                        """))
        # TODO: delete following if not used in LeCroy
        ivi.add_property(self, 'timebase.mode',
                        self._get_timebase_mode,
                        self._set_timebase_mode,
                        None,
                        ivi.Doc("""
                        Sets the current time base. There are four time base modes:

                        * 'main': normal timebase
                        * 'window': zoomed or delayed timebase
                        * 'xy': channels are plotted against each other, no timebase
                        * 'roll': data moves continuously from left to right
                        """))
        ivi.add_property(self, 'timebase.reference',
                        self._get_timebase_reference,
                        self._set_timebase_reference,
                        None,
                        ivi.Doc("""
                        Sets the time reference to one division from the left side of the screen,
                        to the center of the screen, or to one division from the right side of the
                        screen. Time reference is the point on the display where the trigger point
                        is referenced.
                        
                        Values:
                        * 'left'
                        * 'center'
                        * 'right'
                        """))
        ivi.add_property(self, 'timebase.position',
                        self._get_timebase_position,
                        self._set_timebase_position,
                        None,
                        ivi.Doc("""
                        Sets the time interval between the trigger event and the display reference
                        point on the screen. The display reference point is either left, right, or
                        center and is set with the timebase.reference property. The maximum
                        position value depends on the time/division settings.
                        """))
        ivi.add_property(self, 'timebase.range',
                        self._get_timebase_range,
                        self._set_timebase_range,
                        None,
                        ivi.Doc("""
                        Sets the full-scale horizontal time in seconds for the main window. The
                        range is 10 times the current time-per-division setting.
                        """))
        ivi.add_property(self, 'timebase.scale',
                        self._get_timebase_scale,
                        self._set_timebase_scale,
                        None,
                        ivi.Doc("""
                        Sets the horizontal scale or units per division for the main window.
                        """))
        ivi.add_property(self, 'timebase.window.position',
                        self._get_timebase_window_position,
                        self._set_timebase_window_position,
                        None,
                        ivi.Doc("""
                        Sets the horizontal position in the zoomed (delayed) view of the main
                        sweep. The main sweep range and the main sweep horizontal position
                        determine the range for this command. The value for this command must
                        keep the zoomed view window within the main sweep range.
                        """))
        ivi.add_property(self, 'timebase.window.range',
                        self._get_timebase_window_range,
                        self._set_timebase_window_range,
                        None,
                        ivi.Doc("""
                        Sets the fullscale horizontal time in seconds for the zoomed (delayed)
                        window. The range is 10 times the current zoomed view window seconds per
                        division setting. The main sweep range determines the range for this
                        command. The maximum value is one half of the timebase.range value.
                        """))
        ivi.add_property(self, 'timebase.window.scale',
                        self._get_timebase_window_scale,
                        self._set_timebase_window_scale,
                        None,
                        ivi.Doc("""
                        Sets the zoomed (delayed) window horizontal scale (seconds/division). The
                        main sweep scale determines the range for this command. The maximum value
                        is one half of the timebase.scale value.
                        """))
        ivi.add_property(self, 'display.vectors',
                        self._get_display_vectors,
                        self._set_display_vectors,
                        None,
                        ivi.Doc("""
                        When enabled, draws a line between consecutive waveform data points.
                        """))
        ivi.add_property(self, 'display.grid',
                        self._get_grid_mode,
                        self._set_grid_mode,
                        None,
                        ivi.Doc("""
                        Sets the current grid used in the display. There are multiple grid modes.

                        Values:
                        * 'single'
                        * 'dual'
                        * 'quad'
                        * 'octal'
                        * 'auto'
                        * 'xy'
                        * 'xysingle'
                        * 'xydual'
                        """))
        ivi.add_method(self, 'system.fetch_setup',
                        self._system_fetch_setup,
                        ivi.Doc("""
                        Returns the current oscilloscope setup in the form of a binary block.  The
                        setup can be stored in memory or written to a file and then reloaded to the
                        oscilloscope at a later time with system.load_setup.
                        """))
        ivi.add_method(self, 'system.load_setup',
                        self._system_load_setup,
                        ivi.Doc("""
                        Transfers a binary block of setup data to the scope to reload a setup
                        previously saved with system.fetch_setup.
                        """))
        ivi.add_method(self, 'system.display_string',
                        self._system_display_string,
                        ivi.Doc("""
                        Writes a string to the advisory line on the instrument display.  Send None
                        or an empty string to clear the advisory line.  
                        """))
        ivi.add_method(self, 'display.fetch_screenshot',
                        self._display_fetch_screenshot,
                        ivi.Doc("""
                        Captures the oscilloscope screen and transfers it in the specified format.
                        The display graticule is optionally inverted.
                        """))
        ivi.add_method(self, 'memory.save',
                        self._memory_save,
                        ivi.Doc("""
                        Stores the current state of the instrument into an internal storage
                        register.  Use memory.recall to restore the saved state.
                        """))
        ivi.add_method(self, 'memory.recall',
                        self._memory_recall,
                        ivi.Doc("""
                        Recalls the state of the instrument from an internal storage register
                        that was previously saved with memory.save.
                        """))
        
        self._init_channels()
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        
        super(lecroyBaseScope, self).initialize(resource, id_query, reset, **keywargs)
        
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
            self.utility.reset()

    # Modified for LeCroy, working
    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            lst = self._ask("*IDN?").split(",")
            self._identity_instrument_manufacturer = lst[0]
            self._identity_instrument_model = lst[1]
            self._identity_instrument_firmware_revision = lst[3]
            self._set_cache_valid(True, 'identity_instrument_manufacturer')
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')
    def _get_identity_instrument_manufacturer(self):
        if self._get_cache_valid():
            return self._identity_instrument_manufacturer
        self._load_id_string()
        return self._identity_instrument_manufacturer
    def _get_identity_instrument_model(self):
        if self._get_cache_valid():
            return self._identity_instrument_model
        self._load_id_string()
        return self._identity_instrument_model
    def _get_identity_instrument_firmware_revision(self):
        if self._get_cache_valid():
            return self._identity_instrument_firmware_revision
        self._load_id_string()
        return self._identity_instrument_firmware_revision
    
    def _utility_disable(self):
        pass
    # TODO: Determine how to implement system:error? with LeCroy scope
    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        if not self._driver_operation_simulate:
            error_code, error_message = self._ask(":system:error?").split(',')
            error_code = int(error_code)
            error_message = error_message.strip(' "')
        return (error_code, error_message)
    
    def _utility_lock_object(self):
        pass
    # TODO: test utility reset
    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("*RST")
            self.driver_operation.invalidate_all_attributes()
    
    def _utility_reset_with_defaults(self):
        self._utility_reset()
    # TODO: test self test, check if the time.sleep() is sufficient
    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            self._write("*TST?")
            # wait for test to complete
            time.sleep(40)
            code = int(self._read())
            if code != 0:
                message = "Self test failed"
        return (code, message)
    
    def _utility_unlock_object(self):
        pass
    
    def _init_channels(self):
        try:
            super(lecroyBaseScope, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_name = list()
        self._channel_label = list()
        self._channel_probe_skew = list()
        self._channel_invert = list()
        self._channel_probe_id = list()
        self._channel_bw_limit = list()
        self._channel_input_impedance = list()
        
        self._analog_channel_name = list()
        for i in range(self._analog_channel_count):
            self._channel_name.append("C%d" % (i+1))
            self._channel_label.append("%d" % (i+1))
            self._analog_channel_name.append("C%d" % (i+1))
            self._channel_probe_skew.append(0)
            self._channel_invert.append(False)
            self._channel_probe_id.append("NONE")
            self._channel_bw_limit.append(False)
        
        # digital channels
        self._digital_channel_name = list()
        if (self._digital_channel_count > 0):
            for i in range(self._digital_channel_count):
                self._channel_name.append("digital%d" % i)
                self._channel_label.append("D%d" % i)
                self._digital_channel_name.append("digital%d" % i)

            for i in range(self._analog_channel_count, self._channel_count):
                self._channel_input_frequency_max[i] = 1e9
                self._channel_probe_attenuation[i] = 1
                self._channel_coupling[i] = 'D1M'
                self._channel_offset[i] = 0
                self._channel_range[i] = 1
        
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self.channels._set_list(self._channel_name)
    # TODO: how to implement the following on LeCroy scope?
    def _system_fetch_setup(self):
        if self._driver_operation_simulate:
            return b''
        
        self._write(":system:setup?")
        
        return self._read_ieee_block()
    # TODO: how to implement the following on LeCroy scope?
    def _system_load_setup(self, data):
        if self._driver_operation_simulate:
            return
        
        self._write_ieee_block(data, ':system:setup ')
        
        self.driver_operation.invalidate_all_attributes()
    # TODO: test display_string
    def _system_display_string(self, string = None):
        if string is None:
            string = ""
        
        if not self._driver_operation_simulate:
            self._write("MESSAGE \"%s\"" % string)
    # Modified for LeCroy, working
    def _display_fetch_screenshot(self, format='png', invert=True):
        if self._driver_operation_simulate:
            return b''
        
        if format not in ScreenshotImageFormatMapping:
            raise ivi.ValueNotSupportedException()
        format = ScreenshotImageFormatMapping[format]
        if invert == False:
            color = "BLACK"
        elif invert == True:
            color = "WHITE"
        else:
            color = "WHITE"
        self._write("HCSU DEV,%s,FORMAT,PORTRAIT,BCKG,%s,DEST,\"REMOTE\",PORT,\"NET\",AREA,GRIDAREAONLY" % (str(format), color))
        self._write("SCDP")
        return self._read_raw()

    # TODO: determine how to handle all :timebase: methods for LeCroy
    def _get_timebase_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":timebase:mode?").lower()
            self._timebase_mode = [k for k,v in TimebaseModeMapping.items() if v==value][0]
            self._set_cache_valid
        return self._timebase_mode
    
    def _set_timebase_mode(self, value):
        if value not in TimebaseModeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":timebase:mode %s" % TimebaseModeMapping[value])
        self._timebase_mode = value
        self._set_cache_valid()
    
    def _get_timebase_reference(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":timebase:reference?").lower()
            self._timebase_reference = [k for k,v in TimebaseReferenceMapping.items() if v==value][0]
            self._set_cache_valid
        return self._timebase_reference
    
    def _set_timebase_reference(self, value):
        if value not in TimebaseReferenceMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":timebase:reference %s" % TimebaseReferenceMapping[value])
        self._timebase_reference = value
        self._set_cache_valid()
        
    def _get_timebase_position(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_position = float(self._ask(":timebase:position?"))
            self._set_cache_valid()
        return self._timebase_position
    
    def _set_timebase_position(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":timebase:position %e" % value)
        self._timebase_position = value
        self._set_cache_valid()

    # Modified for LeCroy, working
    def _get_timebase_range(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_scale = float(self._ask("TDIV?"))
            self._timebase_range = self._timebase_scale * self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_scale')
        return self._timebase_range

    # Modified for LeCroy, working
    def _set_timebase_range(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("TDIV %e" % (value / self._horizontal_divisions))
        self._timebase_scale = value / self._horizontal_divisions
        self._timebase_range = value
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_scale')

    # Modified for LeCroy, working
    def _get_timebase_scale(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_scale = float(self._ask("TDIV?"))
            self._timebase_range = self._timebase_scale * self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_range')
        return self._timebase_scale

    # Modified for LeCroy, working
    def _set_timebase_scale(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("TDIV %e" % value)
        self._timebase_scale = value
        self._timebase_range = value * self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_range')
        
    def _get_timebase_window_position(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_window_position = float(self._ask(":timebase:window:position?"))
            self._set_cache_valid()
        return self._timebase_window_position
    
    def _set_timebase_window_position(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":timebase:window:position %e" % value)
        self._timebase_window_position = value
        self._set_cache_valid()
        
    def _get_timebase_window_range(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_window_range = float(self._ask(":timebase:window:range?"))
            self._timebase_window_scale = self._timebase_window_range / self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_window_scale')
        return self._timebase_window_range
    
    def _set_timebase_window_range(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":timebase:window:range %e" % value)
        self._timebase_window_range = value
        self._timebase_window_scale = value / self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_window_scale')
        
    def _get_timebase_window_scale(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_window_scale = float(self._ask(":timebase:window:scale?"))
            self._timebase_window_range = self._timebase_window_scale * self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_window_range')
        return self._timebase_window_scale
    
    def _set_timebase_window_scale(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":timebase:window:scale %e" % value)
        self._timebase_window_scale = value
        self._timebase_window_range = value * self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_window_range')
    
    def _get_display_vectors(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._display_vectors = bool(int(self._ask(":display:vectors?")))
            self._set_cache_valid()
        return self._display_vectors
    
    def _set_display_vectors(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":display:vectors %d" % int(value))
        self._display_vectors = value
        self._set_cache_valid()
    # Modified for LeCroy, working
    def _get_grid_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._display_vectors = str(self._ask("GRID?"))
            self._set_cache_valid()
        return self._display_vectors
    # Modified for LeCroy, working
    def _set_grid_mode(self, value):
        if not self._driver_operation_simulate:
            self._write("GRID %s" % str(value))
        self._display_vectors = str(value)
        self._set_cache_valid()

    def _get_acquisition_start_time(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_start_time = float(self._ask(":waveform:xorigin?"))
            self._set_cache_valid()
        return self._acquisition_start_time
    
    def _set_acquisition_start_time(self, value):
        value = float(value)
        value = value + self._get_acquisition_time_per_record() * 5 / 10
        if not self._driver_operation_simulate:
            self._write(":timebase:position %e" % value)
        self._acquisition_start_time = value
        self._set_cache_valid()
    
    def _get_acquisition_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":acquire:type?").lower()
            self._acquisition_type = [k for k,v in AcquisitionTypeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._acquisition_type
    
    def _set_acquisition_type(self, value):
        if value not in AcquisitionTypeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":acquire:type %s" % AcquisitionTypeMapping[value])
        self._acquisition_type = value
        self._set_cache_valid()
    
    def _get_acquisition_number_of_points_minimum(self):
        return self._acquisition_number_of_points_minimum
    
    def _set_acquisition_number_of_points_minimum(self, value):
        value = int(value)
        self._acquisition_number_of_points_minimum = value

    # Modified for LeCroy, WORKING ON WR104XI-A
    # is MSIZ correct here?
    def _get_acquisition_record_length(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_record_length = int(float(self._ask("MSIZ?")))
            self._set_cache_valid()
        return self._acquisition_record_length

    # Modified for LeCroy, WORKING ON WR104XI-A
    def _get_acquisition_time_per_record(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_time_per_record = float(self._ask("TDIV?")) * self._horizontal_divisions
            self._set_cache_valid()
        return self._acquisition_time_per_record

    # Modified for LeCroy, WORKING ON WR104XI-A
    def _set_acquisition_time_per_record(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("TDIV %e" % (value / self._horizontal_divisions))
        self._acquisition_time_per_record = value * self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(False, 'acquisition_start_time')

    # This method implemented differently in WRXIA, not tested with other LeCroy scope
    def _get_channel_label(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_label[index] = self._ask(":%s:label?" % self._channel_name[index]).strip('"')
            self._set_cache_valid(index=index)
        return self._channel_label[index]

    # This method implemented differently in WRXIA, not tested with other LeCroy scope
    def _set_channel_label(self, index, value):
        value = str(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write(":%s:label \"%s\"" % (self._channel_name[index], value))
        self._channel_label[index] = value
        self._set_cache_valid(index=index)

    # Modified for LeCroy, WORKING ON WR104XI-A
    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            trace = self._ask("%s:TRA?" % self._channel_name[index])
            if trace == "ON":
                self._channel_enabled[index] = True
            elif trace == "OFF":
                self._channel_enabled[index] = False
            self._set_cache_valid(index=index)
        return self._channel_enabled[index]

    # Modified for LeCroy, WORKING ON WR104XI-A
    def _set_channel_enabled(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            if value == False:
                self._write("%s:TRA OFF" % self._channel_name[index])
            elif value == True:
                self._write("%s:TRA ON" % self._channel_name[index])
        self._channel_enabled[index] = value
        self._set_cache_valid(index=index)

    # Edited for LeCroy, NOT WORKING YET
    # TODO: test channel.input_impedance
    def _get_channel_input_impedance(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            val = str(self._ask("%s:coupling?" % self._channel_name[index]))
            if val == 'A1M':
                self._channel_input_impedance[index] = 1000000
                self._channel_input_coupling[index] = "AC"
            elif val == "D1M":
                self._channel_input_impedance[index] = 1000000
                self._channel_input_coupling[index] = "DC"
            elif val == 'D50':
                self._channel_input_impedance[index] = 50
                self._channel_input_coupling[index] = "DC"
            elif val == 'GND':
                self._channel_input_impedance[index] = 1000000
                self._channel_input_coupling[index] = "GND"
            self._set_cache_valid(index=index)
        return self._channel_input_impedance[index], self._channel_input_coupling[index]
    # TODO: test channel.input_impedance
    def _set_channel_input_impedance(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if value not in VerticalCoupling:
            raise Exception('Invalid impedance selection')
        # Check current coupling setting to know if AC or DC
        result = str(self._ask("%s:coupling?" % self._channel_name[index]))
        if result[0] == "A" and value == 1000000:
            coupling = "A1M"
        elif result[0] == "A" and value == 50:
            raise Exception('Invalid impedance selection')
        elif result[0] == "D" and value == 1000000:
            coupling = "D1M"
        elif result[0] == "D" and value == 50:
            coupling = "D50"
        elif result == "GND":
            if value == 50:
                coupling = "D50"
            elif value == 1000000:
                coupling = "D1M"
        else:
            raise Exception('Invalid impedance selection')

        if not self._driver_operation_simulate:
            self._write("%s:coupling %s" % (self._channel_name[index], coupling))
        self._channel_input_impedance[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_input_frequency_max(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        return self._channel_input_frequency_max[index]
    
    def _set_channel_input_frequency_max(self, index, value):
        value = float(value)
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            self._set_channel_bw_limit(index, value < 20e6)
        self._channel_input_frequency_max[index] = value
        self._set_cache_valid(index=index)

    # TODO: test channel.probe_attenuation
    def _get_channel_probe_attenuation(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_attenuation[index] = float(self._ask("%s:attenuation?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_attenuation[index]
    # TODO: test channel.probe_attenuation
    def _set_channel_probe_attenuation(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("%s:attenuation %e" % (self._channel_name[index], value))
        self._channel_probe_attenuation[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_probe_skew(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_skew[index] = float(self._ask(":%s:probe:skew?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_skew[index]
    
    def _set_channel_probe_skew(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:probe:skew %e" % (self._channel_name[index], value))
        self._channel_probe_skew[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_invert(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_invert[index] = bool(int(self._ask(":%s:invert?" % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_invert[index]
    
    def _set_channel_invert(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":%s:invert %e" % (self._channel_name[index], int(value)))
        self._channel_invert[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_probe_id(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_id[index] = self._ask(":%s:probe:id?" % self._channel_name[index])
            self._set_cache_valid(index=index)
        return self._channel_probe_id[index]

    # Modified for LeCroy, WORKING ON WR104XI-A
    def _get_channel_bw_limit(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            # Bandwidth limits are read out all at one time, need to split the list to get specified channel
            limits = (self._ask("BWL?").strip()).split(',')
            if self._channel_name[index] in limits:
                self._channel_bw_limit[index] = limits[limits.index(self._channel_name[index]) + 1]
            self._set_cache_valid(index=index)
        return self._channel_bw_limit[index]

    # Modified for LeCroy, WORKING ON WR104XI-A
    def _set_channel_bw_limit(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            self._write("BWL %s,%s" % (self._channel_name[index], value))
        self._channel_bw_limit[index] = value
        self._set_cache_valid(index=index)
    # TODO: FIX COUPLING AND IMPEDANCE
    def _get_channel_coupling(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_enabled[index] = self._ask("%s:coupling?" % self._channel_name[index]).lower()
            self._set_cache_valid(index=index)
        return self._channel_coupling[index]
    # TODO: FIX COUPLING AND IMPEDANCE
    def _set_channel_coupling(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if value not in VerticalCoupling:
            raise ivi.ValueNotSupportedException()
        # Check current impedance setting to know if 1M, 50, or GND
        result = str(self._ask("%s:coupling?" % self._channel_name[index]))
        if result[1:3] == "1M" and value == "ac":
            coupling = "A1M"
        elif result[1:3] == "50" and value == "ac":
            raise Exception('Invalid coupling selection, set correct impedance')
        elif result[1:3] == "1M" and value == "dc":
            coupling = "D1M"
        elif result[1:3] == "50" and value == "dc":
            coupling = "D50"
        elif result == "GND":
            if value == "dc":
                coupling = "D1M"
            elif value == "ac":
                coupling = "A1M"
        if not self._driver_operation_simulate:
            self._write("%s:coupling %s" % (self._channel_name[index], coupling))
        self._channel_coupling[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_offset[index] = float(self._ask(":%s:offset?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_offset[index]
    
    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:offset %e" % (self._channel_name[index], value))
        self._channel_offset[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_range(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_range[index] = float(self._ask(":%s:range?" % self._channel_name[index]))
            self._channel_scale[index] = self._channel_range[index] / self._vertical_divisions
            self._set_cache_valid(index=index)
            self._set_cache_valid(True, "channel_scale", index)
        return self._channel_range[index]
    
    def _set_channel_range(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:range %e" % (self._channel_name[index], value))
        self._channel_range[index] = value
        self._channel_scale[index] = value / self._vertical_divisions
        self._set_cache_valid(index=index)
        self._set_cache_valid(True, "channel_scale", index)
    
    def _get_channel_scale(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_scale[index] = float(self._ask(":%s:scale?" % self._channel_name[index]))
            self._channel_range[index] = self._channel_scale[index] * self._vertical_divisions
            self._set_cache_valid(index=index)
            self._set_cache_valid(True, "channel_range", index)
        return self._channel_scale[index]
    
    def _set_channel_scale(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:scale %e" % (self._channel_name[index], value))
        self._channel_scale[index] = value
        self._channel_range[index] = value * self._vertical_divisions
        self._set_cache_valid(index=index)
        self._set_cache_valid(True, "channel_range", index)
    
    def _get_measurement_status(self):
        return self._measurement_status
    
    def _get_trigger_coupling(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            cpl = self._ask(":trigger:coupling?").lower()
            noise = int(self._ask(":trigger:nreject?"))
            hf = int(self._ask(":trigger:hfreject?"))
            for k in TriggerCouplingMapping:
                if (cpl, noise, hf) == TriggerCouplingMapping[k]:
                    self._trigger_coupling = k
        return self._trigger_coupling
    
    def _set_trigger_coupling(self, value):
        if value not in TriggerCouplingMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            cpl, noise, hf = TriggerCouplingMapping[value]
            self._write(":trigger:coupling %s" % cpl)
            self._write(":trigger:nreject %d" % noise)
            self._write(":trigger:hfreject %d" % hf)
        self._trigger_coupling = value
        self._set_cache_valid()
    
    def _get_trigger_holdoff(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_holdoff = float(self._ask(":trigger:holdoff?"))
            self._set_cache_valid()
        return self._trigger_holdoff
    
    def _set_trigger_holdoff(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:holdoff %e" % value)
        self._trigger_holdoff = value
        self._set_cache_valid()
    
    def _get_trigger_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_level = float(self._ask(":trigger:level?"))
            self._set_cache_valid()
        return self._trigger_level
    
    def _set_trigger_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:level %e" % value)
        self._trigger_level = value
        self._set_cache_valid()
    
    def _get_trigger_edge_slope(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:edge:slope?").lower()
            self._trigger_edge_slope = [k for k,v in SlopeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_edge_slope
    
    def _set_trigger_edge_slope(self, value):
        if value not in SlopeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:edge:slope %s" % SlopeMapping[value])
        self._trigger_edge_slope = value
        self._set_cache_valid()
    
    def _get_trigger_source(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:source?").lower()
            # TODO process value
            self._trigger_source = value
            self._set_cache_valid()
        return self._trigger_source
    
    def _set_trigger_source(self, value):
        value = str(value)
        if value not in self._channel_name:
            raise ivi.UnknownPhysicalNameException()
        if not self._driver_operation_simulate:
            self._write(":trigger:source %s" % value)
        self._trigger_source = value
        self._set_cache_valid()
    
    def _get_trigger_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("TRMD?").lower()
            if value == 'norm':
                src = self._ask("TRSE?").lower()
                if src == 'line':
                    value = 'ac_line'
            elif value == 'glit':
                qual = self._ask(":trigger:glitch:qualifier?").lower()
                if qual == 'rang':
                    value = 'width'
                else:
                    value = 'glitch'
            else:
                value = [k for k,v in TriggerTypeMapping.items() if v==value][0]
            self._trigger_type = value
            self._set_cache_valid()
        return self._trigger_type
    
    def _set_trigger_type(self, value):
        if value not in TriggerTypeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("TRMD %s" % TriggerTypeMapping[value])
            if value == 'ac_line':
                self._write(":trigger:source line")
            if value == 'glitch':
                if self._trigger_glitch_condition == 'greater_than':
                    self._write(":trigger:glitch:qualifier greaterthan")
                else:
                    self._write(":trigger:glitch:qualifier lessthan")
            if value == 'width':
                self._write(":trigger:glitch:qualifier range")
        self._trigger_type = value
        self._set_cache_valid()
    
    def _measurement_abort(self):
        pass
    
    def _get_trigger_tv_trigger_event(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:tv:mode?").lower()
            # may need processing
            self._trigger_tv_trigger_event = [k for k,v in TVTriggerEventMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_tv_trigger_event
    
    def _set_trigger_tv_trigger_event(self, value):
        if value not in TVTriggerEvent:
            raise ivi.ValueNotSupportedException()
        # may need processing
        if not self._driver_operation_simulate:
            self._write(":trigger:tv:mode %s" % TVTriggerEventMapping[value])
        self._trigger_tv_trigger_event = value
        self._set_cache_valid()
    
    def _get_trigger_tv_line_number(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = int(self._ask(":trigger:tv:line?"))
            # may need processing
            self._trigger_tv_line_number = value
            self._set_cache_valid()
        return self._trigger_tv_line_number
    
    def _set_trigger_tv_line_number(self, value):
        value = int(value)
        # may need processing
        if not self._driver_operation_simulate:
            self._write(":trigger:tv:line %e" % value)
        self._trigger_tv_line_number = value
        self._set_cache_valid()
    
    def _get_trigger_tv_polarity(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:tv:polarity?").lower()
            self._trigger_tv_polarity = [k for k,v in PolarityMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_tv_polarity
    
    def _set_trigger_tv_polarity(self, value):
        if value not in PolarityMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:tv:polarity %s" % PolarityMapping[value])
        self._trigger_tv_polarity = value
        self._set_cache_valid()
    
    def _get_trigger_tv_signal_format(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:tv:standard?").lower()
            self._trigger_tv_signal_format = [k for k,v in TVTriggerFormatMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_tv_signal_format
    
    def _set_trigger_tv_signal_format(self, value):
        if value not in TVTriggerFormatMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:tv:standard %s" % TVTriggerFormatMapping[value])
        self._trigger_tv_signal_format = value
        self._set_cache_valid()
    
    def _get_trigger_glitch_condition(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:glitch:qualifier?").lower()
            if value in GlitchConditionMapping.values():
                self._trigger_glitch_condition = [k for k,v in GlitchConditionMapping.items() if v==value][0]
                self._set_cache_valid()
        return self._trigger_glitch_condition
    
    def _set_trigger_glitch_condition(self, value):
        if value not in GlitchConditionMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:glitch:qualifier %s" % GlitchConditionMapping[value])
        self._trigger_glitch_condition = value
        self._set_cache_valid()
    
    def _get_trigger_glitch_polarity(self):
        return self._get_trigger_width_polarity()
    
    def _set_trigger_glitch_polarity(self, value):
        self._set_trigger_width_polarity(value)
    
    def _get_trigger_glitch_width(self):
        if self._get_trigger_glitch_condition() == 'greater_than':
            return self._get_trigger_width_threshold_low()
        else:
            return self._get_trigger_width_threshold_high()
    
    def _set_trigger_glitch_width(self, value):
        if self._get_trigger_glitch_condition() == 'greater_than':
            self._set_trigger_width_threshold_low(value)
        else:
            self._set_trigger_width_threshold_high(value)
        
    def _get_trigger_width_condition(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:glitch:qualifier?").lower()
            if value in WidthConditionMapping.values():
                self._trigger_width_condition = [k for k,v in WidthConditionMapping.items() if v==value][0]
                self._set_cache_valid()
        return self._trigger_width_condition
    
    def _set_trigger_width_condition(self, value):
        if value not in WidthConditionMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:glitch:qualifier %s" % WidthConditionMapping[value])
        self._trigger_width_condition = value
        self._set_cache_valid()
    
    def _get_trigger_width_threshold_high(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_width_threshold_high = float(self._ask(":trigger:glitch:lessthan?"))
            self._set_cache_valid()
        return self._trigger_width_threshold_high
    
    def _set_trigger_width_threshold_high(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:glitch:lessthan %e" % value)
        self._trigger_width_threshold_high = value
        self._set_cache_valid()
    
    def _get_trigger_width_threshold_low(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_width_threshold_low = float(self._ask(":trigger:glitch:greaterthan?"))
            self._set_cache_valid()
        return self._trigger_width_threshold_low
    
    def _set_trigger_width_threshold_low(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:glitch:greaterthan %e" % value)
        self._trigger_width_threshold_low = value
        self._set_cache_valid()
    
    def _get_trigger_width_polarity(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:glitch:polarity?").lower()
            self._trigger_width_polarity = [k for k,v in PolarityMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_width_polarity
    
    def _set_trigger_width_polarity(self, value):
        if value not in Polarity:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:glitch:polarity %s" % PolarityMapping[value])
        self._trigger_width_polarity = value
        self._set_cache_valid()
    
    def _get_trigger_ac_line_slope(self):
        return self._get_trigger_edge_slope()
    
    def _set_trigger_ac_line_slope(self, value):
        self._set_trigger_edge_slope(value)
    
    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)
        
        if self._driver_operation_simulate:
            return list()
        
        self._write(":waveform:byteorder msbfirst")
        self._write(":waveform:unsigned 1")
        self._write(":waveform:format word")
        self._write(":waveform:points normal")
        self._write(":waveform:source %s" % self._channel_name[index])
        
        # Read preamble
        
        pre = self._ask(":waveform:preamble?").split(',')
        
        format = int(pre[0])
        type = int(pre[1])
        points = int(pre[2])
        count = int(pre[3])
        xincrement = float(pre[4])
        xorigin = float(pre[5])
        xreference = int(float(pre[6]))
        yincrement = float(pre[7])
        yorigin = float(pre[8])
        yreference = int(float(pre[9]))
        
        if type == 1:
            raise scope.InvalidAcquisitionTypeException()
        
        if format != 1:
            raise UnexpectedResponseException()
        
        self._write(":waveform:data?")
        
        # Read waveform data
        raw_data = raw_data = self._read_ieee_block()
        
        # Split out points and convert to time and voltage pairs
        
        data = list()
        for i in range(points):
            x = ((i - xreference) * xincrement) + xorigin
            
            yval = struct.unpack(">H", raw_data[i*2:i*2+2])[0]
            
            if yval == 0:
                # hole value
                y = float('nan')
            else:
                y = ((yval - yreference) * yincrement) + yorigin
            
            data.append((x, y))
        
        return data
    
    def _measurement_read_waveform(self, index, maximum_time):
        return self._measurement_fetch_waveform(index)
    
    def _measurement_initiate(self):
        if not self._driver_operation_simulate:
            self._write(":acquire:complete 100")
            self._write(":digitize")
            self._set_cache_valid(False, 'trigger_continuous')
    
    def _get_reference_level_high(self):
        return self._reference_level_high
    
    def _set_reference_level_high(self, value):
        value = float(value)
        if value < 5: value = 5
        if value > 95: value = 95
        self._reference_level_high = value
        if not self._driver_operation_simulate:
            self._write(":measure:define thresholds, %e, %e, %e" %
                        (self._reference_level_high,
                        self._reference_level_middle,
                        self._reference_level_low))
    
    def _get_reference_level_low(self):
        return self._reference_level_low
    
    def _set_reference_level_low(self, value):
        value = float(value)
        if value < 5: value = 5
        if value > 95: value = 95
        self._reference_level_low = value
        if not self._driver_operation_simulate:
            self._write(":measure:define thresholds, %e, %e, %e" %
                        (self._reference_level_high,
                        self._reference_level_middle,
                        self._reference_level_low))
    
    def _get_reference_level_middle(self):
        return self._reference_level_middle
    
    def _set_reference_level_middle(self, value):
        value = float(value)
        if value < 5: value = 5
        if value > 95: value = 95
        self._reference_level_middle = value
        if not self._driver_operation_simulate:
            self._write(":measure:define thresholds, %e, %e, %e" %
                        (self._reference_level_high,
                        self._reference_level_middle,
                        self._reference_level_low))
    
    def _measurement_fetch_waveform_measurement(self, index, measurement_function, ref_channel = None):
        index = ivi.get_index(self._channel_name, index)
        if index < self._analog_channel_count:
            if measurement_function not in MeasurementFunctionMapping:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMapping[measurement_function]
        else:
            if measurement_function not in MeasurementFunctionMappingDigital:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMappingDigital[measurement_function]
        if not self._driver_operation_simulate:
            l = func.split(' ')
            l[0] = l[0] + '?'
            if len(l) > 1:
                l[-1] = l[-1] + ','
            func = ' '.join(l)
            query = ":measure:%s %s" % (func, self._channel_name[index])
            if measurement_function in ['ratio', 'phase', 'delay']:
                ref_index = ivi.get_index(self._channel_name, ref_channel)
                query += ", %s" % self._channel_name[ref_index]
            return float(self._ask(query))
        return 0
    
    def _measurement_read_waveform_measurement(self, index, measurement_function, maximum_time):
        return self._measurement_fetch_waveform_measurement(index, measurement_function)
    
    def _get_acquisition_number_of_envelopes(self):
        return self._acquisition_number_of_envelopes
    
    def _set_acquisition_number_of_envelopes(self, value):
        self._acquisition_number_of_envelopes = value
    
    def _measurement_fetch_waveform_min_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        data = list()
        return data
    
    def _measurement_read_waveform_min_max(self, index, maximum_time):
        return _measurement_fetch_waveform_min_max(index)
    
    def _get_trigger_continuous(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_continuous = (int(self._ask(":oper:cond?")) & 1 << 3) != 0
            self._set_cache_valid()
        return self._trigger_continuous
    
    def _set_trigger_continuous(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            t = 'stop'
            if value: t = 'run'
            self._write(":%s" % t)
        self._trigger_continuous = value
        self._set_cache_valid()
    
    def _get_acquisition_number_of_averages(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_number_of_averages = int(self._ask(":acquire:count?"))
            self._set_cache_valid()
        return self._acquisition_number_of_averages
    
    def _set_acquisition_number_of_averages(self, value):
        if value < 1 or value > 65536:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":acquire:count %d" % value)
        self._acquisition_number_of_averages = value
        self._set_cache_valid()
    
    def _get_acquisition_sample_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":acquire:mode?").lower()
            self._acquisition_sample_mode = [k for k,v in SampleModeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._acquisition_sample_mode
    
    def _set_acquisition_sample_mode(self, value):
        if value not in SampleModeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":acquire:mode %s" % SampleModeMapping[value])
        self._acquisition_sample_mode = value
        self._set_cache_valid()
    
    def _measurement_auto_setup(self):
        if not self._driver_operation_simulate:
            self._write(":autoscale")
    #TODO: test
    def _memory_save(self, index):
        index = int(index)
        if index < 0 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*sav %d" % index)
    #TODO: test
    def _memory_recall(self, index):
        index = int(index)
        if index < 0 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*rcl %d" % index)
            self.driver_operation.invalidate_all_attributes()
    
    
    


