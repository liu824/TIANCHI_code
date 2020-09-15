[toc]

# 注意

## BMN提名生成部分

- 依赖环境:Ubuntu 18.04TS,  paddlepaddle1.8.0 python3.7 
- 预训练模型:  百度网盘链接: https://pan.baidu.com/s/1jSTqd4pFRbkgogWLCcJewg  提取码: npuy

## PGCN提名分类部分

- 依赖环境: Ubuntu 18.04TS,  Python 3.7.2,  cuda 10.1, cudnn 7.6.4,  PyTorch 1.3.1

  - Python 依赖包:

    - torchvision

    - numpy

    - scikit-learn

    - terminaltables

    - pandas

    - scipy


# 解决方案

## BMN部分
BMN模型是百度自研，2019年ActivityNet夺冠方案，为视频动作定位问题中proposal的生成提供高效的解决方案，在PaddlePaddle上首次开源。
### 算法思路
BMN的目的是生成视频的proposal,此模型引入边界匹配(Boundary-Matching, BM)机制来评估proposal的置信度，按照proposal开始边界的位置及其长度将所有可能存在的proposal组合成一个二维的BM置信度图。网络由三个模块组成，基础模块作为主干网络处理输入的特征序列，TEM模块预测每一个时序位置属于动作开始、动作结束的概率，PEM模块生成BM置信度图

### 实现细节:

1. 本代码部分使用BMN生成训练集和测试集的proposal,训练集每个视频1500个proposal，保存在文件夹.\user_data\train_proposal下，由于单个文件过大，共分成10个json文件保存。测试集每个视频生成100个proposal,保存在文件user_data\tmp_data下
2. 训练及推理部分的代码放在code文件夹下，训练模型时，请运行打开train.ipynb,推理时打开infer.ipynb
3. 请根据config文件夹下的bmn.yaml的配制存放训练数据集及标签文件，train时需要把训练的I3D特征文件放在data/dataset/bmn/train文件夹下，推理时将测试数据存放在data/dataset/bmn/videofeature文件夹下.
4. 训练及推理的标签文件分别是trainlabel.jon和infer1.list

## PGCN部分

### 算法思路

PGCN用图神经网络来学习proposal-proposal间的关系, 来实现对提名的分类. 首先我们构建了一个动作提名图, 图中的每个节点代表了一个提名, 图的边代表了proposal之间的关系.  实现中,我们使用了两种类型的关系, 一种是获取每个proposal与其他proposal的上下文信息, 另外一种是构建不同动作之间的联系. 最后我们应用上述构建出来的图神经网络来建模不同proposal之间的关系和学习动作分类和定位的有效表达.

### 训练推理过程

- 数据: 使用比赛组织方提供的I3D特征和BMN生成的提名
- 总共训练900个epoch,  训练过程的主要指标: 损失值loss

### 实现细节

1. 初始学习率设置为0.01, 随着epoch的增长, 学习率逐渐下降; 每八十个epoch, 学习率缩减为原来的十分之一

2. 受限于硬件资源, 我们将所有视频的特征每1000个视频为一份, 依次训练

3. 首先需要将bmn生成的proposal解析成PGCN的格式, 然后开始训练, 训练完成后对测试集进行测试, 并将结果解析成提交格式. 

