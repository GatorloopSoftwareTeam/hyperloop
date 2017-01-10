import socket
import constants
import struct


def send_pod_data(pod_data, logging):
    try:
        # send state via udp socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

        pod_data_str = struct.pack('!BBi7I', pod_data.team_id, pod_data.status, pod_data.acceleration.x, pod_data.wheel_1_dist, pod_data.wheel_1_speed, pod_data.v_val, pod_data.current, pod_data.bat_temp, pod_data.pod_temp, pod_data.num_stripes_passed)
        print pod_data_str
        #pod_data_str = pod_data.to_str()
        #logging.debug("sending a state message to spacex: " + pod_data_str)
        sock.sendto(pod_data_str, (constants.SPACEX_UDP_IP, constants.SPACEX_UDP_PORT))
        return True
    except Exception, e:
        logging.debug("send_pod_data: UDP packet failed to send with error: " + str(e))
        return False
