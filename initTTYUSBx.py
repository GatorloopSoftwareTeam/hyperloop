import serial, time
def initTTYUSBx(ser_str, inited_tty, logging):
	x=1
	while x==1:
		ser1 = serial.Serial()
		ser1.baudrate = 9600
		ser1.port = "/dev/ttyUSB" + ser_str
		ser1.open()
		logging.debug("Sending RUOK to "+ser_str)
		ser1.write(b'r')
		time.sleep(.5)
		bytesToRead = ser1.inWaiting()
		logging.debug("bytesToRead is "+str(bytesToRead))
		response = ser1.read(bytesToRead)
		if response == "imokw2\n":
			logging.debug("wheel 2 ok")
			inited_tty["wheel2"] = ser1
			x=2
		elif response == "imokw1\n":
			logging.debug("wheel 1 ok")
			inited_tty["wheel1"] = ser1
			x=2
		elif response == "imok\n":
			logging.debug("roof ok")
			inited_tty["roof"] = ser1
			x=2
		else:
			logging.debug("wheel 1 returned " + response + ", initialization bad")
			time.sleep(2)
	return inited_tty