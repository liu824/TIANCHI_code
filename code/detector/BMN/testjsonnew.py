# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 20:50:48 2020

@author: lenovo
"""

import json
import os
f = open("user_data/bmn_results_train.json",encoding="utf-8")
BMNresult = json.load(f)
outfile = open(
    os.path.join('user_data', "bmn_results_train2.json"), "w")

json.dump(BMNresult['results'], outfile)
outfile.close()