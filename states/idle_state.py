import constants
import datetime
import states.check_systems_state
import states.drive_state


def start(pod_data, sql_wrapper):
    sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "IDLE STATE STARTED"))

    while True:
        line = raw_input("Enter 1 to enter the check systems state, 2 to enter drive state, 3 to enter the ready state")
        if line == "1":
            states.check_systems_state.start(pod_data)
        elif line == "2":
            states.drive_state.start(sql_wrapper)
        elif line == "3":
            break
        else:
            print "Invalid input"
