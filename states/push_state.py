import Queue
import datetime
import logging
import thread

import constants
from sensors.get_roof_speed import getRoofSpeed
from sensors.get_speed import getSpeed


def start(pod_data, inited_tty, sql_wrapper):
    push_start_time = datetime.datetime.now()
    # set database to push
    pod_data.state = constants.STATE_PUSHING
    logging.debug("Now in PUSH state")
    sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "PUSH STARTED"))

    # update speed from R wheel
    logging.debug("read_wheel = " + str(constants.READ_WHEEL))
    logging.debug("read_roof = " + str(constants.READ_ROOF))
    q = Queue.Queue()
    if constants.READ_WHEEL == 1:
        # start all speed getting threads
        wheel1 = thread.start_new_thread(getSpeed, (
            inited_tty["wheel1"], "wheel1", constants.WHEEL_CIRCUMFERENCE, constants.DIST_BRAKE, pod_data.acceleration,
            sql_wrapper, logging, q))
        wheel2 = thread.start_new_thread(getSpeed, (
            inited_tty["wheel2"], "wheel2", constants.WHEEL_CIRCUMFERENCE, constants.DIST_BRAKE, pod_data.acceleration,
            sql_wrapper, logging, q))

    if constants.READ_ROOF == 1:
        thread.start_new_thread(getRoofSpeed, (
            inited_tty["roof"], "roof", constants.NUM_STRIPES_BRAKE, constants.NUM_STRIPES_PANIC, pod_data.acceleration,
            sql_wrapper, logging, q))

    # will block until we get the brake command
    q.get()

    # do not brake if we are still being pushed
    while datetime.datetime.now() - push_start_time > constants.TOTAL_PUSH_TIME:
        continue

    logging.debug("Got a brake command")