# encoding:utf-8

import os
import json
import time
import csv
import Levenshtein

resutl_path = './../result/chinese_result0416/'
threshold_maximum = 0.5 #阈值大于0.95认为相似
threshold_minimum = 0.0  #阈值小于0.8认为不相似

def read_data(path):
    data = []
    preprocess_path = './../data/preprocess_result_chinese'
    path = os.path.join(preprocess_path, path)
    with open(path, 'r', encoding='utf-8') as csv_read:
        reader = csv.reader(csv_read)
        for row in reader:
            data.append(row)
    return data[:]


def cal_blank_subj_Levenshtein_ratio(data, sort_name):
    tmp_dict = {}
    for idx in range(len(data)):
        if idx % 100 == 0:
            print(sort_name, '已经完成：', idx / len(data) * 100, '%')
        for jdx in range(idx, len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].replace(' ', '')
                curr_txt2 = data[jdx][1].replace(' ', '')
                leven_ratio_val = Levenshtein.ratio(curr_txt1, curr_txt2)
                curr_str1 = data[idx][0] + ' ' + curr_txt1
                curr_str2 = data[jdx][0] + ' ' + curr_txt2
                ss = {}
                ss['str1'] = curr_str1
                ss['str2'] = curr_str2
                tmp_dict[leven_ratio_val] = ss
    top = sorted(tmp_dict.items(), key=lambda x: x[0], reverse=True)
    similiarity_name = os.path.join(resutl_path, sort_name + '_result.txt')
    with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
        for tmp in top:
            if tmp[0] > threshold_maximum:
                f.write('题干相似度: ' + str(tmp[0]) + '\n')
                f.write('题目1的题干: ' + tmp[1]['str1'] + '\n')
                f.write('题目2的题干: ' + tmp[1]['str2'] + '\n')
                f.write('\n')


def cal_single_choice_Levenshtein_ratio(data, sort_name):
    tmp_dict = {}
    for idx in range(len(data)):
        if idx % 100 == 0:
            print(sort_name, '已经完成：', idx / len(data) * 100, '%')
        for jdx in range(idx, len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].split(' ', 1)
                curr_txt2 = data[jdx][1].split(' ', 1)
                if len(curr_txt1) == 2 and len(curr_txt2) == 2:
                    ques_stem1 = curr_txt1[0]
                    ques_stem2 = curr_txt2[0]
                    choice_txt1 = curr_txt1[1]
                    choice_txt2 = curr_txt2[1]
                    stem_leven_ratio_val = Levenshtein.ratio(ques_stem1, ques_stem2)
                    choice_leven_ratio_val = Levenshtein.ratio(choice_txt1, choice_txt2)
                    stem_leven_ratio_val = round(stem_leven_ratio_val, 4)  # 保留四位小数
                    choice_leven_ratio_val = round(choice_leven_ratio_val, 4)

                    curr_str1 = data[idx][0] + ' ' + ques_stem1
                    curr_str2 = data[jdx][0] + ' ' + ques_stem2
                    curr_str3 = choice_txt1
                    curr_str4 = choice_txt2
                    ss = {}
                    ss['choice_val'] = choice_leven_ratio_val
                    ss['str1'] = curr_str1
                    ss['str2'] = curr_str2
                    ss['str3'] = curr_str3
                    ss['str4'] = curr_str4
                    tmp_dict[stem_leven_ratio_val] = ss
    # print(tmp_dict)
    top = sorted(tmp_dict.items(), key=lambda x: x[0], reverse=True)

    similiarity_name = os.path.join(resutl_path, sort_name + '_result.txt')
    with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
        for tmp in top:
            if tmp[0] > threshold_maximum and tmp[1]['choice_val'] > threshold_maximum:
                f.write('题干相似度: ' + str(tmp[0]) + '\n')
                f.write('答案相似度: ' + str(tmp[1]['choice_val']) + '\n')
                f.write('题目1的题干: ' + tmp[1]['str1'] + '\n')
                f.write('题目2的题干: ' + tmp[1]['str2'] + '\n')
                f.write('题目1的答案: ' + tmp[1]['str3'] + '\n')
                f.write('题目2的答案: ' + tmp[1]['str4'] + '\n')
                f.write('\n')


if __name__ == '__main__':
    print('start...')
    data_file_list = ['fill_in_blanks_data.csv', 'single_choice_data.csv',
                      'subjective_question_data.csv','judge_question_data.csv',
                      'multi_choice_question_data.csv','no_choice_data.csv']
    for curr_file in data_file_list:
        data = read_data(curr_file)
        if curr_file == 'single_choice_data.csv' or curr_file == 'multi_choice_question_data.csv' \
                or curr_file == 'fill_in_blanks_data.csv' or curr_file =='subjective_question_data.csv':
            cal_single_choice_Levenshtein_ratio(data, curr_file[:-4] + '_相似度比较')
        else:
            # pass
            cal_blank_subj_Levenshtein_ratio(data, curr_file[:-4] + '_相似度比较')

    print('end...')
