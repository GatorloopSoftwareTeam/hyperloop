import time
import logging
import constants
import datetime


def start(pod_data, drive_controller, sql_wrapper):
    initial_time = datetime.datetime.now()
    # prepare for the worst
    initial_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
    # 20% of total expected brake time - .1 seconds
    time.sleep(1.81)
    previous_velocity_sample_time = datetime.datetime.now()
    previous_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
    # finish 20% of braking time
    time.sleep(.1)
    aux_brakes_activated = False

    while True:
        if pod_data.stopped:
            logging.debug("POD STOPPED")
            break
        measured_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
        calculated_acceleration = \
            (measured_velocity - previous_velocity)/(datetime.datetime.now() - previous_velocity_sample_time).total_seconds()

        # max is closest to the end of the tube
        measured_distance = max(pod_data.wheel_1_dist, pod_data.wheel_2_dist)
        calculated_stopped_distance = \
            measured_distance + ((-1 * measured_velocity) ** 2)/(2 * calculated_acceleration * constants.GRAVITY)
        if calculated_stopped_distance > constants.STOPPED_DISTANCE:
            logging.debug("brakes are not stopping fast enough. activate the second one")
            drive_controller.send_engage_auxililary_brakes()
            while drive_controller.get_response() != constants.ENGAGE_AUXILIARY_BRAKES + "\n":
                drive_controller.send_engage_auxiliary_brakes()
                time.sleep(.1)
            sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""",
                                (datetime.datetime.now().strftime(constants.TIME_FORMAT), "AUX BRAKE ENGAGED"))
            logging.debug("second brake activated")
            break
        else:
            logging.debug("brakes are stopping fine, pod still going")

        previous_velocity_sample_time = datetime.datetime.now()
        previous_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
