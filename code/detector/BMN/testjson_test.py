# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 19:56:04 2020

@author: lenovo
"""

#s生成测试文件的.list文件，本来直接用trainlabel.json就行,但这次的特征过大，需要分成多部分推理
import os
import cv2
import json
abspath=os.path.abspath(os.path.dirname(__file__))#绝对路径
laspath=os.path.abspath(os.path.dirname(os.getcwd()))#上级目录
annos = json.load(open(os.path.join(abspath,'data/dataset/bmn/trainlabel.json'),'rb'))

npy_path=os.path.join(laspath,"data/Round2_Test/i3d_feature")#video路径
npy_list=os.listdir(npy_path)

save_path=os.path.join(laspath,'user_data/trainlabel2.list')#新的json文件保存路径后缀名无所谓，主要是里边内容的格式，该list文件采用的是字典的方式存储

dataset={}
jsonfile=open(save_path,'w',encoding='utf-8')
i=0
j=0
for videoId in annos.keys():
    if os.path.exists(os.path.join(npy_path,str(videoId)+'.npy')):#判断文件是否已存在
          
        # dataset[str(videoId)]={"duration_second":duration,"subset": "validation","annotations":[]}
        dataset[str(videoId)]=annos[str(videoId)]
        i=i+1
    else:
        # print(videoId)
        j=j+1
    
json.dump(dataset,jsonfile,ensure_ascii=False)
jsonfile.close()