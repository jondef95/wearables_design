from argparse import ArgumentParser
from sync import *
from compression import *

def main():
	parser = ArgumentParser(description="Compress and sync data from local directory to remote directory")
	parser.add_argument(
		'--mode',
		dest='mode', default='send',
		choices=['send', 'recv'], 
		help='Mode for the manager to run in (default: client).\n'
			+ 'send: Send a session to another machine\n'
			+ 'recv: Search current directory for packaged session to extract')

	parser.add_argument(
		dest='session',
		help='Session ID that needs to be packaged and sent, or retrieved')

	parser.add_argument(
		'--priority', 
		dest='priority', default='low',
		choices=['low', 'medium', 'high'],
		help='Priority of the session being sent (default: low).\n'
			+ 'low: Compress locally, utilize minimal network resources until after hours, then increase to max\n'
			+ 'medium: Compress locally, use moderate network resources until after hours, then increase to max\n'
			+ 'high: Compress locally, use maximum network resources until transmission is complete.')

	parser.add_argument(
		dest = 'dest',
		help="Username, address, and directory of destination machine. Will use SSH keys "
			+ "if available, otherwise will require password for destination machine's user")

	args = parser.parse_args()

	if args.mode == 'recv':
		tarname = args.session + ".tar.gz"
		ExtractFolder(tarname)

	if '@' not in args.dest:
		rsp = input("This destination appears to be on this machine. Continue with sync? (y/n):")
		while rsp is not 'y' or rsp is not 'n':
			rsp = input("Please try 'y' or 'n':")
		if rsp is 'n':
			sys.exit()

	if args.priority == 'low':
		print("Sending files over low priority transmission...")
		send_to_low(args.session, args.dest)
	elif args.priority == 'medium':
		print("Sending files over medium priority transmission...")
		send_to_med(args.session, args.dest)
	elif args.priority == 'high':
		print("Sending files over high priority transmission...")
		send_to_high(args.session, args.dest)

		
if __name__ == "__main__":
	main()
