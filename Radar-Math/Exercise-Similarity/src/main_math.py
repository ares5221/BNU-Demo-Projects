# encoding:utf-8
import re
import os
import json
import time
import csv
import Levenshtein
import uuid

resutl_path = './../result/math_result0421/'

# 公式与描述阈值
formula_threshold = 0.5
str_threshold = 0.5
ans_threshold = 0.5
weight_val_dict = {'stem_formula': 10, 'stem_str': 5, 'sele_formula': 5, 'sele_str': 1, 'ans': 50, }
topK = 3


def read_data(path):
    data = []
    preprocess_path = './../data/preprocess_result_math'
    path = os.path.join(preprocess_path, path)
    with open(path, 'r', encoding='utf-8') as csv_read:
        reader = csv.reader(csv_read)
        for row in reader:
            data.append(row)
    return data[:]


def get_single_choice_similary_exercise(input_exercise, exercisebase_name):
    exercises_data = read_data(exercisebase_name)
    id_similarity_dict = {}
    for idx in range(len(exercises_data)):
        if idx % 300 == 0:
            print('题库数据比较已经完成：', idx / len(exercises_data) * 100, '%')
            # input_id = input_exercise[0]
            input_content = input_exercise
            curr_id = exercises_data[idx][0]
            curr_content = exercises_data[idx][1]
            # print(curr_id,curr_content)
            input_stem = input_content.split('###')[0]
            input_sele = input_content.split('###')[1]
            input_ans = input_content.split('###')[2]

            curr_stem = curr_content.split('###')[0]
            curr_sele = curr_content.split('###')[1]
            curr_ans = curr_content.split('###')[2]
            # 输入的题干公式 题干描述 选项公式 选项描述
            is_input_stem_contain_formula, input_stem_formula, input_stem_str = is_Contain_Latex_Formula(input_stem)
            is_input_sele_contain_formula, input_sele_formula, input_sele_str = is_Contain_Latex_Formula(input_sele)
            # 题库的题干公式 题干描述 选项公式 选项描述
            is_curr_stem_contain_formula, curr_stem_formula, curr_stem_str = is_Contain_Latex_Formula(curr_stem)
            is_curr_sele_contain_formula, curr_sele_formula, curr_sele_str = is_Contain_Latex_Formula(curr_sele)

            # 1两个题干含有公式
            if is_input_stem_contain_formula and is_curr_stem_contain_formula:
                # 1.1 选项都含有公式
                if is_input_sele_contain_formula and is_curr_sele_contain_formula:
                    stem_formula_similarity_value = Levenshtein.ratio(input_stem_formula, curr_stem_formula)
                    stem_str_similarity_value = Levenshtein.ratio(input_stem_str, curr_stem_str)
                    sele_formula_similarity_value = Levenshtein.ratio(input_sele_formula, curr_sele_formula)
                    sele_str_similarity_value = Levenshtein.ratio(input_sele_str, curr_sele_str)
                    ans_similarity_value = Levenshtein.ratio(input_ans, curr_ans)

                    # 各个部分均相似
                    if ans_similarity_value > ans_threshold and stem_formula_similarity_value > formula_threshold \
                            and stem_str_similarity_value > str_threshold and sele_formula_similarity_value > formula_threshold \
                            and sele_str_similarity_value > str_threshold:
                        ensemble_similarity = stem_formula_similarity_value * weight_val_dict['stem_formula'] + \
                                              stem_str_similarity_value * weight_val_dict['stem_str'] + \
                                              sele_formula_similarity_value * weight_val_dict['sele_formula'] + \
                                              sele_str_similarity_value * weight_val_dict['sele_str'] + \
                                              ans_similarity_value * weight_val_dict['ans']
                        id_similarity_dict[curr_id] = ensemble_similarity
                    else:
                        pass
                # 1.2 部分选项含有公式
                elif (is_input_sele_contain_formula and not is_curr_sele_contain_formula) or (
                        not is_input_sele_contain_formula and is_curr_sele_contain_formula):
                    stem_formula_similarity_value = Levenshtein.ratio(input_stem_formula, curr_stem_formula)
                    stem_str_similarity_value = Levenshtein.ratio(input_stem_str, curr_stem_str)
                    sele_similarity_value = Levenshtein.ratio(input_sele, curr_sele)
                    ans_similarity_value = Levenshtein.ratio(input_ans, curr_ans)
                    # 各个部分均相似
                    if ans_similarity_value > ans_threshold and stem_formula_similarity_value > formula_threshold \
                            and stem_str_similarity_value > str_threshold and sele_similarity_value > formula_threshold:
                        ensemble_similarity = stem_formula_similarity_value * weight_val_dict['stem_formula'] + \
                                              stem_str_similarity_value * weight_val_dict['stem_str'] + \
                                              sele_similarity_value * weight_val_dict['sele_str'] + \
                                              ans_similarity_value * weight_val_dict['ans']
                        id_similarity_dict[curr_id] = ensemble_similarity
                # 1.3 选项不含有公式
                else:
                    stem_formula_similarity_value = Levenshtein.ratio(input_stem_formula, curr_stem_formula)
                    stem_str_similarity_value = Levenshtein.ratio(input_stem_str, curr_stem_str)
                    sele_similarity_value = Levenshtein.ratio(input_sele, curr_sele)
                    ans_similarity_value = Levenshtein.ratio(input_ans, curr_ans)
                    # 各个部分均相似
                    if ans_similarity_value > ans_threshold and stem_formula_similarity_value > formula_threshold \
                            and stem_str_similarity_value > str_threshold and sele_similarity_value > formula_threshold:
                        ensemble_similarity = stem_formula_similarity_value * weight_val_dict['stem_formula'] + \
                                              stem_str_similarity_value * weight_val_dict['stem_str'] + \
                                              sele_similarity_value * weight_val_dict['sele_str'] + \
                                              ans_similarity_value * weight_val_dict['ans']
                        id_similarity_dict[curr_id] = ensemble_similarity

            # 2部分题干含有公式
            elif (is_input_stem_contain_formula and not is_curr_stem_contain_formula) or (
                    not is_input_stem_contain_formula and is_curr_stem_contain_formula):
                # 2.1 选项都含有公式
                if is_input_sele_contain_formula and is_curr_sele_contain_formula:
                    stem_similarity_value = Levenshtein.ratio(input_stem, curr_stem)
                    sele_formula_similarity_value = Levenshtein.ratio(input_sele_formula, curr_sele_formula)
                    sele_str_similarity_value = Levenshtein.ratio(input_sele_str, curr_sele_str)
                    ans_similarity_value = Levenshtein.ratio(input_ans, curr_ans)
                    # 各个部分均相似
                    if ans_similarity_value > ans_threshold and stem_similarity_value > formula_threshold \
                            and sele_formula_similarity_value > formula_threshold \
                            and sele_str_similarity_value > str_threshold:
                        ensemble_similarity = stem_similarity_value * weight_val_dict['stem_str'] + \
                                              sele_formula_similarity_value * weight_val_dict['sele_formula'] + \
                                              sele_str_similarity_value * weight_val_dict['sele_str'] + \
                                              ans_similarity_value * weight_val_dict['ans']
                        id_similarity_dict[curr_id] = ensemble_similarity
                    else:
                        pass
                # 2.2 部分选项含有公式
                elif (is_input_sele_contain_formula and not is_curr_sele_contain_formula) or (
                        not is_input_sele_contain_formula and is_curr_sele_contain_formula):
                    stem_similarity_value = Levenshtein.ratio(input_stem, curr_stem)
                    sele_similarity_value = Levenshtein.ratio(input_sele, curr_sele)
                    ans_similarity_value = Levenshtein.ratio(input_ans, curr_ans)
                    # 各个部分均相似
                    if ans_similarity_value > ans_threshold and stem_similarity_value > str_threshold and sele_similarity_value > formula_threshold:
                        ensemble_similarity = stem_similarity_value * weight_val_dict['stem_str'] + \
                                              sele_similarity_value * weight_val_dict['sele_str'] + \
                                              ans_similarity_value * weight_val_dict['ans']
                        id_similarity_dict[curr_id] = ensemble_similarity
                # 2.3 选项不含有公式
                else:
                    stem_similarity_value = Levenshtein.ratio(input_stem, curr_stem)
                    sele_similarity_value = Levenshtein.ratio(input_sele, curr_sele)
                    ans_similarity_value = Levenshtein.ratio(input_ans, curr_ans)
                    # 各个部分均相似
                    if ans_similarity_value > ans_threshold and stem_similarity_value > str_threshold and sele_similarity_value > formula_threshold:
                        ensemble_similarity = stem_similarity_value * weight_val_dict['stem_str'] + \
                                              sele_similarity_value * weight_val_dict['sele_str'] + \
                                              ans_similarity_value * weight_val_dict['ans']
                        id_similarity_dict[curr_id] = ensemble_similarity
            else:
                stem_similarity_value = Levenshtein.ratio(input_stem, curr_stem)
                sele_similarity_value = Levenshtein.ratio(input_sele, curr_sele)
                ans_similarity_value = Levenshtein.ratio(input_ans, curr_ans)
                # 各个部分均相似
                if ans_similarity_value > ans_threshold and stem_similarity_value > str_threshold and sele_similarity_value > formula_threshold:
                    ensemble_similarity = stem_similarity_value * weight_val_dict['stem_str'] + \
                                          sele_similarity_value * weight_val_dict['sele_str'] + \
                                          ans_similarity_value * weight_val_dict['ans']
                    id_similarity_dict[curr_id] = ensemble_similarity
                else:
                    pass

    # sort result
    tmp = sorted(id_similarity_dict.items(), key=lambda x: x[1], reverse=True)
    print(tmp)
    result_exercise = []
    if len(tmp) >= topK:
        for id_simi in tmp[:topK]:
            idx = id_simi[0]
            for ed in exercises_data:
                if ed[0] == idx:
                    result_exercise.append(ed[1])
    else:
        for id_simi in tmp:
            idx = id_simi[0]
            for ed in exercises_data:
                if ed[0] == idx:
                    result_exercise.append(ed[1])
    print('相似的题目为：', result_exercise)
    return result_exercise


def get_fill_in_blanks_similary_exercise(input_exercise, exercisebase_name):
    exercises_data = read_data(exercisebase_name)
    id_similarity_dict = {}
    for idx in range(len(exercises_data)):
        if idx % 300 == 0:
            print('题库数据比较已经完成：', idx / len(exercises_data) * 300, '%')
            # input_id = input_exercise[0]
            input_content = input_exercise
            curr_id = exercises_data[idx][0]
            curr_content = exercises_data[idx][1]
            print(curr_id, curr_content)
            input_stem = input_content.split('###')[0]
            input_ans = input_content.split('###')[1]

            curr_stem = curr_content.split('###')[0]
            curr_ans = curr_content.split('###')[1]
            # 输入的题干公式 题干描述
            is_input_stem_contain_formula, input_stem_formula, input_stem_str = is_Contain_Latex_Formula(input_stem)
            # 题库的题干公式 题干描述
            is_curr_stem_contain_formula, curr_stem_formula, curr_stem_str = is_Contain_Latex_Formula(curr_stem)

            # 1两个题干含有公式
            if is_input_stem_contain_formula and is_curr_stem_contain_formula:
                stem_formula_similarity_value = Levenshtein.ratio(input_stem_formula, curr_stem_formula)
                stem_str_similarity_value = Levenshtein.ratio(input_stem_str, curr_stem_str)
                ans_similarity_value = Levenshtein.ratio(input_ans, curr_ans)
                # 各个部分均相似
                if ans_similarity_value > ans_threshold and stem_formula_similarity_value > formula_threshold \
                        and stem_str_similarity_value > str_threshold:
                    ensemble_similarity = stem_formula_similarity_value * weight_val_dict['stem_formula'] + \
                                          stem_str_similarity_value * weight_val_dict['stem_str'] + \
                                          ans_similarity_value * weight_val_dict['ans']
                    id_similarity_dict[curr_id] = ensemble_similarity
                else:
                    pass
            # 2部分题干含有公式
            elif (is_input_stem_contain_formula and not is_curr_stem_contain_formula) or (
                    not is_input_stem_contain_formula and is_curr_stem_contain_formula):
                stem_similarity_value = Levenshtein.ratio(input_stem, curr_stem)
                ans_similarity_value = Levenshtein.ratio(input_ans, curr_ans)
                # 各个部分均相似
                if ans_similarity_value > ans_threshold and stem_similarity_value > formula_threshold:
                    ensemble_similarity = stem_similarity_value * weight_val_dict['stem_str'] + \
                                          ans_similarity_value * weight_val_dict['ans']
                    id_similarity_dict[curr_id] = ensemble_similarity
                else:
                    pass
            # 3题干均不含有公式
            else:
                stem_similarity_value = Levenshtein.ratio(input_stem, curr_stem)
                ans_similarity_value = Levenshtein.ratio(input_ans, curr_ans)
                # 各个部分均相似
                if ans_similarity_value > ans_threshold and stem_similarity_value > formula_threshold:
                    ensemble_similarity = stem_similarity_value * weight_val_dict['stem_str'] + \
                                          ans_similarity_value * weight_val_dict['ans']
                    id_similarity_dict[curr_id] = ensemble_similarity
                else:
                    pass
    # sort result
    tmp = sorted(id_similarity_dict.items(), key=lambda x: x[1], reverse=True)
    print(tmp)
    result_exercise = []
    if len(tmp) >= topK:
        for id_simi in tmp[:topK]:
            idx = id_simi[0]
            for ed in exercises_data:
                if ed[0] == idx:
                    result_exercise.append(ed[1])
    else:
        for id_simi in tmp:
            idx = id_simi[0]
            for ed in exercises_data:
                if ed[0] == idx:
                    result_exercise.append(ed[1])
    print('填空相似的题目为：', result_exercise)
    return result_exercise


def get_subjective_question_similary_exercise(input_exercise, exercisebase_name):
    exercises_data = read_data(exercisebase_name)
    id_similarity_dict = {}
    for idx in range(len(exercises_data)):
        if idx % 300 == 0:
            print('题库数据比较已经完成：', idx / len(exercises_data) * 300, '%')
            # input_id = input_exercise[0]
            input_content = input_exercise
            curr_id = exercises_data[idx][0]
            curr_content = exercises_data[idx][1]
            print(curr_id, curr_content)

            # 输入的题干公式 题干描述
            is_input_stem_contain_formula, input_stem_formula, input_stem_str = is_Contain_Latex_Formula(input_content)
            # 题库的题干公式 题干描述
            is_curr_stem_contain_formula, curr_stem_formula, curr_stem_str = is_Contain_Latex_Formula(curr_content)

            # 1两个题干含有公式
            if is_input_stem_contain_formula and is_curr_stem_contain_formula:
                stem_formula_similarity_value = Levenshtein.ratio(input_stem_formula, curr_stem_formula)
                stem_str_similarity_value = Levenshtein.ratio(input_stem_str, curr_stem_str)
                # 各个部分均相似
                if stem_formula_similarity_value > formula_threshold and stem_str_similarity_value > str_threshold:
                    ensemble_similarity = stem_formula_similarity_value * weight_val_dict['stem_formula'] + \
                                          stem_str_similarity_value * weight_val_dict['stem_str']
                    id_similarity_dict[curr_id] = ensemble_similarity
                else:
                    pass
            # 2部分题干含有公式
            elif (is_input_stem_contain_formula and not is_curr_stem_contain_formula) or (
                    not is_input_stem_contain_formula and is_curr_stem_contain_formula):
                stem_similarity_value = Levenshtein.ratio(input_content, curr_content)
                # 各个部分均相似
                if stem_similarity_value > formula_threshold:
                    ensemble_similarity = stem_similarity_value * weight_val_dict['stem_str']
                    id_similarity_dict[curr_id] = ensemble_similarity
                else:
                    pass
            # 3题干均不含有公式
            else:
                stem_similarity_value = Levenshtein.ratio(input_content, curr_content)
                # 各个部分均相似
                if stem_similarity_value > formula_threshold:
                    ensemble_similarity = stem_similarity_value * weight_val_dict['stem_str']
                    id_similarity_dict[curr_id] = ensemble_similarity
                else:
                    pass
    # sort result
    tmp = sorted(id_similarity_dict.items(), key=lambda x: x[1], reverse=True)
    print(tmp)
    result_exercise = []
    if len(tmp) >= topK:
        for id_simi in tmp[:topK]:
            idx = id_simi[0]
            for ed in exercises_data:
                if ed[0] == idx:
                    result_exercise.append(ed[1])
    else:
        for id_simi in tmp:
            idx = id_simi[0]
            for ed in exercises_data:
                if ed[0] == idx:
                    result_exercise.append(ed[1])
    print('主观题相似的题目为：', result_exercise)
    return result_exercise


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
    input_type = '单选'
    input_exercise = "1 如果一个命题的逆命题是真命题那么这个命题的###A、否命题必是真命题B、否命题必是假命题C、原命题必是假命题D、逆否命题必是真命题###A、否命题必是真命题"

    if input_type == '单选':
        get_single_choice_similary_exercise(input_exercise, 'single_choice_data.csv')
    if input_type == '填空':
        get_fill_in_blanks_similary_exercise(input_exercise, 'fill_in_blanks_data.csv')
    if input_type == '主观题':
        get_subjective_question_similary_exercise(input_exercise, 'subjective_question_data.csv')
    if input_type == '无选项题':
        get_subjective_question_similary_exercise(input_exercise, 'no_choice_data.csv')
    print('end...')
