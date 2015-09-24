import MapReduce
import sys

"""
Problem 4 - Asymmetric friendship count
"""

mr = MapReduce.MapReduce()

def mapper(record):
	key = (record[0], record[1])
	value = record
	mr.emit_intermediate(key, 1)

	key = (record[1], record[0])
	value = record
	mr.emit_intermediate(key, -1)

def reducer(key, list_of_values):

	if not len(list_of_values) == 2:
		mr.emit(key)


if __name__ == '__main__':
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)
