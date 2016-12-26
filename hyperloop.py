import Queue as queue
import datetime
import logging
import thread
import time

import RPi.GPIO as GPIO

import Constants
from dto.podData import PodData
from getAcc import getAcc
from getRoofSpeed import getRoofSpeed
from getSpeed import getSpeed
from initTTYUSBx import init_tty_usb_x
from mySQLWrapper import MySQLWrapper
from spacexUDPSender import send_pod_data

logging.basicConfig(filename=('test.log'), level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

pod_data = PodData()
wheel_circumference = 12
wheel_1_dist = 0
wheel_2_dist = 0
total_stripes = 0
num_stripes_brake = 3
num_stripes_panic = 70
dist_brake = 40
read_roof = 1
read_wheel = 1
read_acc = 1
coast_detect = 1

# STATE: INITIALIZATION
def INITIALIZATION(sql_wrapper):
    # set database to initialization
    logging.debug("About to write INITIALIZATION state to db")
    # conn = connection_manager.connection
    # x = conn.cursor()
    # try:
        # x.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "INITIALIZATION STARTED"))
        # conn.commit()
    sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "INITIALIZATION STARTED"))
    logging.debug("Wrote state to db")
    # except Exception, e:
    #     logging.debug(e)
        # conn.rollback()

    logging.debug("set pod state to 1 (idle)")
    global pod_data
    pod_data.state = Constants.STATE_IDLE

    # Initialize the spacex message sender


    # logging.debug("initializing read from accelerometer")
    thread.start_new_thread(getAcc, (pod_data, logging))
    time.sleep(5)

    # TODO: figure out how these sensors get ordered each boot up
    # send ruok to optical sensor 1
    logging.debug("About to open serial connections")
    possible_tty = ["0", "1", "2"]
    inited_tty = {}
    for i in possible_tty:
        # pass in list of inited_tty so we can add to it after we initialize
        inited_tty = init_tty_usb_x(i, inited_tty, logging)
    # logging.debug("initted tty is now")
    # logging.debug(inited_tty)
    # x.close()
    return inited_tty


# read status from acc
# if depressurized and if user input OK
# MOVE TO PUSH

# STATE: PUSH
# def PUSH(ser1,ser2,ser3, conn):
def PUSH(inited_tty, sql_wrapper):
    global wheel_circumference, wheel_1_dist, wheel_2_dist, num_stripes_brake, read_wheel, total_stripes, read_roof
    # set database to push
    global pod_data
    pod_data.state = Constants.STATE_PUSH
    logging.debug("Now in PUSH state")
    logging.debug("About to write PUSH state to db")
    # conn = connection_manager.connection
    # cursor = conn.cursor()
    sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "PUSH STARTED"))
    # try:
    #     cursor.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "PUSH STARTED"))
    #     conn.commit()
    #
    # except Exception, e:
    #     logging.debug("Could not insert push state to db with error: " + str(e) + ". Rolling back")
    #     conn.rollback()
    # is this a thing
    # db1.close()
    # conn.close()
    logging.debug("Wrote state to db")
    # update speed from R wheel

    logging.debug("read_wheel = " + str(read_wheel))
    logging.debug("read_roof = " + str(read_roof))
    q = queue.Queue()
    if read_wheel == 1:
        # start all speed getting threads
        wheel1 = thread.start_new_thread(getSpeed, (
        inited_tty["wheel1"], "wheel1", wheel_circumference, dist_brake, pod_data.acceleration, sql_wrapper, logging, q))
        wheel2 = thread.start_new_thread(getSpeed, (
        inited_tty["wheel2"], "wheel2", wheel_circumference, dist_brake, pod_data.acceleration, sql_wrapper, logging, q))

    if read_roof == 1:
        thread.start_new_thread(getRoofSpeed, (
        inited_tty["roof"], "roof", num_stripes_brake, num_stripes_panic, pod_data.acceleration, sql_wrapper, logging, q))

    # if coast_detect==1:
    #	thread.start_new_thread(coastDetect,(conn,logging))

    # will block until we get the brake command
    q.get()
    logging.debug("Just got a brake command")
    # cursor.close()
    # time.sleep(300)


# STATE: BRAKE
def BRAKE(inited_tty, sql_wrapper):
    while True:
        stripe_diff = 0
        stripe_time = 0
        global wheel_circumference, wheel_1_dist, wheel_2_dist, num_stripes_brake, total_stripes, read_roof
        # set database to brake
        # set GPIO to high
        logging.debug("Setting brake 1 to high")
        GPIO.output(17, 1)
        logging.debug("Now in BRAKE state")
        logging.debug("About to write BRAKE state to db")
        # conn = connection_manager.connection
        # db1 = conn.cursor()
        # try:
        #     # db1.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "BRAKE STARTED"))
        #     # conn.commit()
        #     connection_manager.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "BRAKE STARTED"))
        #     logging.debug("Wrote state to db")
        # except Exception as e:
        #     # TODO: maybe add an asynchronous retry instead? don't want to hit the 2nd brakes for an unknown exception
        #     # set second brake anyways
        #     GPIO.output(27, 1)
        #     logging.debug("DATABASE ERROR:" + str(e) + "Set 2nd brake just to make sure")
        #     connection_manager.connection
        #     print e
        #     conn.rollback()
        sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "BRAKE STARTED"))

        logging.debug("BRAKING")
        logging.debug("Sending Spacex Status 5")
        # send spacex state 5 (braking)
        global pod_data
        pod_data.state = Constants.STATE_BRAKING
        # db1.close()


# this monitors initial braking and checks to make sure we don't need to activate second brake
def BRAKE2():
    ##VERY IMPORTANT
    ##THE TIME WE SLEEP FOR IS THE TIME WE WAIT TO SEE IF THE FIRST BRAKE WORKED AND
    ##IF WE NEED TO ACTIVATE THE SECOND BRAKE
    time.sleep(.2)
    ##IM JUST GUESSING HERE
    ##END IMPORTANT
    global pod_data
    while True:
        logging.debug("Y_G is " + str(pod_data.acceleration.y_g))
        ##VERY IMPORTANT
        ##THIS IS THE G WE EXPECT BEFORE ACTIVATING THE SECOND BRAKE
        if pod_data.acceleration.y_g > -.5:
            ##END IMPORTANT
            # TODO: move data into podData
            # If you crashed because you got here it's a good sign
            if pod_data.speed > 10:
                logging.debug("brakes are not stopping fast enough. activate the second one")
                GPIO.output(27, 1)
                logging.debug("second brake activated")
            else:
                logging.debug("not decelerating and below 10 m/s")
                logging.debug("pod stopped")
                return 1
        else:
            logging.debug("brakes are stopping fine, pod still going")


def DRIVE(conn):
    GPIO.output(17, 0)
    GPIO.output(27, 0)
    import wiringpi
    wiringpi.wiringPiSetupGpio()
    # GPIO 1 is hardware PWM, Mode 2 is PWM
    wiringpi.pinMode(1, 2)
    wiringpi.pwmWrite(1, 512)

# TODO: do testing things e.g. actuate brakes
def TESTING():
    global pod_data
    pod_data.state = Constants.STATE_CHECK_SYSTEMS


def send_pod_data_in_interval():
    while True:
        global pod_data
        logging.debug("send pod data interval")
        send_pod_data(pod_data, logging)
        time.sleep(.1)

# INIT GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
# GPIO for brake 1
GPIO.setup(17, GPIO.OUT)
# GPIO for brake 2
GPIO.setup(27, GPIO.OUT)
sql_wrapper = MySQLWrapper(logging)
thread.start_new_thread(send_pod_data_in_interval, ())
inited_tty = INITIALIZATION(sql_wrapper)
# while True:
#     line = raw_input("Enter 1 to enter the testing state, 2 to continue to the push state")
#     if line == "1":
#         TESTING()
#     elif line == "2":
#         break
#     else:
#         print "Invalid input"
#
# # TODO: SET POD STATE 2 (READY)
# # PUSH(ser1,ser2,ser3)
PUSH(inited_tty, sql_wrapper)
BRAKE(inited_tty, sql_wrapper)
BRAKE2()
# DRIVE(conn)




# STATE: COAST
# while True:
# set database to coast
# update speed from R wheel
# update speed from L wheel
# update speed from roof
# count readings(stripes)
# update bms
# update acc
# if passed X stripes
# MOVE TO BRAKE

# STATE: BRAKE
# while True:
# set database to brake
# engage brake 1
# update speed from R wheel
# update speed from L wheel
# update speed from roof
# count readings(stripes)
# update bms
# update acc
# if acceleration < expected
# engage brake 2

# STATE: EXIT
# while True:
# set database to exit
# update speed from R wheel
# update speed from L wheel
# update speed from roof
# count readings(stripes)
# update bms
# update acc
# if user input
# engage drive
