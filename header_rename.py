#!/usr/bin/env python

import sys
import os


def header_rename(infile, sample_name, barcode):
	o = open("re_"+infile, 'w')
	with open(infile, 'r') as f:
		i = 1
		for line in f.readlines():
			if line[:4] == "@HWI":
				flowcell_id = line.split(':')[2]
				new_header = "@%s_%i %s orig_bc=%s new_bc=%s bc_diffs=0\n" % (sample_name, i, flowcell_id, barcode, barcode) 
				o.write(new_header)
				i += 1
			else:
				o.write(line)	
	o.close()
	return 0


def map_create(sample_name, barcode, description, mapfile):
	print sample_name
	if not os.path.isfile(mapfile):
		map = open(mapfile, 'w')
		base_header = "#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tDescription\n"
		map.write(base_header)
	else:
		map=open(mapfile, 'a')

	content = "%s\t%s\t%s\t%s\n" % (sample_name, barcode, "CCTACGGGNGGCWGCAG", description)
	map.write(content)
	map.close()
	return 0


def main():
	for fq in [x for x in os.listdir('.') if x[-1] == "q"]:
		infile = fq
		sample_name = infile.split('_')[0]
		barcode = ''.join(infile.split('_')[1].split('-'))
		header_rename(infile, sample_name, barcode)
		map_create(sample_name, barcode, "sample", "map.txt")
	return 0

if __name__ == "__main__":
	main()
