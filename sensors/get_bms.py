import socket
import constants
import datetime
import re


def getBMS(pod_data, sql_wrapper, logging):
    logging.debug("Started BMS thread")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # TODO make this autorecognize its own ip address
    sock.bind(("192.168.0.201", constants.BMS_PORT))
    bms_v_val = 0
    bms_vs_val = 0
    while True:
        bms_recv = sock.recvfrom(1024)[0]

        if bms_recv[0:2] == 'V\t':
            bms_v_val = int(re.match('.*\t([0-9]*)', bms_recv).group(1))

        elif bms_recv[0:2] == 'VS':
            bms_vs_val = int(re.match('.*\t([0-9]*)', bms_recv).group(1))
        # logging.debug("BMS voltage update "+str(bms_v_val))
        sql_wrapper.execute("INSERT INTO bms VALUES (%s,%s,%s)", (datetime.datetime.now(), bms_v_val, bms_vs_val))
