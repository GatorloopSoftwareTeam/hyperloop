import logging

import spacexUDPSender
from dto.accData import AccelerationData


class PodData(object):

    def __init__(self):
        self._state = 1
        self.speed = 0
        self.acceleration = AccelerationData()
        self.num_stripes_passed = 0
        self.wheel_1_dist = 0
        self.wheel_2_dist = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state != self._state:
            self._state = state
            spacexUDPSender.send_pod_data(self, logging)

    # TODO: what do we want to send to spacex?
    def to_str(self):
        return str(
            "STATE: " + str(self._state) + "," +
            "SPEED: " + str(self.speed) + "," +
            "ACCELERATION: X: " + str(self.acceleration.x_g) + " Y: " + str(self.acceleration.y_g) + " Z: " + str(self.acceleration.z_g) + ","

        )