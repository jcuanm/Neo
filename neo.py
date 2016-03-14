import sys

#prints a matrix in the traditional form
def print_matrix(m):
	for row in m:
		print(row)
	return m

#TODO: function that generates random matrix with the specified dimensions

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


def main():
	#args is a list of the arguments passed at command line
	args = sys.argv
	flag = args[1]
	dimension = args[2]

	#testing multiplying two 3x3 matrices
	print_matrix(typical([[1,2,3], [4,5,6], [7,8,9]], [[1,2,3], [4,5,6], [7,8,9]]))
	return 1


if __name__ == '__main__':
	main()