import datetime
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


def _read_temp(device_file, pod_data, sql_wrapper, sensor_number):
    while True:
        lines = _read_temp_raw(device_file)
        while lines[0].strip()[-3:] != 'YES':
            lines = _read_temp_raw(device_file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            formatted_temp_string = float(temp_string) / 1000.0

            # check for a bad temperature
            if formatted_temp_string > constants.BATTERY_MAX_TEMP:
                # bad temp, enter fault state
                pod_data.state = constants.STATE_FAULT
                # TODO: save fault state

            if sensor_number == 1:
                pod_data.main_battery_1_temp = formatted_temp_string
                sql_wrapper.execute("""INSERT INTO battery_m1_temp VALUES (NULL, %s,%s)""",
                                    (datetime.datetime.now().strftime(constants.TIME_FORMAT), formatted_temp_string))
            elif sensor_number == 2:
                pod_data.main_battery_2_temp = formatted_temp_string
                sql_wrapper.execute("""INSERT INTO battery_m2_temp VALUES (NULL, %s,%f)""",
                                    (datetime.datetime.now().strftime(constants.TIME_FORMAT), formatted_temp_string))
            elif sensor_number == 3:
                pod_data.main_battery_3_temp = formatted_temp_string
                sql_wrapper.execute("""INSERT INTO battery_m3_temp VALUES (NULL, %s,%f)""",
                                    (datetime.datetime.now().strftime(constants.TIME_FORMAT), formatted_temp_string))
            elif sensor_number == 4:
                pod_data.aux_battery_1_temp = formatted_temp_string
                sql_wrapper.execute("""INSERT INTO battery_a1_temp VALUES (NULL, %s,%f)""",
                                    (datetime.datetime.now().strftime(constants.TIME_FORMAT), formatted_temp_string))
            elif sensor_number == 5:
                pod_data.aux_battery_2_temp = formatted_temp_string
                sql_wrapper.execute("""INSERT INTO battery_a2_temp VALUES (NULL, %s,%f)""",
                                    (datetime.datetime.now().strftime(constants.TIME_FORMAT), formatted_temp_string))
            elif sensor_number == 6:
                pod_data.aux_battery_3_temp = formatted_temp_string
                sql_wrapper.execute("""INSERT INTO battery_a3_temp VALUES (NULL, %s,%f)""",
                                    (datetime.datetime.now().strftime(constants.TIME_FORMAT), formatted_temp_string))


def get_battery_temperature(pod_data, sql_wrapper, logging):
    logging.debug("Get battery temperature started")

    # TODO: change this back after functional test
    # m1_file = _get_device_path(constants.MAIN_BATTERY_1)
    # m2_file = _get_device_path(constants.MAIN_BATTERY_2)
    # m3_file = _get_device_path(constants.MAIN_BATTERY_3)
    # a1_file = _get_device_path(constants.AUX_BATTERY_1)
    # a2_file = _get_device_path(constants.AUX_BATTERY_2)
    # a3_file = _get_device_path(constants.AUX_BATTERY_3)
    #
    # thread.start_new_thread(_read_temp, (m1_file, pod_data, sql_wrapper, 1))
    # thread.start_new_thread(_read_temp, (m2_file, pod_data, sql_wrapper, 2))
    # thread.start_new_thread(_read_temp, (m3_file, pod_data, sql_wrapper, 3))
    # thread.start_new_thread(_read_temp, (a1_file, pod_data, sql_wrapper, 4))
    # thread.start_new_thread(_read_temp, (a2_file, pod_data, sql_wrapper, 5))
    # thread.start_new_thread(_read_temp, (a3_file, pod_data, sql_wrapper, 6))

    high_temp_file = "/home/pi/highTempFile"
    low_temp_file = "/home/pi/lowTempFile"
    reg_temp_file = "/home/pi/regTempFile"

    thread.start_new_thread(_read_temp, (high_temp_file, pod_data, sql_wrapper, 1))
