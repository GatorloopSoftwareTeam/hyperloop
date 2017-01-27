import socket
import constants
import time
import struct
import sys
from threading import Thread


def recieve_suspension_tcp(tcp_sock, pod_data):
    while True:
        vcu_tcp_received_message = tcp_sock.recv(1024)
        scu_message_request =  struct.unpack_from(constants.network_endinanness+'BB', vcu_tcp_received_message)
        #print >>sys.stderr, 'TCP received "%s"' % [hex(ord(c)) for c in vcu_tcp_received_message]
        #print >>sys.stderr, 'TCP received length of TCP datagram "%s"' % len(scu_message_request)

        if (scu_message_request[0] == 0x17): #HEARTBEAT REQUEST
            scu_message_request =  struct.unpack_from(constants.network_endinanness+'BB', vcu_tcp_received_message)
            heartbeat_message_reply = struct.pack(constants.network_endinanness+'BBH', 0x57, 8, 0);
            #print >>sys.stderr, 'received: HEARTBEAT REQUEST \TypeID: %d\nPayloadLength: %d' % scu_message_request
            #print >>sys.stderr, 'sending: HEARTBEAT REPLY %s' % [hex(ord(c)) for c in heartbeat_message_reply]
            tcp_sock.send(heartbeat_message_reply)

        elif (scu_message_request[0] == 0x50): # PING REPLY
            scu_message_request =  struct.unpack_from(constants.network_endinanness+'BBH', vcu_tcp_received_message)
            print >>sys.stderr, 'received: PING REPLY \TypeID: %d PayloadLength: %d FW vers: %d' % scu_message_request
            
        elif (scu_message_request[0] == 0x51): # START SCU REPLY
            scu_message_request =  struct.unpack_from(constants.network_endinanness+'BBH', vcu_tcp_received_message)
            print >>sys.stderr, 'received: START SCU REPLY \TypeID: %d PayloadLength: %d Start Fault %d' % scu_message_request
            # Check Suspension Response
            if (scu_message_request[2]==0x00):
                # We received a successful response
                pod_data.scu_sus_started_tcp = True

        elif (scu_message_request[0] == 0x54): # STOP SCU REPLY
            scu_message_request =  struct.unpack_from(constants.network_endinanness+'BBH', vcu_tcp_received_message)
            print >>sys.stderr, 'received: STOP SCU REPLY \TypeID: %d PayloadLength: %d Stop Fault %d' % scu_message_request
            if (scu_message_request[2]==0x00):
                # We received a successful response
                pod_data.scu_sus_started_tcp = False

        elif (scu_message_request[0] == 0x52): # START LOGGING REPLY
            scu_message_request =  struct.unpack_from(constants.network_endinanness+'BB8s', vcu_tcp_received_message)
            print >>sys.stderr, 'received: START LOGGING REPLY \TypeID: %d PayloadLength: %d Filename %s' % scu_message_request
            pod_data.scu_log_started_tcp = True


        elif (scu_message_request[0] == 0x53): # STOP LOGGING REPLY
            scu_message_request =  struct.unpack_from(constants.network_endinanness+'BB8s', vcu_tcp_received_message)
            print >>sys.stderr, 'received: STOP LOGGING REPLY \TypeID: %d PayloadLength: %d Filename %s' % scu_message_request
            if (scu_message_request[2]==0x00):
                # We received a successful response
                pod_data.scu_log_started_tcp = False

def recieve_suspension_udp(pod_data, logging):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('',3000))
    while True:
        try:
            msg = udp_sock.recv(4096)
        except socket.timeout, e:
            err = e.args[0]
            # this next if/else is a bit redundant, but illustrates how the
            # timeout exception is setup
            if err == 'timed out':
                #print 'recv timed out, retry later'
                continue
            else:
                print e
                sys.exit(1)
        except socket.error, e:
            # Something else happened, handle error, exit, etc.
            print e
            sys.exit(1)
        else:
            if len(msg) != 0:
                vcu_udp_received_message =  struct.unpack_from(constants.network_endinanness+'BB', msg)

                # Handling UDP received package

                if (vcu_udp_received_message[0] == 0x21):
                    vcu_udp_received_message =  struct.unpack_from(constants.network_endinanness+'BBfffffffHH', msg)
                    #print 'SUSPENSION TRAVELS FL: %f FR: %f RL: %f RR: %f X Acc: %f Y Acc:  %f Z Acc:  %f Faults:  %d Status: %d' % vcu_udp_received_message[2:]

                    #logging.debug(vcu_udp_received_message[9])
                    #logging.debug(vcu_udp_received_message[10])
                    if vcu_udp_received_message[9] == 0 and vcu_udp_received_message[10] == 4:
                        #logging.debug("Got a fault 0 and sus started i think")
                        pod_data.scu_sus_started_udp = True
                    elif vcu_udp_received_message[9] == 0 and vcu_udp_received_message[10] == 3:
                        #logging.debug("Got a fault 0 and sus stopped i think")
                        pod_data.scu_sus_started_udp = False
                    #faults is [9]
                    #status is [10]
                elif (vcu_udp_received_message[0] == 0x22):
                    vcu_udp_received_message =  struct.unpack_from(constants.network_endinanness+'BBffff', msg)
                    #print 'PAD DISTANCES FL: %f FR Pad: %f RL: %f RR Pad: %f' % vcu_udp_received_message[2:]
                else:
                    print 'UDP received "%s"' % [hex(ord(c)) for c in vcu_udp_received_message]

def init_suspension(pod_data, logging):
    logging.debug("About to init suspension")
    port=3000
    ip='192.168.0.10'
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((ip, port))
    tcp_sock.settimeout(2) #10 ms
    while (pod_data.sus_inited==False):
        # Send the suspension a ping
        tcp_sock.send(constants.ping_message_req)
        logging.debug("Sent suspension ping")

        # Get ping response
        vcu_tcp_received_message = tcp_sock.recv(1024)
        scu_message_request =  struct.unpack_from(constants.network_endinanness+'BB', vcu_tcp_received_message)
        print >>sys.stderr, 'TCP received "%s"' % [hex(ord(c)) for c in vcu_tcp_received_message]
        print >>sys.stderr, 'TCP received length of TCP datagram "%s"' % len(scu_message_request)

        # If ping replies successfully
        if (scu_message_request[0] == 0x50):
            scu_message_request =  struct.unpack_from(constants.network_endinanness+'BBH', vcu_tcp_received_message)
            print >>sys.stderr, 'received: PING REPLY \TypeID: %d PayloadLength: %d FW vers: %d' % scu_message_request
            logging.debug("Suspension successfully replied to ping")

            # Start the listener for tcp replies
            t = Thread(target=recieve_suspension_tcp, args=(tcp_sock, pod_data))
            t.start()

            # Start the listener for udp steam data
            t = Thread(target=recieve_suspension_udp, args=(pod_data, logging))
            t.start()

            logging.debug("Testing starting suspension")
            # Turn the active suspension on
            tcp_sock.send(constants.start_scu_message_req)

            # Wait for the udp stream data that says suspension on
            while pod_data.scu_sus_started_udp == False:
                time.sleep(1)
                continue
            logging.debug("Suspension is on, sleeping 5 secs")

            time.sleep(5)

            # Turn the active suspension off
            logging.debug("Testing stopping suspension")
            tcp_sock.send(constants.stop_scu_message_req)

            # Wait for the udp stream data that says suspension off
            while pod_data.scu_sus_started_udp == True:
                time.sleep(1)
                continue
            logging.debug("Suspension is off")

            # If we got here then we have done a ping and a full power up and power off test
            logging.debug("Suspension functionality has passed full test")
            pod_data.sus_inited = True

            #while pod_data.sus_inited == False:
            #    time.sleep(1)
            #    continue
            #sus_inited=True
            return tcp_sock
        else:
            logging.debug("Suspension sent something else")
            #logging.debug(struct.unpack_from(constants.network_endinanness+'BB', scu_message_request))

