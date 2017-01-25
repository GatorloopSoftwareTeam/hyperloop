import struct
import sys

# States
STATE_FAULT = 0  # will cause tube run to abort
STATE_IDLE = 1  # pod is on, but not ready to be pushed
STATE_READY = 2  # pod is ready to be pushed
STATE_PUSHING = 3 # optional
STATE_COAST = 4 # optional
STATE_BRAKING = 5  # pod is applying brakes


# Spacex UDP connection info
SPACEX_UDP_IP = "192.168.0.1"
SPACEX_UDP_PORT = 3000

# Suspension UDP connection info
SUSPENSION_UDP_IP = "192.168.0.10"
SUSPENSION_UDP_PORT = 3000

# Local mysql db connection info
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_DB = "test"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Sensor related
BMS_PORT = 2001
# In meters
WHEEL_CIRCUMFERENCE = 1.835
WHEEL_1_DIST = 0
WHEEL_2_DIST = 0
TOTAL_STRIPES = 0
NUM_STRIPES_BRAKE = 3
NUM_STRIPES_PANIC = 70
DIST_BRAKE = 400
READ_ROOF = 1
READ_WHEEL = 1
READ_ACC = 1
COAST_DETECT = 1

"""
Minimum Y direction G force that we consider the pod to be in the push state
"""
MIN_PUSH_ACCELERATION = 0.2

"""
Total time that the pusher is active (in seconds)
"""
TOTAL_PUSH_TIME = 4.0

# Battery Voltages
LOW_BATTERY = 30000
HIGH_BATTERY = 45000

# Battery temperature sensors
MAIN_BATTERY_1 = "28-0416513911ff"
MAIN_BATTERY_2 = "28-03164546f2ff"
MAIN_BATTERY_3 = "28-041650bd37ff"
AUX_BATTERY_1 = "28-041652b584ff"
AUX_BATTERY_2 = "28-0416508ce6ff"
AUX_BATTERY_3 = "28-0316457ef7ff"

# Battery Temp Limits
BATTERY_MAX_TEMP = 70
BATTERY_LOW_TEMP = 20

# Arduino
OK = "RUOK"
ENGAGE_MAIN_BRAKES = "EM"
ENGAGE_AUXILIARY_BRAKES = "EA"
RELEASE_MAIN_BRAKES = "RM"
RELEASE_AUXILIARY_BRAKES = "RA"
LOWER_LINEAR_ACTUATORS = "LL"
RAISE_LINEAR_ACTUATORS = "RL"
FORWARD = "FW"
BACKWARD = "BW"
OFF_BRAKES = "OM"
OFF_AUXILIARY = "OA"
OFF_LINEAR_ACTUATORS = "OL"
STOPPED = "STOPPED"
KILL_ALL = "KILLALL"
RUNNING = "RUNNING"
STATUS = "STATUS"
KILL_POD = "KILLPOD"
BLDC_BRAKE = "BK"

# Suspension codes
network_endinanness = '>'
ping_message_req = struct.pack(network_endinanness+'BB', 0x10, 0)
start_scu_message_req = struct.pack(network_endinanness+'BB', 0x11, 0)
start_logging_message_req = struct.pack(network_endinanness+'BB', 0x12, 0)
stop_logging_message_req = struct.pack(network_endinanness+'BB', 0x13, 0)
stop_scu_message_req = struct.pack(network_endinanness+'BB', 0x14, 0)
available_space_message_req = struct.pack(network_endinanness+'BB', 0x15, 0) # Not implemented yet
clear_logs_message_req = struct.pack(network_endinanness+'BB', 0x16, 0) # Not implemented yet
heartbeat_message_reply = struct.pack(network_endinanness+'BBH', 0x57, 2, 0)
