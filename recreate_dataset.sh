#!/bin/bash

rm -rf jsut_ver1.1
rm -rf datasets

unzip jsut_ver1.1

python divide_dir.py -i jsut_ver1.1/basic5000 -o datasets/Basic5000 -t jsut_ver1.1/basic5000/transcript_utf8.txt

cp utils/g2p/bpe_69.json datasets/Basic5000/

python create_dataset.py -i datasets/Basic5000/
