import socket
import constants

def init_bms(pod_data, logging):
    logging.debug("About to init BMS")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # TODO make this autorecognize its own ip address
    sock.bind(("192.168.0.203", constants.BMS_PORT))
    while True:
	    bms_recv = int(sock.recvfrom(1024)[0])
	    if bms_recv>12000 and bms_recv<18000:
	    	pod_data.voltage = bms_recv
	    	logging.debug("BMS initialized with voltage "+str(bms_recv))
	    	return 1
	    elif bms_recv>5000 and bms_recv<=12000:
	    	logging.debug("Potential low battery, BMS indicated voltage " + str(bms_recv))
