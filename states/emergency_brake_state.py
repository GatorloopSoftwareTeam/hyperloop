import time
import constants
from drive_controller import DriveController


def start():
    drive_controller = DriveController()
    main_brakes_engaged = False
    aux_brakes_engaged = False

    while not (main_brakes_engaged and aux_brakes_engaged):
        drive_controller.send_engage_main_brakes()
        main_brakes_response = drive_controller.get_response()
        if main_brakes_response == constants.ENGAGE_MAIN_BRAKES:
            main_brakes_engaged = True

        drive_controller.send_engage_auxiliary_brakes()
        aux_brakes_engaged = drive_controller.get_response()
        if aux_brakes_engaged == constants.ENGAGE_AUXILIARY_BRAKES:
            aux_brakes_engaged = True

        time.sleep(.1)

