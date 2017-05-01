import serial, sys, os, datetime, time, atexit

hr_session = 0
hr = []
temp_session = 0
temp = []
pr_session = 0
pr = []
curr_type = ""

@atexit.register
def shutdown():
	print("Shutting down...")
	write_to_file(hr, "heartrate")
	write_to_file(pr, "pressure")
	write_to_file(temp, "temp")


def write_to_file(data_list, name):
	prefix = str(name) + "_"
	date = datetime.datetime.now().strftime("%d-%m-%y_") 
	session_id = 1
	filename = prefix + date + str(session_id)
	switch = True
	f = open(filename, 'a')
	for data in data_list:
		if data is not None:
			f.write(str(data))
			f.write(',\n')
			switch = True
		elif switch:
			session_id = session_id + 1
			filename = prefix + date + str(session_id)
			f.close()
			f = open(filename, 'a')
			switch = False

	f.close()

def process_line(line):
	global hr, pr, temp
	data_type, data = str.split(line, "~")

	if data_type == "rate":
		print("getting heartrate")
		hr.append(data)
		pr.append(None)
		temp.append(None)
	elif data_type == "temp":
		print("getting temperature")
		# write to temperature file
		temp.append(data)
		hr.append(None)
		pr.append(None)
	elif data_type == "press": 
		print("getting pressure")
		pr.append(data)
		hr.append(None)
		temp.append(None)
	else:
		sys.stderr("Unrecognized datatype: \'%s\'" % data_type)


def read_serial():
	serialport = None
	while serialport is None:
		try:
			serialport = serial.Serial("/dev/ttyACM0", 9600, timeout=0.5)
		except (serial.SerialException, serial.SerialException) as error:
			sys.stderr.write(("Error while trying to establish connection. Trying again...\n"))
			time.sleep(5)
	line = ""
	while True:
		try:
			byte = serialport.read()
			char = byte.decode("utf-8") 
			print(byte, char)
		except (serial.SerialException, serial.SerialTimeoutException) as error:
			sys.stderr("Error while trying to read. Shutting down...\n")
			char = "\n"
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
