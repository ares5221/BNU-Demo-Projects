# encoding:utf-8
import re
import os
import json
import time
import csv
import Levenshtein

resutl_path = './../result/math_result0415/'
threshold_maximum = 0.95 #阈值大于0.95认为相似
threshold_minimum = 0.8  #阈值小于0.8认为不相似
threshold_latex_maximum = 0.8  #阈值小于0.8认为不相似
threshold_latex_minimum = 0.8  #阈值小于0.8认为不相似

threshold_save = 0.5

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
            if tmp[0] <= threshold_maximum and tmp[0] > threshold_minimum:
                f.write('Levenshtein_ratio: ' + str(tmp[0]) + '\n')
                f.write('str1: ' + tmp[1]['str1'] + '\n')
                f.write('str2: ' + tmp[1]['str2'] + '\n')
                f.write('\n')


def cal_single_choice_Levenshtein_ratio(data, sort_name):
    que_str_latex_choice_str_latex_pos = {} #题干及选项中的字符串及公式都相同
    que_str_latex_choice_latex_str_notsure = {} #题干中公式及字符相似 选项公式相似 选项字符不确定
    que_str_latex_choice_latex_str_neg = {} #题干中公式及字符相似 选项公式相似  选项字符不相似

    que_str_latex_choice_latex_notsure = {} #题干中公式及字符相似 选项公式不确定
    que_str_latex_choice_latex_neg = {} #题干中公式及字符相似 选项公式不相似

    que_str_latex_choice_str_latex_diff = {} #题干中公式及字符相似 选项不同，一个有公式一个没有公式

    que_str_latex_choice_str_pos = {} #题干中公式及字符相似 选项都没有公式且相同
    que_str_latex_choice_str_notsure = {} #题干中公式及字符相似 选项都没有公式且不确定
    que_str_latex_choice_str_neg = {} #题干中公式及字符相似 选项都没有公式且不相似

    que_str_latex_notsure = {}  # 题干中公式相同,字符部分不确定
    que_str_latex_neg = {}  # 题干中公式相同，字符不相似
    que_latex_notsure = {}  # 题干中公式不确定
    que_latex_neg = {}  # 题干中公式不相似

    que_latex_diff = {} # 题干中一个有公式一个没公式

    #题干都没有公式的情况
    que_str_choice_str_latex_pos = {}  # 题干字符串相同，选项的公式及字符串也相同
    que_str_choice_latex_str_notsure = {}  # 题干字符串相同，选项的公式相似及字符串不确定
    que_str_choice_latex_str_neg = {}  # 题干字符串相同，选项的公式相似及字符串不相似

    que_str_choice_latex_notsure = {}  # 题干中字符相似 选项公式不确定
    que_str_choice_latex_neg = {}  # 题干中字符相似 选项公式不相似

    que_str_choice_latex_diff = {}  # 题干中字符相似 选项不同，一个有公式一个没有公式

    que_str_choice_str_pos = {} #题干中字符相似 选项都没有公式且相同
    que_str_choice_str_notsure = {} #题干中字符相似 选项都没有公式且不确定
    que_str_choice_str_neg = {} #题干中字符相似 选项都没有公式且不相似

    que_str_notsure = {}  # 题干中字符部分不确定
    que_str_neg = {}  # 题干中字符不相似


    for idx in range(len(data)):
        if idx % 100 == 0:
            print(sort_name, '已经完成：', idx / len(data) * 100, '%')
        for jdx in range(idx, len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].split(' ', 1)
                curr_txt2 = data[jdx][1].split(' ', 1)
                if len(curr_txt1) == 2 and len(curr_txt2) == 2:#保证两个题目都含有题干与选项内容两部分
                    ques_stem1 = curr_txt1[0]
                    ques_stem2 = curr_txt2[0]
                    choice_txt1 = curr_txt1[1]
                    choice_txt2 = curr_txt2[1]
                    is_q1_latex, q1_latex_str, q1_str = is_Contain_Latex_Formula(ques_stem1)
                    is_q2_latex, q2_latex_str, q2_str = is_Contain_Latex_Formula(ques_stem2)
                    is_c1_latex, c1_latex_str, c1_str = is_Contain_Latex_Formula(choice_txt1)
                    is_c2_latex, c2_latex_str, c2_str = is_Contain_Latex_Formula(choice_txt2)
                    # 1若两个题干都包含公式
                    if is_q1_latex and is_q2_latex:
                        latex_simi_val = Levenshtein.ratio(q1_latex_str, q2_latex_str)
                        # 1.1若题干中的公式相似
                        if latex_simi_val > threshold_latex_maximum:
                            que_stem_simi_val = Levenshtein.ratio(q1_str,q2_str)
                            # 1.1.1若题干描述部分也相似
                            if que_stem_simi_val > threshold_maximum:
                                # 1.1.1.1若选项都含有公式
                                if is_c1_latex and is_c2_latex:
                                    choice_latex_simi_val = Levenshtein.ratio(c1_latex_str, c2_latex_str)
                                    # 1.1.1.1.1若选项公式相似
                                    if choice_latex_simi_val > threshold_latex_maximum:
                                        choice_str_simi_val = Levenshtein.ratio(c1_str,c2_str)
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        choice_desc_str_val = round(choice_str_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        # 1.1.1.1.1比较选项的描述部分
                                        if choice_str_simi_val > threshold_maximum:
                                            ss = {}
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_str_latex_choice_str_latex_pos[que_desc_latex_val] = ss
                                        elif choice_str_simi_val <= threshold_maximum and choice_str_simi_val >threshold_minimum:
                                            ss = {}
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_str_latex_choice_latex_str_notsure[que_desc_latex_val] = ss
                                        else:
                                            ss = {}
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_str_latex_choice_latex_str_neg[que_desc_latex_val] = ss
                                    # 选项公式不确定
                                    elif choice_latex_simi_val <= threshold_latex_maximum and choice_latex_simi_val > threshold_latex_minimum:
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)

                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        ss = {}
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_latex_choice_latex_notsure[que_desc_latex_val] = ss
                                    # 选项公式不同
                                    else:
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)

                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        ss = {}
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_latex_choice_latex_neg[que_desc_latex_val] = ss
                                # 若选项一个有公式一个没有公式
                                elif (is_c1_latex and not is_c2_latex) or (not is_c1_latex and is_c2_latex):
                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)

                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    ss = {}
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_latex_choice_str_latex_diff[que_desc_latex_val] = ss
                                # 若选项都没有公式
                                else:
                                    # 比较选项的字符部分
                                    choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)

                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)
                                    choice_desc_str_val = round(choice_str_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2

                                    if choice_str_simi_val > threshold_maximum:
                                        ss = {}
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_latex_choice_str_pos[que_desc_latex_val] = ss
                                    elif choice_str_simi_val <= threshold_maximum and choice_str_simi_val > threshold_minimum:
                                        ss = {}
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_latex_choice_str_notsure[que_desc_latex_val] = ss
                                    else:
                                        ss = {}
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_latex_choice_str_neg[que_desc_latex_val] = ss

                            elif que_stem_simi_val <= threshold_maximum and que_stem_simi_val >threshold_minimum:
                                que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                que_desc_str_val = round(que_stem_simi_val, 4)

                                curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                ss = {}
                                ss['que_desc_str_val'] = que_desc_str_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                que_str_latex_notsure[que_desc_latex_val] = ss

                            else:
                                que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                que_desc_str_val = round(que_stem_simi_val, 4)
                                curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                ss = {}
                                ss['que_desc_str_val'] = que_desc_str_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                que_str_latex_neg[que_desc_latex_val] = ss

                        elif latex_simi_val <= threshold_latex_maximum and latex_simi_val >threshold_latex_minimum:
                            que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                            curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                            curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                            ss = {}
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            que_latex_notsure[que_desc_latex_val] = ss
                        else:
                            que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                            curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                            curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                            ss = {}
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            que_latex_neg[que_desc_latex_val] = ss

                    # 2若两个题干一个包含公式，一个不包含公式
                    elif (is_q1_latex and not is_q2_latex) or (not is_q1_latex and is_q2_latex):
                        que_simi_val = Levenshtein.ratio(q1_str, q2_str)
                        que_desc_latex_val = round(que_simi_val, 4)  # 保留四位小数
                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                        ss = {}
                        ss['str1'] = curr_str1
                        ss['str2'] = curr_str2
                        que_latex_diff[que_desc_latex_val] = ss

                    # 3若两个题干都不包含公式
                    else:
                        que_desc_str_simi_val = Levenshtein.ratio(q1_str,q2_str)
                        # 若题目相似 需要比较选项
                        if que_desc_str_simi_val >threshold_maximum:
                            # 若选项都含有公式，继续比较选项部分
                            if is_c1_latex and is_c2_latex:
                                choice_latex_simi_val = Levenshtein.ratio(c1_latex_str, c2_latex_str)
                                # 选项公式也相似
                                if choice_latex_simi_val > threshold_latex_maximum:
                                    # 比较选项的非公式部分
                                    choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                    que_desc_str_simi_val = round(que_desc_str_simi_val, 4)
                                    choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                    choice_desc_str_val = round(choice_str_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2

                                    if choice_str_simi_val > threshold_maximum:
                                        ss = {}
                                        ss['que_desc_str_val'] = que_desc_str_simi_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_choice_str_latex_pos[que_desc_latex_val] = ss
                                    elif choice_str_simi_val <= threshold_maximum and choice_str_simi_val > threshold_minimum:
                                        ss = {}
                                        ss['que_desc_str_val'] = que_desc_str_simi_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_choice_latex_str_notsure[que_desc_latex_val] = ss
                                    else:
                                        ss = {}
                                        ss['que_desc_str_val'] = que_desc_str_simi_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_choice_latex_str_neg[que_desc_latex_val] = ss
                                # 选项公式不确定
                                elif choice_latex_simi_val <= threshold_latex_maximum and choice_latex_simi_val > threshold_latex_minimum:
                                    que_desc_str_val = round(que_desc_str_simi_val, 4)
                                    choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    ss = {}
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['choice_desc_latex_val'] = choice_desc_latex_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_choice_latex_notsure[que_desc_latex_val] = ss
                                # 选项公式不同
                                else:
                                    que_desc_str_val = round(que_desc_str_simi_val, 4)
                                    choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    ss = {}
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['choice_desc_latex_val'] = choice_desc_latex_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_choice_latex_neg[que_desc_latex_val] = ss
                            # 若选项一个有公式一个没有公式
                            elif (is_c1_latex and not is_c2_latex) or (not is_c1_latex and is_c2_latex):
                                que_desc_str_val = round(que_desc_str_simi_val, 4)
                                curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                ss = {}
                                ss['que_desc_str_val'] = que_desc_str_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                que_str_choice_latex_diff[que_desc_latex_val] = ss
                            # 若选项都没有公式
                            else:
                                # 比较选项的字符部分
                                choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                que_desc_str_val = round(que_desc_str_simi_val, 4)
                                choice_desc_str_val = round(choice_str_simi_val, 4)
                                curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2

                                if choice_str_simi_val > threshold_maximum:
                                    ss = {}
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['choice_desc_str_val'] = choice_desc_str_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_choice_str_pos[que_desc_latex_val] = ss
                                elif choice_str_simi_val <= threshold_maximum and choice_str_simi_val > threshold_minimum:
                                    ss = {}
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['choice_desc_str_val'] = choice_desc_str_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_choice_str_notsure[que_desc_latex_val] = ss
                                else:
                                    ss = {}
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['choice_desc_str_val'] = choice_desc_str_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_choice_str_neg[que_desc_latex_val] = ss
                        elif que_desc_str_simi_val <=threshold_maximum and que_desc_str_simi_val >threshold_minimum:
                            que_desc_str_simi_val = round(que_desc_str_simi_val, 4)  # 保留四位小数
                            curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                            curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                            ss = {}
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            que_str_notsure[que_desc_str_simi_val] = ss
                        else:
                            que_desc_str_simi_val = round(que_desc_str_simi_val, 4)  # 保留四位小数
                            curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                            curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                            ss = {}
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            que_str_neg[que_desc_str_simi_val] = ss

    # 1 题干及选项都包含公式与字符描述
    sele_dict = [que_str_latex_choice_str_latex_pos, que_str_latex_choice_latex_str_notsure
        ,que_str_latex_choice_latex_str_neg]
    for tmp_dict_idx in range(len(sele_dict)):
        top1 = sorted(sele_dict[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干及选项的公式及描述均相似'
        elif tmp_dict_idx == 1:
            tmp_name = '题干的公式及描述相似，选项的公式相似，描述不确定相似'
        else:
            tmp_name = '题干的公式及描述相似，选项的公式相似，描述不相似'
        print(tmp_name, top1)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' +tmp_name +'.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top1:
                if tmp[0] > threshold_save and tmp[1]['que_desc_str_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[0]) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('选项公式相似度: ' + str(tmp[1]['choice_desc_latex_val']) + '\n')
                    f.write('选项描述相似度: ' + str(tmp[1]['choice_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 2 题干公式及描述相似,选项公式不确定相似
    sele_dict2 = [que_str_latex_choice_latex_notsure,que_str_latex_choice_latex_neg]
    for tmp_dict_idx in range(len(sele_dict2)):
        top2 = sorted(sele_dict2[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干公式及描述相似,选项公式不确定相似'
        if tmp_dict_idx == 1:
            tmp_name = '题干的公式及描述相似，选项公式不相似'
        print(tmp_name,top2)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top2:
                if tmp[0] > threshold_save and tmp[1]['que_desc_str_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[0]) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 3 题干公式及描述相似,一个有选项公式一个没有选项公式
    sele_dict3 = [que_str_latex_choice_str_latex_diff]
    for tmp_dict_idx in range(len(sele_dict3)):
        top3 = sorted(sele_dict3[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干公式及描述相似,其中只有一个选包含选项公式'

        print(tmp_name,top3)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top3:
                if tmp[0] > threshold_save and tmp[1]['que_desc_str_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[0]) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 4 题干公式及描述相似,选项都没有公式
    sele_dict4 = [que_str_latex_choice_str_pos,que_str_latex_choice_str_notsure,que_str_latex_choice_str_neg]
    for tmp_dict_idx in range(len(sele_dict4)):
        top4 = sorted(sele_dict4[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干公式及描述相似,选项不包含公式，选项描述相似'
        if tmp_dict_idx == 1:
            tmp_name = '题干公式及描述相似,选项不包含公式，选项描述不确定'
        if tmp_dict_idx == 2:
            tmp_name = '题干公式及描述相似,选项不包含公式，选项描述不相似'
        print(tmp_name, top4)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top4:
                if tmp[0] > threshold_save and tmp[1]['que_desc_str_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[0]) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('选项描述相似度: ' + str(tmp[1]['choice_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 5 题干公式相似
    sele_dict5 = [que_str_latex_notsure,que_str_latex_neg]
    for tmp_dict_idx in range(len(sele_dict5)):
        top5 = sorted(sele_dict5[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干公式相似，题干描述不确定'
        if tmp_dict_idx == 1:
            tmp_name = '题干公式相似，题干描述不相似'
        if tmp_dict_idx == 2:
            tmp_name = '题干公式及描述相似,选项不包含公式，选项描述不相似'
        print(tmp_name, top5)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top5:
                if tmp[0] > threshold_save and tmp[1]['que_desc_str_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[0]) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 6 题干公式不确定与不相似
    sele_dict6 = [que_latex_notsure,que_latex_neg,que_latex_diff]
    for tmp_dict_idx in range(len(sele_dict6)):
        top6 = sorted(sele_dict6[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干公式不确定'
        if tmp_dict_idx == 1:
            tmp_name = '题干公式不相似'
        if tmp_dict_idx ==2:
            tmp_name = '两个题目的题干一个有公式一个没公式'
        print(tmp_name, top6)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top6:
                if tmp[0] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[0]) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 7 题干仅为字符描述，选项公式相似
    sele_dict7 = [que_str_choice_str_latex_pos, que_str_choice_latex_str_notsure,que_str_choice_latex_str_neg]
    for tmp_dict_idx in range(len(sele_dict7)):
        top7 = sorted(sele_dict7[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干描述相似，选项的公式相似，描述均相似'
        elif tmp_dict_idx == 1:
            tmp_name = '题干描述相似，选项的公式相似，描述不确定相似'
        else:
            tmp_name = '题干描述相似，选项的公式相似，描述不相似'
        print(tmp_name, top7)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' +tmp_name +'.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top7:
                if tmp[0] > threshold_save and tmp[1]['choice_desc_latex_val'] > threshold_save:
                    f.write('题干描述相似度: ' + str(tmp[0]) + '\n')
                    f.write('选项公式相似度: ' + str(tmp[1]['choice_desc_latex_val']) + '\n')
                    f.write('选项描述相似度: ' + str(tmp[1]['choice_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 8 题干仅为字符描述，选项公式不确定
    sele_dict8 = [que_str_choice_latex_notsure, que_str_choice_latex_neg]
    for tmp_dict_idx in range(len(sele_dict8)):
        top8 = sorted(sele_dict8[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干描述相似，选项的公式不确定'
        elif tmp_dict_idx == 1:
            tmp_name = '题干描述相似，选项的公式不相似'
        else:
            pass
        print(tmp_name, top8)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' +tmp_name +'.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top8:
                if tmp[0] > threshold_save :
                    f.write('题干描述相似度: ' + str(tmp[0]) + '\n')
                    f.write('选项公式相似度: ' + str(tmp[1]['choice_desc_latex_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 9 题干仅为字符描述，选项一个有公式一个没公式
    sele_dict9 = [que_str_choice_latex_diff,]
    for tmp_dict_idx in range(len(sele_dict9)):
        top9 = sorted(sele_dict9[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干描述相似，选项一个有公式，一个没公式'
        elif tmp_dict_idx == 1:
            pass
        else:
            pass
        print(tmp_name, top9)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' +tmp_name +'.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top9:
                if tmp[0] > threshold_save :
                    f.write('题干描述相似度: ' + str(tmp[0]) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 10 题干仅为字符描述，选项都没公式
    sele_dict10 = [que_str_choice_str_pos,que_str_choice_str_notsure, que_str_choice_str_neg]
    for tmp_dict_idx in range(len(sele_dict10)):
        top10 = sorted(sele_dict10[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干描述相似，选项描述相似'
        elif tmp_dict_idx == 1:
            tmp_name = '题干描述相似，选项描述不确定'
        else:
            tmp_name = '题干描述相似，选项描述不相似'
        print(tmp_name, top10)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' +tmp_name +'.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top10:
                if tmp[0] > threshold_save:
                    f.write('题干描述相似度: ' + str(tmp[0]) + '\n')
                    f.write('选项描述相似度: ' + str(tmp[1]['choice_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 11 题干描述不确定及不相似
    sele_dict11 = [que_str_notsure,que_str_neg]
    for tmp_dict_idx in range(len(sele_dict11)):
        top11 = sorted(sele_dict11[tmp_dict_idx].items(), key=lambda x: x[0], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '题干描述不确定'
        elif tmp_dict_idx == 1:
            tmp_name = '题干描述不相似'
        else:
            pass
        print(tmp_name, top11)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' +tmp_name +'.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top11:
                if tmp[0] > threshold_save:
                    f.write('题干描述相似度: ' + str(tmp[0]) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')


def is_Contain_Latex_Formula(desc):
    pattern = re.compile(r'\\\((.+?)\\\)')  # 匹配latex
    latex_formula = pattern.findall(desc)
    split_res = pattern.split(desc)
    no_formula_str, formula_str = '',''
    if latex_formula:
        for tmp in latex_formula:
            formula_str += tmp
            no_formula_str = desc.replace(tmp,'')

        return True, formula_str,no_formula_str
    else:
        return False, formula_str, desc



if __name__ == '__main__':
    print('start...')
    data_file_list = ['fill_in_blanks_data.csv', 'single_choice_data.csv', 'subjective_question_data.csv']
    for curr_file in data_file_list:
        data = read_data(curr_file)
        if curr_file == 'single_choice_data.csv':
            cal_single_choice_Levenshtein_ratio(data, curr_file[:-4] + '_')
        else:
            pass
            # cal_blank_subj_Levenshtein_ratio(data, curr_file[:-4] + '_')

    print('end...')
