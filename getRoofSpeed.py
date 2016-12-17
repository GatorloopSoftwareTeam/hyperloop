import time, datetime, MySQLdb
def getRoofSpeed(ser1,ser_str,num_stripes_brake,num_stripes_panic,accData, db1,conn,logging,q):
	x=1
	total_stripes=0
	stripe_diff=datetime.timedelta(microseconds=0)
	stripe_time=datetime.datetime.now()
	# conn = MySQLdb.connect(host="localhost",
	# 	user="root",
	# 	passwd="password",
	# 	db="test")
	db1=conn.cursor()
	while x==1:
		#logging.debug("Getting speed from "+ser_str)
		bytesToRead = ser1.inWaiting()
		if bytesToRead==0:
			time.sleep(0.5)
		else:
			response = ser1.readline(bytesToRead)  ## MIGHT need to swap in a readline
			logging.debug("roof returned " + response)
			logging.debug("bytes to read was " + str(bytesToRead))
			total_stripes += 1
			logging.debug("total stripes dist is now " + str(total_stripes))

			last_stripe_diff = stripe_diff
			last_stripe_time=stripe_time
			stripe_time=datetime.datetime.now()
			stripe_diff=stripe_time-last_stripe_time
			logging.debug("last_stripe_time was")
			logging.debug(last_stripe_time)

			##VERY IMPORTANT
			#this multiplier is the delta for close strips vs normal strips based on time
			if(3*stripe_diff<last_stripe_diff):
				logging.debug("CLOSE STRIPS DETECTED")
				q.put("brake")
			if total_stripes>num_stripes_panic:
				logging.debug("PANIC")
				#TODO: Brake?
			try:
				db1.execute("""INSERT INTO roofspeed VALUES (%s,%s)""",(datetime.datetime.now(), response))
				conn.commit()
			except Exception as e:

				logging.debug("error writing to db")
				logging.debug("e is " + str(type(e)))
				print e
				conn.rollback()
		if total_stripes > num_stripes_brake:
			if accData.y_g> -0.1:
				logging.debug("Passed the distance on "+ser_str+".  Lets brake")
				q.put("brake")
			else:
				logging.debug("Passed the braking distance but Y G's was "+str(accData.y_g) + " so we are still accelerating probably")
				#return 1