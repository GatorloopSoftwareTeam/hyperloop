import Queue
import datetime
import logging
import thread
import MySQLdb

import constants
from sensors.get_roof_speed import getRoofSpeed
from sensors.get_speed import getSpeed


def start(pod_data, inited_tty, sql_wrapper):
    pod_data.push_start_time = datetime.datetime.now()
    # set database to push
    pod_data.state = constants.STATE_PUSHING
    logging.debug("Now in PUSH state")
    try:
        sql_wrapper.execute("""INSERT INTO states VALUES (NULL, %s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "PUSH STARTED"))
    except MySQLdb.Error, e:
        logging.error("MySQL error in push state: " + str(e))
        pass

    # update speed from R wheel
    logging.debug("read_wheel = " + str(constants.READ_WHEEL))
    logging.debug("read_roof = " + str(constants.READ_ROOF))
    q = Queue.Queue()
    if constants.READ_WHEEL == 1:
        # start all speed getting threads
        wheel1 = thread.start_new_thread(getSpeed, (
            inited_tty["wheel1"], "wheel1", constants.WHEEL_CIRCUMFERENCE, constants.DIST_BRAKE, pod_data,pod_data.acceleration,
            sql_wrapper, logging, q))
        wheel2 = thread.start_new_thread(getSpeed, (
            inited_tty["wheel2"], "wheel2", constants.WHEEL_CIRCUMFERENCE, constants.DIST_BRAKE, pod_data,pod_data.acceleration,
            sql_wrapper, logging, q))

    if constants.READ_ROOF == 1:
        thread.start_new_thread(getRoofSpeed, (
            inited_tty["roof"], "roof", constants.NUM_STRIPES_BRAKE, constants.NUM_STRIPES_PANIC,pod_data, pod_data.acceleration,
            sql_wrapper, logging, q))

    # will block until we get the brake command
    q.get()

    logging.debug("Got a brake command")

    # do not brake if we are still being pushed
    time_since_push = (datetime.datetime.now() - pod_data.push_start_time)
    while time_since_push.total_seconds() < constants.TOTAL_PUSH_TIME:
        logging.debug("Brake requested. Cannot brake for " + str((constants.TOTAL_PUSH_TIME - time_since_push).total_seconds()) + "seconds")

    logging.debug("We can brake now. Leaving push state")
