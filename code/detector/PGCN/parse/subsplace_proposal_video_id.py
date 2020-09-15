import os


def main():
    proposal_list_file = "/home/myliu/Project/TActionDet/PGCN/data/bsn_test_proposal_list.txt"
    prefix_dir = "/home/myliu/baidunetdiskdownload/Rgb_Test_feature"
    with open(proposal_list_file) as f:
        proposal_lines = f.read().split('\n')

    proposal_length = len(proposal_lines)
    name_lines = [(proposal_lines[i+1], i+1) for i in range(proposal_length) if proposal_lines[i].startswith('#')]
    new_name_lines = [(os.path.join(prefix_dir, line[0].split('/')[-1]), line[1]) for line in name_lines]
    for line in new_name_lines:
        proposal_lines[line[1]] = line[0]

    save_path = "/home/myliu/Project/TActionDet/PGCN/data/new_test_proposal_list.txt"
    with open(save_path, 'w') as fw:
        for line in proposal_lines:
            line += '\n'
            fw.write(line)


if __name__ == '__main__':
    main()




