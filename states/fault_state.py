import datetime
import constants
import MySQLdb


def start(pod_data, sql_wrapper):
    pod_data.state = constants.STATE_FAULT

    try:
        sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "FAULT STATE"))
    except MySQLdb.OperationalError, e:
        # We probably got here from an operational error but we will try to save the state anyways
        pass
