#    time rsync -av -e ssh --partial /home/jonathan/wearables/compression/full/ jonathan@172.29.84.39:/home/jonathan/rsync_test

import subprocess, sys, time
from speedtest import *
import datetime
from compression import *

def high_traffic():
	oldout = sys.stdout
	sys.stdout = open(os.devnull, 'w')
	upload = shell()
	sys.stdout = oldout
	print('%0.2f' % upload)


def after_hours():
	now = datetime.datetime.now().time()
	print(now)
	return datetime.time(18, 00) <= now <= datetime.time(6, 00)


def send_to_low(session, dest):
	limit = "--bwlimit=1000"
	fast = False
	# if after_hours():
	#	limit = ""
	# elif high_traffic():
	# 	limit = limit + 500
	# else:
	#	limit = limit + 1000
	compress = CompressDirectory()
	dirname = "/tmp/" + session
	compress.processdir(dirname, session)
	filename = "/tmp/" + session + "/" + session + ".tar.gz"
	args = "rsync %s -av -e ssh %s %s" % (limit, filename, dest)
	p = subprocess.Popen(args, shell=True)
	p.poll()
	while p.returncode != 0:
		if p.returncode != None:
			time.sleep(600)
			args = "rsync %s -av -e ssh %s %s" % (limit, filename, dest)
			p = subprocess.Popen(args, shell=True)
		elif after_hours():
			print("after-hours")
			p.terminate()
			args = "rsync -av -e ssh %s %s" % (filename, dest)
			p = subprocess.Popen(args, shell=True)
			fast = True
		elif fast:
			print("resetting")
			p.terminate()
			args = "rsync %s -av -e ssh %s %s" % (limit, filename, dest)
			p = subprocess.Popen(args, shell=True)
			fast = False
		print("outside")
		time.sleep(5)
		p.poll()
		
def send_to_med(session, dest):
	limit = "--bwlimit=10000"
	fast = False
	# if after_hours():
	#	limit = ""
	# elif high_traffic():
	# 	limit = limit + 5000
	# else:
	#	limit = limit + 10000
	compress = CompressDirectory()
	dirname = "/tmp/" + session
	compress.processdir(dirname, session)
	filename = "/tmp/" + session + "/" + session + ".tar.gz"
	args = "rsync %s -av -e ssh %s %s" % (limit, filename, dest)
	p = subprocess.Popen(args, shell=True)
	p.poll()
	while p.returncode != 0:
		if p.returncode != None:
			time.sleep(300)
			args = "rsync %s -av -e ssh %s %s" % (limit, filename, dest)
			p = subprocess.Popen(args, shell=True)
		elif after_hours():
			p.terminate()
			args = "rsync -av -e ssh %s %s" % (filename, dest)
			p = subprocess.Popen(args, shell=True)
			fast = True
		elif fast:
			p.terminate()
			args = "rsync %s -av -e ssh %s %s" % (limit, filename, dest)
			p = subprocess.Popen(args, shell=True)
			fast = False
		time.sleep(60)
		p.poll()



def send_to_high(session, dest):
	limit = ""
	compress = CompressDirectory()
	dirname = "/tmp/" + session
	compress.processdir(dirname, session)
	filename = "/tmp/" + session + "/" + session + ".tar.gz"
	args = "rsync %s -av -e ssh %s %s" % (limit, filename, dest)
	p = subprocess.Popen(args, shell=True)
	p.poll()
	while p.returncode != 0:
		if p.returncode != None:
			time.sleep(300)
			p = subprocess.Popen(args, shell=True)
		time.sleep(60)
		p.poll()


if __name__ == "__main__":
	high_traffic()