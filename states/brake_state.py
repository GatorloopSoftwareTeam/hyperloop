import logging
import constants
import datetime
import MySQLdb
import time
import constants


def start(pod_data, sql_wrapper, drive_controller):
    logging.debug("Now in BRAKE state")
    try:
        sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""",
                            (datetime.datetime.now().strftime(constants.TIME_FORMAT), "BRAKE STARTED"))
        pod_data.state = constants.STATE_BRAKING
    except MySQLdb.OperationalError, e:
        # Ignore error because we need to keep braking
        logging.error(e)

    drive_controller.send_engage_main_brakes()
    #if drive_controller.get_response() != constants.ENGAGE_MAIN_BRAKES + "\n":
    #    logging.debug("Primary not engaged")
    drive_controller.send_engage_auxiliary_brakes()
    #if drive_controller.get_response() != constants.ENGAGE_AUXILIARY_BRAKES + "\n":
    #    logging.debug("Auxiliary not engaged")

    logging.debug("BRAKES ENGAGED")
