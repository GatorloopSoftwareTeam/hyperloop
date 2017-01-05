import constants


# TODO: do pre-run testing on brakes, etc.
def start(pod_data):
    pod_data.state = constants.STATE_CHECK_SYSTEMS
