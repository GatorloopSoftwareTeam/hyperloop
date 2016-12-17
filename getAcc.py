from mma8451 import MMA8451
def getAcc(accData1,podData,logging):
	accData1.x_g=0
	accData1.y_g=0
	accData1.z_g=0
	acc = MMA8451()
	accData1.moving_y_average = 0

	#init
	#TODO: move this into init
	axes = acc.get_axes_measurement()
	if axes['z']<.9:
		logging.debug("BAD ACCELEROMETER POSITIONING, MAKE SURE Z IS DOWN AND THE ACC IS FLAT")
	while True:
		axes = acc.get_axes_measurement()
		accData1.x_g=axes['x']
		accData1.y_g=axes['y']
		accData1.z_g=axes['z']
		accData1.moving_y_average = .5*accData1.moving_y_average+.5*accData1.y_g
		logging.debug(axes)
		logging.debug("Moving y average is " + str(accData1.moving_y_average))

		##VERY IMPORTANT
		##THIS IS THE G FORCES WE EXPECT TO DETECT WHEN MOVING TO COAST
		##COAST CONTROLS NOTHING FOR NOW	if pod is being pushed
		#if(accData1.moving_y_average<0 and podData.state==3):
			#set pod to coast
	# 		podData.state = 4