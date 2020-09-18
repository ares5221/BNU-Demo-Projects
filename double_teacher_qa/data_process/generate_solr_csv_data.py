#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import os
import csv
from utils import replace_punctuation
from utils import re_filter_str


def read_save_data(sub):
    data_path = './../download_data_from_mysql'
    data_dir = os.path.join(data_path, sub + '_qa_data.txt')
    save_path = './double_teacher_ques_ans.csv'
    chinese = json.load(open(data_dir, encoding='utf-8'))
    # print(chinese)
    with open(save_path, 'a',encoding='utf-8',newline='') as csv_write:
        # save title
        csv_write = csv.writer(csv_write)
        csv_write.writerow(['id','ques','ans','raw_title','raw_content','clean_title', 'clean_content'])
        for tmp in chinese:
            # print(tmp['question_id'])
            # print('question_title_clean:',tmp['question_title_clean'])
            # print('question_content_clean:',tmp['question_content_clean'])
            # print('answer_content:',tmp['answer_content'])
            # print('##'*88)
            curr_id = tmp['question_id']
            curr_ques = replace_punctuation(tmp['question_title_clean']) + '--' + replace_punctuation(tmp['question_content_clean'])
            curr_ans = tmp['answer_content']
            curr_raw_title = tmp['question_title_original'].replace(',','，')
            curr_raw_content = tmp['question_content_original'].replace(',','，')
            curr_clean_title = tmp['question_title_clean'].replace(',','，')
            curr_clean_content = tmp['question_content_clean'].replace(',','，')
            is_accept_curr_data, curr_ques, curr_ans = process_data(curr_ques, curr_ans, curr_clean_title, curr_clean_content)
            if is_accept_curr_data:
                csv_write.writerow([curr_id, curr_ques, curr_ans, curr_raw_title,curr_raw_content, curr_clean_title,curr_clean_content])


def process_data(curr_ques, curr_ans, curr_clean_title, curr_clean_content):
    if curr_clean_title in curr_clean_content:
        curr_ques = curr_clean_content
    if curr_clean_content in curr_clean_title:
        curr_ques = curr_clean_title
    # 判断当前问答数据是否采用，若过短等问题则跳过
    is_accept_curr_data = True
    curr_ques = curr_ques.strip().replace(',','，')
    curr_ans = curr_ans.strip().replace(',','，').replace('\n','')
    curr_ques = re_filter_str(curr_ques)
    # curr_ans = re_filter_str(curr_ans)
    if len(curr_ques) <5 or len(curr_ans)<5:
        is_accept_curr_data = False

    return is_accept_curr_data,curr_ques, curr_ans



def start():
    curr_sub = 'cn'
    read_save_data(curr_sub)


if __name__ == '__main__':
    start()
    print('run end')