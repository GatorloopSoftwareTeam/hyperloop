import logging
import thread
import time
import states.initialization_state
import states.testing_state
import states.push_state
import states.brake_state
import states.brake_2_state

from dto.pod_data import PodData
from mysql_wrapper import MySQLWrapper
from spacex_udp_sender import send_pod_data


def send_pod_data_in_interval(data):
    while True:
        send_pod_data(data, logging)
        time.sleep(.1)


logging.basicConfig(filename='test.log', level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
pod_data = PodData()
sql_wrapper = MySQLWrapper(logging)
thread.start_new_thread(send_pod_data_in_interval, pod_data)
inited_tty = states.initialization_state.start(pod_data, sql_wrapper)
while True:
    line = raw_input("Enter 1 to enter the testing state, 2 to continue to the push state")
    if line == "1":
        states.testing_state.start(pod_data)
    elif line == "2":
        break
    else:
        print "Invalid input"

states.push_state.start(pod_data, inited_tty, sql_wrapper)
states.brake_state.start(pod_data, sql_wrapper)
states.brake_2_state.start()

# DRIVE(conn)


# def DRIVE(conn):
#     GPIO.output(17, 0)
#     GPIO.output(27, 0)
#     import wiringpi
#     wiringpi.wiringPiSetupGpio()
#     # GPIO 1 is hardware PWM, Mode 2 is PWM
#     wiringpi.pinMode(1, 2)
#     wiringpi.pwmWrite(1, 512)

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
