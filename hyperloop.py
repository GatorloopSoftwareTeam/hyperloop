import MySQLdb, datetime, serial, logging, time, thread
from initTTYUSBx import initTTYUSBx
from getSpeed import getSpeed
from getRoofSpeed import getRoofSpeed

import Queue as queue
logging.basicConfig(filename='test.log',level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

wheel_circumference = 12
wheel_1_dist=0
wheel_2_dist=0
total_stripes=0
num_stripes_brake = 5
num_stripes_panic=7
dist_brake = 20
read_roof=1
read_wheel=1

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
	

	#TODO: figure out how these sensors get ordered each boot up
	#send ruok to optical sensor 1
	logging.debug("About to open serial connection to wheel 1")
	possible_tty = ["0","1","2"]
	inited_tty = {}
	for i in possible_tty:
		inited_tty = initTTYUSBx(i,inited_tty, logging)
		logging.debug("initted tty is now")
		logging.debug(inited_tty)

	return inited_tty, conn
	#read status from acc
		#if depressurized and if user input OK
			#MOVE TO PUSH

#STATE: PUSH
#def PUSH(ser1,ser2,ser3, conn):
def PUSH(inited_tty, conn):
	global wheel_circumference, wheel_1_dist, wheel_2_dist, num_stripes_brake, read_roof, total_stripes, read_roof
	#set database to push
	logging.debug("Now in PUSH state")
	logging.debug("About to write PUSH state to db")

	db1=conn.cursor()
	try:
		db1.execute("""INSERT INTO states VALUES ( %s,%s)""",(datetime.datetime.now(), "PUSH STARTED"))
		conn.commit()
	except:
		conn.rollback()
	#conn.close()
	logging.debug("Wrote state to db")
	x=1
	#loop getting all speeds
	while x==1:
		#update speed from R wheel
		
		q=queue.Queue()
		if read_wheel==1:
			
			#start all speed getting threads
			wheel1 = thread.start_new_thread(getSpeed,(inited_tty["wheel1"],"wheel1",wheel_circumference,dist_brake, db1,conn,logging,q))
			wheel2 = thread.start_new_thread(getSpeed,(inited_tty["wheel2"],"wheel2",wheel_circumference,dist_brake, db1,conn,logging,q))
			
		if read_roof==1:
			thread.start_new_thread(getRoofSpeed,(inited_tty["roof"],"roof",num_stripes_brake,num_stripes_panic, db1,conn,logging,q))
		#will block until we get the brake command
		q.get()
		logging.debug("Just got a brake command")
		time.sleep(300)
				

#STATE: BRAKE
def BRAKE(inited_tty,conn):
	while True:
		stripe_diff=0
		stripe_time=0
		global wheel_circumference, wheel_1_dist, wheel_2_dist, num_stripes_brake, total_stripes, read_roof
		# set database to brake
		logging.debug("Now in BRAKE state")
		logging.debug("About to write BRAKE state to db")

		db1=conn.cursor()
		try:
			db1.execute("""INSERT INTO states VALUES ( %s,%s)""",(datetime.datetime.now(), "BRAKE STARTED"))
			conn.commit()
		except:
			conn.rollback()
		#conn.close()
		logging.debug("Wrote state to db")
		# engage brake 1
		logging.debug("BRAKING")
		



	
				
		# update speed from R wheel
		# update speed from L wheel
		# update speed from roof
		# 	count readings(stripes)


		# update bms
		# update acc
		# if acceleration < expected
		acc = 0
		if acc>-.5:
			logging.debug("Not detecting braking. Engage brake 2")
		# 	engage brake 2
	
	
	
#ser1,ser2,ser3 = INITIALIZATION()
inited_tty,conn = INITIALIZATION()
#PUSH(ser1,ser2,ser3)
PUSH(inited_tty,conn)
BRAKE(inited_tty,conn)
		
	
	#update acc
	#if acceleration == 0 or passed X stripes
		#MOVE TO COAST

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