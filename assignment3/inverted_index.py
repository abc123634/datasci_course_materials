import MapReduce
import sys

"""
Problem 1 - inverted index 
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    term_appeared = []
    words = value.split()

    for w in words:
        if w in term_appeared:
          pass
        else:
          term_appeared.append(w)
          mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: list of documents
    doc_list = []
    for v in list_of_values:
      doc_list.append(v)
    mr.emit((key, doc_list))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
