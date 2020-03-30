#encoding:utf-8

import os
import cal_similarity
import json
import time
import csv


def read_data(path):
    data = []
    preprocess_path = './preprocess_result'
    path = os.path.join(preprocess_path, path)
    with open(path, 'r', encoding='utf-8') as csv_read:
        reader = csv.reader(csv_read)
        for row in reader:
            data.append(row)
    return data[:]


def sort_by_Levenshtein_ratio(data,sort_name):
    t1 = time.time()
    tmp_dict = {}
    for idx in range(len(data)):
    # for idx in range(0, 3):
        if idx % 100 == 0:
            print(sort_name, '已经完成：', idx / len(data) * 100, '%')
        for jdx in range(len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].replace(' ', '')
                curr_txt2 = data[jdx][1].replace(' ', '')
                leven_ratio_val = cal_similarity.ssim(curr_txt1, curr_txt2, model='Leven_ratio')
                difflib_val = cal_similarity.ssim(curr_txt1, curr_txt2, model='difflib')
                curr_str1 = data[idx][0] + ' ' + curr_txt1
                curr_str2 = data[jdx][0] + ' ' + curr_txt2
                ss = {}
                ss['Difflib: '] = difflib_val
                ss['str1'] = curr_str1
                ss['str2'] = curr_str2
                tmp_dict[leven_ratio_val] = ss
    # print(tmp_dict)
    top = sorted(tmp_dict.items(), key=lambda x: x[0], reverse=True)
    result_name = os.path.join('./difflib2leven3', sort_name + '_result.txt')
    with open(result_name, 'a', encoding='utf-8', newline='') as f:

        for tmp in top:
            if tmp[0]>0.5:
                f.write('Levenshtein_ratio: ' + str(tmp[0]) + '\n')
                f.write('Difflib: '+str(tmp[1]['Difflib: '])+ '\n')
                f.write('str1: '+tmp[1]['str1']+ '\n')
                f.write('str2: '+tmp[1]['str2']+ '\n')
                f.write('\n')


if __name__ == '__main__':
    print('start...')
    data_file_list = ['fill_in_blanks_data.csv','single_choice_data.csv','subjective_question_data.csv']
    for curr_file in data_file_list:
        data = read_data(curr_file)
        sort_by_Levenshtein_ratio(data,curr_file[:-4] +'_Leven&LCS')

    print('end...')




