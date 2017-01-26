import time
import logging
import constants
import datetime


def start(pod_data, drive_controller, sql_wrapper):
    initial_time = datetime.datetime.now()
    initial_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
    time.sleep(2)
    iteration = 0
    aux_brakes_activated = False

    while True:
        if pod_data.stopped:
            logging.debug("POD STOPPED")
            break
        expected_velocity = initial_velocity - 1.4 * 9.8 * (initial_time - datetime.datetime.now()).total_seconds()
        measured_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
        if measured_velocity > expected_velocity * 1.1:
            logging.debug("brakes are not stopping fast enough. activate the second one")
            drive_controller.send_pulse_auxiliary_brakes()
            while drive_controller.get_response() != constants.PULSE_AUXILIARY_BRAKES + "\n":
                drive_controller.send_pulse_auxiliary_brakes()
                time.sleep(.1)
            sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""",
                                (datetime.datetime.now().strftime(constants.TIME_FORMAT), "AUX BRAKE ENGAGED"))
            logging.debug("second brake activated")
            break
        else:
            logging.debug("brakes are stopping fine, pod still going")

    time.sleep(1)

    while True:
        if pod_data.stopped:
            logging.debug("POD STOPPED")
            break
        expected_velocity = initial_velocity - 1.4 * 9.8 * (initial_time - datetime.datetime.now()).total_seconds()
        measured_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
        if measured_velocity > expected_velocity * 1.1:
            logging.debug("Brakes are not stopping fast enough. Full force on both!")
            drive_controller.send_engage_main_brakes()
            while drive_controller.get_response() != constants.ENGAGE_MAIN_BRAKES + "\n":
                drive_controller.send_engage_main_brakes()
                time.sleep(.1)
            drive_controller.send_engage_auxiliary_brakes()
            while drive_controller.get_response() != constants.ENGAGE_AUXILIARY_BRAKES + "\n":
                drive_controller.send_engage_auxiliary_brakes()
                time.sleep(.1)
            sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""",
                                (datetime.datetime.now().strftime(constants.TIME_FORMAT), "FULL FORCE ENGAGE!!!"))
            break
        else:
            logging.debug("Speed is OK. Both brakes pulsing.")