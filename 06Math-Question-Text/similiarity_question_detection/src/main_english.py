# encoding:utf-8

import os
import json
import time
import csv
import Levenshtein
import uuid
resutl_path = './../result/english_result0509/'
threshold_maximum = 0.95 #阈值大于0.9认为相似
threshold_minimum = 0.9  #阈值小于0.8认为不相似

# 用于无选项或者答案的题目及判断题的情况的阈值设定
threshold_maximum1 = 0.95 #阈值大于0.95认为相似
threshold_minimum2 = 0.9  #阈值小于0.8认为不相似

threshold_save = 0.5  #阈值小于0.5不保存

def read_data(path):
    data = []
    preprocess_path = './../data/preprocess_result_english'
    path = os.path.join(preprocess_path, path)
    with open(path, 'r', encoding='utf-8') as csv_read:
        reader = csv.reader(csv_read)
        for row in reader:
            data.append(row)
    return data[:]


def cal_question_no_choice_or_answer(data, sort_name):
    que_str_pos = {}
    que_str_notsure = {}
    for idx in range(len(data)):
        if idx % 100 == 0:
            print(sort_name, '已经完成：', idx / len(data) * 100, '%')
        for jdx in range(idx, len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1]
                curr_txt2 = data[jdx][1]
                que_str_simi_val = Levenshtein.ratio(curr_txt1, curr_txt2)
                que_str_simi_val = round(que_str_simi_val,4)
                curr_str1 = data[idx][0] + '-*-' + curr_txt1
                curr_str2 = data[jdx][0] + '-*-' + curr_txt2

                if que_str_simi_val >= threshold_maximum1:
                    ss = {}
                    ss['que_str_simi_val'] = que_str_simi_val
                    ss['str1'] = curr_str1
                    ss['str2'] = curr_str2
                    que_str_pos[uuid.uuid1()] = ss
                elif que_str_simi_val >threshold_minimum2 and que_str_simi_val <threshold_maximum1:
                    ss = {}
                    ss['que_str_simi_val'] = que_str_simi_val
                    ss['str1'] = curr_str1
                    ss['str2'] = curr_str2
                    que_str_notsure[uuid.uuid1()] = ss
                else:
                    pass

    sele_dict = [que_str_pos, que_str_notsure]
    # sele_dict = [que_str_pos]
    for tmp_dict_idx in range(len(sele_dict)):
        top1 = sorted(sele_dict[tmp_dict_idx].items(), key=lambda x: x[1]['que_str_simi_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '01题干描述相似0.9及以上 认为相似'
            # tmp_name = '英语题目比较'
        elif tmp_dict_idx == 1:
            tmp_name = '02题干描述不确定 人工校验'

        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top1:
                if tmp[1]['que_str_simi_val'] > threshold_save:
                    f.write('题干相似度: ' + str(tmp[1]['que_str_simi_val']) + '\n')
                    f.write('题目1的题干: ' + tmp[1]['str1'] + '\n')
                    f.write('题目2的题干: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')


def cal_question_with_choice_or_answer(data, sort_name):
    # 处理带答案或者选项的单选多选填空主观题
    que_str_pos_choice_pos = {}#题干描述相似0.9及以上 答案描述相似或者不确定，认为相似
    que_str_notsure_choice_pos = {}#题干描述不确定 答案描述相似 认为相似
    que_str_notsure_choice_notsure = {}#题干描述不确定 答案描述不确定 人工校验

    for idx in range(len(data)):
        if idx % 100 == 0:
            print(sort_name, '已经完成：', idx / len(data) * 100, '%')
        for jdx in range(idx, len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].split('$$$', 1)
                curr_txt2 = data[jdx][1].split('$$$', 1)
                if len(curr_txt1) == 2 and len(curr_txt2) == 2:
                    ques_stem1 = curr_txt1[0]
                    ques_stem2 = curr_txt2[0]
                    choice_txt1 = curr_txt1[1]
                    choice_txt2 = curr_txt2[1]
                    stem_leven_ratio_val = Levenshtein.ratio(ques_stem1, ques_stem2)
                    choice_leven_ratio_val = Levenshtein.ratio(choice_txt1, choice_txt2)
                    stem_leven_ratio_val = round(stem_leven_ratio_val, 4)  # 保留四位小数
                    choice_leven_ratio_val = round(choice_leven_ratio_val, 4)

                    curr_str1 = data[idx][0] + '-*-' + ques_stem1
                    curr_str2 = data[jdx][0] + '-*-' + ques_stem2
                    curr_str3 = choice_txt1
                    curr_str4 = choice_txt2
                    if stem_leven_ratio_val >=threshold_maximum:
                        if choice_leven_ratio_val >=threshold_minimum:
                            ss = {}
                            ss['que_str_simi_val'] = stem_leven_ratio_val
                            ss['choice_val'] = choice_leven_ratio_val
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            ss['str3'] = curr_str3
                            ss['str4'] = curr_str4
                            que_str_pos_choice_pos[uuid.uuid1()] = ss
                    elif stem_leven_ratio_val >threshold_minimum and stem_leven_ratio_val <threshold_maximum:
                        if choice_leven_ratio_val >= threshold_maximum:
                            ss = {}
                            ss['que_str_simi_val'] = stem_leven_ratio_val
                            ss['choice_val'] = choice_leven_ratio_val
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            ss['str3'] = curr_str3
                            ss['str4'] = curr_str4
                            que_str_notsure_choice_pos[uuid.uuid1()] = ss
                        elif choice_leven_ratio_val >threshold_minimum and choice_leven_ratio_val <threshold_maximum:
                            ss = {}
                            ss['que_str_simi_val'] = stem_leven_ratio_val
                            ss['choice_val'] = choice_leven_ratio_val
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            ss['str3'] = curr_str3
                            ss['str4'] = curr_str4
                            que_str_notsure_choice_notsure[uuid.uuid1()] = ss

    sele_dict = [que_str_pos_choice_pos, que_str_notsure_choice_pos,que_str_notsure_choice_notsure]
    # sele_dict = [que_str_pos_choice_pos]
    for tmp_dict_idx in range(len(sele_dict)):
        top1 = sorted(sele_dict[tmp_dict_idx].items(), key=lambda x: x[1]['que_str_simi_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '01题干描述相似0.95及以上 答案描述相似或者不确定，认为相似'
            # tmp_name = '英语题目比较'
        elif tmp_dict_idx == 1:
            tmp_name = '02题干描述不确定 答案描述相似 认为相似'
        elif tmp_dict_idx == 2:
            tmp_name = '03题干描述不确定 答案描述不确定 人工校验'
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top1:
                if tmp[1]['que_str_simi_val'] > threshold_save:
                    f.write('题干相似度: ' + str(tmp[1]['que_str_simi_val']) + '\n')
                    f.write('答案相似度: ' + str(tmp[1]['choice_val']) + '\n')
                    f.write('题目1的题干: ' + tmp[1]['str1'] + '\n')
                    f.write('题目2的题干: ' + tmp[1]['str2'] + '\n')
                    f.write('题目1的答案: ' + tmp[1]['str3'] + '\n')
                    f.write('题目2的答案: ' + tmp[1]['str4'] + '\n')
                    f.write('\n')


def cal_set_question(data, sort_name):
    # 处理带答案或者选项的单选多选填空主观题
    pos = {}  # 存储相似结果
    notsure = {}  # 存储不确定题目，需要人工校验

    for idx in range(len(data)):
        if idx % 100 == 0:
            print(sort_name, '已经完成：', idx / len(data) * 100, '%')
        for jdx in range(idx, len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].split('###')
                curr_txt2 = data[jdx][1].split('###')
                print(len(curr_txt1), len(curr_txt2),curr_txt1)
                if len(curr_txt1) == 3 and len(curr_txt2) == 3:
                    ques_cont1 = curr_txt1[0]
                    ques_cont2 = curr_txt2[0]
                    ques_stem1 = curr_txt1[1]
                    ques_stem2 = curr_txt2[1]
                    choice_txt1 = curr_txt1[2]
                    choice_txt2 = curr_txt2[2]
                    part1_leven_val = Levenshtein.ratio(ques_cont1, ques_cont2)
                    part2_leven_val = Levenshtein.ratio(ques_stem1, ques_stem2)
                    part3_leven_val = Levenshtein.ratio(choice_txt1, choice_txt2)
                    part1_leven_val = round(part1_leven_val, 4)  # 保留四位小数
                    part2_leven_val = round(part2_leven_val, 4)
                    part3_leven_val = round(part3_leven_val, 4)

                    curr_str1 = data[idx][0] + '-*-' + ques_cont1+ '-*-' + ques_stem1
                    curr_str2 = data[jdx][0] + '-*-' + ques_cont2+ '-*-' + ques_stem1
                    curr_str3 = choice_txt1
                    curr_str4 = choice_txt2
                    if part1_leven_val >= threshold_maximum:
                        if part2_leven_val >= threshold_maximum1:
                            if part3_leven_val >= threshold_minimum:
                                ss = {}
                                ss['part1'] = part1_leven_val
                                ss['part2'] = part2_leven_val
                                ss['part3'] = part3_leven_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                ss['str3'] = curr_str3
                                ss['str4'] = curr_str4
                                pos[uuid.uuid1()] = ss
                            else:
                                # 有一项小于0.9，认为不相似
                                pass
                        elif part2_leven_val > threshold_minimum and part2_leven_val < threshold_maximum:
                            if part3_leven_val >= threshold_maximum:
                                ss = {}
                                ss['part1'] = part1_leven_val
                                ss['part2'] = part2_leven_val
                                ss['part3'] = part3_leven_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                ss['str3'] = curr_str3
                                ss['str4'] = curr_str4
                                pos[uuid.uuid1()] = ss
                            elif part3_leven_val > threshold_minimum and part3_leven_val < threshold_maximum:
                                ss = {}
                                ss['part1'] = part1_leven_val
                                ss['part2'] = part2_leven_val
                                ss['part3'] = part3_leven_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                ss['str3'] = curr_str3
                                ss['str4'] = curr_str4
                                notsure[uuid.uuid1()] = ss
                            else:
                                # 有一项小于0.9，认为不相似
                                pass
                        else:
                            # 有一项小于0.9，认为不相似
                            pass
                    elif part1_leven_val >threshold_minimum and part1_leven_val<threshold_maximum1:
                        if part2_leven_val >=threshold_maximum:
                            if part3_leven_val >=threshold_maximum:
                                ss = {}
                                ss['part1'] = part1_leven_val
                                ss['part2'] = part2_leven_val
                                ss['part3'] = part3_leven_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                ss['str3'] = curr_str3
                                ss['str4'] = curr_str4
                                pos[uuid.uuid1()] = ss
                            elif part3_leven_val >threshold_minimum and part3_leven_val <threshold_maximum:
                                ss = {}
                                ss['part1'] = part1_leven_val
                                ss['part2'] = part2_leven_val
                                ss['part3'] = part3_leven_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                ss['str3'] = curr_str3
                                ss['str4'] = curr_str4
                                notsure[uuid.uuid1()] = ss
                            else:
                                pass
                        elif part2_leven_val >threshold_minimum and part2_leven_val <threshold_maximum:
                            if part3_leven_val >=threshold_minimum:
                                ss = {}
                                ss['part1'] = part1_leven_val
                                ss['part2'] = part2_leven_val
                                ss['part3'] = part3_leven_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                ss['str3'] = curr_str3
                                ss['str4'] = curr_str4
                                notsure[uuid.uuid1()] = ss
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass


    sele_dict = [pos, notsure]
    for tmp_dict_idx in range(len(sele_dict)):
        top1 = sorted(sele_dict[tmp_dict_idx].items(), key=lambda x: x[1]['que_str_simi_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '套题相似情况'
        elif tmp_dict_idx == 1:
            tmp_name = '套题不确定需人工校验'
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top1:
                if tmp[1]['part1'] > threshold_save:
                    f.write('套题内容相似度: ' + str(tmp[1]['part1']) + '\n')
                    f.write('套题题干相似度: ' + str(tmp[1]['part2']) + '\n')
                    f.write('套题选项/答案相似度: ' + str(tmp[1]['part3']) + '\n')
                    f.write('题目1的题干: ' + tmp[1]['str1'] + '\n')
                    f.write('题目2的题干: ' + tmp[1]['str2'] + '\n')
                    f.write('题目1的答案: ' + tmp[1]['str3'] + '\n')
                    f.write('题目2的答案: ' + tmp[1]['str4'] + '\n')
                    f.write('\n')


if __name__ == '__main__':
    print('start...')
    data_file_list = ['fill_in_blanks_data.csv', 'single_choice_data.csv',
                      'subjective_question_data.csv','judge_question_data.csv',
                      'no_choice_data.csv','set_question_data.csv']
    for curr_file in data_file_list:
        data = read_data(curr_file)
        if curr_file == 'single_choice_data.csv' or curr_file == 'fill_in_blanks_data.csv'\
                or curr_file =='subjective_question_data.csv' or curr_file=='judge_question_data.csv':
            # cal_question_with_choice_or_answer(data, curr_file[:-4] + '_')
            pass
        elif curr_file =='set_question_data.csv':
            cal_set_question(data, curr_file[:-4] + '_')
        else:
            pass
            # cal_question_no_choice_or_answer(data, curr_file[:-4] + '_')

    print('end...')
