import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
    
# Brake 1
GPIO.setup(16, GPIO.OUT)  # GND
GPIO.setup(12, GPIO.OUT)  # PWM
GPIO.setup(6, GPIO.OUT)   # DIR

# Brake 2
GPIO.setup(21, GPIO.OUT)  # GND
GPIO.setup(20, GPIO.OUT)  # PWM
GPIO.setup(26, GPIO.OUT)  # DIR

def forward():
  # Positive voltage from terminal A to B
  GPIO.output(21, 0)  # Brake 2 GND
  GPIO.output(16, 0)  # Brake 1 GND

  GPIO.output(26, 0)  # Brake 2 DIR
  GPIO.output(6, 0)   # Brake 1 DIR

  GPIO.output(20, 1)  # Brake 2 PWM
  GPIO.output(12, 1)  # Brake 1 PWM
 
def backward():
  # Positive voltage from terminal B to A
  GPIO.output(21, 0)  # Brake 2 GND
  GPIO.output(16, 0)  # Brake 1 GND

  GPIO.output(26, 1)  # Brake 2 DIR
  GPIO.output(6, 1)   # Brake 1 DIR

  GPIO.output(20, 1)  # Brake 2 PWM
  GPIO.output(12, 1)  # Brake 1 PWM
 
def off():
  # No voltage acroos A,B
  GPIO.output(21, 0)  # Brake 2 GND
  GPIO.output(16, 0)  # Brake 1 GND

  GPIO.output(20, 0)  # Brake 2 PWM
  GPIO.output(12, 0)  # Brake 1 PWM

  GPIO.output(26, 0)  # Brake 2 DIR
  GPIO.output(6, 0)   # Brake 1 DIR
