import socket
import constants
import datetime
import re


def get_bms(pod_data, sql_wrapper, logging):
    logging.debug("Started BMS thread")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # TODO make this autorecognize its own ip address
    sock.bind(('', constants.BMS_PORT))
    bms_v_val = 0
    bms_vs_val = 0
    while True:
        bms_recv = sock.recvfrom(1024)[0]

        if bms_recv[0:2] == 'V\t':
            bms_v_val = int(re.match('.*\t([0-9]*)', bms_recv).group(1))
            if bms_v_val < constants.LOW_BATTERY:
                pod_data.state = constants.STATE_FAULT

        elif bms_recv[0:2] == 'VS':
            bms_vs_val = int(re.match('.*\t([0-9]*)', bms_recv).group(1))
            if bms_vs_val < constants.LOW_BATTERY:
                pod_data.state = constants.STATE_FAULT

        sql_wrapper.execute("INSERT INTO bms VALUES (%s,%s,%s)", (datetime.datetime.now(), bms_v_val, bms_vs_val))
