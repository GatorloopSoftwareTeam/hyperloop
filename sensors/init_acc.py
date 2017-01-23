from lib.mma8451 import MMA8451
import datetime
import constants


def init_acc(pod_data, sql_wrapper, logging):
    acc = MMA8451()

    # init
    # TODO: move this into init
    axes = acc.get_axes_measurement()
    if axes['x'] == 0 and axes['y'] == 0 and axes['z'] == 0:
        pod_data.state = constants.STATE_FAULT
        logging.debug("Fault: Accelerometer returned all 0s")
    elif axes['z'] < .9:
        pod_data.state = constants.STATE_FAULT
        logging.debug("BAD ACCELEROMETER POSITIONING, MAKE SURE Z IS DOWN AND THE ACC IS FLAT")
    else:
        pod_data.acceleration.x_g = axes['x']
        pod_data.acceleration.y_g = axes['y']
        pod_data.acceleration.z_g = axes['z']
        sql_wrapper.execute("INSERT INTO acc VALUES (%s,%s,%s,%s)",
                            (datetime.datetime.now().strftime(constants.TIME_FORMAT), axes['x'], axes['y'], axes['z']))