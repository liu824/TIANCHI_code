#! /bin/bash/

python pgcn_test.py thumos14 $1 result -j2
python eval_detection_results.py thumos14 result  --nms_threshold 0.5
