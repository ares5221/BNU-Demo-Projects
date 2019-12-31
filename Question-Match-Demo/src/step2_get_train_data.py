#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import os
from bert_serving.client import BertClient
import numpy as np

def get_train_data(base_dir):
    bc = BertClient()
    json_data_dir = './../data/data_clean/data_form.json'
    with open(json_data_dir, 'r', encoding='utf-8') as jd:
        data = json.load(jd)
    train_data1 = []
    train_data2 = []
    train_label = []
    for idx in data:
        part1 = data[idx]['first_part']
        part2 = data[idx]['second_part']
        part3 = data[idx]['third_part']
        vec1 = bc.encode([part1]).tolist()[0]
        vec2 = bc.encode([part2]).tolist()[0]
        sign = part3
        train_data1.append(vec1)
        train_data2.append(vec2)
        train_label.append(sign)

    train_data1_dir = os.path.join(base_dir, 'train_data1.npy')
    train_data2_dir = os.path.join(base_dir, 'train_data2.npy')
    train_label_dir = os.path.join(base_dir, 'train_label.npy')
    np.save(train_data1_dir, train_data1)
    np.save(train_data2_dir, train_data2)
    np.save(train_label_dir, train_label)


if __name__ == '__main__':
    base_dir = './../data/train_data'
    train_data1_dir = os.path.join(base_dir, 'train_data1.npy')
    train_data2_dir = os.path.join(base_dir, 'train_data2.npy')
    train_label_dir = os.path.join(base_dir, 'train_label.npy')
    if not os.path.exists(train_data1_dir) and not os.path.exists(train_data2_dir) and not os.path.exists(train_label_dir):
        get_train_data(base_dir)
    print('数据处理完成，并保存结束')