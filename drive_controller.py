import time
import serial

OK = "IG"
ENGAGE_BRAKES = "EM"
ENGAGE_AUXILIARY = "EA"
RELEASE_BRAKES = "RM"
RELEASE_AUXILIARY = "RA"
LOWER_LINEAR_ACTUATORS = "LL"
RAISE_LINEAR_ACTUATORS = "RL"
FORWARD = "FW"
BACKWARD = "BW"


class DriveController:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

    def send_ok(self):
        self.ser.write(OK)

    def send_engage_main_brakes(self):
        self.ser.write(ENGAGE_BRAKES)

    def send_release_main_brakes(self):
        self.ser.write(RELEASE_BRAKES)

    def send_lower_linear_actuators(self):
        self.ser.write(LOWER_LINEAR_ACTUATORS)

    def send_raise_linear_actuators(self):
        self.ser.write(RAISE_LINEAR_ACTUATORS)

    def send_forward(self):
        self.ser.write(FORWARD)

    def send_backward(self):
        self.ser.write(BACKWARD)

    def send_engage_auxiliary_brakes(self):
        self.ser.write(ENGAGE_AUXILIARY)

    def send_release_auxiliary_brakes(self):
        self.ser.write(RELEASE_AUXILIARY)
