import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
# GPIO for brake 1
GPIO.setup(17, GPIO.OUT)
# GPIO for brake 2
GPIO.setup(27, GPIO.OUT)
# Test brake 1
GPIO.output(17, 1)
# Test brake 2
GPIO.output(27, 1)
