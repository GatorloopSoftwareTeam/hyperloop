import serial
import time

ser = serial.Serial(
    port='/dev/tty.usbserial-AH03FHKZ',
    baudrate=4800,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

while True:
    cabin_temperature = float(ser.read(5).strip())
    print cabin_temperature
