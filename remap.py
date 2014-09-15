#!/usr/bin/env python

import os
import yaml

with open('config.yaml', 'r') as f:
	params = yaml.load(f)
	id_map = params['ID_translation_map']

map_f = open(id_map, 'r').readlines()
id_dict = {}

for line in map_f:
	k = line.split('\t')[0]
	v= line.split('\t')[1].rstrip()
	id_dict[k] = v

fqs = [x for x in os.listdir('.') if x[-2:] == "fq" or x[-5:] == 'fastq']

for item in fqs:
	print item

for f in fqs:
	extid = f.split('_')[0]
	intid = id_dict[extid]
	new_name = intid + f[4:]
	print new_name
	os.rename(f, new_name)
	
