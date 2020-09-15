#!/bin/bash
python parse/parse_file.py --json_path $1 --save_name $2
bash test.sh $3
cd parse
python parse_res.py --predict_pc $4 --save_json $5

