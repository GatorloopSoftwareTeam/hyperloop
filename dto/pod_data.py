import logging

import spacex_udp_sender
from dto.acc_data import AccelerationData


class PodData(object):

    def __init__(self):
        ##Spacex Values
        self.team_id=1
        self.status=2
        self.current=0
        self.batt_temp=0
        self.pod_temp=0
        

        self._state = 1
        self.speed = 0
        self.acceleration = AccelerationData()
        self.num_stripes_passed = 0
        self.wheel_1_dist = 0
        self.wheel_2_dist = 0
        self.v_val = 0
        self.vs_val = 0
        self.main_battery_1_temp = 0
        self.main_battery_2_temp = 0
        self.main_battery_3_temp = 0
        self.aux_battery_1_temp = 0
        self.aux_battery_2_temp = 0
        self.aux_battery_3_temp = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if self._state != state:
            logging.debug("State changed from " + str(self._state) + " to " + str(state))
        self._state = state

    # TODO: what do we want to send to spacex?
    def to_str(self):
        return str(
            "STATE: " + str(self.state) + "," +
            "SPEED: " + str(self.speed) + "," +
            "ACCELERATION: X: " + str(self.acceleration.x_g) + " Y: " + str(self.acceleration.y_g) + " Z: " + str(self.acceleration.z_g) + ","

        )
