import datetime
import time
import constants
import sensors.get_acc
from reporters.suspension_telemetry import send_suspension_telemetry


def start(pod_data, suspension_tcp_socket, sql_wrapper, logging, thread):
    logging.debug("Now in SENSOR DATA ACQUISITION state")
    sql_wrapper\
        .execute("""INSERT INTO states VALUES (%s,%s)""", (datetime.datetime.now(), "SENSOR DATA ACQUISITION STARTED"))

    thread.start_new_thread(sensors.get_acc.getAcc, (pod_data, sql_wrapper, logging))

    #Turn suspension on
    while not pod_data.scu_sus_started:
        logging.debug("Sending Suspension Start")
        suspension_tcp_socket.send(constants.start_scu_message_req)
        time.sleep(.5)
    while not pod_data.scu_log_started:
        logging.debug("Sending Logging Start")
        suspension_tcp_socket.send(constants.start_logging_message_req)
        time.sleep(.5)
    thread.start_new_thread(send_suspension_telemetry, (pod_data, logging))
    time.sleep(5)
    if(pod_data.state == 0):
        while True:
            logging.debug("Can't enter ready state, in fault state")
            time.sleep(5)
