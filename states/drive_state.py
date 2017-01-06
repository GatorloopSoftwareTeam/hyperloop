import datetime


def start(sql_wrapper):
    sql_wrapper.execute("""INSERT INTO states VALUES ( %s,%s)""", (datetime.datetime.now(), "DRIVE STATE STARTED"))
    meters_to_travel = 0

    while True:
        line = raw_input("How many meters do you want to drive?")
        try:
            global meters_to_travel
            meters_to_travel = int(line)
            break
        except ValueError:
            print "value is not an integer. Retry..."

    print "Driving " + str(meters_to_travel) + " meters"

    lin_act_right = md.MotorDriver(gpio_init.lin_act_right_pwm, gpio_init.lin_act_right_dir)
    lin_act_left = md.MotorDriver(gpio_init.lin_act_left_pwm, gpio_init.lin_act_left_dir)

    # lower wheels
    lin_act_left.engage()
    lin_act_right.engage()

    # start motors and monitor distance until distance is traveled
    # allow user to turn off motor at any time

    # raise wheels
    lin_act_left.release()
    lin_act_right.release()



