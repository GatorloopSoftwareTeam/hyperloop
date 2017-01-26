import time
import serial
import logging
import constants

END_OF_MESSAGE = "*"
OK = constants.OK + END_OF_MESSAGE
ENGAGE_MAIN_BRAKES = constants.ENGAGE_MAIN_BRAKES + END_OF_MESSAGE
ENGAGE_AUXILIARY_BRAKES = constants.ENGAGE_AUXILIARY_BRAKES + END_OF_MESSAGE
RELEASE_MAIN_BRAKES = constants.RELEASE_MAIN_BRAKES + END_OF_MESSAGE
RELEASE_AUXILIARY_BRAKES = constants.RELEASE_AUXILIARY_BRAKES + END_OF_MESSAGE
LOWER_LINEAR_ACTUATORS = constants.LOWER_LINEAR_ACTUATORS + END_OF_MESSAGE
RAISE_LINEAR_ACTUATORS = constants.RAISE_LINEAR_ACTUATORS + END_OF_MESSAGE
FORWARD = constants.FORWARD + END_OF_MESSAGE
BACKWARD = constants.BACKWARD + END_OF_MESSAGE
OFF_BRAKES = constants.OFF_BRAKES + END_OF_MESSAGE
OFF_AUXILIARY = constants.OFF_AUXILIARY + END_OF_MESSAGE
OFF_LINEAR_ACTUATORS = constants.OFF_LINEAR_ACTUATORS + END_OF_MESSAGE
STOPPED = constants.STOPPED + END_OF_MESSAGE
KILL_ALL = constants.KILL_ALL + END_OF_MESSAGE
KILL_POD = constants.KILL_POD + END_OF_MESSAGE
RUNNING = constants.RUNNING + END_OF_MESSAGE
STATUS = constants.STATUS + END_OF_MESSAGE
BLDC_BRAKE = constants.BLDC_BRAKE + END_OF_MESSAGE
PULSE_MAIN_BRAKES = constants.PULSE_MAIN_BRAKES + END_OF_MESSAGE
PULSE_AUXILIARY_BRAKES = constants.PULSE_AUXILIARY_BRAKES + END_OF_MESSAGE

OK_RESPONSE = "IAMOK"


class DriveController:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

    def get_response(self):
        return self.ser.readline()

    def health_check(self):
        self.ser.write(OK)
        response = self.get_response()
        if response == OK_RESPONSE:
            return True
        else:
            logging.error("RUOK request to drive_controller returned incorrect value: " + response)
            return False

    def send_engage_main_brakes(self):
        self.ser.write(ENGAGE_MAIN_BRAKES)

    def send_release_main_brakes(self):
        self.ser.write(RELEASE_MAIN_BRAKES)

    def send_lower_linear_actuators(self):
        self.ser.write(LOWER_LINEAR_ACTUATORS)

    def send_raise_linear_actuators(self):
        self.ser.write(RAISE_LINEAR_ACTUATORS)

    def send_forward(self):
        self.ser.write(FORWARD)

    def send_backward(self):
        self.ser.write(BACKWARD)

    def send_bldc_brake(self):
        self.ser.write(BLDC_BRAKE)

    def send_engage_auxiliary_brakes(self):
        self.ser.write(ENGAGE_AUXILIARY_BRAKES)

    def send_release_auxiliary_brakes(self):
        self.ser.write(RELEASE_AUXILIARY_BRAKES)

    def send_off_main_brakes(self):
        self.ser.write(OFF_BRAKES)

    def send_off_auxiliary_brakes(self):
        self.ser.write(OFF_AUXILIARY)

    def send_off_linear_actuators(self):
        self.ser.write(OFF_LINEAR_ACTUATORS)

    def send_stopped(self):
        self.ser.write(STOPPED)

    def send_kill_all(self):
        self.ser.write(KILL_ALL)

    def send_running(self):
        self.ser.write(RUNNING)

    def send_command(self, command):
        self.ser.write(command)

    def send_kill_pod(self):
        self.ser.write(KILL_POD)

    def get_status(self):
        self.ser.write(STATUS)
        response = self.get_response()
        print "Pod status = " + response
        return response

    def send_pulse_main_brakes(self):
        self.ser.write(PULSE_MAIN_BRAKES)

    def send_pulse_auxiliary_brakes(self):
        self.ser.write(PULSE_AUXILIARY_BRAKES)
