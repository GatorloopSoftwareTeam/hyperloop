import socket
import sys
import struct

port=3000
ip='192.168.0.10'

if sys.byteorder == 'little':
    network_endinanness='>'
    print >>sys.stderr, 'Network endianness: opposite of system\'s'
else:
    network_endinanness='<'
    print >>sys.stderr, 'Network endianness: same as system\'s'

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect((ip, port))
time.sleep(2)

start_scu_message_req = struct.pack(network_endinanness+'BB', 0x11, 0);
start_logging_message_req = struct.pack(network_endinanness+'BB', 0x12, 0);
stop_scu_message_req = struct.pack(network_endinanness+'BB', 0x14, 0);
stop_logging_message_req = struct.pack(network_endinanness+'BB', 0x13, 0);

tcp_sock.send(stop_logging_message_req)
tcp_sock.send(stop_scu_message_req)