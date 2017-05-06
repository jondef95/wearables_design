import serial, sys, os, datetime, time, random, string, atexit
from argparse import ArgumentParser


hr = []
temp = []
pr = []
write = False
pw = False
hw = False
tw = False

@atexit.register
def shutdown():
	global pr, hr, temp, pw, hw, tw
	print("Shutting down...")
	if write:
		path = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(12))
		os.chdir("/tmp")
		if not os.path.exists(path):
			os.makedirs(path)
		os.chdir(path)
		if hw:
			write_to_file(hr, "heartrate")
		if pw:
			write_to_file(pr, "pressure")
		if tw:
			write_to_file(temp, "temp")
		if not (pw or hw or tw):
			output = "\nNo session created"
		else:
			output = "\nYour session name is: %s" % path
		print(output)

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
	global hr, pr, temp, hw, pw, tw
	data_type, data = str.split(line, "~")

	if data_type == "rate":
		print("getting heartrate")
		hr.append(data)
		pr.append(None)
		temp.append(None)
		hw = True
	elif data_type == "temp":
		print("getting temperature")
		# write to temperature file
		temp.append(data)
		hr.append(None)
		pr.append(None)
		tw = True
	elif data_type == "press": 
		print("getting pressure")
		pr.append(data)
		hr.append(None)
		temp.append(None)
		pw = True
	else:
		sys.stderr.write("Unrecognized datatype: \'%s\'" % data_type)


def read_serial():
	serialport = None
	while serialport is None:
		try:
			serialport = serial.Serial("/dev/ttyACM0", 9600, timeout=0.5)
		except (FileNotFoundError, serial.SerialException, serial.SerialException):
			sys.stderr.write(("Error while trying to establish connection. Trying again...\n"))
			time.sleep(5)
	line = ""
	while True:
		try:
			byte = serialport.read()
			char = byte.decode("utf-8") 
			print(byte, char)
		except (FileNotFoundError, serial.SerialException, serial.SerialTimeoutException) as error:
			sys.stderr.write("Error while trying to read. Shutting down...\n")
			char = "\n"
		if char is '#':
			print(line)
			process_line(line)
			line = ""
		elif char is not '\r' and char is not '\n':
			line = line + char

def display_data():
	mode = input("Which type of data would you like to display? ('heartrate', 'temperature', 'pressure')\n> ")
	if mode == 'q' or mode == 'quit':
		sys.exit()
	options = ['heartrate', 'temperature', 'pressure']
	while mode not in options:
		mode = input("Invalid data type: please select from 'heartrate', 'temperature', and 'pressure'\n> ")
		if mode == 'q' or mode == 'quit':
			sys.exit()
	date_text = input("What date was your data recorded? (DD-MM-YYYY)")
	if mode == 'q' or mode == 'quit':
		sys.exit()
	date = ""
	while True:
		try:
		    date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
		except ValueError:
			date_text = input("Incorrect date format (DD-MM-YYYY):")
			continue
		break




def main():
	global write
	parser = ArgumentParser(description="Read incoming data from sensing device and store in separate, displayable files")
	parser.add_argument(
		'-R', '--read',
		action="store_true",
		help='Read from a COM port and write data to individual files')
	parser.add_argument(
		'-D', '--display',
		action="store_true",
		help='Search current directory for displayable files, open for viewing')

	args = parser.parse_args()

	if args.read:
		write = True
		read_serial()
	elif args.display:
		display_data()
	else:
		sys.stderr.write("Invalid mode; please using tag '-h' for help with options")
if __name__ == "__main__":
	main()
