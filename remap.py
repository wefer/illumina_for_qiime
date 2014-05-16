#!/usr/bin/env python

import os

map = open('id_map.txt', 'r').readlines()
id_dict = {}

for line in map:
	k = line.split('\t')[0]
	v= line.split('\t')[1].rstrip()
	id_dict[k] = v

fqs = [x for x in os.listdir('.') if x[-1:] == "q"]

for item in fqs:
	print item

for file in fqs:
	extid = file.split('_')[0]
	intid = id_dict[extid]
	new_name = intid + file[4:]
	print new_name
	os.rename(file, new_name)
	
