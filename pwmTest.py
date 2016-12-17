#import wiringpi2 as wiringpi
import wiringpi
wiringpi.wiringPiSetupGpio()
#GPIO 1 is hardware PWM, Mode 2 is PWM
wiringpi.pinMode(1,2)
#Writes to do a 50% duty cycle
#values are between 0 and 1023
wiringpi.pwmWrite(1,512)
