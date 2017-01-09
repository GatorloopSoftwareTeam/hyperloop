import logging
import constants
import datetime
import MySQLdb
import time
import RPi.GPIO as GPIO
from lib.MotorDriver import MotorDriver


def start(pod_data, sql_wrapper, drive_controller):
    logging.debug("Now in BRAKE state")

    drive_controller.send_engage_main_brakes()

    while drive_controller.get_response() != constants.ENGAGE_MAIN_BRAKES:
        drive_controller.send_engage_main_brakes()
        time.sleep(.1)

    try:
        pod_data.state = constants.STATE_BRAKING
        sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "BRAKE STARTED"))
    except MySQLdb.OperationalError, e:
        # Ignore error because we need to keep braking
        logging.error(e)

    logging.debug("BRAKING")
