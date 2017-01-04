import socket
import constants
import datetime

def getBMS(pod_data, sql_wrapper, logging):
	logging.debug("Started BMS thread")
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# TODO make this autorecognize its own ip address
	sock.bind(("192.168.0.203", constants.BMS_PORT))
	while True:
	    bms_recv = int(sock.recvfrom(1024)[0])
	    if bms_recv>1000 and bms_recv<18000:
	    	pod_data.voltage = bms_recv
	    	logging.debug("BMS voltage updated "+str(bms_recv))
	    	sql_wrapper.execute("INSERT INTO bms VALUES (%s,%s)", (datetime.datetime.now(), bms_recv))
	    	