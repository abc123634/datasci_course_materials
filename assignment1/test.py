name = raw_input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)

dic = dict()
for line in handle:
    if line.startswith('From'):
        terms = line.split(" ")

        if len(terms) < 5: continue 
        time = terms[6].split(":")
        hr = time[0]
        dic[hr] = dic.get(hr, 0) + 1

lst = dic.items()

lst.sort(key=lambda x: x[0])
for k, v in lst:
    print k, v