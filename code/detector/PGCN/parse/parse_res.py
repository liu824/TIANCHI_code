import pandas as pd
import pickle
import json
from multiprocessing.pool import Pool
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description="PGCN Parse Result")
parser.add_argument('--predict_pc', type=str, default=None)
parser.add_argument('--save_json', type=str, default=None)
args = parser.parse_args()
duration_time = json.load(open('detector/PGCN/parse/test_duration_time.json', 'r'))

classes_name = {0: '鼓掌', 1: '跑', 2: '持枪', 3: '阅读', 4: '哭', 5: '打斗', 6: '唱歌', 7: '打电话', 8: '跳舞', 9: '挽手臂/搀扶',
10: '饮酒/喝液体', 11: '持刀', 12: '吃饭/吃东西', 13: '拥抱', 14: '挥手', 15: '行走', 16: '驾驶汽车', 17: '射击', 18: '写作', 19: '牵手',
20: '吸烟', 21: '使用手机', 22: '弹吉他', 23: '骑马', 24: '使用计算机', 25: '亲吻', 26: '骑摩托车', 27: '骑自行车', 28: '打架子鼓',
29: '打篮球', 30: '回头', 31: '战争对抗', 32: '弹钢琴', 33: '现代会议', 34: '拉小提琴', 35: '踢足球', 36: '化妆', 37: '游泳',
38: '玩纸牌类游戏', 39: '健身', 40: '上课', 41: '宴会', 42: '婚礼', 43: '炒菜', 44: '跳水', 45: '扫地', 46: '刷牙', 47: '拖地',
48: '手术', 49: '打排球', 50: '太极', 51: '滑冰', 52: '打高尔夫球'}


def save_duration_time(proposal_json_file, save_path):
    bmn_items = json.load(open(proposal_json_file, 'rb'))
    duration_time_res = {}
    for key, val in tqdm(bmn_items.items()):
        duration_time_res[key] = val['duration_second']

    json.dump(duration_time_res, open(save_path, 'wb'))


def parse_res(path):
    res_file = path[0]
    save_path = path[1]
    raw_res = pickle.load(open(res_file, 'rb'))
    res = {}
    for cls, val in enumerate(raw_res):
        for index in val.index:
            item = val.loc[index].values
            video_id = item[0]
            score = item[-1]
            assert cls == item[1]
            segment = [item[2]*duration_time[video_id], item[3]*duration_time[video_id]]
            label = {"label": classes_name[cls], "score": score, "segment": segment}
            if video_id not in res.keys():
                res[video_id] = [label]
            else:
                res[video_id].append(label)
    json.dump(res, open(save_path, 'w'))


def join_all_res(res_paths, save_path):
    res = [json.load(open(path, 'r')) for path in res_paths]
    res_update = res[0].copy()
    for r in res[1:]:
        res_update.update(r)
    print(len(res_update))
    assert len(res_update) == 4833
    res_sorted = {}
    for key, val in res_update.items():
        sorted_val = sorted(val, key=lambda keys:keys['score'], reverse=True)
        res_sorted = sorted_val[:100]

    json.dump(res_sorted, open(save_path, 'w'))

def sort_result(res_paths, save_path):
    res = json.load(open(res_paths, 'r'))
    assert len(res) == 4834
    res_sorted = {}
    for key, val in res.items():
        sorted_val = sorted(val, key=lambda keys: keys['score'], reverse=True)
        res_sorted[key] = sorted_val[:100]

    json.dump(res_sorted, open(save_path, 'w'))


if __name__ == '__main__':
    temp_json_name = args.save_json[:-5] + '_temp.json'
    thread_args = [(args.predict_pc, temp_json_name)]
    print(thread_args)
    with Pool(processes=8) as p:
        res = list(tqdm(p.imap(parse_res, thread_args), total=len(thread_args), desc="Parse result into json ... "))
    p.close()
    p.join()
    sort_result(temp_json_name, args.save_json)




