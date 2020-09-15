import json
import numpy as np
import pickle
import os
from tqdm import tqdm
import joblib
import random


def json_to_pickle(features_path = '../data/test'):
    feature_file = os.listdir(features_path)

    for file in tqdm(feature_file):
        feature = np.load(os.path.join(features_path, file))
        feature_list = [list(x) for x in feature]
        feature_list_path = os.path.join('../data/test', file[:-4])
        pickle.dump(feature_list, open(feature_list_path, 'wb'))


def pickle_to_txt(file_path):
    video_ids = joblib.load(file_path)
    print(len(video_ids))
    txt_file_path = file_path[:-4] + '.txt'
    with open(txt_file_path, 'w') as f:
        for v_id in tqdm(video_ids):
            v_id += '\n'
            f.write(v_id)


def merge_two_txt(txt_file_one, txt_file_two, save_path):
    txt_one_contents = []
    txt_two_contents = []
    with open(txt_file_one, 'r') as f:
        txt_one_contents = f.readlines()
    with open(txt_file_two, 'r') as f:
        txt_two_contents = f.readlines()
    merged_contents = txt_one_contents + txt_two_contents

    with open(save_path, 'w') as f:
        for content in tqdm(merged_contents):
            f.write(content)


def random_select_from_proposal_list(numbers, proposal_list_file, save_path):
    select_nums = set([random.randint(0, 8000) for i in range(numbers)])
    print(len(select_nums))
    lines = list(open(proposal_list_file))
    from itertools import groupby
    groups = groupby(lines, lambda x: x.startswith('#'))
    info_list = [[x for x in list(g)] for k, g in groups if not k]
    res = []
    for i, number in tqdm(enumerate(select_nums)):
        res.append('#'+str(i)+'\n')
        res += info_list[number]

    with open(save_path, 'w') as f:
        f.writelines(res)


if __name__ == '__main__':
    # random_select_from_proposal_list(360, '../data/bmn_train_proposal_list_24000_32000.txt',
    #                                 '../data/bmn_train_proposal_split_32000/bmn_val_proposal_32000.txt')
    pickle_to_txt('../data/train_video_id_16000_24000.pkl')