import datetime
import constants
import time


def go_forward():
    line = raw_input("How many meters do we go forward for? Enter r to return to the main menu")

    if line == "r" or line == "R":
        return

    meters_to_travel = 0
    try:
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
        meters_to_travel = int(line)
        if meters_to_travel < 0:
            raise ValueError
    except ValueError:
        print "Enter a distance in meters greater than 0"
        go_backward()

    # TODO: send go backward until we hit distance?


def start(pod_data, suspension_tcp_socket, sql_wrapper, drive_controller):
    sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), "DRIVE STATE STARTED"))

    print "Pod is stopped."
    while True:
        line = raw_input("Please enter a command: \n"
                         "1. Engage Main Brakes\n"
                         "2. Release Main Brakes\n"
                         "3. Engage Auxiliary Brakes\n"
                         "4. Release Auxiliary Brakes\n"
                         "5. BLDC Forward\n"
                         "6. BLDC Backward\n"
                         "7. BLDC Brake"
                         "8. Raise Linear Actuators\n"
                         "9. Lower Linear Actuators\n"
                         "10. Disable Suspension\n")

        choice = -1
        try:
            choice = int(line)
            if choice < 1 or choice > 10:
                raise ValueError
        except ValueError:
            print "Enter a value between 1-10"
            continue

        if choice == -1:
            print "Try again"
            continue
        elif choice == 1:
            drive_controller.send_engage_main_brakes()
            response = drive_controller.get_response()
            if response != constants.ENGAGE_MAIN_BRAKES + "\n":
                print "Engage main brakes not acknowledged. Got " + response
            time.sleep(constants.TIME_TO_BEAM)
            drive_controller.send_off_main_brakes()
        elif choice == 2:
            drive_controller.send_release_main_brakes()
            response = drive_controller.get_response()
            if response != constants.RELEASE_MAIN_BRAKES + "\n":
                print "Release main brakes not acknowledged. Got: " + response
            time.sleep(constants.TIME_TO_BEAM)
            drive_controller.send_off_main_brakes()
        elif choice == 3:
            drive_controller.send_engage_auxiliary_brakes()
            response = drive_controller.get_response()
            if response != constants.RELEASE_AUXILIARY_BRAKES + "\n":
                print "Engage auxiliary brakes not acknowledged. Got: " + response
            time.sleep(constants.TIME_TO_BEAM)
            drive_controller.send_off_auxiliary_brakes()
        elif choice == 4:
            drive_controller.send_release_auxiliary_brakes()
            response = drive_controller.get_response()
            if response != constants.RELEASE_AUXILIARY_BRAKES + "\n":
                print "Release auxiliary brakes not acknowledged. Got: " + response
            time.sleep(constants.TIME_TO_BEAM)
            drive_controller.send_off_auxiliary_brakes()
        elif choice == 5:
            go_forward()
        elif choice == 6:
            go_backward()
        elif choice == 7:
            drive_controller.send_bldc_brake()
            response = drive_controller.get_response()
            if response != constants.BLDC_BRAKE + "\n":
                print "BLDC brake not acknowledged. Got: " + response
        elif choice == 8:
            drive_controller.send_raise_linear_actuators()
            response = drive_controller.get_response()
            if response != constants.RAISE_LINEAR_ACTUATORS + "\n":
                print "Raise linear actuators not acknowledged. Got: " + response
        elif choice == 9:
            drive_controller.send_lower_linear_actuators()
            response = drive_controller.get_response()
            if response != constants.LOWER_LINEAR_ACTUATORS + "\n":
                print "Lower linear actuators not acknowledged. Got: " + response
        elif choice == 10:
            while pod_data.scu_sus_started:
                suspension_tcp_socket.send(constants.stop_scu_message_req)
                time.sleep(.5)
            while pod_data.scu_log_started:
                suspension_tcp_socket.send(constants.stop_logging_message_req)
                time.sleep(.5)
        else:
            print "Enter a value between 1-10"
