
"""
Script for interpreting blastall results
argument1 = folder where the blast results are
argument2 = output name for blasthits matrix

"""
#imports
import re
import os
import sys

# sys.argv

folder = sys.argv[1]
output = sys.argv[2]
#def line counter
def lines_number(result_file):
	number = 0
	with open(result_file, 'r') as f:
    		for line in f:
        		number = number + 1
	return str(number)


#def results detector
def detect_file(txt):
	i = txt.strip("result.txt")
	names = i.split("_")
	query = names[0]
	db = names[1]
	return [query, db]
#variables
all_files = os.listdir(folder)
query_list_all,query_list,db_list_all,db_list = [],[],[],[]
#script
for i in all_files:
	open(folder+"/"+i)
	query_list_all.append(detect_file(i)[0])
	db_list_all.append(detect_file(i)[1])
	for i in db_list_all:
		if i not in db_list:
			db_list.append(i)
	db_list.sort()
	for i in query_list_all:
		if i not in query_list:
			query_list.append(i)
	query_list.sort()
print (query_list)
print (db_list)
header = ["query_name"]+db_list
header = "	".join(header)
print (header)
final_file = [header]
for a in query_list:
	line = [a]
	for b in db_list:
		number = lines_number(folder+"/"+a+"_"+b+"_result.txt")
		line.append(number)
	line = "	".join(line)
	final_file.append(line)
	print (line)
final_file = "\n".join(final_file)

#write output
with open(output,"w+") as F:
	F.write(final_file)
F.close()
