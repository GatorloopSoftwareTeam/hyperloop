import socket
import constants
import re
import datetime


def init_bms(pod_data, sql_wrapper, logging):
    logging.debug("About to init BMS")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', constants.BMS_PORT))
    bms_v_val = 0
    bms_vs_val = 0
    bms_current_val = 0
    while True:
        bms_recv = sock.recvfrom(1024)[0]

        if bms_recv[0:2] == 'V\t':
            bms_v_val = int(re.match('.*\t([0-9]*)', bms_recv).group(1))

        elif bms_recv[0:2] == 'VS':
            bms_vs_val = int(re.match('.*\t([0-9]*)', bms_recv).group(1))
        elif bms_recv[0:1] == 'I':
            bms_current_val = int(re.match('.*\t([0-9]*)', bms_recv).group(1))

        # TODO add the correct battery voltages as parameters
        if constants.LOW_BATTERY < bms_v_val < constants.HIGH_BATTERY and constants.LOW_BATTERY < bms_vs_val < constants.HIGH_BATTERY and bms_current_val > 0:
            pod_data.v_val = bms_v_val
            pod_data.vs_val = bms_vs_val
            logging.debug("BMS initialized with voltage %d and %d", bms_v_val, bms_vs_val)
            sql_wrapper.execute("INSERT INTO bms VALUES (NULL,%s,%s,%s,%s)", (datetime.datetime.now().strftime(constants.TIME_FORMAT), bms_v_val, bms_vs_val, bms_current_val))
            return 1
        # compare to >1 to make sure it isn't just an uninitialized 0
        elif 1 < bms_v_val <= constants.LOW_BATTERY and 1 < bms_vs_val <= constants.LOW_BATTERY:
            logging.debug("FAULT: BMS initialized with invalid voltage %d and %d" % (bms_v_val, bms_vs_val))
            pod_data.state = constants.STATE_FAULT


        # bms_recv = int(sock.recvfrom(1024)[0])
        # if bms_recv>12000 and bms_recv<18000:
        # 	pod_data.voltage = bms_recv
        # 	logging.debug("BMS initialized with voltage "+str(bms_recv))
        # 	return 1
        # elif bms_recv>5000 and bms_recv<=12000:
        # 	logging.debug("Potential low battery, BMS indicated voltage " + str(bms_recv))
