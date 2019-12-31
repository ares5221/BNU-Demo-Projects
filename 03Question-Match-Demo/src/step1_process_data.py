#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from docx import Document
import json


def read_source_data():
    source_docx_path = './../data/data_origin/'
    curr_file = os.path.join(source_docx_path, '【问答】相似题例.docx')
    document = Document(curr_file)
    content = []
    for paragraph in document.paragraphs:
        # print(paragraph.text)     # 打印各段落内容文本
        content.append(paragraph.text)

    tmp = ''.join(content).replace('\n', '').replace('\xa0', '')

    print('切分问题对')
    ques_pairs_list = tmp.split('————————————————————————————————')
    return ques_pairs_list


def save_json_data(data_list):
    curr_json_dir = './../data/data_clean/data_form.json'
    print(len(data_list))
    data_json = {}
    for pairs in data_list:
        tmp_json = {}
        if pairs:  # 去掉空的
            split_part = pairs.split('【')
            first_part = '【' + split_part[1]
            second_part = '【' + split_part[2]
            third_part = 1
            tmp_json['first_part'] = first_part
            tmp_json['second_part'] = second_part
            tmp_json['third_part'] = third_part
            if len(data_json) not in data_json:
                data_json[len(data_json)] = tmp_json

    with open(curr_json_dir, 'w', encoding='utf-8') as json_write:
        json.dump(data_json, json_write, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    print('开始读取文件内容...')
    ques_pairs_list = read_source_data()
    save_json_data(ques_pairs_list)
    print('问题对数据保存在json中完成')
