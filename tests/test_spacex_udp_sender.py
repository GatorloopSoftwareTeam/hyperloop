import sys
sys.path.append('../')
import logging
import socket
import unittest
from spacex_udp_sender import *
from dto.pod_data import PodData
from mockito import *


class TestSpacexUDPSender(unittest.TestCase):

    def setUp(self):
        self.mocked_socket = mock()
        self.mocked_logging = mock()
        self.pod_data = PodData()

    def tearDown(self):
        unstub()

    def test_happy_path(self):
        when(socket).socket(socket.AF_INET, socket.SOCK_DGRAM).thenReturn(self.mocked_socket)
        when(self.mocked_socket).sendto(any(), any(tuple)).thenReturn(None)
        self.assertTrue(send_pod_data(self.pod_data, self.mocked_logging))
        verify(self.mocked_logging, times=1).debug("sending a state message to spacex: " + self.pod_data.to_str())

    def test_socket_initialization_fails(self):
        exception_message = "Socket initialization failed"
        when(socket).socket(socket.AF_INET, socket.SOCK_DGRAM).thenRaise(Exception(exception_message))
        when(self.mocked_socket).sendto(any(), any(tuple)).thenReturn(None)
        self.assertFalse(send_pod_data(self.pod_data, self.mocked_logging))
        verify(self.mocked_logging, times=1).debug("send_pod_data: UDP packet failed to send with error: " + exception_message)

    def test_socket_connection_fails(self):
        when(socket).socket(socket.AF_INET, socket.SOCK_DGRAM).thenReturn(self.mocked_socket)
        when(self.mocked_socket).sendto(any(), any(tuple)).thenRaise(Exception("Could not connect to host"))
        self.assertFalse(send_pod_data(self.pod_data, self.mocked_logging))
        verify(self.mocked_logging, times=1).debug("sending a state message to spacex: " + self.pod_data.to_str())

if __name__ == '__main__':
    unittest.main()
