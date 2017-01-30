import socket
import constants
import struct
import time


def spacex_udp_sender(pod_data, logging):
    while True:
        if pod_data.state == '':
            pod_data.state = 1
        pod_data_str = struct.pack('!BBi7I', int(pod_data.team_id), int(pod_data.state), 0,
                                   int(pod_data.wheel_1_dist), int(pod_data.wheel_1_speed * 100),
                                   int(pod_data.v_val), int(pod_data.current),
                                   int(pod_data.main_battery_1_temp)*10, int(0), int(pod_data.num_stripes_passed))
        try:
            # send state via udp socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

            #print pod_data_str
            #pod_data_str = pod_data.to_str()
            #logging.debug("sending a state message to spacex: " + pod_data_str)
            sock.sendto(pod_data_str, (constants.SPACEX_UDP_IP, constants.SPACEX_UDP_PORT))

        except Exception, e:
            logging.debug("send_pod_data: UDP packet failed to send with error: " + str(e))
        time.sleep(.1)
