import datetime


def start(sql_wrapper, drive_controller):
    sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "DRIVE STATE STARTED"))
    meters_to_travel = 0

    while True:
        line = raw_input("How many meters do you want to drive?")
        try:
            global meters_to_travel
            meters_to_travel = int(line)
            break
        except ValueError:
            print "value is not an integer. Retry..."

    print "Driving " + str(meters_to_travel) + " meters"

    drive_controller.send_lower_linear_actuators()
    drive_controller.send_release_main_brakes()
    drive_controller.send_release_auxiliary_brakes()
    # TODO: wait
    drive_controller.send_forward()
    # TODO: measure distance and speed before raising
    drive_controller.send_raise_linear_actuators()



