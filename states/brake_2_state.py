import time
import logging
import RPi.GPIO as GPIO
import constants


def start(pod_data, drive_controller):
    # this monitors initial braking and checks to make sure we don't need to activate second brake
    ##VERY IMPORTANT
    ##THE TIME WE SLEEP FOR IS THE TIME WE WAIT TO SEE IF THE FIRST BRAKE WORKED AND
    ##IF WE NEED TO ACTIVATE THE SECOND BRAKE
    time.sleep(.2)
    ##IM JUST GUESSING HERE
    ##END IMPORTANT
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
                drive_controller.send_engage_auxiliary_brakes()
                logging.debug("second brake activated")
                break
            else:
                logging.debug("not decelerating and below 10 m/s")
                logging.debug("pod stopped")
                return 1
        else:
            logging.debug("brakes are stopping fine, pod still going")

    while drive_controller.get_response() != constants.ENGAGE_AUXILIARY_BRAKES:
        drive_controller.send_engage_auxiliary_brakes()
        time.sleep(.1)
