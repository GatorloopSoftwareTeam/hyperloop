import datetime
import time
import constants
import sensors.get_acc
import sensors.get_calc_acc
import thread
from reporters.suspension_telemetry import send_suspension_telemetry


def start(pod_data, suspension_tcp_socket, sql_wrapper, logging, inited_tty):
    logging.debug("Now in SENSOR DATA ACQUISITION state")
    sql_wrapper\
        .execute("""INSERT INTO states VALUES (NULL,%s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "SENSOR DATA ACQUISITION STARTED"))

    thread.start_new_thread(sensors.get_acc.getAcc, (pod_data, sql_wrapper, logging))
    thread.start_new_thread(sensors.get_calc_acc.start, (pod_data, sql_wrapper, logging))

    wheel1 = inited_tty["wheel1"]
    print "Wheel 1 serial open? " + str(wheel1.isOpen())
    wheel1.write(b'r')
    time.sleep(1)
    wheel1_btr = wheel1.inWaiting()
    logging.debug("Wheel 1 bytes to read = " + str(wheel1_btr))
    wheel1_response = wheel1.read(wheel1_btr)
    if wheel1_response != constants.LEFT_WHEEL_OK_RESPONSE:
        logging.error("Wheel 1 sensor not OK. Got response: " + wheel1_response)
        pod_data.state = constants.STATE_FAULT
        sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""",
                            (datetime.datetime.now().strftime(constants.TIME_FORMAT), "FAULT STATE"))

    wheel2 = inited_tty["wheel2"]
    print "Wheel 2 serial open? " + str(wheel2.isOpen())
    wheel2.write(b'r')
    time.sleep(1)
    wheel2_btr = wheel2.inWaiting()
    logging.debug("Wheel 2 bytes to read = " + str(wheel2_btr))
    wheel2_response = wheel2.read(wheel2_btr)
    if wheel2_response != constants.RIGHT_WHEEL_OK_RESPONSE:
        logging.error("Wheel 2 sensor not OK. Got response: " + wheel2_response)
        pod_data.state = constants.STATE_FAULT

    roof = inited_tty["roof"]
    print "roof serial open? " + str(roof.isOpen())
    roof.write(b'r')
    time.sleep(1)
    roof_btr = roof.inWaiting()
    logging.debug("roof bytes to read = " + str(roof_btr))
    roof_response = roof.read(roof_btr)
    if roof_response != constants.ROOF_OK_RESPONSE:
        logging.error("Roof sensor not OK. Got response: " + roof_response)
        pod_data.state = constants.STATE_FAULT
        sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""",
                            (datetime.datetime.now().strftime(constants.TIME_FORMAT), "FAULT STATE"))


    # Turn suspension on
    while not pod_data.scu_sus_started_tcp and not pod_data.scu_sus_started_udp:
        logging.debug("Sending Suspension Start")
        suspension_tcp_socket.send(constants.start_scu_message_req)
        time.sleep(.5)
    while not pod_data.scu_log_started_tcp:
        logging.debug("Sending Logging Start")
        suspension_tcp_socket.send(constants.start_logging_message_req)
        time.sleep(.5)

    thread.start_new_thread(send_suspension_telemetry, (pod_data, logging))

    time.sleep(5)
    if pod_data.state == constants.STATE_FAULT:
        while True:
            logging.debug("Can't enter ready state, in fault state")
            time.sleep(2)
