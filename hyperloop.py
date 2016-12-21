import MySQLdb, datetime, serial, logging, time, thread, wiringpi
import RPi.GPIO as GPIO

import accData
import podData
from initTTYUSBx import initTTYUSBx
from getSpeed import getSpeed
from getRoofSpeed import getRoofSpeed
from getAcc import getAcc
from spacexTCPSender import spacexTCPSender

import Queue as queue
logging.basicConfig(filename=('test.log'),level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

wheel_circumference = 12
wheel_1_dist=0
wheel_2_dist=0
total_stripes=0
num_stripes_brake = 3
num_stripes_panic=70
dist_brake = 40
read_roof=1
read_wheel=1
read_acc = 1
coast_detect=1

#STATE: INITIALIZATION
def INITIALIZATION():
	#set database to initialization
	logging.debug("About to write INITIALIZATION state to db")
	conn = MySQLdb.connect(host="localhost",
		user="root",
		passwd="password",
		db="test")
	x=conn.cursor()
	try:
		x.execute("""INSERT INTO states VALUES ( %s,%s)""",(datetime.datetime.now(), "INITIALIZATION STARTED"))
		conn.commit()
		logging.debug("Wrote state to db")
	except:
		conn.rollback()
	#conn.close()
	stateQueue = queue.Queue()
	#SET POD STATE 1 (IDLE)
	logging.debug("set pod state to 1 (idle)")
	stateQueue.put(1)
	#Initialize the spacex message sender
	logging.debug("started the spacex message sender")
	thread.start_new_thread(spacexTCPSender,(stateQueue,logging))

	logging.debug("initializing read from accelerometer")
	thread.start_new_thread(getAcc,(accData,podData,logging))
	time.sleep(5)

	#TODO: figure out how these sensors get ordered each boot up
	#send ruok to optical sensor 1
	logging.debug("About to open serial connections")
	possible_tty = ["0","1","2"]
	inited_tty = {}
	for i in possible_tty:
		#pass in list of inited_tty so we can add to it after we initialize
		inited_tty = initTTYUSBx(i,inited_tty, logging)
		#logging.debug("initted tty is now")
		#logging.debug(inited_tty)

	return inited_tty, conn, stateQueue
	#read status from acc
		#if depressurized and if user input OK
			#MOVE TO PUSH

#STATE: PUSH
#def PUSH(ser1,ser2,ser3, conn):
def PUSH(inited_tty, conn, stateQueue):
	global wheel_circumference, wheel_1_dist, wheel_2_dist, num_stripes_brake, read_roof, total_stripes, read_roof
	#set database to push
	logging.debug("Now in PUSH state")
	stateQueue.put(2)
	logging.debug("About to write PUSH state to db")

	db1=conn.cursor()
	try:
		db1.execute("""INSERT INTO states VALUES ( %s,%s)""",(datetime.datetime.now(), "PUSH STARTED"))
		conn.commit()
	except:
		conn.rollback()
	#is this a thing
	#db1.close()
	#conn.close()
	logging.debug("Wrote state to db")
	x=1
	#loop getting all speeds
	while x==1:
		#update speed from R wheel

		q=queue.Queue()
		if read_wheel==1:

			#start all speed getting threads
			wheel1 = thread.start_new_thread(getSpeed,(inited_tty["wheel1"],"wheel1",wheel_circumference,dist_brake,accData, db1,conn,logging,q))
			wheel2 = thread.start_new_thread(getSpeed,(inited_tty["wheel2"],"wheel2",wheel_circumference,dist_brake,accData, db1,conn,logging,q))

		if read_roof==1:
			thread.start_new_thread(getRoofSpeed,(inited_tty["roof"],"roof",num_stripes_brake,num_stripes_panic,accData, db1,conn,logging,q))

		#if coast_detect==1:
		#	thread.start_new_thread(coastDetect,(conn,logging))

		#will block until we get the brake command
		q.get()
		logging.debug("Just got a brake command")
		return conn
		#time.sleep(300)


#STATE: BRAKE
def BRAKE(inited_tty,conn,stateQueue):
	while True:
		stripe_diff=0
		stripe_time=0
		global wheel_circumference, wheel_1_dist, wheel_2_dist, num_stripes_brake, total_stripes, read_roof
		# set database to brake
		#set GPIO to high
		logging.debug("Setting brake 1 to high")
		GPIO.output(17,1)
		logging.debug("Now in BRAKE state")
		logging.debug("About to write BRAKE state to db")

		db1=conn.cursor()
		try:
			db1.execute("""INSERT INTO states VALUES ( %s,%s)""",(datetime.datetime.now(), "BRAKE STARTED"))
			conn.commit()
			logging.debug("Wrote state to db")
		except Exception as e:
			#set second brake anyways
			GPIO.output(27,1)
			logging.debug("DATABASE ERROR: Set 2nd brake just to make sure")
			print e
			conn.rollback()
			conn.close()

		logging.debug("BRAKING")
		logging.debug("Sending Spacex Status 5")
		#send spacex state 5 (braking)
		stateQueue.put(5)
		return 1


#this monitors initial braking and checks to make sure we don't need to activate second brake
def BRAKE2(conn):
	##VERY IMPORTANT
	##THE TIME WE SLEEP FOR IS THE TIME WE WAIT TO SEE IF THE FIRST BRAKE WORKED AND
	##IF WE NEED TO ACTIVATE THE SECOND BRAKE
	time.sleep(.2)
	##IM JUST GUESSING HERE
	##END IMPORTANT
	while True:
		logging.debug("Y_G is "+str(accData.y_g))
		##VERY IMPORTANT
		##THIS IS THE G WE EXPECT BEFORE ACTIVATING THE SECOND BRAKE
		if accData.y_g> -.5:
		##END IMPORTANT
			#TODO: move data into podData
			#If you crashed because you got here it's a good sign
			if podData.speed>10:
				logging.debug("brakes are not stopping fast enough. activate the second one")
				GPIO.output(27,1)
				logging.debug("second brake activated")
			else:
				logging.debug("not decelerating and below 10 m/s")
				logging.debug("pod stopped")
				return 1
		else:
			logging.debug("brakes are stopping fine, pod still going")

def DRIVE(conn):
	GPIO.output(17,0)
	GPIO.output(27,0)
	import wiringpi
	wiringpi.wiringPiSetupGpio()
	#GPIO 1 is hardware PWM, Mode 2 is PWM
	wiringpi.pinMode(1,2)
	wiringpi.pwmWrite(1,512)

#INIT GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
#GPIO for brake 1
GPIO.setup(17, GPIO.OUT)
#GPIO for brake 2
GPIO.setup(27, GPIO.OUT)
inited_tty,conn,stateQueue = INITIALIZATION()
#TODO: SET POD STATE 2 (READY)
#PUSH(ser1,ser2,ser3)
conn = PUSH(inited_tty,conn,stateQueue)
BRAKE(inited_tty,conn,stateQueue)
BRAKE2(conn)
DRIVE(conn)




#STATE: COAST
#while True:
	#set database to coast
	#update speed from R wheel
	#update speed from L wheel
	#update speed from roof
		#count readings(stripes)
	#update bms
	#update acc
	#if passed X stripes
		#MOVE TO BRAKE

#STATE: BRAKE
#while True:
	#set database to brake
	#engage brake 1
	#update speed from R wheel
	#update speed from L wheel
	#update speed from roof
		#count readings(stripes)
	#update bms
	#update acc
	#if acceleration < expected
		#engage brake 2

#STATE: EXIT
#while True:
	#set database to exit
	#update speed from R wheel
	#update speed from L wheel
	#update speed from roof
		#count readings(stripes)
	#update bms
	#update acc
	#if user input
		#engage drive
