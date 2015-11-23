import MapReduce
import sys

"""
Problem 6 - matrix multiplication
"""

mr = MapReduce.MapReduce()

def mapper(record):
	table, row, col = record[0], record[1], record[2]

	if table == 'a':
		for i in range(5):
			key = (row, i)
			mr.emit_intermediate(key, record)
	else:
		for i in range(5):
			key = (i, col)
			mr.emit_intermediate(key, record)
	

def reducer(key, list_of_values):
	a = dict()
	b = dict()

	for value in list_of_values:
		if value[0] == 'a':
			a[value[2]] = value[3]
			
		else:
			b[value[1]] = value[3]

	sum_product = 0
	for i in range(5):
		temp = a.get(i, 0) * b.get(i, 0)
		sum_product += temp

	row, col = key[0], key[1]
	mr.emit((row, col, sum_product))



if __name__ == '__main__':
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)

