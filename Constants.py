# States
STATE_FAULT = 0  # will cause tube run to abort
STATE_INITIALIZATION = 1  # pod is on, but not ready to be pushed
STATE_IDLE = 2  # pod is ready to be pushed
STATE_CHECK_SYSTEMS = 3
STATE_PUSH = 4  # pod is being pushed
STATE_BRAKING = 5  # pod is applying brakes
STATE_EMERGENCY = 6
STATE_EXIT = 7  # turns off sensor data collection, disengage brakes and wait for user input

# Spacex UDP connection info
SPACEX_UDP_IP = "192.168.0.1"
SPACEX_UDP_PORT = 3000

# Local mysql db connection info
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_DB = "test"