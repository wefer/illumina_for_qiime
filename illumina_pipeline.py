#!/usr/bin/env python

import os, subprocess, sys
import yaml


with open('config.yaml', 'r') as f:
	params =  yaml.load(f)
	seq_prep = params['seqprep_loc']
	R1_bases_trim = params['fwd_bases_to_trim']
	R2_bases_trim = params['rev_bases_to_trim']


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
	basename = fwd.split('_R1')[0].split('/')[-1]
	merged = 'merged/' + basename + '_merg.' + filend + '.gz'
	unm1 = 'unmerged/' + basename + '_R1_unm.' + filend + '.gz'
	unm2 = 'unmerged/' + basename + '_R2_unm.' + filend + '.gz'

	#Create directories for output
	if not os.path.isdir('unmerged'):
		os.makedirs('unmerged')
	if not os.path.isdir('merged'):
		os.makedirs('merged')	

	merge_cmd = "%s -f %s -r %s -s %s -1 %s -2 %s" % (seqprep_binary, fwd, rev, merged, unm1, unm2)
	print "Start merging:\n"
	merge = subprocess.Popen(merge_cmd, shell=True)
	merge.wait()
	return merge.returncode


def run_pipe(fwd, rev, R1_bases_trim, R2_bases_trim):
	"""Run trim and merge on forward and reverse sequences"""	

	t1 = trim(fwd, R1_bases_trim)
	t2 = trim(rev, R2_bases_trim)
	merge(t1, t2)
	return 0

def main():
	files = [x for x in os.listdir('./') if "_R1" in x]
	for f in files:
		fwd = f
		rev = f.replace('_R1', '_R2')
		print fwd, rev
		run_pipe(fwd, rev, R1_bases_trim, R2_bases_trim)



if __name__ == "__main__":
	main()


