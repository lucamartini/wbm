#!/bin/bash

# you must chose a run number present in runs/* and a lumi in E33
# i.e. ./run.sh 251168 1.

python read_wbm_L1.py $1
python read_wbm_HLT.py $1
python csv2tex.py $1 $2
cd news/
pdflatex news
pdflatex news
mv news.pdf ../run_rates/news_$1.pdf
cd ..
