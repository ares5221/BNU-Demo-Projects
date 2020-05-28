# encoding:utf-8
import re
import os
import json
import time
import csv
import Levenshtein
import uuid

resutl_path = './../result/math_result0421/'
threshold_maximum = 0.95  # 描述阈值最大值
threshold_minimum = 0.8  # 描述阈值最小值
threshold_latex_maximum = 0.95  # 公式阈值最大值
threshold_latex_minimum = 0.8  # 公式阈值最小值

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


def cal_question_no_choice_or_answer(data, sort_name):
    # 两个题目都含有公式
    que_latex_str_pos = {}  # 两个题目的公式相似 描述相似或不确定 认定相似
    que_latex_str_neg = {}  # 两个题目的公式相似，描述不相似 认定不相似

    que_latex_notsure_str_pos = {}  # 两个题目的公式不确定 描述相似 认定相似
    que_latex_notsure_str_notsure = {}  # 两个题目的公式不确定 描述不确定 人工校验
    que_latex_notsure_str_neg = {}  # 两个题目的公式不确定 描述相似 认定不相似
    que_latex_neg = {}  # 两个题目的公式不相似 认定不相似

    que_latex_diff = {}  # 两个题目一个含有公式一个没有 人工校验

    # 两个题目都没有公式
    que_str_pos = {}  # 两个题目的描述相似 认定相似
    que_str_notsure = {}  # 两个题目的描述不确定 人工校验
    que_str_neg = {}  # 两个题目的描述不相似

    for idx in range(len(data)):
        if idx % 100 == 0:
            print(sort_name, '已经完成：', idx / len(data) * 100, '%')
        for jdx in range(idx, len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].replace(' ', '')
                curr_txt2 = data[jdx][1].replace(' ', '')
                curr_str1 = data[idx][0] + ' ' + curr_txt1
                curr_str2 = data[jdx][0] + ' ' + curr_txt2
                is_q1_latex, q1_latex_str, q1_str = is_Contain_Latex_Formula(curr_txt1)
                is_q2_latex, q2_latex_str, q2_str = is_Contain_Latex_Formula(curr_txt2)
                # 1两个题目都含有公式
                if is_q1_latex and is_q2_latex:
                    latex_simi_val = Levenshtein.ratio(q1_latex_str, q2_latex_str)
                    # 1.1若公式相似
                    if latex_simi_val >= threshold_latex_maximum:
                        que_stem_simi_val = Levenshtein.ratio(q1_str, q2_str)
                        # 1.1.1若题干描述部分也相似
                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                        que_desc_str_val = round(que_stem_simi_val, 4)
                        if que_stem_simi_val > threshold_maximum:
                            ss = {}
                            ss['que_desc_latex_val'] = que_desc_latex_val
                            ss['que_desc_str_val'] = que_desc_str_val
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            que_latex_str_pos[uuid.uuid1()] = ss
                        else:
                            ss = {}
                            ss['que_desc_latex_val'] = que_desc_latex_val
                            ss['que_desc_str_val'] = que_desc_str_val
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            que_latex_str_neg[uuid.uuid1()] = ss

                    elif latex_simi_val < threshold_latex_maximum and latex_simi_val > threshold_latex_minimum:
                        que_stem_simi_val = Levenshtein.ratio(q1_str, q2_str)
                        # 1.1.1若题干描述部分也相似
                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                        que_desc_str_val = round(que_stem_simi_val, 4)
                        if que_stem_simi_val > threshold_maximum:
                            ss = {}
                            ss['que_desc_latex_val'] = que_desc_latex_val
                            ss['que_desc_str_val'] = que_desc_str_val
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            que_latex_notsure_str_pos[uuid.uuid1()] = ss
                        elif que_stem_simi_val <= threshold_maximum and que_stem_simi_val > threshold_minimum:
                            ss = {}
                            ss['que_desc_latex_val'] = que_desc_latex_val
                            ss['que_desc_str_val'] = que_desc_str_val
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            que_latex_notsure_str_notsure[uuid.uuid1()] = ss
                        else:
                            ss = {}
                            ss['que_desc_latex_val'] = que_desc_latex_val
                            ss['que_desc_str_val'] = que_desc_str_val
                            ss['str1'] = curr_str1
                            ss['str2'] = curr_str2
                            que_latex_notsure_str_neg[uuid.uuid1()] = ss
                    else:
                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                        ss = {}
                        ss['que_desc_latex_val'] = que_desc_latex_val
                        ss['str1'] = curr_str1
                        ss['str2'] = curr_str2
                        que_latex_neg[uuid.uuid1()] = ss
                # 2若两个题干一个包含公式，一个不包含公式
                elif (is_q1_latex and not is_q2_latex) or (not is_q1_latex and is_q2_latex):
                    que_stem_simi_val = Levenshtein.ratio(q1_str, q2_str)
                    que_desc_val = round(que_stem_simi_val, 4)  # 保留四位小数
                    ss = {}
                    ss['que_desc_val'] = que_desc_val
                    ss['str1'] = curr_str1
                    ss['str2'] = curr_str2
                    que_latex_diff[uuid.uuid1()] = ss
                else:
                    que_stem_simi_val = Levenshtein.ratio(q1_str, q2_str)
                    que_desc_val = round(que_stem_simi_val, 4)  # 保留四位小数
                    if que_stem_simi_val > threshold_maximum:
                        ss = {}
                        ss['que_desc_val'] = que_desc_val
                        ss['str1'] = curr_str1
                        ss['str2'] = curr_str2
                        que_str_pos[uuid.uuid1()] = ss
                    elif que_stem_simi_val <= threshold_maximum and que_stem_simi_val > threshold_minimum:
                        ss = {}
                        ss['que_desc_val'] = que_desc_val
                        ss['str1'] = curr_str1
                        ss['str2'] = curr_str2
                        que_str_notsure[uuid.uuid1()] = ss
                    else:
                        ss = {}
                        ss['que_desc_val'] = que_desc_val
                        ss['str1'] = curr_str1
                        ss['str2'] = curr_str2
                        que_str_neg[uuid.uuid1()] = ss

    # 1 题干及选项都包含公式与字符描述
    sele_dict = [que_latex_str_pos, que_latex_notsure_str_pos, que_latex_notsure_str_notsure]
    for tmp_dict_idx in range(len(sele_dict)):
        top1 = sorted(sele_dict[tmp_dict_idx].items(), key=lambda x: x[1]['que_desc_latex_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '01两个题目的公式相似 描述相似或不确定 认定相似'
        elif tmp_dict_idx == 1:
            tmp_name = '02两个题目的公式不确定 描述相似 认定相似'
        elif tmp_dict_idx == 2:
            tmp_name = '03两个题目的公式不确定 描述不确定 人工校验'
        print(tmp_name, top1)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top1:
                if tmp[1]['que_desc_latex_val'] > threshold_save and tmp[1]['que_desc_str_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[1]['que_desc_latex_val']) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 3 题目一个有公式一个没有公式 及题目都没有的公式的情况
    sele_dict2 = [que_latex_diff, que_str_pos, que_str_notsure]
    for tmp_dict_idx in range(len(sele_dict2)):
        top2 = sorted(sele_dict2[tmp_dict_idx].items(), key=lambda x: x[1]['que_desc_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '04两个题目一个含有公式一个没有 人工校验'
        elif tmp_dict_idx == 1:
            tmp_name = '05两个题目都没有公式且描述相似 认定相似'
        elif tmp_dict_idx == 2:
            tmp_name = '06两个题目都没有公式且描述不确定 人工校验'
        print(tmp_name, top2)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top2:
                if tmp[1]['que_desc_val'] > threshold_save:
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')


def cal_question_with_choice_or_answer(data, sort_name):
    que_str_latex_choice_str_latex_pos = {}  # 题干公式相似0.95及以上 题干描述相似0.95及以上 选项公式相似0.95及以上 选项描述相似0.8以上，判定相似
    que_str_latex_choice_latex_str_neg = {}  # 题干公式相似0.95及以上 题干描述相似0.95及以上 选项公式相似0.95及以上 选项描述相似0.8及以下，判定不相似

    que_str_latex_choice_latex_notsure_str_pos = {}  # 题干公式相似0.95及以上 题干描述相似0.95及以上 选项公式不确定0.8-0.95， 选项描述相似0.95及以上，判定相似
    que_str_latex_choice_latex_notsure_str_notsure = {}  # 题干公式相似0.95及以上 题干描述相似0.95及以上 选项公式不确定0.8-0.95， 选项描述不确定0.8-0.95，人工判定
    que_str_latex_choice_latex_neg = {}  # 题干公式相似0.95及以上 题干描述相似0.95及以上 选项公式不相似0.8及以下，判定不相似

    que_str_latex_choice_str_latex_diff = {}  # 题干公式相似0.95及以上 题干描述相似0.95及以上 选项一个有公式一个没有需人工判定
    que_str_latex_choice_str_pos = {}  # 题干公式相似0.95及以上 题干描述相似0.95及以上  选项都没有公式且相同
    que_str_latex_choice_str_notsure = {}  # 题干公式相似0.95及以上 题干描述相似0.95及以上  选项都没有公式且不确定
    que_str_latex_choice_str_neg = {}  # 题干公式相似0.95及以上 题干描述相似0.95及以上  选项都没有公式且不相似

    que_latex_str_notsure_choice_latex_pos = {}  # 题干公式相似0.95及以上 题干描述不确定0.8-0.95 选项公式相似0.95及以上，判定相似
    que_latex_str_notsure_choice_latex_notsure = {}  # 题干公式相似0.95及以上 题干描述不确定0.8-0.95 选项公式不确定0.8-0.95，人工判定
    que_latex_str_notsure_choice_latex_neg = {}  # 题干公式相似0.95及以上 题干描述不确定0.8-0.95，选项公式不相似0.8及以下 ，判定不相似

    que_str_latex_neg = {}  # 题干公式相似0.95及以上 题干描述不相似0.8及以下 ，判定不相似(不需要保存)

    que_latex_notsure_str_pos_choice_latex_pos_str_pos = {}  # 题干公式0.8-0.95 题干描述相似0.95及以上 选项选项公式相似 选项描述相似 不确定，认为相似
    que_latex_notsure_str_pos_choice_latex_pos_str_neg = {}  # 题干公式0.8-0.95 题干描述相似0.95及以上 选项选项公式相似 选项描述不相似，不相似

    que_latex_notsure_str_pos_choice_latex_notsure_str_pos = {}  # 题干公式0.8-0.95 题干描述相似0.95及以上 选项选项公式不确定 选项描述相似，认为相似
    que_latex_notsure_str_pos_choice_latex_notsure_str_notsure = {}  # 题干公式0.8-0.95 题干描述相似0.95及以上 选项选项公式不确定 选项描述不确定，人工校验
    que_latex_notsure_str_pos_choice_latex_notsure_str_neg = {}  # 题干公式0.8-0.95 题干描述相似0.95及以上 选项选项公式不确定 选项描述不相似，不相似(不需要保存)

    que_latex_notsure_str_pos_choice_latex_neg = {}  # 题干公式0.8-0.95 题干描述相似0.95及以上 选项选项公式不相似，不相似(不需要保存)
    que_latex_notsure_str_pos_choice_str_pos = {}  # 题干公式0.8-0.95 题干描述相似0.95及以上  选项都没有公式且相同，认为相似
    que_latex_notsure_str_pos_choice_str_notsure = {}  # 题干公式0.8-0.95 题干描述相似0.95及以上  选项都没有公式且不确定，人工校验
    que_latex_notsure_str_pos_choice_str_neg = {}  # 题干公式0.8-0.95 题干描述相似0.95及以上  选项都没有公式且不相似(不需要保存)

    que_latex_notsure_str_notsure_choice_pos = {}  # 题干公式0.8-0.95 题干描述0.8-0.95  如选项描述及公式存在一个不相似，则认为不相似，否则人工校验
    que_latex_notsure_str_notsure_choice_neg = {}  # 题干公式0.8-0.95 题干描述0.8-0.95  如选项描述及公式存在一个不相似，则认为不相似，否则人工校验

    que_latex_diff = {}  # 题干中一个有公式一个没公式

    # 题干都没有公式的情况
    que_str_choice_str_latex_pos = {}  # 题干描述相似0.95及以上 选项公式相似0.95及以上 选项描述相似0.8以上，判定相似
    que_str_choice_latex_str_neg = {}  # 题干描述相似0.95及以上 选项公式相似0.95及以上 选项描述相似0.8及以下，判定不相似

    que_str_choice_latex_notsure_str_pos = {}  # 题干描述相似0.95及以上 选项公式0.8-0.95 选项描述相似0.95及以上，判定相似
    que_str_choice_latex_notsure_str_notsure = {}  # 题干描述相似0.95及以上 选项公式0.8-0.95 选项描述相似0.8-0.95，人工校验
    que_str_choice_latex_notsure_str_neg = {}  # 题干描述相似0.95及以上 选项公式0.8-0.95 选项描述相似0.8及以下，不相似

    que_str_choice_latex_diff = {}  # 题干描述相似0.95及以上 选项不同，一个有公式一个没有公式

    que_str_choice_str_pos = {}  # 题干描述相似0.95及以上 选项都没有公式且相同
    que_str_choice_str_notsure = {}  # 题干描述相似0.95及以上 选项都没有公式且不确定
    que_str_choice_str_neg = {}  # 题干描述相似0.95及以上 选项都没有公式且不相似

    que_str_notsure_choice_pos = {}  # 题干描述0.8-0.95 选项相似
    que_str_notsure_choice_notsure = {}  # 题干中字符不相似

    for idx in range(len(data)):
        if idx % 100 == 0:
            print(sort_name, '已经完成：', idx / len(data) * 100, '%')
        for jdx in range(idx, len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].split(' ', 1)
                curr_txt2 = data[jdx][1].split(' ', 1)
                if len(curr_txt1) == 2 and len(curr_txt2) == 2:  # 保证两个题目都含有题干与选项内容两部分
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
                        if latex_simi_val >= threshold_latex_maximum:
                            que_stem_simi_val = Levenshtein.ratio(q1_str, q2_str)
                            # 1.1.1若题干描述部分也相似
                            if que_stem_simi_val >= threshold_maximum:
                                # 1.1.1.1若选项都含有公式
                                if is_c1_latex and is_c2_latex:
                                    choice_latex_simi_val = Levenshtein.ratio(c1_latex_str, c2_latex_str)
                                    # 选项公式相似
                                    if choice_latex_simi_val >= threshold_latex_maximum:
                                        choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        choice_desc_str_val = round(choice_str_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        # 1.1.1.1.1比较选项的描述部分
                                        if choice_str_simi_val > threshold_minimum:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_str_latex_choice_str_latex_pos[uuid.uuid1()] = ss
                                        else:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_str_latex_choice_latex_str_neg[uuid.uuid1()] = ss
                                    # 选项公式不确定
                                    elif choice_latex_simi_val < threshold_latex_maximum and choice_latex_simi_val > threshold_latex_minimum:
                                        choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        choice_desc_str_val = round(choice_str_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        # 比较选项的描述部分
                                        if choice_str_simi_val >= threshold_maximum:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_str_latex_choice_latex_notsure_str_pos[uuid.uuid1()] = ss
                                        if choice_str_simi_val < threshold_maximum and choice_str_simi_val > threshold_minimum:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_str_latex_choice_latex_notsure_str_notsure[uuid.uuid1()] = ss
                                    # 公式不相似
                                    else:
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_latex_choice_latex_neg[uuid.uuid1()] = ss
                                # 若选项一个有公式一个没有公式
                                elif (is_c1_latex and not is_c2_latex) or (not is_c1_latex and is_c2_latex):
                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    ss = {}
                                    ss['que_desc_latex_val'] = que_desc_latex_val
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_latex_choice_str_latex_diff[uuid.uuid1()] = ss
                                # 若选项都没有公式
                                else:
                                    # 比较选项的描述部分
                                    choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)
                                    choice_desc_str_val = round(choice_str_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    if choice_str_simi_val >= threshold_maximum:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_latex_choice_str_pos[uuid.uuid1()] = ss
                                    elif choice_str_simi_val <= threshold_maximum and choice_str_simi_val > threshold_minimum:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_latex_choice_str_notsure[uuid.uuid1()] = ss
                                    else:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_latex_choice_str_neg[uuid.uuid1()] = ss
                            # 1.1.2若题干描述部分不确定
                            elif que_stem_simi_val < threshold_maximum and que_stem_simi_val > threshold_minimum:
                                choice_latex_simi_val = Levenshtein.ratio(c1_latex_str, c2_latex_str)
                                # 选项公式相似
                                if choice_latex_simi_val >= threshold_latex_maximum:
                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)
                                    choice_latex_simi_val = round(choice_latex_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    ss = {}
                                    ss['que_desc_latex_val'] = que_desc_latex_val
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['choice_desc_latex_val'] = choice_latex_simi_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_latex_str_notsure_choice_latex_pos[uuid.uuid1()] = ss
                                # 选项公式不确定
                                elif choice_latex_simi_val < threshold_latex_maximum and choice_latex_simi_val > threshold_latex_minimum:
                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)
                                    choice_latex_simi_val = round(choice_latex_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    ss = {}
                                    ss['que_desc_latex_val'] = que_desc_latex_val
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['choice_desc_latex_val'] = choice_latex_simi_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_latex_str_notsure_choice_latex_notsure[uuid.uuid1()] = ss
                                # 公式不相似
                                else:
                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)
                                    choice_latex_simi_val = round(choice_latex_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    ss = {}
                                    ss['que_desc_latex_val'] = que_desc_latex_val
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['choice_desc_latex_val'] = choice_latex_simi_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_latex_str_notsure_choice_latex_neg[uuid.uuid1()] = ss

                            # 1.1.3若题干公式相似，描述部分不相似
                            else:
                                que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                que_desc_str_val = round(que_stem_simi_val, 4)
                                curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                ss = {}
                                ss['que_desc_latex_val'] = que_desc_latex_val
                                ss['que_desc_str_val'] = que_desc_str_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                que_str_latex_neg[uuid.uuid1()] = ss
                        # 1.2若题干中的公式不确定
                        elif latex_simi_val < threshold_latex_maximum and latex_simi_val > threshold_latex_minimum:
                            que_stem_simi_val = Levenshtein.ratio(q1_str, q2_str)
                            # 1.2.1若题干描述部分相似
                            if que_stem_simi_val >= threshold_maximum:
                                # 1.2.1.1若选项都含有公式
                                if is_c1_latex and is_c2_latex:
                                    choice_latex_simi_val = Levenshtein.ratio(c1_latex_str, c2_latex_str)
                                    # 选项公式相似
                                    if choice_latex_simi_val >= threshold_latex_maximum:
                                        choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        choice_desc_str_val = round(choice_str_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        # 1.2.1.1.1比较选项的描述部分
                                        if choice_str_simi_val > threshold_minimum:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_latex_notsure_str_pos_choice_latex_pos_str_pos[uuid.uuid1()] = ss
                                        else:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_latex_notsure_str_pos_choice_latex_pos_str_neg[uuid.uuid1()] = ss
                                    # 选项公式不确定
                                    elif choice_latex_simi_val < threshold_latex_maximum and choice_latex_simi_val > threshold_latex_minimum:
                                        choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        choice_desc_str_val = round(choice_str_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        # 比较选项的描述部分
                                        if choice_str_simi_val >= threshold_maximum:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_latex_notsure_str_pos_choice_latex_notsure_str_pos[
                                                uuid.uuid1()] = ss
                                        if choice_str_simi_val < threshold_maximum and choice_str_simi_val > threshold_minimum:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_latex_notsure_str_pos_choice_latex_notsure_str_notsure[
                                                uuid.uuid1()] = ss
                                    # 公式不相似
                                    else:
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_latex_notsure_str_pos_choice_latex_neg[uuid.uuid1()] = ss
                                # 若选项一个有公式一个没有公式
                                elif (is_c1_latex and not is_c2_latex) or (not is_c1_latex and is_c2_latex):
                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    ss = {}
                                    ss['que_desc_latex_val'] = que_desc_latex_val
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_latex_choice_str_latex_diff[uuid.uuid1()] = ss
                                # 若选项都没有公式
                                else:
                                    # 比较选项的描述部分
                                    choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)
                                    choice_desc_str_val = round(choice_str_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    if choice_str_simi_val >= threshold_maximum:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_latex_notsure_str_pos_choice_str_pos[uuid.uuid1()] = ss
                                    elif choice_str_simi_val <= threshold_maximum and choice_str_simi_val > threshold_minimum:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_latex_notsure_str_pos_choice_str_notsure[uuid.uuid1()] = ss
                                    else:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_latex_notsure_str_pos_choice_str_neg[uuid.uuid1()] = ss
                            # 1.2.2若题干描述部分不确定
                            elif que_stem_simi_val > threshold_minimum and que_stem_simi_val < threshold_maximum:
                                if is_c1_latex and is_c2_latex:
                                    choice_latex_simi_val = Levenshtein.ratio(c1_latex_str, c2_latex_str)
                                    # 选项公式相似
                                    if choice_latex_simi_val >= threshold_latex_maximum:
                                        choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        choice_desc_str_val = round(choice_str_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        # 1.2.1.1.1比较选项的描述部分
                                        if choice_str_simi_val > threshold_minimum:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_latex_notsure_str_notsure_choice_pos[uuid.uuid1()] = ss
                                        else:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_latex_notsure_str_notsure_choice_neg[uuid.uuid1()] = ss
                                    # 选项公式不确定
                                    elif choice_latex_simi_val < threshold_latex_maximum and choice_latex_simi_val > threshold_latex_minimum:
                                        choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        choice_desc_str_val = round(choice_str_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        # 比较选项的描述部分
                                        if choice_str_simi_val >= threshold_maximum:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_latex_notsure_str_notsure_choice_pos[uuid.uuid1()] = ss
                                        if choice_str_simi_val < threshold_maximum and choice_str_simi_val > threshold_minimum:
                                            ss = {}
                                            ss['que_desc_latex_val'] = que_desc_latex_val
                                            ss['que_desc_str_val'] = que_desc_str_val
                                            ss['choice_desc_latex_val'] = choice_desc_latex_val
                                            ss['choice_desc_str_val'] = choice_desc_str_val
                                            ss['str1'] = curr_str1
                                            ss['str2'] = curr_str2
                                            que_latex_notsure_str_notsure_choice_pos[uuid.uuid1()] = ss
                                    # 公式不相似
                                    else:
                                        que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                        que_desc_str_val = round(que_stem_simi_val, 4)
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_latex_notsure_str_notsure_choice_neg[uuid.uuid1()] = ss
                                # 若选项一个有公式一个没有公式
                                elif (is_c1_latex and not is_c2_latex) or (not is_c1_latex and is_c2_latex):
                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    ss = {}
                                    ss['que_desc_latex_val'] = que_desc_latex_val
                                    ss['que_desc_str_val'] = que_desc_str_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_latex_choice_str_latex_diff[uuid.uuid1()] = ss
                                # 若选项都没有公式
                                else:
                                    # 比较选项的描述部分
                                    choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                    que_desc_latex_val = round(latex_simi_val, 4)  # 保留四位小数
                                    que_desc_str_val = round(que_stem_simi_val, 4)
                                    choice_desc_str_val = round(choice_str_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    if choice_str_simi_val >= threshold_maximum:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_latex_notsure_str_notsure_choice_pos[uuid.uuid1()] = ss
                                    elif choice_str_simi_val <= threshold_maximum and choice_str_simi_val > threshold_minimum:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_latex_notsure_str_notsure_choice_pos[uuid.uuid1()] = ss
                                    else:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_latex_val
                                        ss['que_desc_str_val'] = que_desc_str_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_latex_notsure_str_notsure_choice_neg[uuid.uuid1()] = ss
                            else:
                                pass
                        # 1.2若题干中的公式不相似
                        else:
                            pass
                    # 2若两个题干一个包含公式，一个不包含公式
                    elif (is_q1_latex and not is_q2_latex) or (not is_q1_latex and is_q2_latex):
                        que_simi_val = Levenshtein.ratio(q1_str, q2_str)
                        que_desc_latex_val = round(que_simi_val, 4)  # 保留四位小数
                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                        ss = {}
                        ss['que_desc_latex_val'] = que_desc_latex_val
                        ss['str1'] = curr_str1
                        ss['str2'] = curr_str2
                        que_latex_diff[uuid.uuid1()] = ss

                    # 3若两个题干都不包含公式
                    else:
                        que_desc_str_simi_val = Levenshtein.ratio(q1_str, q2_str)
                        # 若题目相似 需要比较选项
                        if que_desc_str_simi_val >= threshold_maximum:
                            # 若选项都含有公式，继续比较选项部分
                            if is_c1_latex and is_c2_latex:
                                choice_latex_simi_val = Levenshtein.ratio(c1_latex_str, c2_latex_str)
                                # 选项公式也相似
                                if choice_latex_simi_val >= threshold_latex_maximum:
                                    # 比较选项的非公式部分
                                    choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                    que_desc_str_simi_val = round(que_desc_str_simi_val, 4)
                                    choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                    choice_desc_str_val = round(choice_str_simi_val, 4)
                                    curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                    curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                    if choice_str_simi_val > threshold_minimum:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_str_simi_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_choice_str_latex_pos[uuid.uuid1()] = ss
                                    else:
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_str_simi_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_choice_latex_str_neg[uuid.uuid1()] = ss
                                # 选项公式不确定
                                elif choice_latex_simi_val < threshold_latex_maximum and choice_latex_simi_val > threshold_latex_minimum:
                                    choice_latex_simi_val = Levenshtein.ratio(c1_latex_str, c2_latex_str)
                                    # 选项公式相似
                                    if choice_latex_simi_val >= threshold_latex_maximum:
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        choice_desc_str_val = round(choice_str_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_str_simi_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_choice_latex_notsure_str_pos[uuid.uuid1()] = ss
                                    # 选项公式不确定
                                    elif choice_latex_simi_val < threshold_latex_maximum and choice_latex_simi_val > threshold_latex_minimum:
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        choice_desc_str_val = round(choice_str_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_str_simi_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_choice_latex_notsure_str_notsure[uuid.uuid1()] = ss
                                    # 公式不相似
                                    else:
                                        choice_desc_latex_val = round(choice_latex_simi_val, 4)
                                        choice_desc_str_val = round(choice_str_simi_val, 4)
                                        curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                        curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                        ss = {}
                                        ss['que_desc_latex_val'] = que_desc_str_simi_val
                                        ss['choice_desc_latex_val'] = choice_desc_latex_val
                                        ss['choice_desc_str_val'] = choice_desc_str_val
                                        ss['str1'] = curr_str1
                                        ss['str2'] = curr_str2
                                        que_str_choice_latex_notsure_str_neg[uuid.uuid1()] = ss
                                # 选项公式不同
                                else:
                                    pass
                            # 若选项一个有公式一个没有公式
                            elif (is_c1_latex and not is_c2_latex) or (not is_c1_latex and is_c2_latex):
                                que_desc_str_val = round(que_desc_str_simi_val, 4)
                                curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                ss = {}
                                ss['que_desc_latex_val'] = que_desc_str_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                que_str_choice_latex_diff[uuid.uuid1()] = ss
                            # 若选项都没有公式
                            else:
                                # 比较选项的字符部分
                                choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                                que_desc_str_val = round(que_desc_str_simi_val, 4)
                                choice_desc_str_val = round(choice_str_simi_val, 4)
                                curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                                curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                                if choice_str_simi_val >= threshold_maximum:
                                    ss = {}
                                    ss['que_desc_latex_val'] = que_desc_str_val
                                    ss['choice_desc_str_val'] = choice_desc_str_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_choice_str_pos[uuid.uuid1()] = ss
                                elif choice_str_simi_val <= threshold_maximum and choice_str_simi_val > threshold_minimum:
                                    ss = {}
                                    ss['que_desc_latex_val'] = que_desc_str_val
                                    ss['choice_desc_str_val'] = choice_desc_str_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_choice_str_notsure[uuid.uuid1()] = ss
                                else:
                                    ss = {}
                                    ss['que_desc_latex_val'] = que_desc_str_val
                                    ss['choice_desc_str_val'] = choice_desc_str_val
                                    ss['str1'] = curr_str1
                                    ss['str2'] = curr_str2
                                    que_str_choice_str_neg[uuid.uuid1()] = ss
                        # 若题目不确定
                        elif que_desc_str_simi_val < threshold_maximum and que_desc_str_simi_val > threshold_minimum:
                            # 比较选项的字符部分
                            choice_str_simi_val = Levenshtein.ratio(c1_str, c2_str)
                            que_desc_str_val = round(que_desc_str_simi_val, 4)
                            choice_desc_str_val = round(choice_str_simi_val, 4)
                            curr_str1 = data[idx][0] + ' ' + ques_stem1 + ' ' + choice_txt1
                            curr_str2 = data[jdx][0] + ' ' + ques_stem2 + ' ' + choice_txt2
                            if choice_str_simi_val >= threshold_maximum:
                                ss = {}
                                ss['que_desc_latex_val'] = que_desc_str_val
                                ss['choice_desc_str_val'] = choice_desc_str_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                que_str_notsure_choice_pos[uuid.uuid1()] = ss
                            elif choice_str_simi_val <= threshold_maximum and choice_str_simi_val > threshold_minimum:
                                ss = {}
                                ss['que_desc_latex_val'] = que_desc_str_val
                                ss['choice_desc_str_val'] = choice_desc_str_val
                                ss['str1'] = curr_str1
                                ss['str2'] = curr_str2
                                que_str_notsure_choice_notsure[uuid.uuid1()] = ss
                            else:
                                pass
                        # 若题目不相似
                        else:
                            pass

    # 1 题干及选项都包含公式与字符描述
    sele_dict = [que_str_latex_choice_str_latex_pos, que_str_latex_choice_latex_notsure_str_pos,
                 que_str_latex_choice_latex_notsure_str_notsure]
    for tmp_dict_idx in range(len(sele_dict)):
        top1 = sorted(sele_dict[tmp_dict_idx].items(), key=lambda x: x[1]['que_desc_latex_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '01题干公式相似0.95及以上 题干描述相似0.95及以上 选项公式相似0.95及以上 选项描述相似0.8以上 判定相似'
        elif tmp_dict_idx == 1:
            tmp_name = '02题干公式相似0.95及以上 题干描述相似0.95及以上 选项公式不确定0.8-0.95 选项描述相似0.95及以上 判定相似'
        elif tmp_dict_idx == 2:
            tmp_name = '03题干公式相似0.95及以上 题干描述相似0.95及以上 选项公式不确定0.8-0.95， 选项描述不确定0.8-0.95，人工校验'

        print(tmp_name, top1)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top1:
                if tmp[1]['que_desc_latex_val'] > threshold_save and tmp[1]['que_desc_str_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[1]['que_desc_latex_val']) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('选项公式相似度: ' + str(tmp[1]['choice_desc_latex_val']) + '\n')
                    f.write('选项描述相似度: ' + str(tmp[1]['choice_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 2 题干公式及描述相似,选项公式不确定相似及不相似及一个选项有公式一个没有公式
    sele_dict2 = [que_str_latex_choice_str_latex_diff]
    for tmp_dict_idx in range(len(sele_dict2)):
        top2 = sorted(sele_dict2[tmp_dict_idx].items(), key=lambda x: x[1]['que_desc_latex_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '04题干公式相似0.95及以上 题干描述相似0.95及以上 选项一个有公式一个没有需人工判定'
        print(tmp_name, top2)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top2:
                if tmp[1]['que_desc_latex_val'] > threshold_save and tmp[1]['que_desc_str_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[1]['que_desc_latex_val']) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 3 题目一个有公式一个没有公式 及题目都没有的公式的情况
    sele_dict3 = [que_latex_diff, que_str_choice_latex_diff, que_str_notsure_choice_pos]
    for tmp_dict_idx in range(len(sele_dict3)):
        top3 = sorted(sele_dict3[tmp_dict_idx].items(), key=lambda x: x[1]['que_desc_latex_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '15题干中一个有公式一个没公式 人工校验'
        elif tmp_dict_idx == 1:
            tmp_name = '19题干都没有公式且题干描述相似0.95及以上 选项不同一个有公式一个没有公式'
        elif tmp_dict_idx == 2:
            tmp_name = '22题干描述0.8-0.95不确定 选项相似 认为相似'
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top3:
                if tmp[1]['que_desc_latex_val'] > threshold_save:
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_latex_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 4 题干公式及描述相似,选项都没有公式
    sele_dict4 = [que_str_latex_choice_str_pos, que_str_latex_choice_str_notsure,
                  que_latex_notsure_str_pos_choice_str_pos,
                  que_latex_notsure_str_pos_choice_str_notsure, que_latex_notsure_str_notsure_choice_pos]
    for tmp_dict_idx in range(len(sele_dict4)):
        top4 = sorted(sele_dict4[tmp_dict_idx].items(), key=lambda x: x[1]['que_desc_latex_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '05题干公式相似0.95及以上 题干描述相似0.95及以上 选项描述相似 认定相似'
        elif tmp_dict_idx == 1:
            tmp_name = '06题干公式相似0.95及以上 题干描述相似0.95及以上 选项描述不确定 人工校验'
        elif tmp_dict_idx == 2:
            tmp_name = '12题干公式0.8-0.95 题干描述相似0.95及以上 选项都没有公式且描述相似 认定相似'
        elif tmp_dict_idx == 3:
            tmp_name = '13题干公式0.8-0.95 题干描述相似0.95及以上 选项都没有公式且描述不确定 人工校验'
        elif tmp_dict_idx == 4:
            tmp_name = '14题干公式不确认0.8-0.95 题干描述不确认0.8-0.95 判定相似的情况'
        print(tmp_name, top4)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top4:
                if tmp[1]['que_desc_latex_val'] > threshold_save and tmp[1]['que_desc_str_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[1]['que_desc_latex_val']) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('选项描述相似度: ' + str(tmp[1]['choice_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 5 题干公式相似，选项不确定
    sele_dict5 = [que_latex_str_notsure_choice_latex_pos, que_latex_str_notsure_choice_latex_notsure]
    for tmp_dict_idx in range(len(sele_dict5)):
        top5 = sorted(sele_dict5[tmp_dict_idx].items(), key=lambda x: x[1]['que_desc_latex_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '7题干公式相似0.95及以上 题干描述不确定0.8-0.95 选项公式相似0.95及以上，判定相似'
        elif tmp_dict_idx == 1:
            tmp_name = '8题干公式相似0.95及以上 题干描述不确定0.8-0.95 选项公式0.8-0.95不确定，人工校验'
        else:
            pass
        print(tmp_name, top5)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top5:
                if tmp[1]['que_desc_latex_val'] > threshold_save and tmp[1]['que_desc_str_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[1]['que_desc_latex_val']) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('选项公式相似度: ' + str(tmp[1]['choice_desc_latex_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 6 题干公式不确定
    sele_dict6 = [que_latex_notsure_str_pos_choice_latex_pos_str_pos,
                  que_latex_notsure_str_pos_choice_latex_notsure_str_pos,
                  que_latex_notsure_str_pos_choice_latex_notsure_str_notsure]
    for tmp_dict_idx in range(len(sele_dict6)):
        top6 = sorted(sele_dict6[tmp_dict_idx].items(), key=lambda x: x[1]['que_desc_latex_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '9题干公式0.8-0.95 题干描述相似0.95及以上 选项选项公式相似 选项描述相似 不确定，认为相似'
        if tmp_dict_idx == 1:
            tmp_name = '10题干公式0.8-0.95 题干描述相似0.95及以上 选项选项公式不确定 选项描述相似，认为相似'
        if tmp_dict_idx == 2:
            tmp_name = '11题干公式0.8-0.95 题干描述相似0.95及以上 选项选项公式不确定 选项描述不确定，人工校验'
        print(tmp_name, top6)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top6:
                if tmp[1]['que_desc_latex_val'] > threshold_save:
                    f.write('题干公式相似度: ' + str(tmp[1]['que_desc_latex_val']) + '\n')
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_str_val']) + '\n')
                    f.write('选项公式相似度: ' + str(tmp[1]['choice_desc_latex_val']) + '\n')
                    f.write('选项描述相似度: ' + str(tmp[1]['choice_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 7 题干不包含公式仅描述，选项公式相似
    sele_dict7 = [que_str_choice_str_latex_pos, que_str_choice_latex_notsure_str_pos,
                  que_str_choice_latex_notsure_str_notsure]
    for tmp_dict_idx in range(len(sele_dict7)):
        top7 = sorted(sele_dict7[tmp_dict_idx].items(), key=lambda x: x[1]['que_desc_latex_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '16题干描述相似0.95及以上 选项公式相似0.95及以上 选项描述相似0.8以上，判定相似'
        elif tmp_dict_idx == 1:
            tmp_name = '17题干描述相似0.95及以上 选项公式0.8-0.95 选项描述相似0.95及以上，判定相似'
        else:
            tmp_name = '18题干描述相似0.95及以上 选项公式0.8-0.95 选项描述相似0.8-0.95，人工校验'
        print(tmp_name, top7)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top7:
                if tmp[1]['que_desc_latex_val'] > threshold_save and tmp[1]['choice_desc_latex_val'] > threshold_save:
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_latex_val']) + '\n')
                    f.write('选项公式相似度: ' + str(tmp[1]['choice_desc_latex_val']) + '\n')
                    f.write('选项描述相似度: ' + str(tmp[1]['choice_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')

    # 8 题干仅为字符描述，选项公式不确定
    sele_dict8 = [que_str_choice_str_pos, que_str_choice_str_notsure]
    for tmp_dict_idx in range(len(sele_dict8)):
        top8 = sorted(sele_dict8[tmp_dict_idx].items(), key=lambda x: x[1]['que_desc_latex_val'], reverse=True)
        if tmp_dict_idx == 0:
            tmp_name = '20题干描述相似0.95及以上 选项都没有公式且相似 认为相似'
        elif tmp_dict_idx == 1:
            tmp_name = '21题干描述相似0.95及以上 选项都没有公式且不确定 人工校验'
        else:
            pass
        print(tmp_name, top8)
        similiarity_name = os.path.join(resutl_path, sort_name + '_' + tmp_name + '.txt')
        with open(similiarity_name, 'a', encoding='utf-8', newline='') as f:
            for tmp in top8:
                if tmp[1]['que_desc_latex_val'] > threshold_save:
                    f.write('题干描述相似度: ' + str(tmp[1]['que_desc_latex_val']) + '\n')
                    f.write('选项公式相似度: ' + str(tmp[1]['choice_desc_str_val']) + '\n')
                    f.write('str1: ' + tmp[1]['str1'] + '\n')
                    f.write('str2: ' + tmp[1]['str2'] + '\n')
                    f.write('\n')


def is_Contain_Latex_Formula(desc):
    pattern = re.compile(r'\\\((.+?)\\\)')  # 匹配latex
    latex_formula = pattern.findall(desc)
    split_res = pattern.split(desc)
    no_formula_str, formula_str = '', ''
    if latex_formula:
        for tmp in latex_formula:
            formula_str += tmp
            no_formula_str = desc.replace(tmp, '')

        return True, formula_str, no_formula_str
    else:
        return False, formula_str, desc


if __name__ == '__main__':
    print('start...')
    data_file_list = ['fill_in_blanks_data.csv', 'single_choice_data.csv',
                      'subjective_question_data.csv', 'no_choice_data.csv']
    for curr_file in data_file_list:
        data = read_data(curr_file)
        if curr_file == 'single_choice_data.csv' or curr_file=='fill_in_blanks_data.csv':
            # pass
            cal_question_with_choice_or_answer(data, curr_file[:-4] + '_')
        else:
            # pass
            cal_question_no_choice_or_answer(data, curr_file[:-4] + '_')

    print('end...')
