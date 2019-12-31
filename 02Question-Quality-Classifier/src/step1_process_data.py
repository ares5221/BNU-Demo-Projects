#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from docx import Document
import re
import uuid
import json
# setting
# good_quality_doc_path = './../data/data_origin/good_docx/【问答】质量较好问题.docx'
# bad_quality_doc_path = './../data/data_origin/bad_docx/【问答】质量较差问题.docx'

def read_good_question():
    good_quality_doc_path = './../data/data_origin/good_docx/'
    doc_info_list = []
    for fname in os.listdir(good_quality_doc_path):
        curr_file_dir = os.path.join(good_quality_doc_path, fname)
        content = read_docx_content(curr_file_dir)
        content_info_json = content_formatting(content)
        doc_info_list.append(content_info_json)
    if len(doc_info_list) == 1:
        print('当前只处理单一文档的数据')
        good_quality_json_path = './../data/data_clean/good.json'
        with open(good_quality_json_path, 'w', encoding='utf-8') as json_write:
            json.dump(doc_info_list[0], json_write, indent=4, ensure_ascii=False)


def read_bad_question():
    bad_quality_doc_path = './../data/data_origin/bad_docx/'
    doc_info_list = []
    for fname in os.listdir(bad_quality_doc_path):
        curr_file_dir = os.path.join(bad_quality_doc_path, fname)
        content = read_docx_content(curr_file_dir)
        content_info_json = content_formatting(content)
        doc_info_list.append(content_info_json)
        if len(doc_info_list) == 1:
            print('当前只处理 bad 单一文档的数据')
            good_quality_json_path = './../data/data_clean/bad.json'
            with open(good_quality_json_path, 'w', encoding='utf-8') as json_write:
                json.dump(doc_info_list[0], json_write, indent=4, ensure_ascii=False)


def content_formatting(content):
    tmp = ''.join(content).replace('\xa0', '').replace('\n', '')
    print(len(tmp), tmp)
    #get subject info
    subject_pattern = re.compile(r'【.{2}】')  # 正则表达式提取【生物】
    subject_info = re.findall(subject_pattern,tmp)
    question_info = re.split(subject_pattern, tmp)
    if len(question_info) >len(subject_info):
        print('切分的问题中有空格出现')
        for qi in question_info:
            if not qi:
                question_info.remove(qi)
    # print(len(question_info), question_info)
    # get 问题 解题思路 解题办法
    content_info = {}
    for idx in range(len(question_info)):
        tmp_json = {}
        if '解题思路' in question_info[idx] and '解题办法' in question_info[idx]:
            wenti = question_info[idx].split('解题思路')[0]
            jietisilu = '解题思路' + question_info[idx].split('解题思路')[1].split('解题办法')[0]
            jietibanfa = '解题办法'+ question_info[idx].split('解题思路')[1].split('解题办法')[1]
            # print(idx,'ss', wenti, ' ssss ', jietisilu, ' sssssss ', jietibanfa)
            tmp_json['学科'] = subject_info[idx]
            tmp_json['问题'] = wenti
            tmp_json['解题思路'] = jietisilu
            tmp_json['解题办法'] = jietibanfa
            content_info[idx] = tmp_json
        elif '解题思路' not in question_info[idx] and '解题办法' in question_info[idx]:
            wenti = question_info[idx].split('解题办法')[0]
            jietisilu = '解题思路：'
            jietibanfa = '解题办法' + question_info[idx].split('解题办法')[1]
            # print(idx,'ss', wenti, ' ssss ', jietisilu, ' sssssss ', jietibanfa)
            tmp_json['学科'] = subject_info[idx]
            tmp_json['问题'] = wenti
            tmp_json['解题思路'] = jietisilu
            tmp_json['解题办法'] = jietibanfa
            content_info[idx] = tmp_json
        elif '解题办法' not in question_info[idx] and '解题思路' in question_info[idx]:
            wenti = question_info[idx].split('解题思路')[0]
            jietisilu = '解题思路' + question_info[idx].split('解题思路')[1]
            jietibanfa = '解题办法：'
            # print(idx,'ss', wenti, ' ssss ', jietisilu, ' sssssss ', jietibanfa)
            tmp_json['学科'] = subject_info[idx]
            tmp_json['问题'] = wenti
            tmp_json['解题思路'] = jietisilu
            tmp_json['解题办法'] = jietibanfa
            content_info[idx] = tmp_json
        else:
            wenti = question_info[idx]
            jietisilu = '解题思路：'
            jietibanfa = '解题办法：'
            # print(idx,'ss', wenti, ' ssss ', jietisilu, ' sssssss ', jietibanfa)
            tmp_json['学科'] = subject_info[idx]
            tmp_json['问题'] = wenti
            tmp_json['解题思路'] = jietisilu
            tmp_json['解题办法'] = jietibanfa
            content_info[idx] = tmp_json
    return content_info


def read_docx_content(docx_file):
    document = Document(docx_file)
    content = []
    for paragraph in document.paragraphs:
        # print(paragraph.text)     # 打印各段落内容文本
        content.append(paragraph.text)
    return content

if __name__ == '__main__':
    print('开始读取docx文本内容...')
    read_good_question()
    read_bad_question()
