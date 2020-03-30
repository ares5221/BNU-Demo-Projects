#encoding:utf-8

import os
import cal_similarity
import json
import time
import csv


def read_data(path):
    data = []
    preprocess_path = './preprocess_result_pro'
    path = os.path.join(preprocess_path, path)
    with open(path, 'r', encoding='utf-8') as csv_read:
        reader = csv.reader(csv_read)
        for row in reader:
            data.append(row)
    return data[:]

def sort_by_difflib(data, sort_name):
    # print(len(data)) #3321
    # print(data[0])#['2', '如果一个命题的逆命题是真命题，那么这个命题的(\xa0\xa0\xa0)']
    # print(data[0][1])#如果一个命题的逆命题是真命题，那么这个命题的(   )
    t1 = time.time()
    tmp_dict = {}
    for idx in range(len(data)):
    # for idx in range(0,3):
        if idx % 100 == 0:
            print(sort_name,'已经完成：',idx/len(data) *100,'%')
        for jdx in range(len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].replace(' ','')
                curr_txt2 = data[jdx][1].replace(' ','')
                difflib_val = cal_similarity.ssim(curr_txt1,curr_txt2,model='difflib')
                Levenshtein_dist = cal_similarity.ssim(curr_txt1, curr_txt2, model='editdist')
                curr_str1 = data[idx][0] + ' '+  curr_txt1
                curr_str2 = data[jdx][0] + ' '+  curr_txt2
                tmp_dict['Levenshtein_dist: ' + str(Levenshtein_dist) + ' ' + curr_str1 + '<--->' + curr_str2] = difflib_val
    # print(tmp_dict)
    top = sorted(tmp_dict.items(), key=lambda x: x[1], reverse=True)
    result_name = os.path.join('./difflib2leven',sort_name+'_result.csv')
    with open(result_name,'a', encoding='utf-8',newline='') as csv_write:
        f_csv = csv.writer(csv_write)
        f_csv.writerow(['--------------The result of sort by %s ------------------' % sort_name])
        f_csv.writerow(['\tThe computing cost %.3f seconds' % (time.time() - t1)])
        f_csv.writerow(['相似值', '编辑距离及题目对及对应id'])
        for tmp in top:
            f_csv.writerow([tmp[1],tmp[0]])
        f_csv.writerow('\n\n')

def sort_by_Levenshtein_dist(data,sort_name):
    t1 = time.time()
    tmp_dict = {}
    for idx in range(len(data)):
    # for idx in range(0,3):
        if idx % 100 == 0:
            print(sort_name,'已经完成：',idx/len(data) *100,'%')
        for jdx in range(len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].replace(' ','')
                curr_txt2 = data[jdx][1].replace(' ','')
                leven_dist_val = cal_similarity.ssim(curr_txt1,curr_txt2,model='editdist')
                difflib_val = cal_similarity.ssim(curr_txt1, curr_txt2, model='difflib')
                curr_str1 = data[idx][0] + ' '+  curr_txt1
                curr_str2 = data[jdx][0] + ' '+  curr_txt2
                tmp_dict['difflib_value: ' + str(difflib_val) + ' ' + curr_str1 + '<--->' + curr_str2] = leven_dist_val
    # print(tmp_dict)
    top = sorted(tmp_dict.items(), key=lambda x: x[1], reverse=False)
    result_name = os.path.join('./difflib2leven',sort_name+'_result.csv')
    with open(result_name,'a', encoding='utf-8',newline='') as csv_write:
        f_csv = csv.writer(csv_write)
        f_csv.writerow(['--------------The result of sort by %s ------------------' % sort_name])
        f_csv.writerow(['\tThe computing cost %.3f seconds' % (time.time() - t1)])
        f_csv.writerow(['相似值', '编辑距离及题目对及对应id'])
        for tmp in top:
            f_csv.writerow([tmp[1],tmp[0]])
        f_csv.writerow('\n\n')


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
    result_name = os.path.join('./difflib2leven2', sort_name + '_result.csv')
    with open(result_name, 'a', encoding='utf-8', newline='') as csv_write:
        f_csv = csv.writer(csv_write)

        for tmp in top:
            if tmp[0]>0.5:
                f_csv.writerow(['Levenshtein_ratio: ' + tmp[0]])
                f_csv.writerow(['Difflib: '+tmp[1]['Difflib: ']])
                f_csv.writerow(['str1： '+tmp[1]['str1']])
                f_csv.writerow(['str2： '+tmp[1]['str2']])
                f_csv.writerow('\n')


if __name__ == '__main__':
    print('start...')
    data_file_list = ['fill_in_blanks_data.csv','single_choice_data.csv','subjective_question_data.csv']
    for curr_file in data_file_list:
        data = read_data(curr_file)
        # sort_by_difflib(data,curr_file +'_difflib')
        # sort_by_Levenshtein_dist(data,curr_file +'_Leven_dist')
        sort_by_Levenshtein_ratio(data,curr_file[:-4] +'_Leven&LCS')

    print('end...')




