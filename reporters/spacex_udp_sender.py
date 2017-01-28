import socket
import constants
import struct
import time


def spacex_udp_sender(pod_data, logging):
    try:
        # send state via udp socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

        pod_data_str = struct.pack('!BBi7I', pod_data.team_id, pod_data.state, int(pod_data.acceleration.y_g*1000), int(pod_data.wheel_1_dist), int(pod_data.wheel_1_speed*100), int(pod_data.v_val*0.447*100), int(pod_data.current), int(pod_data.main_battery_1_temp), 0, pod_data.num_stripes_passed)
        #print pod_data_str
        #pod_data_str = pod_data.to_str()
        #logging.debug("sending a state message to spacex: " + pod_data_str)
        sock.sendto(pod_data_str, (constants.SPACEX_UDP_IP, constants.SPACEX_UDP_PORT))

    except Exception, e:
        logging.debug("send_pod_data: UDP packet failed to send with error: " + str(e))
    time.sleep(.1)
