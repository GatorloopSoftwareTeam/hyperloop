from subprocess import Popen, PIPE
import datetime
import constants
from time import sleep


def get_proc_temp(sql_wrapper, logging):
    while True:
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        output, _error = process.communicate()
        proc_temp = float(output[output.index('=') + 1:output.rindex("'")])
        sql_wrapper.execute("""INSERT INTO proc_temp VALUES (%s,%s)""", (datetime.datetime.now().strftime(constants.TIME_FORMAT), proc_temp))
        sleep(3)