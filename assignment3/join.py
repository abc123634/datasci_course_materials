import MapReduce
import sys

"""
Problem 2 - Natural Join Operation 
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: join attribute(order_id)
    # value: whole record include the table name which the record originated from
    key = record[1]
    value = record

    mr.emit_intermediate(key, record)

def reducer(key, list_of_values):
    # key: join attribute(order_id)
    # value: whole record include the table name which the record originated from

    order_record = list()
    temp = list()
    result = list()
    for value in list_of_values:
      if value[0] == "order":
          order_record = value
          # mr.emit(order_record)
    # print order_record  

    for value in list_of_values:
        if value[0] == "line_item":
            join_record = list(order_record)
            join_record.extend(value)
            result.append(join_record)
            mr.emit(join_record)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
