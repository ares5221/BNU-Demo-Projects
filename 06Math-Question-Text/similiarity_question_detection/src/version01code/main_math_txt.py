# encoding:utf-8

import os
import json
import time
import csv
import Levenshtein

resutl_path = './../result/math_result0409/'
threshold_maximum = 0.95 #阈值大于0.95认为相似
threshold_minimum = 0.8  #阈值小于0.8认为不相似

def read_data(path):
    data = []
    preprocess_path = './../data/preprocess_result_math'
    path = os.path.join(preprocess_path, path)
    with open(path, 'r', encoding='utf-8') as csv_read:
        reader = csv.reader(csv_read)
        for row in reader:
            data.append(row)
    return data[:]


def cal_blank_subj_Levenshtein_ratio(data, sort_name):
    tmp_dict = {}
    for idx in range(len(data)):
        # for idx in range(0, 3):
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
    # print(tmp_dict)
    top = sorted(tmp_dict.items(), key=lambda x: x[0], reverse=True)

    similiarity_name = os.path.join(resutl_path, sort_name + '_判定相似.txt')
    with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
        for tmp in top:
            if tmp[0] > threshold_maximum:
                f.write('Levenshtein_ratio: ' + str(tmp[0]) + '\n')
                f.write('str1: ' + tmp[1]['str1'] + '\n')
                f.write('str2: ' + tmp[1]['str2'] + '\n')
                f.write('\n')

    check_name = os.path.join(resutl_path, sort_name + '_待人工校验.txt')
    with open(check_name, 'a', encoding='utf-8', newline='') as f:
        for tmp in top:
            if tmp[0] < threshold_maximum and tmp[0] > threshold_minimum:
                f.write('Levenshtein_ratio: ' + str(tmp[0]) + '\n')
                f.write('str1: ' + tmp[1]['str1'] + '\n')
                f.write('str2: ' + tmp[1]['str2'] + '\n')
                f.write('\n')


def cal_single_choice_Levenshtein_ratio(data, sort_name):
    tmp_dict = {}
    for idx in range(len(data)):
        # for idx in range(0, 3):
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

                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                    ss = {}
                    ss['choice_val'] = choice_leven_ratio_val
                    ss['str1'] = curr_str1
                    ss['str2'] = curr_str2
                    tmp_dict[stem_leven_ratio_val] = ss
    # print(tmp_dict)
    top = sorted(tmp_dict.items(), key=lambda x: x[0], reverse=True)

    similiarity_name = os.path.join(resutl_path, sort_name + '_判定相似.txt')
    with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
        for tmp in top:
            if tmp[0] > threshold_maximum and tmp[1]['choice_val'] > threshold_maximum:
                f.write('题干相似度: ' + str(tmp[0]) + '\n')
                f.write('选项相似度: ' + str(tmp[1]['choice_val']) + '\n')
                f.write('str1: ' + tmp[1]['str1'] + '\n')
                f.write('str2: ' + tmp[1]['str2'] + '\n')
                f.write('\n')

    check_name = os.path.join(resutl_path, sort_name + '_待人工校验.txt')
    with open(check_name, 'a', encoding='utf-8', newline='') as f:
        for tmp in top:
            if (tmp[0] < threshold_maximum and tmp[0] > threshold_minimum) or (tmp[0]>=threshold_maximum and tmp[1]['choice_val'] < threshold_maximum):
                f.write('题干相似度: ' + str(tmp[0]) + '\n')
                f.write('选项相似度: ' + str(tmp[1]['choice_val']) + '\n')
                f.write('str1: ' + tmp[1]['str1'] + '\n')
                f.write('str2: ' + tmp[1]['str2'] + '\n')
                f.write('\n')


if __name__ == '__main__':
    print('start...')
    data_file_list = ['fill_in_blanks_data.csv', 'single_choice_data.csv', 'subjective_question_data.csv']
    for curr_file in data_file_list:
        data = read_data(curr_file)
        if curr_file == 'single_choice_data.csv':
            cal_single_choice_Levenshtein_ratio(data, curr_file[:-4] + '_Edit_Distance_Value')
        else:
            # pass
            cal_blank_subj_Levenshtein_ratio(data, curr_file[:-4] + '_Edit_Distance_Value')

    print('end...')
