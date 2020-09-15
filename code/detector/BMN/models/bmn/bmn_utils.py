#  Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserve.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and

import numpy as np
from paddle.fluid.initializer import Uniform
import pandas as pd
import multiprocessing as mp
import json
import os


def iou_with_anchors(anchors_min, anchors_max, box_min, box_max):
    """Compute jaccard score between a box and the anchors.
    """
    len_anchors = anchors_max - anchors_min
    int_xmin = np.maximum(anchors_min, box_min)
    int_xmax = np.minimum(anchors_max, box_max)
    inter_len = np.maximum(int_xmax - int_xmin, 0.)
    union_len = len_anchors - inter_len + box_max - box_min
    jaccard = np.divide(inter_len, union_len)
    return jaccard


def ioa_with_anchors(anchors_min, anchors_max, box_min, box_max):
    """Compute intersection between score a box and the anchors.
    """
    len_anchors = anchors_max - anchors_min
    int_xmin = np.maximum(anchors_min, box_min)
    int_xmax = np.minimum(anchors_max, box_max)
    inter_len = np.maximum(int_xmax - int_xmin, 0.)
    scores = np.divide(inter_len, len_anchors)
    return scores


def boundary_choose(score_list):
    max_score = max(score_list)
    mask_high = (score_list > max_score * 0.5)
    score_list = list(score_list)
    score_middle = np.array([0.0] + score_list + [0.0])
    score_front = np.array([0.0, 0.0] + score_list)
    score_back = np.array(score_list + [0.0, 0.0])
    mask_peak = ((score_middle > score_front) & (score_middle > score_back))
    mask_peak = mask_peak[1:-1]
    mask = (mask_high | mask_peak).astype('float32')
    return mask


def soft_nms(df, alpha, t1, t2):
    '''
    df: proposals generated by network;
    alpha: alpha value of Gaussian decaying function;
    t1, t2: threshold for soft nms.
    '''
    df = df.sort_values(by="score", ascending=False)
    tstart = list(df.xmin.values[:])
    tend = list(df.xmax.values[:])
    tscore = list(df.score.values[:])

    rstart = []
    rend = []
    rscore = []

    while len(tscore) > 1 and len(rscore) < 101:
        max_index = tscore.index(max(tscore))
        tmp_iou_list = iou_with_anchors(
            np.array(tstart),
            np.array(tend), tstart[max_index], tend[max_index])
        for idx in range(0, len(tscore)):
            if idx != max_index:
                tmp_iou = tmp_iou_list[idx]
                tmp_width = tend[max_index] - tstart[max_index]
                if tmp_iou > t1 + (t2 - t1) * tmp_width:
                    tscore[idx] = tscore[idx] * np.exp(-np.square(tmp_iou) /
                                                       alpha)

        rstart.append(tstart[max_index])
        rend.append(tend[max_index])
        rscore.append(tscore[max_index])
        tstart.pop(max_index)
        tend.pop(max_index)
        tscore.pop(max_index)

    newDf = pd.DataFrame()
    newDf['score'] = rscore
    newDf['xmin'] = rstart
    newDf['xmax'] = rend
    return newDf


def video_process(video_list,
                  video_dict,
                  output_path,
                  result_dict,
                  snms_alpha=0.4,
                  snms_t1=0.55,
                  snms_t2=0.9):

    for video_name in video_list:
        df = pd.read_csv(os.path.join(output_path, video_name + ".csv"))
        if len(df) > 1:
            df = soft_nms(df, snms_alpha, snms_t1, snms_t2)

        video_duration = video_dict[video_name]["duration_second"]
        proposal_list = []
        for idx in range(min(100, len(df))):
            tmp_prop={"score":df.score.values[idx],\
                      "segment":[max(0,df.xmin.values[idx])*video_duration,\
                                 min(1,df.xmax.values[idx])*video_duration]}
            proposal_list.append(tmp_prop)
        result_dict[video_name[2:]] = proposal_list


def bmn_post_processing(video_dict, subset, output_path, result_path):
    video_list = video_dict.keys()
    video_list = list(video_dict.keys())
    global result_dict
    result_dict = mp.Manager().dict()
    pp_num = 12

    num_videos = len(video_list)
    num_videos_per_thread = int(num_videos / pp_num)
    processes = []
    for tid in range(pp_num - 1):
        tmp_video_list = video_list[tid * num_videos_per_thread:(tid + 1) *
                                    num_videos_per_thread]
        p = mp.Process(
            target=video_process,
            args=(tmp_video_list, video_dict, output_path, result_dict))
        p.start()
        processes.append(p)
    tmp_video_list = video_list[(pp_num - 1) * num_videos_per_thread:]
    p = mp.Process(
        target=video_process,
        args=(tmp_video_list, video_dict, output_path, result_dict))
    p.start()
    processes.append(p)
    for p in processes:
        p.join()

    result_dict = dict(result_dict)
    output_dict = {
        "version": "VERSION 1.3",
        "results": result_dict,
        "external_data": {}
    }
    outfile = open(
        os.path.join(result_path, "bmn_results_%s.json" % subset), "w")

    json.dump(output_dict, outfile)
    outfile.close()
