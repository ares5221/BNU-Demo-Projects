#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import numpy as np
from bert_serving.client import BertClient
import csv
import random
import xlrd
import os


def getQAquestion():
    print('start read moral_fqa_data...')
    filePath = './../data/moral_fqa_data.csv'
    q_data = []
    with open(filePath, 'r', encoding='utf-8') as csvfile:
        read = csv.reader(csvfile)
        for i in read:
            q_data.append(i[0])
            # print(i[0])
    print('获取到', len(q_data), '条问题')
    return q_data


def bertconvert(datas):
    print('start convet question_str2vector...')
    question_list = []
    bc = BertClient()
    for i in range(0, len(datas)):
        data = datas[i]
        newdata = "".join(data.split())  # data.replace(' ', '')
        question_list.append(newdata)
    ss = bc.encode(question_list)
    np.save("./../data/question2vec.npy", ss)


if __name__ == '__main__':
    print('将整理好的moral_fqa_data 生成相应的词向量文件...')
    if True:
        data = getQAquestion()
        bertconvert(data)
    print('Finish OK--->')
