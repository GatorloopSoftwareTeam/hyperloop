import socket
import constants


def send_pod_data(pod_data, logging):
    try:
        # send state via udp socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        pod_data_str = pod_data.to_str()
        #logging.debug("sending a state message to spacex: " + pod_data_str)
        sock.sendto(pod_data_str, (constants.SPACEX_UDP_IP, constants.SPACEX_UDP_PORT))
        return True
    except Exception, e:
        logging.debug("send_pod_data: UDP packet failed to send with error: " + str(e))
        return False
