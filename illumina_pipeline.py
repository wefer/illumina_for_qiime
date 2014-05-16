#!/usr/bin/env python

import os, subprocess, sys


def trim(infile, n_bases):
	"""Trim away primer sequences (n number of bases at the beginning of the sequence)"""

	if not os.path.isdir('trimmed'):
		os.makedirs('trimmed')

	outfile = 'trimmed/' + infile.split('.')[0] + "_trim." + infile.split('.')[-1]
	o = open(outfile,'w')	
	with open(infile, 'r') as f:
		flag = 0			#flag next line as sequence
		for line in f.readlines():
			if flag == 0:
				if "@HWI" in line or line == "+\n":
					o.write(line)
					flag = 1
			else:
				o.write(line[n_bases:])
				flag = 0

	o.close()
	return outfile


def merge(fwd, rev):
	"""Send sequences to SeqPrep for merging"""

	filend = fwd.split('.')[-1]
	basename = fwd.split('R1')[0].split('/')[-1]
	merged = 'merged/' + basename + 'merg.' + filend + '.gz'
	unm1 = 'unmerged/' + basename + 'R1_unm.' + filend + '.gz'
	unm2 = 'unmerged/' + basename + 'R2_unm.' + filend + '.gz'

	#Create directories for output
	if not os.path.isdir('unmerged'):
		os.makedirs('unmerged')
	if not os.path.isdir('merged'):
		os.makedirs('merged')	

	merge_cmd = "/home/hugow/bin/SeqPrep -f %s -r %s -s %s -1 %s -2 %s" % (fwd, rev, merged, unm1, unm2)
	print "Start merging:\n"
	merge = subprocess.Popen(merge_cmd, shell=True)
	merge.wait()
	return merge.returncode


def run_pipe(fwd, rev):
	"""Run trim and merge on forward and reverse sequences"""	

	R1_n_bases = 22
	R2_n_bases = 21
	t1 = trim(fwd, R1_n_bases)
	t2 = trim(rev, R2_n_bases)
	merge(t1, t2)
	return 0

def main():
	files = [x for x in os.listdir('./') if "R1" in x]
	for file in files:
		fwd = file
		rev = file.replace('R1', 'R2')
		print fwd, rev
		run_pipe(fwd, rev)



if __name__ == "__main__":
	main()


