import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
# GPIO.setup(23, GPIO.OUT)
# GPIO.setup(24, GPIO.OUT)
# GPIO.output(23, 0)
# GPIO.output(24, 0)

class MotorDriver(object):
    """
    Class to drive the RobotShop motor driver boards.
    """
    
    #~ def __init__(gnd_pin, pwm_pin, dir_pin):
    def __init__(self, pwm_pin, dir_pin):
        # Initialize class variables
        #~ self.gnd_pin = gnd_pin
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        
        # Initialize pins as output
        #~ GPIO.setup(self.gnd_pin, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT) 
        GPIO.setup(self.dir_pin, GPIO.OUT)
        
        # Ensure there is no voltage across terminals A and B
        self.off()
    
    def engage(self):
        """
        Apply a positive voltage from terminal A to B
        """
        #~ GPIO.output(self.gnd_pin, 0)
        GPIO.output(self.pwm_pin, 1)
        GPIO.output(self.dir_pin, 0)
        
    def release(self):
        """
        Apply a positive voltage from terminal B to A
        """
        #~ GPIO.output(self.gnd_pin, 0)
        GPIO.output(self.pwm_pin, 1)
        GPIO.output(self.dir_pin, 1)
        
    def off(self):
        """
        Apply no voltage across terminals A and B
        """
        #~ GPIO.output(self.gnd_pin, 0)
        GPIO.output(self.pwm_pin, 0)
        GPIO.output(self.dir_pin, 0)

    def test():
        self.engage()
        time.sleep(3)
        
        self.off()
        time.sleep(1)
        
        self.release()
        time.sleep(3)
        
        self.off()
        
class DualMotorDriver(object):
    """
    Class to drive 2 RobotShop motor driver boards.
    """
    
    def __init__(self, pwm_pin1, dir_pin1, pwm_pin2, dir_pin2):
        # Initialize class variables
        self.pwm_pin1 = pwm_pin1
        self.dir_pin1 = dir_pin1
        
        self.pwm_pin2 = pwm_pin2
        self.dir_pin2 = dir_pin2
        
        # Initialize pins as output
        GPIO.setup(self.pwm_pin1, GPIO.OUT) 
        GPIO.setup(self.dir_pin1, GPIO.OUT)
        
        GPIO.setup(self.pwm_pin2, GPIO.OUT) 
        GPIO.setup(self.dir_pin2, GPIO.OUT)
        
        # Ensure there is no voltage across terminals A and B
        self.off()
    
    def engage(self):
        """
        Apply a positive voltage from terminal A to B
        """
        GPIO.output(self.dir_pin1, 0)
        GPIO.output(self.dir_pin2, 0)
        GPIO.output(self.pwm_pin1, 1)
        GPIO.output(self.pwm_pin2, 1)
        
    def release(self):
        """
        Apply a positive voltage from terminal B to A
        """
        GPIO.output(self.dir_pin1, 1)
        GPIO.output(self.dir_pin2, 1)
        GPIO.output(self.pwm_pin1, 1)
        GPIO.output(self.pwm_pin2, 1)
        
    def off(self):
        """
        Apply no voltage across terminals A and B
        """
        GPIO.output(self.pwm_pin1, 0)
        GPIO.output(self.pwm_pin2, 0)
        GPIO.output(self.dir_pin1, 0)
        GPIO.output(self.dir_pin2, 0)

    def test(self):
        # Engage for active_time seconds, stop, and release for active_time seconds
        active_time = .25  # seconds
        
        self.engage()
        time.sleep(active_time)
        
        self.off()
        time.sleep(1)
        
        self.release()
        time.sleep(active_time)
        
        self.off()
        
