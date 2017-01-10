import socket
import constants
import re


def recieve_suspension_tcp(tcp_sock, pod_data):
    while True:
        vcu_tcp_received_message = tcp_sock.recv(1024)
        scu_message_request =  struct.unpack_from(network_endinanness+'BB', vcu_tcp_received_message)
        print >>sys.stderr, 'TCP received "%s"' % [hex(ord(c)) for c in vcu_tcp_received_message]
        print >>sys.stderr, 'TCP received length of TCP datagram "%s"' % len(scu_message_request)

        if (scu_message_request[0] == 0x17): #HEARTBEAT REQUEST
            scu_message_request =  struct.unpack_from(network_endinanness+'BB', vcu_tcp_received_message)
            heartbeat_message_reply = struct.pack(network_endinanness+'BBH', 0x57, 8, 0);
            print >>sys.stderr, 'received: HEARTBEAT REQUEST \TypeID: %d\nPayloadLength: %d' % scu_message_request
            print >>sys.stderr, 'sending: HEARTBEAT REPLY %s' % [hex(ord(c)) for c in heartbeat_message_reply]
            tcp_sock.send(heartbeat_message_reply)

        elif (scu_message_request[0] == 0x50): # PING REPLY
            scu_message_request =  struct.unpack_from(network_endinanness+'BBH', vcu_tcp_received_message)
            print >>sys.stderr, 'received: PING REPLY \TypeID: %d PayloadLength: %d FW vers: %d' % scu_message_request
            
        elif (scu_message_request[0] == 0x51): # START SCU REPLY
            scu_message_request =  struct.unpack_from(network_endinanness+'BBH', vcu_tcp_received_message)
            print >>sys.stderr, 'received: START SCU REPLY \TypeID: %d PayloadLength: %d Start Fault %d' % scu_message_request
            pod_data.scu_sus_started = True

        elif (scu_message_request[0] == 0x54): # STOP SCU REPLY
            scu_message_request =  struct.unpack_from(network_endinanness+'BBH', vcu_tcp_received_message)
            print >>sys.stderr, 'received: STOP SCU REPLY \TypeID: %d PayloadLength: %d Stop Fault %d' % scu_message_request

        elif (scu_message_request[0] == 0x52): # START LOGGING REPLY
            scu_message_request =  struct.unpack_from(network_endinanness+'BB8s', vcu_tcp_received_message)
            print >>sys.stderr, 'received: START LOGGING REPLY \TypeID: %d PayloadLength: %d Filename %s' % scu_message_request
            pod_data.scu_log_started=True

        elif (scu_message_request[0] == 0x53): # START LOGGING REPLY
            scu_message_request =  struct.unpack_from(network_endinanness+'BB8s', vcu_tcp_received_message)
            print >>sys.stderr, 'received: STOP LOGGING REPLY \TypeID: %d PayloadLength: %d Filename %s' % scu_message_request

def init_suspension(pod_data, logging):
	logging.debug("About to init suspension")

	

	port=3000
	ip='192.168.0.10'
	while (sus_inited==False):
		tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_sock.connect((ip, port))
		tcp_sock.settimeout(10) #10 ms

		tcp_sock.send(constants.ping_message_req)

		svu_message_request = tcp.recv(1024)
		if (scu_message_request[0] == 0x50): # PING REPLY
			scu_message_request =  struct.unpack_from(network_endinanness+'BBH', vcu_tcp_received_message)
			print >>sys.stderr, 'received: PING REPLY \TypeID: %d PayloadLength: %d FW vers: %d' % scu_message_request
			logging.debug("Suspension successfully replied to ping")
			
			t = Thread(target=recieve_suspension_tcp, args=(tcp_sock,))
			t.start()

			sus_inited=True
			return tcp_sock
		
	# Create a TCP socket
	
	

