import logging
import datetime
import thread
import time
import constants
from sensors.get_acc import getAcc
from sensors.get_bms import getBMS
from sensors.get_battery_temperature import get_battery_temperature


def start(pod_data, suspension_tcp_socket, sql_wrapper):
    logging.debug("Now in SENSOR DATA ACQUISITION state")
    sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "SENSOR DATA ACQUISITION STARTED"))
    thread.start_new_thread(getBMS, (pod_data, sql_wrapper, logging))
    thread.start_new_thread(getAcc, (pod_data, sql_wrapper, logging))
    thread.start_new_thread(get_battery_temperature, pod_data)
    #Turn suspension on
    while pod_data.scu_sus_started==False:
    	suspension_tcp_socket.send(constants.start_scu_message_req)
    while pod_data.scu_log_started=False:
    	suspension_tcp_socket.send(constants.start_logging_message_req)
    time.sleep(5)
