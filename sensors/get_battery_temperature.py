import logging
import time
import constants


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
    lines = _read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = _read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        return float(temp_string) / 1000.0


def get_battery_temperature(pod_data):
    logging.debug("Get battery temperature started")

    m1_file = _get_device_path(constants.MAIN_BATTERY_1)
    m2_file = _get_device_path(constants.MAIN_BATTERY_2)
    m3_file = _get_device_path(constants.MAIN_BATTERY_3)
    a1_file = _get_device_path(constants.AUX_BATTERY_1)
    a2_file = _get_device_path(constants.AUX_BATTERY_2)
    a3_file = _get_device_path(constants.AUX_BATTERY_3)

    while True:
        pod_data.main_battery_1_temp = _read_temp(m1_file)
        pod_data.main_battery_2_temp = _read_temp(m2_file)
        pod_data.main_battery_3_temp = _read_temp(m3_file)
        pod_data.aux_battery_1_temp = _read_temp(a1_file)
        pod_data.aux_battery_2_temp = _read_temp(a2_file)
        pod_data.aux_battery_3_temp = _read_temp(a3_file)

        logging.debug("M1 temp = " + str(pod_data.main_battery_1_temp))
        logging.debug("M2 temp = " + str(pod_data.main_battery_2_temp))
        logging.debug("M3 temp = " + str(pod_data.main_battery_3_temp))
        logging.debug("A1 temp = " + str(pod_data.aux_battery_1_temp))
        logging.debug("A2 temp = " + str(pod_data.aux_battery_2_temp))
        logging.debug("A3 temp = " + str(pod_data.aux_battery_3_temp))

        time.sleep(1)
