import logging
import datetime
import thread
import time
from sensors.get_acc import getAcc
from sensors.get_bms import getBMS
from sensors.get_battery_temperature import get_battery_temperature


def start(pod_data, sql_wrapper):
    logging.debug("Now in SENSOR DATA ACQUISITION state")
    sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "SENSOR DATA ACQUISITION STARTED"))
    thread.start_new_thread(getBMS, (pod_data, sql_wrapper, logging))
    thread.start_new_thread(getAcc, (pod_data, sql_wrapper, logging))
    thread.start_new_thread(get_battery_temperature, pod_data)
    time.sleep(5)
