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
	new = []
	for i in range(len(m1)):
		lst = []
		for j in range(len(m1)):
			lst.append(m1[i][j] + m2[i][j])
		new.append(lst)
	return new

# subtract one square matrix from another
def sub(m1, m2):
	new = []
	for i in range(len(m1)):
		lst = []
		for j in range(len(m1)):
			lst.append(m1[i][j] - m2[i][j])
		new.append(lst)
	return new

# strassen's algorithm for multiplying two square matrices
def strassen(m1, m2):
	rows = len(m1)

	half = int(math.ceil(float(rows) / 2))

	# base case: crossover to typical algorithm
	if rows <= 32:
		return typical(m1, m2)

	# create submatrices A through H 
	a, b, c, d, e, f, g, h = [[] for i in range(8)]

	# get submatrices A through H recursively
	x = rows - half
	for i in range(half):
		ar, br, cr, dr, er, fr, gr, hr = [[] for l in range(8)]
		for j in range(half):
			ar.append(m1[i][j])
			er.append(m2[i][j])
			if j != x:
				br.append(m1[i][j + half])
				fr.append(m2[i][j + half])
			else:
				br.append(0)
				fr.append(0)

			if i != x:
				cr.append(m1[i + half][j])
				gr.append(m2[i + half][j])
			else:
				cr.append(0)
				gr.append(0)

			if i != x and j != x:
				dr.append(m1[i + half][j + half])
				hr.append(m2[i + half][j + half])
			else:
				dr.append(0)
				hr.append(0)
		a.append(ar)
		b.append(br)
		c.append(cr)
		e.append(er)
		f.append(fr)
		g.append(gr)
		d.append(dr)
		h.append(hr)

	# calculate p1 through p7
	p1 = strassen(a, sub(f, h))
	p2 = strassen(add(a, b), h)
	p3 = strassen(add(c, d), e)
	p4 = strassen(d, sub(g, e))
	p5 = strassen(add(a, d), add(e, h))
	p6 = strassen(sub(b, d), add(g, h))
	p7 = strassen(sub(a, c), add(e, f))

	# (manually) reconstruct matrix
	new = []
	for i in range(rows):
		hey = []
		for j in range(rows):
			if i < half and j < half:
				hey.append(p5[i][j] + p4[i][j] + p6[i][j] - p2[i][j])
			elif i < half:
				hey.append(p1[i][j - half] + p2[i][j - half])
			elif j < half:
				hey.append(p3[i - half][j] + p4[i - half][j])
			else:
				x = i - half
				y = j - half
				hey.append(p5[x][y] + p1[x][y] - p3[x][y]- p7[x][y])
		new.append(hey)
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

	# flip m2 (for caching)
	for i in range(len(m2)):
		# iterating through m2's columns
		for j in range(i, len(m2)):
			swap = m2[i][j]
			m2[i][j] = m2[j][i]
			m2[j][i] = swap

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

	# test larger dimensions
	for i in range(5):
		a = gen(i)
		b = gen(i)
		j = strassen(a,b)
		k = typical(a,b)
		assert(j == k)

def main():
	# get command-line arguments
	args = sys.argv
	flag = int(args[1])
	dimension = int(args[2])
	inputfile = args[3]
	print(flag)

	# if in testing mode, run tests, do random matrices
	if flag == 0:
		print("HEY")
		# open file
		f = open(inputfile, "r")

		# initialize matrices
		m1, m2 = [[[ None for y in range(dimension) ] \
				for x in range(dimension)] for i in range(2)]

		# fill first matrix
		for i in range(dimension):
			for j in range(dimension):
				m1[i][j] = int(f.readline())
		# fill second matrix
		for i in range(dimension):
			for j in range(dimension):
				m2[i][j] = int(f.readline())

		# close file
		f.close()

	else:
		testing()

		m1 = gen(dimension)
		m2 = gen(dimension)

	# print result of multiplication
	t0 = time.clock() 
	a = strassen(m1,m2)
	print ("strassen", time.clock() - t0)

	t0 = time.clock() 
	b = typical(m1,m2)
	print ("typical", time.clock() - t0)

	assert(a == b)

	return 1

if __name__ == '__main__':
	main()