import sys
import random

# print a matrix in the traditional form
def print_matrix(m):
	for row in m:
		print(row)
	return m

# generate random matrix with dimension d
def gen(d):
	new = [[ None for y in range(d) ] for x in range(d)] 
	for i in range(d):
		for j in range(d):
			new[i][j] = random.randint(1, 10)
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
	half = rows / 2

	# base case: 1x1 matrices -> 1x1 matrix
	if rows == 1:
		return [[m1[0][0] * m2[0][0]]]

	# create submatrices A through H 
	a, b, c, d, e, f, g, h = [[[ None for y in range(half) ] \
				for x in range(half)] for i in range(8)]

	# get submatrices A through H recursively
	for i in range(half):
		for j in range(half):
			a[i][j] = m1[i][j]
			b[i][j] = m1[i][j + half]
			c[i][j] = m1[i + half][j]
			d[i][j] = m1[i + half][j + half]
			e[i][j] = m2[i][j]
			f[i][j] = m2[i][j + half]
			g[i][j] = m2[i + half][j]
			h[i][j] = m2[i + half][j + half]

	# calculate p1 through p7
	p1 = strassen(a, sub(f, h))
	p2 = strassen(add(a, b), h)
	p3 = strassen(add(c, d), e)
	p4 = strassen(d, sub(g, e))
	p5 = strassen(add(a, d), add(e, h))
	p6 = strassen(sub(b, d), add(g, h))
	p7 = strassen(sub(a, c), add(e, f))

	# reconstruct matrix
	topleft = add(p5, add(p4, sub(p6, p2)))
	topright = add(p1, p2)
	bottomleft = add(p3, p4)
	bottomright = add(p5, sub(p1, add(p3, p7)))
	for i in range(rows):
		for j in range(rows):
			if i < half and j < half:
				m1[i][j] = topleft[i][j]
			elif i < half:
				m1[i][j] = topright[i][j - half]
			elif j < rows/2:
				m1[i][j] = bottomleft[i - half][j]
			else:
				m1[i][j] = bottomright[i - half][j - half]
	return m1

# typical way of multiplying two square matrices
def typical(m1, m2):
	new_matrix = []
	new_row = []
	cnt = 0

	# row iteration
	for i in range(len(m1)):
		# iterating through m2's columns
		for j in range(len(m1)):
			# iterating through the second matrix
			for k in range(len(m1)):
				cnt += m1[i][k] * m2[k][j]

			new_row.append(cnt)
			cnt = 0

		new_matrix.append(new_row)
		new_row = []

	return new_matrix

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
	# assert (strassen([[1,2,3], [4,5,6], [7,8,9]], [[1,2,3], [4,5,6], \
	#		[7,8,9]]) == [[30,36,42],[66,81,96],[102,126,150]]), "typ, 3x3"

def main():
	#args is a list of the arguments passed at command line
	args = sys.argv
	flag = args[1]
	dimension = args[2]

	# run tests
	testing()

	# try multiplying two 2x2 matrices w/ strassen's
	print_matrix(strassen([[1,2],[3,4]],[[1,2],[3,4]]))
	return 1

if __name__ == '__main__':
	main()