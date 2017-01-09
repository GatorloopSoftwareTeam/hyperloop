import logging
import time
import constants
import thread


base_dir = '/sys/bus/w1/devices/'
device_temp_file = '/w1_slave'


def _get_device_path(device_directory):
    return base_dir + device_directory + device_temp_file


def _read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def _read_temp(device_file):
    while True:
        lines = _read_temp_raw(device_file)
        while lines[0].strip()[-3:] != 'YES':
            lines = _read_temp_raw(device_file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            formatted_temp_string = float(temp_string) / 1000.0
            print device_file + " = " + str(formatted_temp_string)


def get_battery_temperature():
    logging.debug("Get battery temperature started")

    m1_file = _get_device_path(constants.MAIN_BATTERY_1)
    m2_file = _get_device_path(constants.MAIN_BATTERY_2)
    m3_file = _get_device_path(constants.MAIN_BATTERY_3)
    a1_file = _get_device_path(constants.AUX_BATTERY_1)
    a2_file = _get_device_path(constants.AUX_BATTERY_2)
    a3_file = _get_device_path(constants.AUX_BATTERY_3)

    thread.start_new_thread(_read_temp, (m1_file,))
    thread.start_new_thread(_read_temp, (m2_file,))
    thread.start_new_thread(_read_temp, (m3_file,))
    thread.start_new_thread(_read_temp, (a1_file,))
    thread.start_new_thread(_read_temp, (a2_file,))
    thread.start_new_thread(_read_temp, (a3_file,))

    # while True:

        # pod_data.main_battery_1_temp = _read_temp(m1_file)
        # pod_data.main_battery_2_temp = _read_temp(m2_file)
        # pod_data.main_battery_3_temp = _read_temp(m3_file)
        # pod_data.aux_battery_1_temp = _read_temp(a1_file)
        # pod_data.aux_battery_2_temp = _read_temp(a2_file)
        # pod_data.aux_battery_3_temp = _read_temp(a3_file)
