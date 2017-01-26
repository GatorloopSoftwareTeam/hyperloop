import logging
import constants
import datetime

from dto.acc_data import AccelerationData


class PodData(object):

    def __init__(self):
        ##Spacex Values
        self.team_id=12

        self.current=0
        self.batt_temp=0
        self.pod_temp=0

        self._state = 1
        # self.speed = 0
        self.acceleration = AccelerationData()
        self.num_stripes_passed = 0
        self.wheel_1_dist = 0
        self.wheel_2_dist = 0
        self.wheel_1_speed = 0
        self.wheel_2_speed = 0
        self.last_speed_update = datetime.datetime(year=datetime.MAXYEAR, month=1, day=1)
        self.v_val = 0
        self.vs_val = 0
        self.main_battery_1_temp = 0
        self.main_battery_2_temp = 0
        self.main_battery_3_temp = 0
        self.aux_battery_1_temp = 0
        self.aux_battery_2_temp = 0
        self.aux_battery_3_temp = 0
        self.pod_temp = 0

        self.sus_inited=False
        self.scu_sus_started=False
        self.scu_log_started=False
        self.stopped = False
        self.push_start_time = 0
        self._state = ''

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if self._state != constants.STATE_FAULT:
            self._state = state
        else:
            logging.debug("Error: trying to change state to " + str(state) + ". Changing from a fault state is not allowed")
