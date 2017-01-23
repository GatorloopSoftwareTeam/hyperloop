import time
import logging
import RPi.GPIO as GPIO
import constants


def start(pod_data, drive_controller):

    initial_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
    iteration = 0

    while True:
        if pod_data.stopped:
            break
        logging.debug("Checking e-brake conditions. Y_G is " + str(pod_data.acceleration.y_g))

        expected_velocity = initial_velocity - 1.4 * 9.8 * iteration
        measured_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
        if measured_velocity - expected_velocity > 10:
            logging.debug("brakes are not stopping fast enough. activate the second one")
            drive_controller.send_engage_auxiliary_brakes()
            while drive_controller.get_response() != constants.ENGAGE_AUXILIARY_BRAKES:
                drive_controller.send_engage_auxiliary_brakes()
                time.sleep(.1)
            logging.debug("second brake activated")
            break
        else:
            logging.debug("brakes are stopping fine, pod still going")


