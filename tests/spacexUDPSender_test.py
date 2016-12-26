import sys
sys.path.append('../')
import logging
import socket
import unittest
from spacexUDPSender import *
from dto.podData import PodData
from mockito import *


class TestSpacedUDPSender(unittest.TestCase):

    def test_happy_path(self):
        mocked_socket = mock()
        mocked_logging = mock()
        when(socket).socket(socket.AF_INET, socket.SOCK_DGRAM).thenReturn(mocked_socket)
        when(mocked_socket).sendto(any(), any(tuple)).thenReturn(None)
        pod_data = PodData()
        self.assertTrue(send_pod_data(pod_data, mocked_logging))
        verify(mocked_logging, times=1).debug("sending a state message to spacex: " + pod_data.to_str())
        unstub()

    def test_socket_initialization_fails(self):
        mocked_socket = mock()
        mocked_logging = mock()
        exception_message = "Socket initialization failed"
        when(socket).socket(socket.AF_INET, socket.SOCK_DGRAM).thenRaise(Exception(exception_message))
        when(mocked_socket).sendto(any(), any(tuple)).thenReturn(None)
        pod_data = PodData()
        self.assertFalse(send_pod_data(pod_data, mocked_logging))
        verify(mocked_logging, times=1).debug("send_pod_data: UDP packet failed to send with error: " + exception_message)
        unstub()

    def test_socket_connection_fails(self):
        mocked_socket = mock()
        mocked_logging = mock()
        when(socket).socket(socket.AF_INET, socket.SOCK_DGRAM).thenReturn(mocked_socket)
        when(mocked_socket).sendto(any(), any(tuple)).thenRaise(Exception("Could not connect to host"))
        pod_data = PodData()
        self.assertFalse(send_pod_data(pod_data, mocked_logging))
        verify(mocked_logging, times=1).debug("sending a state message to spacex: " + pod_data.to_str())
        unstub()

if __name__ == '__main__':
    unittest.main()
