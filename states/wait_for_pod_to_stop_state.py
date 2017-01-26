import datetime
import MySQLdb
import logging
import time
import constants


def _check_pod_is_stopped(pod_data):
       #pod_data.acceleration.y_g < 0.1 and
    if datetime.datetime.now() - pod_data.last_speed_update > datetime.timedelta(seconds=constants.SPEED_UPDATE_TIMEDIFF_SEC):
        #if the time difference is more than 2 seconds, we haven't gotten a speed in a while
        return True
    return False


def start(pod_data, sql_wrapper, drive_controller):
    try:
        sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "WAITING FOR POD TO STOP"))
    except MySQLdb.OperationalError, e:
        # Ignore error because we need to keep braking
        logging.error(e)

    while True:
        # be sure that we're stopped
        if pod_data.acceleration.y_g < 0.1:
            if _check_pod_is_stopped(pod_data):
                break

    try:
        sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "POD IS STOPPED"))
    except MySQLdb.OperationalError, e:
        # Ignore error because we need to keep braking
        logging.error(e)

    pod_data.stopped = True
    logging.debug("POD IS STOPPED")
    drive_controller.send_stopped()

    while drive_controller.get_response() != constants.STOPPED + "\n":
        drive_controller.send_stopped()
        time.sleep(.1)

    logging.debug("Pod is stopped. Turning off brakes")
    drive_controller.send_off_main_brakes()
    while drive_controller.get_response != constants.OFF_BRAKES + "\n":
        drive_controller.send_off_main_brakes()
        time.sleep(.1)

    drive_controller.send_off_auxiliary_brakes()
    while drive_controller.get_response != constants.OFF_AUXILIARY + "\n":
        drive_controller.send_off_auxiliary_brakes()
        time.sleep(.1)

    logging.debug("Brakes are both off")

