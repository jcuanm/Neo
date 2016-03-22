import sys
import random
import time
import math

# print a matrix in the traditional form
def print_full(m):
	for row in m:
		print(row)
	return m

# print just the diagonals of a matrix
def print_matrix(m):
	for i in range(len(m)):
		print str(m[i][i])
	return m

# generate random matrix with dimension d
def gen(d):
	new = [[ None for y in range(d) ] for x in range(d)] 
	for i in range(d):
		for j in range(d):
			new[i][j] = random.randint(0, 2)
	return new

# add one square matrix to another
def add(m1, m2):
	new = [[ None for y in range(len(m1)) ] for x in range(len(m1))] 
	for i in range(len(m1)):
		for j in range(len(m1)):
			new[i][j] = m1[i][j] + m2[i][j]
	return new

# subtract one square matrix from another
def sub(m1, m2):
	new = [[ None for y in range(len(m1)) ] for x in range(len(m1))] 
	for i in range(len(m1)):
		for j in range(len(m1)):
			new[i][j] = m1[i][j] - m2[i][j]
	return new

# strassen's algorithm for multiplying two square matrices
def strassen(m1, m2):
	rows = len(m1)

	half = int(math.ceil(float(rows) / 2))

	# base case: crossover to typical algorithm
	if rows <= 1:
		return typical(m1, m2)

	# create submatrices A through H 
	a, b, c, d, e, f, g, h = [[[ 0 for y in range(half) ] \
				for x in range(half)] for i in range(8)]

	# get submatrices A through H recursively
	x = rows - half
	for i in range(half):
		for j in range(half):
			a[i][j] = m1[i][j]
			e[i][j] = m2[i][j]

			if j != x:
				b[i][j] = m1[i][j + half]
				f[i][j] = m2[i][j + half]

			if i != x:
				c[i][j] = m1[i + half][j]
				g[i][j] = m2[i + half][j]

			if i != x and j != x:
				d[i][j] = m1[i + half][j + half]
				h[i][j] = m2[i + half][j + half]

	# calculate p1 through p7
	p1 = strassen(a, sub(f, h))
	p2 = strassen(add(a, b), h)
	p3 = strassen(add(c, d), e)
	p4 = strassen(d, sub(g, e))
	p5 = strassen(add(a, d), add(e, h))
	p6 = strassen(sub(b, d), add(g, h))
	p7 = strassen(sub(a, c), add(e, f))

	# (manually) reconstruct matrix
	new = [[ None for y in range(rows) ] for x in range(rows)] 
	for i in range(rows):
		for j in range(rows):
			if i < half and j < half:
				new[i][j] = p5[i][j] + p4[i][j] + p6[i][j] - p2[i][j]
			elif i < half:
				new[i][j] = p1[i][j - half] + p2[i][j - half]
			elif j < half:
				new[i][j] = p3[i - half][j] + p4[i - half][j]
			else:
				x = i - half
				y = j - half
				new[i][j] = p5[x][y] + p1[x][y] - p3[x][y]- p7[x][y]

	return new

# typical way of multiplying two square matrices
def typical(m1, m2):
	new_matrix = []
	new_row = []
	cnt = 0

	# flip m2 (for caching)
	for i in range(len(m2)):
		# iterating through m2's columns
		for j in range(i, len(m2)):
			swap = m2[i][j]
			m2[i][j] = m2[j][i]
			m2[j][i] = swap

	# row iteration
	for i in range(len(m1)):
		# iterating through m2's columns
		for j in range(len(m1)):
			# iterating through the second matrix
			for k in range(len(m1)):
				cnt += m1[i][k] * m2[j][k]

			new_row.append(cnt)
			cnt = 0

		new_matrix.append(new_row)
		new_row = []

	return new_matrix

# multiply two square matrices
def mult(m1, m2):
	return strassen(m1, m2)

# tests for various functions
def testing():
	# test add
	assert (add([[1]],[[4]]) == [[5]]), "add, 1x1"
	assert (add([[1,2],[3,4]],[[1,2],[3,4]]) == [[2,4],[6,8]]), "add, 2x2"

	# test sub
	assert (sub([[1]],[[4]]) == [[-3]]), "sub, 1x1"
	assert (sub([[1,2],[3,4]],[[1,2],[3,4]]) == [[0,0],[0,0]]), "sub, 2x2"

	# test typical
	assert (typical([[3]],[[4]]) == [[12]]), "typ, 1x1"
	assert (typical([[1,2],[3,4]],[[1,2],[3,4]]) == [[7,10],[15,22]]), \
			"typ, 2x2"
	assert (typical([[1,2,3], [4,5,6], [7,8,9]], [[1,2,3], [4,5,6], \
			[7,8,9]]) == [[30,36,42],[66,81,96],[102,126,150]]), "typ, 3x3"

	# test strassens
	assert (strassen([[3]],[[4]]) == [[12]]), "typ, 1x1"
	assert (strassen([[1,2],[3,4]],[[1,2],[3,4]]) == [[7,10],[15,22]]), \
			"typ, 2x2"
	assert (strassen([[1,2,3], [4,5,6], [7,8,9]], [[1,2,3], [4,5,6], \
			[7,8,9]]) == [[30,36,42],[66,81,96],[102,126,150]]), "typ, 3x3"

def main():
	# get command-line arguments
	args = sys.argv
	flag = int(args[1])
	dimension = int(args[2])
	inputfile = args[3]

	# if in testing mode, run tests
	if flag == 1:
		testing()

	# open file
	f = open(inputfile, "r")

	# initialize matrices
	m1, m2 = [[[ None for y in range(dimension) ] \
			for x in range(dimension)] for i in range(2)]

	'''# fill first matrix
	for i in range(dimension):
		for j in range(dimension):
			m1[i][j] = int(f.readline())
	# fill second matrix
	for i in range(dimension):
		for j in range(dimension):
			m2[i][j] = int(f.readline())'''

	# close file
	f.close()

	m1 = gen(dimension)
	m2 = gen(dimension)

	# print result of multiplication
	t0 = time.clock() 
	print_full(strassen(m1,m2))
	print time.clock() - t0

	t0 = time.clock() 
	print_full(typical(m1,m2))
	print time.clock() - t0

	return 1

if __name__ == '__main__':
	main()