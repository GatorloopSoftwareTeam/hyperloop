import logging
import constants
import datetime
import MySQLdb
import RPi.GPIO as GPIO
from lib.MotorDriver import MotorDriver


def start(pod_data, sql_wrapper, drive_controller):
    logging.debug("Now in BRAKE state")
    while True:
        drive_controller.send_engage_main_brakes()

        try:
            pod_data.state = constants.STATE_BRAKING
            sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "BRAKE STARTED"))
        except MySQLdb.OperationalError, e:
            # Ignore error because we need to keep braking
            logging.error(e)

        logging.debug("BRAKING")
