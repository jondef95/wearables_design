#    time rsync -av -e ssh --partial /home/jonathan/wearables/compression/full/ jonathan@172.29.84.39:/home/jonathan/rsync_test

import subprocess, sys

def send_to_low(dirname, dest):
	args = ['rsync', '--bwlimit=1000', '-av', '-e', 'ssh', dirname, dest]
	p = subprocess.Popen(args)