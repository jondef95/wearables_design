import serial, sys, os, datetime

hr_session = 0
hr = []
temp_session = 0
temp = []
pr_session = 0
pr = []
curr_type = ""

def write_to_hr():
	global hr, hr_session
	filename = "heartrate_"
	date = datetime.datetime.now().strftime("%d-%m-%y_") 
	filename = filename + date + str(hr_session)
	f = open(filename, 'a')
	for data in hr:
		f.write(str(data))
		f.write(',\n')
	f.close()
	hr = []
	hr_session = hr_session + 1

def write_to_temp():
	global temp, temp_session
	filename = "temp_"
	date = datetime.datetime.now().strftime("%d-%m-%y_") 
	filename = filename + date + str(temp_session)
	f = open(filename, 'a')
	for data in temp:
		f.write(str(data))
		f.write(',\n')
	f.close()
	temp = []
	temp_session = temp_session + 1

def process_line(line):
	global curr_type, hr
	data_type, data = str.split(line, "~")
	write = False
	if curr_type == "" or curr_type != data_type:
		curr_type = data_type

	if curr_type != data_type:
		write = True

	if data_type == "rate":
		print("getting heartrate")
		hr.append(data)
		if write:
			# write to heartrate file
			write_to_hr()
	elif data_type == "temp":
		print("getting temperature")
		# write to temperature file
		temp.append(data)
		if write:
			write_to_temp(data)
	elif data_type == "press": 
		print("getting pressure")
		# write to pressure file
		#press.append(data)
		#write_to_pr(data)
	else:
		sys.stderr("Unrecognized datatype: \'%s\'" % data_type)


def read_serial():
	serialport = None
	try:
		serialport = serial.Serial("/dev/ttyACM0", 9600, timeout=0.5)
	except (serial.SerialException, serial.SerialException) as error:
			sys.stderr("Error while trying to establish connection. Shutting down...\n%s" % str(error))
			sys.exit()	
	line = ""
	while True:
		try:
			byte = serialport.read()
			char = byte.decode("utf-8") 
			print(byte, char)
		except (serial.SerialException, serial.SerialTimeoutException) as error:
			sys.stderr("Error while trying to read. Shutting down...\n%s" % str(error))
			sys.exit()	
		if char is '#':
			print(line)
			process_line(line)
			line = ""
		elif char is not '\r' and char is not '\n':
			line = line + char
def main():
	read_serial()

if __name__ == "__main__":
	main()
