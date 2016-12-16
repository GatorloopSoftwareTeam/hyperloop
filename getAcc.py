from mma8451 import MMA8451
def getAcc(accData1,logging):
	accData1.x_g=0
	accData1.y_g=0
	accData1.z_g=0
	acc = MMA8451()

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
		logging.debug(axes)