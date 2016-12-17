import socket
def spacexTCPSender(stateQueue,logging):
	UDP_IP="192.168.0.1"
	UDP_PORT=3000
	#get from the QUEUE a state with a timeout of .2 seconds
	#this means we can send the state 5 times every second
	#spacex wants no more than 10
	#a state change will trigger a send faster than waiting .2 secs
	state = 1
	while True:
		oldstate=state
		state = stateQueue.get(.2)
		if(oldstate!=state):
			logging.debug("state change detected in the spacex sender")
		MESSAGE= state
		try:
			#send state via udp socket
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			logging.debug("sending a state message to spacex")
			sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
		except:
			pass