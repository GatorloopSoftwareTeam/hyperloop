import time, datetime, MySQLdb
def getSpeed(ser1,ser_str,wheel_circumference,dist_brake,accData, db1,conn,logging,q):
	x=1
	wheel_dist=0
	# conn== MySQLdb.connect(host="localhost",
	# 	user="root",
	# 	passwd="password",
	# 	db="test")
	db1=conn.cursor()
	while x==1:
		logging.debug("Getting speed from "+ser_str)
		bytesToRead = ser1.inWaiting()
		if bytesToRead==0:
			time.sleep(0.5)
		else:
			response = ser1.readline(bytesToRead)  ## MIGHT need to swap in a readline
			logging.debug(ser_str+" returned " + response)
			logging.debug("bytes to read was " + str(bytesToRead))
			wheel_dist += wheel_circumference
			logging.debug(ser_str + " dist is now " + str(wheel_dist))
			try:
				db1.execute("INSERT INTO "+ser_str+"speed VALUES (%s,%s)",(datetime.datetime.now(), response))
				conn.commit()
			except Exception as e:

				logging.debug("error writing to db")
				logging.debug("e is " + str(type(e)))
				print e
				conn.rollback()
		#if we have gone the distance
		if wheel_dist > dist_brake:
			#if the acc detects we aren't being pushed
			if accData.y_g> -0.1:
				logging.debug("Passed the distance on "+ser_str+".  Lets brake")
				logging.debug("Y G's detected as " + str(accData.y_g))
				q.put("brake")
			else:
				logging.debug("Passed the braking distance but Y G's was "+str(accData.y_g) + " so we are still accelerating probably")
		

				#return 1