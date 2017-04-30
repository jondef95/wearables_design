#    time rsync -av -e ssh --partial /home/jonathan/wearables/compression/full/ jonathan@172.29.84.39:/home/jonathan/rsync_test

import subprocess, sys, time
from speedtest import *
from datetime import datetime, time


def high_traffic():
	oldout = sys.stdout
	sys.stdout = open(os.devnull, 'w')
	upload = shell()
	sys.stdout = oldout
	print('%0.2f' % upload)


def after_hours():
	now = datetime.now().time()
	return time(18, 00) <= now <= time(6, 00)


def send_to_low(dirname, dest):
	limit = "--bwlimit=1000"
	# if after_hours():
	#	limit = ""
	# elif high_traffic():
	# 	limit = limit + 500
	# else:
	#	limit = limit + 1000
	args = ['rsync', limit, '-av', '-e', 'ssh', dirname, dest]
	p = subprocess.Popen(args, shell=True)
	while p.returncode != 0:
		if p.returncode != None:
			time.sleep(600)
			p = subprocess.Popen(args, shell=True)
		elif after_hours():
			p.terminate()
			args[1] = ""
			p = subprocess.Popen(args, shell=True)
		elif args[1] is "":
			p.terminate()
			args[1] = limit
			p = subprocess.Popen(args, shell=True)
		time.sleep(1800)
		
def send_to_med(dirname, dest):
	limit = "--bwlimit=10000"
	# if after_hours():
	#	limit = ""
	# elif high_traffic():
	# 	limit = limit + 5000
	# else:
	#	limit = limit + 10000
	args = ['rsync', limit, '-av', '-e', 'ssh', dirname, dest]
	p = subprocess.Popen(args, shell=True)
	while p.returncode != 0:
		if p.returncode != None:
			time.sleep(300)
			p = subprocess.Popen(args, shell=True)
		elif after_hours():
			p.terminate()
			args[1] = ""
			p = subprocess.Popen(args, shell=True)
		elif args[1] is "":
			p.terminate()
			args[1] = limit
			p = subprocess.Popen(args, shell=True)
		time.sleep(900)
		p.poll()



def send_to_high(dirname, dest):
	limit = ""
	args = ['rsync', limit, '-av', '-e', 'ssh', dirname, dest]
	p = subprocess.Popen(args, shell=True)
	while p.returncode != 0:
		if p.returncode != None:
			time.sleep(300)
			p = subprocess.Popen(args, shell=True)
		time.sleep(600)
		p.poll()


if __name__ == "__main__":
	high_traffic()