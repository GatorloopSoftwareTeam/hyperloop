import serial
import time
import constants


def init_tty_usb_x(ser_str, inited_tty, logging):
    ser1 = serial.Serial()
    ser1.baudrate = 9600
    ser1.port = "/dev/ttyUSB" + ser_str
    ser1.open()

    while True:
        logging.debug("Sending RUOK to " + ser_str)
        ser1.write(b'r')
        time.sleep(.5)
        bytesToRead = ser1.inWaiting()
        logging.debug("bytesToRead is " + str(bytesToRead))
        response = ser1.read(bytesToRead)
        if response == constants.RIGHT_WHEEL_OK_RESPONSE:
            logging.debug("wheel right ok")
            inited_tty["wheel2"] = ser1
            break
        elif response == constants.LEFT_WHEEL_OK_RESPONSE:
            logging.debug("wheel left ok")
            inited_tty["wheel1"] = ser1
            break
        elif response == constants.ROOF_OK_RESPONSE:
            logging.debug("roof ok")
            inited_tty["roof"] = ser1
            break
        else:
            logging.debug(ser_str + " returned " + response + ", initialization bad")
            time.sleep(2)
    return inited_tty
