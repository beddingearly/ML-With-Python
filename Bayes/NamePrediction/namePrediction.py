#coding=utf-8
'''
@Time    : 2018/10/23 15:23
@Author  : Zt.Wang
@Email   : 137602260@qq.com
@File    : namePrediction.py
@Software: PyCharm
'''

import pandas as pd
from collections import defaultdict
import math

# 读取train.txt
train = pd.read_csv('train.txt')
test = pd.read_csv('test.txt')
submit = pd.read_csv('sample_submit.csv')