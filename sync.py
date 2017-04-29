#    time rsync -av -e ssh --partial /home/jonathan/wearables/compression/full/ jonathan@172.29.84.39:/home/jonathan/rsync_test

import subprocess, sys, time
from speedtest import *


def high_traffic():
	oldout = sys.stdout
	sys.stdout = open(os.devnull, 'w')
	upload = shell()
	sys.stdout = oldout
	print('%0.2f' % upload)


def send_to_low(dirname, dest):
	limit = '--bwlimit='
	# if high_traffic():
	# 	limit = limit + 500
	args = ['rsync', '--bwlimit=1000', '-av', '-e', 'ssh', dirname, dest]
	p = subprocess.Popen(args)
	p.wait()
	print(p.returncode)
	while p.returncode != 0:
		time.sleep(600)
		p = subprocess.Popen(args, shell=True)
