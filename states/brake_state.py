import logging
import constants
import datetime
import MySQLdb
import RPi.GPIO as GPIO
from lib.MotorDriver import MotorDriver


def start(pod_data, sql_wrapper):
    logging.debug("Now in BRAKE state")
    while True:
        # set database to brake
        # set GPIO to high
        md.GPIO.setup(gpio_init.gnd, md.GPIO.OUT)
        md.GPIO.output(gpio_init.gnd, 0)
        main_brake = md.DualMotorDriver(gpio_init.main_brake1_pwm, gpio_init.main_brake1_dir, gpio_init.main_brake2_pwm, gpio_init.main_brake2_dir)

        aux_brake = md.DualMotorDriver(gpio_init.aux_brake1_pwm, gpio_init.aux_brake1_dir, gpio_init.aux_brake2_pwm, gpio_init.aux_brake2_dir)

        lin_act_right = md.MotorDriver(gpio_init.lin_act_right_pwm, gpio_init.lin_act_right_dir)

        lin_act_left = md.MotorDriver(gpio_init.lin_act_left_pwm, gpio_init.lin_act_left_dir)

        # Run tests
        main_brake.test()
        try:
            sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "BRAKE STARTED"))
        except MySQLdb.OperationalError, e:
            # Ignore error because we need to keep braking
            logging.error(e)

        logging.debug("BRAKING")
        pod_data.state = constants.STATE_BRAKING
