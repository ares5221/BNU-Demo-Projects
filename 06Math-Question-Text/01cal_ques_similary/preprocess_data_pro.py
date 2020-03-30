#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import xlrd
import csv
import re

base_dir = './preprocess_result_pro'

'''
不严格的文本预处理，对于含有img的，将img替换为空字符
'''
def get_data(data_path):
    workbook = xlrd.open_workbook(data_path)
    sheet = workbook.sheet_by_index(1)#索引的方式，从0开始
    # sheet = workbook.sheet_by_name('正常')#名字的方式
    print(sheet.name,sheet.nrows,sheet.ncols)#获取当前sheet页的名称，行数，列数，都从1开始
    id_idx = 0
    type_idx = 1 #题目类型

    single_choice_question = ['单选']
    fill_in_blanks_question = ['填空']
    subjective_question = ['主观题']
    all_type_question = ['单选','填空','主观题']
    for row in range(sheet.nrows):
        id = sheet.cell(row, id_idx).value
        if type(id) == float:# 是否是首行 header
            q_type = sheet.cell(row, type_idx).value
            if q_type in single_choice_question:
                process_single_choice(sheet, row,int(id))
            elif q_type in fill_in_blanks_question:
                process_fill_in_blanks(sheet, row,int(id))
            elif q_type in subjective_question:
                process_subjective(sheet, row,int(id))
            else:
                pass


def process_single_choice(sheet, row,id):
    '''
    处理单选题 题干一般很短，引入选项信息 若选项为img 则去除该题目
    :param sheet:curr sheet
    :param row:当前处理的行数
    :return:
    '''
    ques_desc_idx = 2  # 题干内容
    sele_desc_idx = 3  # 选项内容
    min_len = 2 # 题干最小长度
    with open(os.path.join(base_dir,'single_choice_data.csv'), 'a', encoding='utf-8',newline='') as csv_write:
        f_csv = csv.writer(csv_write)
        ques_desc = sheet.cell(row, ques_desc_idx).value
        sele_desc = sheet.cell(row,sele_desc_idx).value

        # is_text_ques_desc = is_text(ques_desc)
        # is_text_sele_desc = is_text(sele_desc)
        ques_desc = replace_img_str(ques_desc)
        sele_desc = replace_img_str(sele_desc)
        if True:
        # if is_text_ques_desc and is_text_sele_desc:
            ques_desc = clean_ques_desc(ques_desc)
            sele_desc = clean_select_desc(sele_desc)
            if len(ques_desc) > min_len:
                f_csv.writerow([id, ques_desc+sele_desc])


def process_fill_in_blanks(sheet, row,id):
    ques_desc_idx = 2  # 题干内容
    min_len = 2  # 题干最小长度
    with open(os.path.join(base_dir,'fill_in_blanks_data.csv'), 'a', encoding='utf-8', newline='') as csv_write:
        f_csv = csv.writer(csv_write)
        ques_desc = sheet.cell(row, ques_desc_idx).value

        ques_desc = replace_img_str(ques_desc)
        if True:
            ques_desc = clean_ques_desc(ques_desc)
            if len(ques_desc) > min_len:
                f_csv.writerow([id, ques_desc])

def process_subjective(sheet, row,id):
    ques_desc_idx = 2  # 题干内容
    min_len = 2  # 题干最小长度
    with open(os.path.join(base_dir,'subjective_question_data.csv'), 'a', encoding='utf-8', newline='') as csv_write:
        f_csv = csv.writer(csv_write)
        ques_desc = sheet.cell(row, ques_desc_idx).value

        ques_desc = replace_img_str(ques_desc)
        if True:
            ques_desc = clean_ques_desc(ques_desc)
            if len(ques_desc) > min_len:
                f_csv.writerow([id, ques_desc])


def clean_ques_desc(ques_desc):
    '''
    清理题干内容
    :param ques_desc:
    :return:
    '''
    # 1去除不合法字符
    ques_desc = ques_desc.replace('　', '').replace('\n', '')\
        .replace('　','').replace('_','').replace('□', '')\
        .replace('．','').replace('（）','').replace('()','').replace(' ','')
    # 2去除（   ）中文括号中多个空格情况
    ques_desc = re.sub(r'（\s+）', '（）', ques_desc)
    # 3去除(    )英文括号中多个空格情况
    ques_desc = re.sub(r'(\s+)', '（）', ques_desc)
    # pattern = re.compile(r'(\s+)')  # 查找数字
    # result1 = pattern.findall(ques_desc)
    # if result1:
    #     print('@@@@@@@@', ques_desc)
    # 4去除【教师题库】情况
    ques_desc = re.sub(r'【(.*?)】', '', ques_desc)
    # 5去除开头（2018九下广东中考）情况
    ques_desc = re.sub(r'^（(.*?)）', '', ques_desc)
    ques_desc = re.sub(r'^（(.*?)）', '', ques_desc)
    ques_desc = re.sub(r'^\((.*?)）', '', ques_desc)
    ques_desc = re.sub(r'^（(.*?)\)', '', ques_desc)
    ques_desc = re.sub(r'^\((.*?)\)', '', ques_desc)
    # 6去除题干末尾出现. 的情况
    if ques_desc.endswith('.') or ques_desc.endswith('。') or ques_desc.endswith('？') \
            or ques_desc.endswith('：') or ques_desc.endswith('?') or ques_desc.endswith(':'):
        ques_desc = ques_desc[:-1]

    return ques_desc


def clean_select_desc(sele_desc):
    '''
    清理选项内容
    :param sele_desc:
    :return:
    '''
    sele_desc = sele_desc.replace('\r\n','').replace('\n','').replace('\xa0','').replace(' ','')
    return sele_desc


def replace_img_str(curr):
    curr = re.sub(r'__img(.*?).(png|jpg|jpeg|bmp|gif)', '', curr)
    return curr

if __name__ == '__main__':
    print('start...')
    data_path = './../source_data/split.xls'
    get_data(data_path)
    print('end...')