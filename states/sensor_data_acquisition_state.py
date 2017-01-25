import datetime
import time
import constants
import sensors.get_acc
import thread
from reporters.suspension_telemetry import send_suspension_telemetry


def start(pod_data, suspension_tcp_socket, sql_wrapper, logging, inited_tty):
    logging.debug("Now in SENSOR DATA ACQUISITION state")
    sql_wrapper\
        .execute("""INSERT INTO states VALUES (NULL,%s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "SENSOR DATA ACQUISITION STARTED"))

    thread.start_new_thread(sensors.get_acc.getAcc, (pod_data, sql_wrapper, logging))

    # Turn suspension on
    while not pod_data.scu_sus_started:
        logging.debug("Sending Suspension Start")
        suspension_tcp_socket.send(constants.start_scu_message_req)
        time.sleep(.5)
    while not pod_data.scu_log_started:
        logging.debug("Sending Logging Start")
        suspension_tcp_socket.send(constants.start_logging_message_req)
        time.sleep(.5)

    wheel1 = inited_tty["wheel1"]
    wheel1.write(b'r')
    wheel1_response = wheel1.read(wheel1.inWaiting())
    if wheel1_response != constants.LEFT_WHEEL_OK_RESPONSE:
        logging.error("Wheel 1 sensor not OK. Got response: " + wheel1_response)
        pod_data.state = constants.STATE_FAULT

    wheel2 = inited_tty["wheel2"]
    wheel2.write(b'r')
    wheel2_response = wheel2.read(wheel2.inWaiting())
    if wheel2_response != constants.RIGHT_WHEEL_OK_RESPONSE:
        logging.error("Wheel 2 sensor not OK. Got response: " + wheel2_response)
        pod_data.state = constants.STATE_FAULT

    roof = inited_tty["roof"]
    roof.write(b'r')
    roof_response = roof.read(roof.inWaiting())
    if roof_response != constants.ROOF_OK_RESPONSE:
        logging.error("Roof sensor not OK. Got response: " + roof_response)
        pod_data.state = constants.STATE_FAULT

    thread.start_new_thread(send_suspension_telemetry, (pod_data, logging))
    time.sleep(5)
    if pod_data.state == constants.STATE_FAULT:
        while True:
            logging.debug("Can't enter ready state, in fault state")
            time.sleep(2)
