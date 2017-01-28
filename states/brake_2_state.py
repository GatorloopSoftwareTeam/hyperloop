import time
import logging
import constants
import datetime


def start(pod_data, drive_controller, sql_wrapper):
    previous_velocity_sample_time = datetime.datetime.now()
    previous_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)

    while True:
        if pod_data.stopped:
            logging.debug("POD STOPPED")
            break
        measured_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
        #calculated_acceleration = \
        #    (measured_velocity - previous_velocity)/(datetime.datetime.now() - previous_velocity_sample_time).total_seconds()
        calculated_acceleration = 50
        logging.debug("calced acc " + str(calculated_acceleration))
        if calculated_acceleration > 1.3 * constants.GRAVITY:
            logging.debug("brakes are not stopping fast enough. pulse brakes")
            drive_controller.send_pulse_main_brakes()
            drive_controller.send_pulse_aux_brakes()
        else:
            logging.debug("brakes are stopping fine, pod still going")

        time.sleep(.1)
        previous_velocity_sample_time = datetime.datetime.now()
        previous_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
        time.sleep(.3)