#!/bin/bash
# python detector/BMN/predict.py --model_name=BMN --config=detector/BMN/configs/bmn.yaml --log_interval=1 \
#                  --weights=./data/checkpoints/BMN.pdopt --use_gpu=True
python detector/BMN/testdatagenerate.py
python detector/BMN/predict.py --model_name=BMN \
                  --config=detector/BMN/configs/bmn.yaml \
                  --log_interval=1 \
                  --weights=/media_ai/user_data/model_data/BMN.pdopt \
                  --use_gpu=True	\
python detector/PGCN/parse/parse_file.py --json_file ../user_data/tmp_data/proposal.json --save_path ../user_data/tmp_data/test_proposal.txt
python detector/PGCN/pgcn_test.py thumos14 ../user_data/model_data/PGCN_model_test.path.tar ../user_data/tmp_data/result_tmp
python detector/PGCN/eval_detection_results.py thumos14 ../user_data/tmp_data/result_tmp --nms_threshold 0.5
python detector/PGCN/parse/parse_res.py --predict_pc ../user_data/tmp_data/pred_dump.pc --save_json ../user_data/tmp_data/submit_rest.json
# ZIP_FILE_PATH=`python -c 'import datetime; filename="../submit/submit_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".zip";print(filename)'`
zip ../result.zip ../user_data/tmp_data/submit_rest.json
