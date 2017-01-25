import datetime
import constants


def go_forward():
    line = raw_input("How many meters do we go forward for? Enter r to return to the main menu")

    if line == "r" or line == "R":
        return

    meters_to_travel = 0
    try:
        global meters_to_travel
        meters_to_travel = int(line)
        if meters_to_travel < 0:
            raise ValueError
    except ValueError:
        print "Enter a distance in meters greater than 0"
        go_forward()

    # TODO: send go forward until we hit distance?


def go_backward():
    line = raw_input("How many meters do we go backward for? Enter r to return to the main menu")

    if line == "r" or line == "R":
        return

    meters_to_travel = 0
    try:
        global meters_to_travel
        meters_to_travel = int(line)
        if meters_to_travel < 0:
            raise ValueError
    except ValueError:
        print "Enter a distance in meters greater than 0"
        go_backward()

    # TODO: send go backward until we hit distance?


def start(sql_wrapper, drive_controller):
    sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "DRIVE STATE STARTED"))

    print "Pod is stopped."
    while True:
        line = raw_input("Please enter a command: \n"
                         "1. Engage Main Brakes\n"
                         "2. Lower Linear Actuators\n"
                         "3. Release Main Brakes\n"
                         "4. Release Auxiliary Brakes\n"
                         "5. Forward\n"
                         "6. Backward\n"
                         "7. Raise Linear Actuators\n"
                         "8. Brake BLDC\n")

        choice = -1
        try:
            global choice
            choice = int(line)
            if choice < 1 or choice > 8:
                raise ValueError
        except ValueError:
            print "Enter a value between 1-8"
            continue

        if choice == -1:
            print "Try again"
            continue
        elif choice == 1:
            drive_controller.send_engage_main_brakes()
            response = drive_controller.get_response()
            if response != constants.ENGAGE_MAIN_BRAKES:
                print "Engage main brakes not acknowledged. Got " + response
        elif choice == 2:
            drive_controller.send_lower_linear_actuators()
            response = drive_controller.get_response()
            if response != constants.LOWER_LINEAR_ACTUATORS:
                print "Lower linear actuators not acknowledged. Got: " + response
        elif choice == 3:
            drive_controller.send_release_main_brakes()
            response = drive_controller.get_response()
            if response != constants.RELEASE_MAIN_BRAKES:
                print "Release main brakes not acknowledged. Got: " + response
        elif choice == 4:
            drive_controller.send_release_auxiliary_brakes()
            response = drive_controller.get_response()
            if response != constants.RELEASE_AUXILIARY_BRAKES:
                print "Release auxiliary brakes not acknowledged. Got: " + response
        elif choice == 5:
            drive_controller.send_forward()
            response = drive_controller.get_response()
            if response != constants.FORWARD:
                print "Forward not acknowledged. Got: " + response
        elif choice == 6:
            drive_controller.send_backward()
            response = drive_controller.get_response()
            if response != constants.BACKWARD:
                print "Backward not acknowledged. Got: " + response
        elif choice == 7:
            drive_controller.send_raise_linear_actuators()
            response = drive_controller.get_response()
            if response != constants.RAISE_LINEAR_ACTUATORS:
                print "Raise linear actuators not acknowledged. Got: " + response
        elif choice == 8:
            drive_controller.send_bldc_brake()
            response = drive_controller.get_response()
            if response != constants.BLDC_BRAKE:
                print "BLDC brake not acknowledged. Got: " + response
        else:
            print "Enter a value between 1-8"
