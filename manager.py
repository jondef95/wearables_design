from argparse import ArgumentParser

def main():
	parser = ArgumentParser(description="Compress and sync data from local directory to remote directory")
	parser.add_argument(
		'--mode',
		dest='mode', default='client',
		choices=['client', 'server'],
		help='Mode for the manager to run in (default: client).\n'
			+ 'client: Send a session to another machine\n'
			+ 'server: Search current directory for packaged session to extract')

	parser.add_argument(
		'session',
		help='Session ID that needs to be packaged and sent')

	parser.add_argument('--priority', 
		dest='priority', default='low',
		choices=['low', 'medium', 'high'],
		help='Priority of the session being sent (default: low).\n'
			+ 'low: Compress locally, utilize minimal network resources until after hours, then increase to max\n'
			+ 'medium: Compress locally, use moderate network resources until after hours, then increase to max\n'
			+ 'high: Compress locally, use maximum network resources until transmission is complete.')

	parser.add_argument('dest',
		help="Username, address, and directory of destination machine. Will use SSH keys"
			+ "if available, otherwise will require password for destination machine's user")

	args = parser.parse_args()

	if '@' is not in args.dest:
		rsp = input("This destination appears to be on this machine. Continue with sync? (y/n):")
		while rsp is not 'y' or rsp is not 'n':
			rsp = input("Please try 'y' or 'n':")
		if rsp is 'n':
			sys.exit()

	if args.priority == 'low':
		print('low')
	elif args.priority == 'medium':
		print('medium')
	elif args.priority == 'high':
		print('high')

		
if __name__ == "__main__":
	main()