import MySQLdb, datetime, serial, logging, time
logging.basicConfig(filename='test.log',level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

wheel_circumference = 12
wheel_1_dist=0
wheel_2_dist=0
total_stripes=0
num_stripes_brake = 5
dist_brake = 180
read_roof=1

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
	ser1 = serial.Serial()
	ser1.baudrate = 9600
	ser1.port = '/dev/ttyUSB0'
	ser1.open()
	x=1
	while x==1:
		logging.debug("Sending RUOK to wheel 1")
		ser1.write(b'r')
		time.sleep(.5)
		bytesToRead = ser1.inWaiting()
		logging.debug("bytesToRead is "+str(bytesToRead))
		response = ser1.read(bytesToRead)
		if response == "imok\n":
			logging.debug("wheel 1 ok")
			x=2
		else:
			logging.debug("wheel 1 returned " + response + ", initialization bad")
			time.sleep(2)
	
	#send ruok to optical sensor 2
	logging.debug("About to open serial connection to wheel 2")
	ser2 = serial.Serial()
	ser2.baudrate = 9600
	ser2.port = '/dev/ttyUSB2'
	ser2.open()
	x=1
	while x==1:
		logging.debug("Sending RUOK to wheel 2")
		ser2.write(b'r')
		time.sleep(.5)
		bytesToRead = ser2.inWaiting()
		response = ser2.read(bytesToRead)
		if response == "imok\n":
			logging.debug("wheel 2 ok")
			x=2
		else:
			logging.debug("wheel 2 returned " + response + ", initialization bad")
			time.sleep(2)

	#send ruok to roof
	logging.debug("About to open serial connection to roof")
	ser3 = serial.Serial()
	ser3.baudrate = 9600
	ser3.port = '/dev/ttyUSB1'
	ser3.open()
	x=1
	while x==1:
		logging.debug("Sending RUOK to roof")
		ser3.write(b'r')
		time.sleep(.5)
		bytesToRead = ser3.inWaiting()
		response = ser3.read(bytesToRead)
		if response == "imok\n":
			logging.debug("roof ok")
			x=2
		else:
			logging.debug("roof returned " + response + ", initialization bad")
			time.sleep(2)

	#return ser1, ser2, ser3, conn
	return ser1, ser2, ser3, conn
	#read status from acc
		#if depressurized and if user input OK
			#MOVE TO PUSH

#STATE: PUSH
#def PUSH(ser1,ser2,ser3, conn):
def PUSH(ser1,ser2,ser3, conn):
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
		
		
		if read_roof==0:
			logging.debug("Getting speed from wheel 1")
			bytesToRead = ser1.inWaiting()
			if bytesToRead==0 and read_roof == 0:
				time.sleep(0.5)
			else:
				response = ser1.readline(bytesToRead)  ## MIGHT need to swap in a readline
				logging.debug("wheel 1 returned " + response)
				logging.debug("bytes to read was " + str(bytesToRead))
				wheel_1_dist += wheel_circumference
				logging.debug("wheel 1 dist is now " + str(wheel_1_dist))
				#try:
				db1.execute("""INSERT INTO wheel1speed VALUES (%s,%s)""",(datetime.datetime.now(), response))
				conn.commit()
				#except Exception as e:

					# logging.debug("error writing to db")
					# logging.debug("e is " + str(type(e)))
					# print e
					# conn.rollback()

		#update speed from L wheel
		if read_roof == 0:
			bytesToRead = ser2.inWaiting()
			if bytesToRead==0:
				time.sleep(0.5)
			else:
				response = ser2.readline(bytesToRead)  ## MIGHT need to swap in a readline
				logging.debug("wheel 2 returned " + response)
				logging.debug("bytes to read was " + str(bytesToRead))
				wheel_2_dist += wheel_circumference
				logging.debug("wheel 2 dist is now " + str(wheel_1_dist))
				#try:
				db1.execute("""INSERT INTO wheel2speed VALUES (%s,%s)""",(datetime.datetime.now(), response))
				conn.commit()
			if wheel_1_dist > dist_brake or wheel_2_dist > dist_brake:
				logging.debug("Passed the distance.  Lets brake")
				return 1

		# #update speed from roof
		if read_roof==1:
			bytesToRead = ser3.inWaiting()
			if bytesToRead==0:
				time.sleep(0.5)
			else:
				response = ser3.readline(bytesToRead)  ## MIGHT need to swap in a readline
				logging.debug("roof returned " + response)
				logging.debug("bytes to read was " + str(bytesToRead))
				total_stripes += 1
				logging.debug("total stripes dist is now " + str(total_stripes))
				#try:
				db1.execute("""INSERT INTO roofspeed VALUES (%s,%s)""",(datetime.datetime.now(), response))
				conn.commit()
			#if total_stripes>num_stripes_brake:
			#	logging.debug("Passed the stripes. Lets brake")
			#	return 1
		# bytesToRead = ser3.inWaiting()
		# response = ser3.read(bytesToRead)  ## MIGHT need to swap in a readline
		# logging.debug("roof returned " + response)
		# try:
		# 	x.execute("""INSERT INTO roofspeed VALUES ( %s,%s)""",(datetime.datetime.now(), response))
		# 	conn.commit()
		# except:
		# 	conn.rollback()
		# #count readings(stripes)

#STATE: BRAKE
def BRAKE(ser1,ser2,ser3,conn):
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
		x=1
		while x==1:
		#update speed from R wheel
			logging.debug("Getting speed from wheel 1")
			
			bytesToRead = ser1.inWaiting()
			if bytesToRead==0 and read_roof == 0:
				time.sleep(0.5)
			else:
				response = ser1.readline(bytesToRead)  ## MIGHT need to swap in a readline
				logging.debug("wheel 1 returned " + response)
				logging.debug("bytes to read was " + str(bytesToRead))
				wheel_1_dist += wheel_circumference
				logging.debug("wheel 1 dist is now " + str(wheel_1_dist))
				#try:
				db1.execute("""INSERT INTO wheel1speed VALUES (%s,%s)""",(datetime.datetime.now(), response))
				conn.commit()
				#except Exception as e:

					# logging.debug("error writing to db")
					# logging.debug("e is " + str(type(e)))
					# print e
					# conn.rollback()

			#update speed from L wheel
			bytesToRead = ser2.inWaiting()
			if bytesToRead==0 and read_roof == 0:
				time.sleep(0.5)
			else:
				response = ser2.readline(bytesToRead)  ## MIGHT need to swap in a readline
				logging.debug("wheel 2 returned " + response)
				logging.debug("bytes to read was " + str(bytesToRead))
				wheel_2_dist += wheel_circumference
				logging.debug("wheel 2 dist is now " + str(wheel_1_dist))
				#try:
				db1.execute("""INSERT INTO wheel2speed VALUES (%s,%s)""",(datetime.datetime.now(), response))
				conn.commit()

			# #update speed from roof
			bytesToRead = ser3.inWaiting()
			if bytesToRead==0 and read_roof==1:
				time.sleep(0.5)
			else:
				response = ser3.readline(bytesToRead)  ## MIGHT need to swap in a readline
				logging.debug("roof returned " + response)
				logging.debug("bytes to read was " + str(bytesToRead))
				total_stripes += 1
				logging.debug("total stripes dist is now " + str(wheel_1_dist))
				#try:
				db1.execute("""INSERT INTO roofspeed VALUES (%s,%s)""",(datetime.datetime.now(), response))
				conn.commit()
				##experimental
				last_stripe_diff = stripe_diff
				last_stripe_time=stripe_time
				stripe_time=datetime.datetime.now().time()
				stripe_diff=stripe_time-last_stripe_time
				if(2*stripe_diff<last_stripe_diff):
					logging.debug("CLOSE STRIPS DETECTED")
				
				if total_stripes>num_stripes_panic:
					logging.debug("PANIC")
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
ser1,ser2,ser3,conn = INITIALIZATION()
#PUSH(ser1,ser2,ser3)
PUSH(ser1,ser2,ser3,conn)
BRAKE(ser1,ser2,ser3,conn)
		
	
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