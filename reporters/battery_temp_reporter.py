import constants
import socket
from time import sleep

def battery_temp_reporter(pod_data, logging):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    while True:
        try:
            # send state via udp socket
            battery_temp_str = ("%s,%s,%s" % pod_data.battery_m1_temp, pod_data.battery_m2_temp, pod_data.battery_m3_temp)
            computer = "main"
            if(computer == "main"):
                battery_temp_str = (
                "%s,%s,%s" % pod_data.main_battery_1_temp, pod_data.main_battery_2_temp, pod_data.main_battery_3_temp)
                sock.sendto(battery_temp_str, (constants.AUX_UDP_IP, constants.MAIN_UDP_BATT_PORT))
            else:
                battery_temp_str = (
                "%s,%s,%s" % pod_data.aux_battery_1_temp, pod_data.aux_battery_2_temp, pod_data.aux_battery_3_temp)
                sock.sendto(battery_temp_str, (constants.MAIN_UDP_IP, constants.MAIN_UDP_BATT_PORT))

        except Exception, e:
            logging.debug("send_suspension_telemetry: UDP packet failed to send with error: " + str(e))
        sleep(1)