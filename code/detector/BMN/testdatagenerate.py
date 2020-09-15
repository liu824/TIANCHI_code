# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 19:34:47 2020

@author: lenovo
"""

#s生成测试文件的.list文件
#docker文件未提供val_video_ids
#s生成测试文件的.list文件
import os
import json
import cv2

video_path="data/train/Round2_Test"#video路径
save_path='user_data/tmp_data/infer.list'#新的json文件保存路径

dataset={}
jsonfile=open(save_path,'w',encoding='utf-8')
i=0

video_list=os.listdir(video_path)
for line in video_list:
    videoId,_=line.split('.')

    cap = cv2.VideoCapture(os.path.join(video_path,str(videoId)+'.mp4')) #增加耗时
    if cap.isOpened():
        rate = cap.get(5)
        frame_num =cap.get(7)
        duration = frame_num/rate            
        dataset[str(videoId)]={"duration_second":duration,"subset": "validation","annotations":[]}
        i=i+1

jsonfile.write(str(dataset))
jsonfile.close()