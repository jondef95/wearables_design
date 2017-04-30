import matplotlib.pyplot as plt
import csv, sys

def graph_file(filename):
	x = []
	y = []

	with open(filename, 'r') as csvfile:
		plots = csv.reader(csvfile, delimiter=',')
		i = 1
		for row in plots:
			x.append(i)
			y.append(int(row[0]))
			i = i + 1

	plt.plot(x,y, label='Loaded from file!')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('Interesting Graph\nCheck it out')
	plt.legend()
	plt.savefig('chart.jpg')
	plt.show()

if __name__ == '__main__':
	graph_file(sys.argv[1])