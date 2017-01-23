import socket
import constants
import struct
from sys import byteorder
from time import sleep


def send_suspension_telemetry(pod_data, logging):
    if byteorder == 'little':
        network_endinanness = '>'
    else:
        network_endinanness = '<'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    while True:
        try:
            # send state via udp socket
            suspension_telemetry_str = struct.pack(network_endinanness+'BBff', 0x20, 8, pod_data.wheel_1_speed, pod_data.acceleration.y_g);
            sock.sendto(suspension_telemetry_str, (constants.SUSPENSION_UDP_IP, constants.SUSPENSION_UDP_PORT))
            sleep(.1)
        except Exception, e:
            logging.debug("send_suspension_telemetry: UDP packet failed to send with error: " + str(e))


