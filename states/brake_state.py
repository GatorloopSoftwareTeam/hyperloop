import logging
import constants
import datetime
import RPi.GPIO as GPIO


def start(pod_data, sql_wrapper):
    logging.debug("Now in BRAKE state")
    while True:
        # set database to brake
        # set GPIO to high
        logging.debug("Setting brake 1 to high")
        GPIO.output(17, 1)
        sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "BRAKE STARTED"))

        logging.debug("BRAKING")
        pod_data.state = constants.STATE_BRAKING
