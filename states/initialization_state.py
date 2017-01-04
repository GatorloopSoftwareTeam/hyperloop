import datetime
import logging
import thread
import time
import socket

import RPi.GPIO as GPIO

import constants
from sensors.get_bms import getBMS
from sensors.get_acc import getAcc
from sensors.init_tty_usb_x import init_tty_usb_x
from sensors.init_bms import init_bms


def start(pod_data, sql_wrapper):
    # INIT GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)
    # GPIO for brake 1
    GPIO.setup(17, GPIO.OUT)
    # GPIO for brake 2
    GPIO.setup(27, GPIO.OUT)

    # save initialization state to database
    sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "INITIALIZATION STARTED"))

    logging.debug("set pod state to 1 (idle)")
    pod_data.state = constants.STATE_IDLE

    # start to recieve voltage from BMS Pi
    init_bms(pod_data, logging)
    thread.start_new_thread(getBMS, (pod_data, sql_wrapper, logging))

    thread.start_new_thread(getAcc, (pod_data, sql_wrapper, logging))
    time.sleep(5)

    # TODO: figure out how these sensors get ordered each boot up
    # send ruok to optical sensor 1
    logging.debug("About to open serial connections")
    possible_tty = ["0", "1", "2"]
    inited_tty = {}
    for i in possible_tty:
        # pass in list of inited_tty so we can add to it after we initialize
        inited_tty = init_tty_usb_x(i, inited_tty, logging)

    return inited_tty
