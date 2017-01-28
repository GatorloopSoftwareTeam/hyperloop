import logging
import sys
import thread
import time

import MySQLdb

import states.brake_2_state
import states.brake_state
import states.demo_motors_state
import states.fault_state
import states.initialization_state
import states.push_state
import states.ready_state
import states.ready_state
import states.sensor_data_acquisition_state
import states.sensor_data_acquisition_state
import states.wait_for_pod_to_stop_state
import ready_listener
from drive_controller import DriveController
from dto.pod_data import PodData
from mysql_wrapper import MySQLWrapper
from reporters.spacex_udp_sender import spacex_udp_sender


def enter_fault_state():
    states.fault_state.start(pod_data, sql_wrapper)
    # Give it time to send fault state to spacex and abort
    time.sleep(10)
    sys.exit(1)


logging.basicConfig(filename='test.log', level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
pod_data = PodData()
sql_wrapper = MySQLWrapper(logging)
thread.start_new_thread(spacex_udp_sender, (pod_data,logging))
drive_controller = DriveController()

inited_tty = None
suspension_tcp_socket = None
try:
    inited_tty, suspension_tcp_socket = states.initialization_state.start(pod_data, sql_wrapper, drive_controller)
except MySQLdb.OperationalError, e:
    logging.error("Initialization state failed because of mysql operational error: " + str(e) + ". Aborting run...")
    enter_fault_state()
except RuntimeError, e:
    logging.error(e)
    enter_fault_state()

ready_listener.start_listener(pod_data, sql_wrapper)
states.sensor_data_acquisition_state.start(pod_data, suspension_tcp_socket, sql_wrapper, logging, inited_tty)
states.ready_state.start(pod_data, sql_wrapper)

try:
    states.push_state.start(pod_data, inited_tty, sql_wrapper)
except MySQLdb.OperationalError, e:
    # figure out what to do here
    # TODO: WRONG!!!!
    pass

states.brake_state.start(pod_data, sql_wrapper, drive_controller)
thread.start_new_thread(states.wait_for_pod_to_stop_state.start, (pod_data, sql_wrapper, drive_controller))
states.brake_2_state.start(pod_data, drive_controller, sql_wrapper)



