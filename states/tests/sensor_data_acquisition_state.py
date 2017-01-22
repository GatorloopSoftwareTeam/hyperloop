import unittest
from mockito import *
import sys
sys.path.append('../../')
import states.sensor_data_acquisition_state
from mock import patch, Mock, MagicMock


class TestSensorDataAcquisitionState(unittest.TestCase):

    def setUp(self):
        self.mocked_logging = mock()
        self.mocked_sql_wrapper = mock()
        self.mocked_thread = mock()
        self.mocked_pod_data = mock()
        self.mocked_suspension_tcp_socket = mock()

        when(self.mocked_thread).start_new_thread().thenReturn(None)

    def tearDown(self):
        unstub()

    @patch('sensors.get_bms')
    @patch('sensors.get_acc')
    @patch('sensors.get_battery_temperature')
    def test_happy_path(self):
        self.mocked_pod_data.scu_sus_started = True
        self.mocked_pod_data.scu_log_started = True
        states\
            .sensor_data_acquisition_state.start(self.mocked_pod_data,
                                                 self.mocked_suspension_tcp_socket,
                                                 self.mocked_sql_wrapper,
                                                 self.mocked_logging,
                                                 self.mocked_thread)
        verify(self.mocked_logging, times=1).debug("Now in SENSOR DATA ACQUISITION state")
        verifyNoMoreInteractions(self.mocked_logging)
        verify(self.mocked_sql_wrapper, times=1).execute(any(), any())
        verify(self.mocked_thread, times=3).start_new_thread(any(), any())
        verifyZeroInteractions(self.mocked_suspension_tcp_socket)


