import unittest
from mockito import *
import sys
sys.path.append('../../')
import states.idle_state
import states.demo_motors_state
import states.drive_state
from mysql_wrapper import MySQLWrapper
import datetime
import MySQLdb


class TestIdleState(unittest.TestCase):

    def setUp(self):
        self.mocked_pod_data = mock()
        self.wrapper = mock()
        self.original_raw_input = __builtins__.raw_input

        when(states.demo_motors_state).start(any()).thenReturn(None)
        when(states.drive_state).start(any()).thenReturn(None)

    def tearDown(self):
        __builtins__.raw_input = self.original_raw_input
        unstub()

    def test_save_state(self):
        __builtins__.raw_input = lambda _: '3'
        states.idle_state.start(self.mocked_pod_data, self.wrapper)

        verify(self.wrapper, times=1)\
            .execute(any(), any())

    def test_demo_motors_state(self):
        __builtins__.raw_input = lambda _: '1'
        input_response = states.idle_state.request_input(self.mocked_pod_data, self.wrapper)

        verify(states.demo_motors_state, times=1)\
            .start(self.mocked_pod_data)
        verify(states.drive_state, times=0)\
            .start(self.wrapper)
        self.assertEqual(input_response, False)

    def test_drive_state(self):
        __builtins__.raw_input = lambda _: '2'
        input_response = states.idle_state.request_input(self.mocked_pod_data, self.wrapper)

        verify(states.demo_motors_state, times=0) \
            .start(self.mocked_pod_data)
        verify(states.drive_state, times=1) \
            .start(self.wrapper)
        self.assertEqual(input_response, False)


if __name__ == '__main__':
    unittest.main()
