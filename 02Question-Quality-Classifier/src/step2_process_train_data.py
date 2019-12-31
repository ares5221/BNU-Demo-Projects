#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import os
from bert_serving.client import BertClient
from sklearn.preprocessing import OneHotEncoder
import numpy as np
def get_train_data():

    good_json_dir = './../data/data_clean/good.json'
    bad_json_dir = './../data/data_clean/bad.json'
    with open(good_json_dir, "rb") as json_object:
        good_data = json.load(json_object)
    with open(bad_json_dir, "rb") as json_object2:
        bad_data = json.load(json_object2)
    # print(good_data)
    # print(bad_data)
    data = []
    for tmp in good_data:
        # print(good_data[tmp])
        good_vec = data_to_vector(good_data[tmp])
        data.append(good_vec)
    for tmp2 in bad_data:
        # print(bad_data[tmp2])
        bad_vec = data_to_vector(bad_data[tmp2])
        data.append(bad_vec)
    print(len(data))
    # save npy data
    np.save(train_data_path, data)


def data_to_vector(curr):
    # todo 需要多加一类others
    one_hot_encoder = {'语文': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                       '数学': [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                       '物理': [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                       '化学': [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       '生物': [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                       '历史': [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                       '地理': [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
                       }
    bc = BertClient()
    subj = curr['学科'][1:-1]
    question = curr['问题'].replace(' ', '')
    problem_solving_thought = curr['解题思路'].replace(' ', '')
    problem_solving_method = curr['解题办法'].replace(' ', '')
    # print(subj)
    # print(question)
    # print(problem_solving_thought)
    # print(problem_solving_method)
    # print('\n')
    vec_part0 = one_hot_encoder[subj]
    vec_part1 = bc.encode([question]).tolist()[0]
    if (not problem_solving_thought) or (not problem_solving_method):
        print('数据中解题思路或者解题办法内容为空，请查看生成数据是否正确！！！！！！！！')
    vec_part2 = bc.encode([problem_solving_thought]).tolist()[0]
    vec_part3 = bc.encode([problem_solving_method]).tolist()[0]
    # 拼接四个部分的向量
    vec_joining = vec_part0 + vec_part1 + vec_part2 + vec_part3
    # print(len(vec_joining), vec_joining)
    return vec_joining


def get_train_label():
    postive_part = [1 for i in range(20)]
    negative_part = [0 for i in range(20)]
    train_label = postive_part + negative_part
    print(train_label)
    # save npy label
    np.save(train_label_path, train_label)


if __name__ == '__main__':
    print('开始生成训练数据...')
    train_data_path = './../data/train_data/train_data.npy'
    if not os.path.exists(train_data_path):
        get_train_data()
    train_label_path = './../data/train_data/train_label.npy'
    if not os.path.exists(train_label_path):
        get_train_label()
    print('数据生成成功。')