import time
import constants
import datetime


def start(pod_data, drive_controller, sql_wrapper, logging):
    logging.debug("BRAKE 2 STATE")
    # let us engage to the I-beam first
    time.sleep(constants.TIME_TO_BEAM/1000)
    previous_velocity_sample_time = datetime.datetime.now()
    previous_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
    time.sleep(constants.BRAKING_SAMPLE_TIME)

    while True:
        if pod_data.stopped:
            logging.debug("POD STOPPED")
            break
        logging.debug("previous velocity = " + str(previous_velocity))
        measured_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
        logging.debug("measured_velocity = " + str(measured_velocity))
        current_distance = max(pod_data.wheel_1_dist, pod_data.wheel_2_dist)
        logging.debug("current distance = " + str(current_distance))
        calculated_acceleration = \
            (measured_velocity - previous_velocity)/(datetime.datetime.now() - previous_velocity_sample_time).total_seconds()
        logging.debug("calced acc = " + str(calculated_acceleration))
        expected_stop_distance = constants.STOPPED_DISTANCE+1
        if calculated_acceleration != 0:
            expected_stop_distance = (-1 * (measured_velocity ** 2))/(2 * calculated_acceleration) + current_distance
        logging.debug("Expected stop distance = " + str(expected_stop_distance))
        if expected_stop_distance > constants.STOPPED_DISTANCE:
            logging.debug("PULSE")
            drive_controller.send_pulse_main_brakes()
            drive_controller.send_pulse_auxiliary_brakes()
        else:
            logging.debug("brakes are stopping fine, pod still going")

        previous_velocity_sample_time = datetime.datetime.now()
        previous_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
        time.sleep(constants.BRAKING_SAMPLE_TIME)
        logging.debug("===")
