import MySQLdb
import datetime
import time
import constants


def getSpeed(ser1, ser_str, wheel_circumference, dist_brake, pod_data, accData, sql_wrapper, logging, q):
    wheel_dist = 0
    braked = False
    while True:
        # logging.debug("Getting speed from "+ser_str)
        bytesToRead = ser1.inWaiting()
        if bytesToRead == 0:
            # TODO can probably take this out
            time.sleep(0.01)
        else:
            response = ser1.readline()  ## MIGHT need to swap in a readline
            logging.debug(ser_str + " returned " + response)
            logging.debug("bytes to read was " + str(bytesToRead))
            wheel_dist += wheel_circumference
            pod_data.last_speed_update = datetime.datetime.now()
            if ser_str == "wheel1":
                pod_data.wheel_1_speed = float(response)
                pod_data.wheel_1_dist = wheel_dist
            elif ser_str == "wheel2":
                pod_data.wheel_2_speed = float(response)
                pod_data.wheel_2_dist = wheel_dist
            logging.debug(ser_str + " dist is now " + str(wheel_dist)) 
            sql_wrapper.execute("INSERT INTO " + ser_str + "speed VALUES (NULL,%s,%s,%s)", (datetime.datetime.now().strftime(constants.TIME_FORMAT), response, wheel_dist))

        if (wheel_dist > dist_brake - (max(pod_data.wheel_1_speed, pod_data.wheel_2_speed) * constants.TIME_TO_BEAM)) and not braked:
            # push state checks to make sure that we've been going long enough that we're not still being pushed
            q.put("brake")
            braked = True
