from tqdm import tqdm
train_proposal_file = '../data/bmn_train_proposal_list_16000_24000.txt'

write_lines = []
pbar = tqdm(total=7913)
with open(train_proposal_file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith('#'):
            block_num = int(line[1:])
            pbar.update(1)
            if (block_num % 1000 == 0 and block_num != 0) or (block_num == 8014):
                file_path = '../data/bmn_train_proposal_split_24000/bmn_split_' + str(block_num) + '.txt'
                with open(file_path, 'w') as split_f:
                    split_f.writelines(write_lines)
                write_lines = []

        write_lines.append(line)

pbar.close()