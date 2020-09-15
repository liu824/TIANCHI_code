import json
import joblib
import argparse

parser = argparse.ArgumentParser(description="PGCN Parse Json File")
parser.add_argument('--json_file', type=str, default=None)
parser.add_argument('--save_path', type=str, default=None)
args = parser.parse_args()

def parse_test_file(test_proposal_file, write_file):
    test_proposals = json.load(open(test_proposal_file, 'rb'))
    gt = '1\n0 0 100'
    res = []
    for i, (id, value) in enumerate(test_proposals.items()):
        index = '#' + str(i)
        res.append(index)
        res.append(id)
        total_frames = value['frame_num']
        res.append(str(int(total_frames)))
        res.append('1')
        res.append(gt)
        FPS = value['fps']
        res.append(str(len(value['annotations'][:250])))
        for anno in value['annotations'][:250]:
            anno_res = [0, 0, 0]
            start_frame = int(anno['segment'][0] * FPS)
            end_frame = int(anno['segment'][1] * FPS)
            anno_res += [start_frame, end_frame]
            anno_str = str(anno_res)[1:-1]
            anno_str = anno_str.replace(', ', ' ')
            res.append(anno_str)

    with open(write_file, 'w') as f:
        for i, r in enumerate(res):
            if i < len(res):
                r += '\n'
            f.write(r)


classes_name = {'鼓掌': 1, '跑': 2, '持枪': 3, '阅读': 4, '哭': 5, '打斗': 6, '唱歌': 7, '打电话': 8, '跳舞': 9, '挽手臂/搀扶': 10,
                '饮酒/喝液体': 11, '持刀': 12, '吃饭/吃东西': 13, '拥抱': 14, '挥手': 15, '行走': 16, '驾驶汽车': 17, '射击': 18, '写作': 19, '牵手': 20,
                '吸烟': 21, '使用手机': 22, '弹吉他': 23, '骑马': 24, '使用计算机': 25, '亲吻': 26, '骑摩托车': 27, '骑自行车': 28, '打架子鼓': 29,
                '打篮球': 30, '回头': 31, '战争对抗': 32, '弹钢琴': 33, '现代会议': 34, '拉小提琴': 35, '踢足球': 36, '化妆': 37, '游泳': 38,
                '玩纸牌类游戏': 39, '健身': 40, '上课': 41, '宴会': 42, '婚礼': 43, '炒菜': 44, '跳水': 45, '扫地': 46, '刷牙': 47, '拖地': 48,
                '手术': 49, '打排球': 50, '太极': 51, '滑冰': 52, '打高尔夫球': 53}


def compute_iou(gt, proposal):
    union = min(gt[0], proposal[0]), max(gt[1], proposal[1])
    inter = max(gt[0], proposal[0]), min(gt[1], proposal[1])
    if inter[0] >= inter[1]:
        return 0.0
    else:
        return float(inter[1] - inter[0]) / float(union[1] - union[0])


def max_iou(gts, proposal):
    ious = [(compute_iou(gt[1], proposal), gt[0]) for gt in gts]
    return max(ious)


def compute_overlop(gt, proposal):
    inter = max(gt[0], proposal[0]), min(gt[1], proposal[1])
    if inter[0] >= inter[1]:
        return 0.0
    else:
        return float(inter[1] - inter[0]) / float(proposal[1] - proposal[0])


def max_overlop(gts, proposal):
    overlops = [(compute_overlop(gt[1], proposal), gt[0]) for gt in gts]
    return max(overlops)


def parse_train_file(train_proposal_file='./data/gtad_results_10000.json',
                     write_file='../data/gtad_train_proposal_list_10000.txt'):
    train_proposals = json.load(open(train_proposal_file, 'rb'))
    train_video_id = list(train_proposals.keys())
    joblib.dump(train_video_id, '../data/train_video_id_gtad.pkl')
    res = []
    for i, (id, value) in enumerate(train_proposals.items()):
        index = '#' + str(i)
        res.append(index)
        res.append(id)
        total_frames = value['frame_num']
        res.append(str(int(total_frames)))
        res.append('1')
        gt_num = len(value['annotations'])
        res.append(str(gt_num))
        FPS = value['fps']
        all_gt = []
        for gt in value['annotations']:
            gt_list = []
            label = classes_name[gt['label']]
            gt_list.append(label)
            segment = [int(x * FPS) for x in gt['segment']]
            all_gt.append((label, segment))
            gt_list += segment
            gt_str = str(gt_list)[1:-1]
            gt_str = gt_str.replace(', ', ' ')
            res.append(gt_str)

        res.append(str(len(value['proposal'])))
        loc_ = len(res) - 1
        proposal_len = 0
        for p in value['proposal']:
            pro_res = []
            proposal = [int(y * FPS) for y in p['segment']]
            max_iou_, proposal_label = max_iou(all_gt, proposal)
            max_overlop_, _ = max_overlop(all_gt, proposal)
            if max_iou_ == 0 and max_overlop_ == 0:
                continue
            pro_res.append(proposal_label)
            pro_res.append(max_iou_)
            pro_res.append(max_overlop_)
            pro_res += proposal
            pro_str = str(pro_res)[1:-1]
            pro_str = pro_str.replace(', ', ' ')
            res.append(pro_str)
            proposal_len += 1

        print(proposal_len)
        if proposal_len < int(res[loc_]):
            res[loc_] = str(proposal_len)
        else:
            print('the same length')

    with open(write_file, 'w') as f:
        for i, r in enumerate(res):
            if i < len(res):
                r += '\n'
            f.write(r)


if __name__ == '__main__':
    parse_test_file(args.json_file, args.save_path)
