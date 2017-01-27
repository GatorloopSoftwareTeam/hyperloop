import os
import datetime
import glob
import socket
import constants

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
# TODO import these from a seperate file
base_dir = '/sys/bus/w1/devices/'
device_temp_file = '/w1_slave'


def _read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def _get_device_path(device_directory):
    return base_dir + device_directory + device_temp_file

def receive_battery_temperature_udp(pod_data, logging):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('', constants.MAIN_UDP_BATT_PORT))
    while True:
        msg = udp_sock.recv(4096)
        logging.debug("got a battery temp message of " + msg)



def init_battery_temperature(pod_data, sql_wrapper, logging):
    m1_file = _get_device_path(constants.MAIN_BATTERY_1)
    m2_file = _get_device_path(constants.MAIN_BATTERY_2)
    m3_file = _get_device_path(constants.MAIN_BATTERY_3)
    a1_file = _get_device_path(constants.AUX_BATTERY_1)
    a2_file = _get_device_path(constants.AUX_BATTERY_2)
    a3_file = _get_device_path(constants.AUX_BATTERY_3)

    if constants.COMPUTER == "main":
        device_files = [m1_file, m2_file, m3_file] #, a1_file, a2_file, a3_file]
    else:
        device_files = [a1_file, a2_file, a3_file]
    if constants.computer == "main":
        sensor_number = 1
    else:
        sensor_number = 3
    for device_file in device_files:
        initialized = False
        while not initialized:
            lines = _read_temp_raw(device_file)
            while lines[0].strip()[-3:] != 'YES':
                lines = _read_temp_raw(device_file)
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos + 2:]
                formatted_temp_string = float(temp_string) / 1000.0

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
                # checks for an invalid temp
                if formatted_temp_string >= constants.BATTERY_MAX_TEMP or (0 < formatted_temp_string < constants.BATTERY_LOW_TEMP):
                    logging.debug("Fault: We have a bad battery temperature of %f on device file %s", formatted_temp_string, device_file)
                    # set the fault state
                    pod_data.state = constants.STATE_FAULT
                    sql_wrapper.execute("""INSERT INTO states VALUES (NULL, %s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "FAULT STATE"))
                # checks for a valid temp
                elif  constants.BATTERY_LOW_TEMP <= formatted_temp_string <= constants.BATTERY_MAX_TEMP:
                    logging.debug("Initialized temp sensor %s with temp %f", (device_file, formatted_temp_string))
                    if sensor_number == 1:
                        pod_data.main_battery_1_temp = formatted_temp_string
                    elif sensor_number == 2:
                        pod_data.main_battery_2_temp = formatted_temp_string
                    elif sensor_number == 3:
                        pod_data.main_battery_3_temp = formatted_temp_string
                    elif sensor_number == 4:
                        pod_data.aux_battery_1_temp = formatted_temp_string
                    elif sensor_number == 5:
                        pod_data.aux_battery_2_temp = formatted_temp_string
                    elif sensor_number == 6:
                        pod_data.aux_battery_3_temp = formatted_temp_string
                    sensor_number += 1
                    initialized = True

                else:
                    logging.debug("Error reading temp sensor %s, retrying...", device_file)
        # TODO: change this once they're all connected
        #sensor_number = 4

    return 1
        # if sensor_number == 1:
        #     pod_data.main_battery_1_temp = formatted_temp_string
        # elif sensor_number == 2:
        #     pod_data.main_battery_2_temp = formatted_temp_string
        # elif sensor_number == 3:
        #     pod_data.main_battery_3_temp = formatted_temp_string
        # elif sensor_number == 4:
        #     pod_data.aux_battery_1_temp = formatted_temp_string
        # elif sensor_number == 5:
        #     pod_data.aux_battery_2_temp = formatted_temp_string
        # elif sensor_number == 6:
        #     pod_data.aux_battery_3_temp = formatted_temp_string
        # sensor_number += 1

