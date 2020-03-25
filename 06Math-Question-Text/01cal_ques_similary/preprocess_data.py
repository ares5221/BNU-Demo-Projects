#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import xlrd
import csv
import re

def get_data(data_path):
    workbook = xlrd.open_workbook(data_path)
    sheet = workbook.sheet_by_index(1)#索引的方式，从0开始
    # sheet = workbook.sheet_by_name('正常')#名字的方式
    print(sheet.name,sheet.nrows,sheet.ncols)#获取当前sheet页的名称，行数，列数，都从1开始
    id_idx = 0
    ques_desc_idx = 2
    with open('data.csv', 'a', encoding='utf-8',newline='') as csv_write:
        f_csv = csv.writer(csv_write)
        for row in range(sheet.nrows):
            id = sheet.cell(row, id_idx).value
            ques_desc = sheet.cell(row,ques_desc_idx).value
            # print(id,ques_desc)
            # 是否是首行 header
            if type(id)== float:
                is_text_ques_desc = is_text(ques_desc)
                if is_text_ques_desc:

                    ques_desc = ques_desc.replace(' ','').replace('\n','')
                    f_csv.writerow([int(id),ques_desc])
            else:
                f_csv.writerow([id,ques_desc])


def is_text(curr):
    pattern = re.compile(r'(.*)__img(.*).png(.*)')  # 匹配非文本的img
    result = pattern.findall(curr)
    # print(result)
    if result:
        return False
    else:
        return True


if __name__ == '__main__':
    data_path = './../data/split.xls'
    get_data(data_path)