import constants
import logging
import datetime


def start(pod_data, sql_wrapper):
    pod_data.state = constants.STATE_READY
    logging.debug("Now in READY state")
    sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "READY STARTED"))

    while True:
        # Busy wait for pod to be pushed
        if pod_data.acceleration.y_g > constants.MIN_PUSH_ACCELERATION:
            break
