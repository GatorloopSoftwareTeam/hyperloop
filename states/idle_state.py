import constants
import datetime
import states.demo_motors_state
import states.drive_state


def request_input(pod_data, sql_wrapper):
    line = raw_input("Enter 1 to enter the check systems state, 2 to enter drive state, 3 to enter the ready state")
    if line == "1":
        states.demo_motors_state.start(pod_data)
        return False
    elif line == "2":
        states.drive_state.start(sql_wrapper)
        return False
    elif line == "3":
        return True
    else:
        print "Invalid input"
        return False


def start(pod_data, sql_wrapper):
    sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "IDLE STATE STARTED"))

    while not request_input(pod_data, sql_wrapper):
        pass
