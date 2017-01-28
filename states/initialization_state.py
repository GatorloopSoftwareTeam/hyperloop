import datetime
import logging
import thread
import time
import socket

import RPi.GPIO as GPIO
import emergency_brake_listener
import kill_power_listener

import constants
from sensors.init_tty_usb_x import init_tty_usb_x
from sensors.init_bms import init_bms
from sensors.get_bms import get_bms
from sensors.init_battery_temperature import init_battery_temperature
from sensors.init_battery_temperature import receive_battery_temperature_udp
from sensors.get_battery_temperature import get_battery_temperature
from sensors.get_proc_temp import get_proc_temp
from sensors.init_suspension import init_suspension
from sensors.init_acc import init_acc

from reporters.battery_temp_reporter import battery_temp_reporter


def start(pod_data, sql_wrapper, drive_controller):
    # INIT GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)
    # GPIO for brake 1
    GPIO.setup(17, GPIO.OUT)
    # GPIO for brake 2
    GPIO.setup(27, GPIO.OUT)

    # clear out old data
    sql_wrapper.execute("""DELETE FROM acc""")
    sql_wrapper.execute("""DELETE FROM battery_m1_temp""")
    sql_wrapper.execute("""DELETE FROM battery_m2_temp""")
    sql_wrapper.execute("""DELETE FROM battery_m3_temp""")
    sql_wrapper.execute("""DELETE FROM bms""")
    sql_wrapper.execute("""DELETE FROM calc_acc""")
    sql_wrapper.execute("""DELETE FROM proc_temp""")
    sql_wrapper.execute("""DELETE FROM roofspeed""")
    sql_wrapper.execute("""DELETE FROM states""")
    sql_wrapper.execute("""DELETE FROM wheel1speed""")
    sql_wrapper.execute("""DELETE FROM wheel2speed""")

    # save initialization state to database
    sql_wrapper.execute("""INSERT INTO states VALUES (NULL, %s, %s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "INITIALIZATION STARTED"))

    logging.debug("set pod state to 1 (idle)")
    pod_data.state = constants.STATE_IDLE

    # start getting processor temperatures
    thread.start_new_thread(get_proc_temp, (sql_wrapper, logging))

    # test the accelerometer
    init_acc(pod_data, sql_wrapper, logging)

    # start to recieve voltage from BMS Pi
    init_bms(pod_data, sql_wrapper, logging)
    thread.start_new_thread(get_bms, (pod_data, sql_wrapper, logging))

    # make sure modprobe commands have been run to init temp sensors
    init_battery_temperature(pod_data, sql_wrapper, logging)
    thread.start_new_thread(get_battery_temperature, (pod_data, sql_wrapper, logging))
    thread.start_new_thread(receive_battery_temperature_udp, (pod_data, logging))
    thread.start_new_thread(battery_temp_reporter,(pod_data,logging))
    # send a ping to the suspension unit
    suspension_tcp_socket = init_suspension(pod_data, logging)

    # start listeners to catch emergency brake or kill power signals
    thread.start_new_thread(emergency_brake_listener.start_listener, (pod_data,))
    thread.start_new_thread(kill_power_listener.start_listener, ())

    drive_controller.set_time_to_brake(constants.TIME_TO_BEAM)
    response = drive_controller.get_response()
    if response != "TTB" + str(constants.TIME_TO_BEAM) + "\n":
        print response
        logging.debug("Time to beam not set!")

    #if not drive_controller.health_check():
    #    raise RuntimeError("Drive controller health check failed!")

    # TODO: figure out how these sensors get ordered each boot up
    # send ruok to optical sensor 1
    logging.debug("About to open serial connections")
    possible_tty = ["0", "1", "2"]
    inited_tty = {}
    for i in possible_tty:
        # pass in list of inited_tty so we can add to it after we initialize
        inited_tty = init_tty_usb_x(i, inited_tty, logging)

    return inited_tty, suspension_tcp_socket
