#!/bin/bash

#Get subsample level

sub_reads=$(awk -F: '/subsample/ {print $2}' <(cat config.yaml | tr -d ' ' ) | cut -f 1); echo $sub_reads

python remap.py
python illumina_pipeline.py && ln -s header_rename.py merged/header_rename.py
cd merged
gunzip *.gz
python header_rename.py

if [ ! -z $sub_reads ]
	then
		for file in re_*; do head -n $(($sub_reads * 4)) $file >> all_seqs.fastq ; done
	else
		cat re_* > all_seqs_fastq
fi

sed -n '1~4s/^@/>/p;2~4p' all_seqs.fastq > all_seqs.fasta




