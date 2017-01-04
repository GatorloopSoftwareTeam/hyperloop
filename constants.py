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

# Local mysql db connection info
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_DB = "test"

# Sensor related
BMS_PORT = 2001
WHEEL_CIRCUMFERENCE = 12
WHEEL_1_DIST = 0
WHEEL_2_DIST = 0
TOTAL_STRIPES = 0
NUM_STRIPES_BRAKE = 3
NUM_STRIPES_PANIC = 70
DIST_BRAKE = 40
READ_ROOF = 1
READ_WHEEL = 1
READ_ACC = 1
COAST_DETECT = 1