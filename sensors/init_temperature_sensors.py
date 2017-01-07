import os
import glob


def init_temperature_sensors():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
