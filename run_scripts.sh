#!/bin/bash

python remap.py
python illumina_pipeline.py
ln -s header_rename.py merged/header_rename.py
cd merged
gunzip *.gz
pyhon header_rename.py



