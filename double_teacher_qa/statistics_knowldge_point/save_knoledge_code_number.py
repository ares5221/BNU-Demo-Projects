#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import pymysql
import xlsxwriter


def query_data(sub):
    result = []
    # 打开数据库连接
    conn = pymysql.connect('172.18.136.94', 'readuser', 'gaojj2019', 'fep-tuoming')
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()  # 游标对象用于执行查询和获取结果
    # 使用execute()方法执行SQL，如果表存在则将其删除
    # cursor.execute(sql)

    # 查询当前知识点code对应的知识点信息
    kn_code_path = './' + sub + '_kn_code_num'
    kn_num_dict = json.load(open(kn_code_path, encoding='utf-8'))
    for kn_code, num in kn_num_dict.items():
        print(kn_code, num)
        sql = 'SELECT * FROM t_knowledge WHERE knowledge_code = \'{}\';'.format(kn_code)
        cursor.execute(sql)
        for x in cursor.fetchall():
            # 根据答案id获取该题目的知识点code
            kn_name = x[1]
            print(kn_name)
            curr = [kn_code, kn_name, num]
            result.append(curr)
    return result


def save_excel(data,sub):
    workbook = xlsxwriter.Workbook(sub+'_知识点-题目数据统计表.xlsx')
    worksheet = workbook.add_worksheet(sub)
    title = ['知识点code','知识点信息','题目数量']
    for t_id in range(3):
        worksheet.write(0, t_id,title[t_id])
    for idx in range(len(data)):
        for jdx in range(3):
            worksheet.write(idx+1, jdx, data[idx][jdx])

    workbook.close()


if __name__ == '__main__':
    sub_list = ['cn', 'ma']
    for sub in sub_list:
        data = query_data(sub)
        save_excel(data, sub)