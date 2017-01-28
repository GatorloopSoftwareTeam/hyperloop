import time
import logging
import constants
import datetime


def start(pod_data, sql_wrapper):
    previous_velocity_sample_time = datetime.datetime.now()
    previous_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)

    while True:
        measured_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)
        calculated_acceleration = \
            (measured_velocity - previous_velocity)/(datetime.datetime.now() - previous_velocity_sample_time).total_seconds()

        sql_wrapper.execute("""INSERT INTO calc_acc VALUES (NULL, %s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), str(calculated_acceleration)))
        time.sleep(.1)
        previous_velocity_sample_time = datetime.datetime.now()
        previous_velocity = max(pod_data.wheel_1_speed, pod_data.wheel_2_speed)