#!/usr/bin/env python
# _*_ coding:utf-8 _*_

'''
统计每个学科涉及的知识点包含的题目个数
如知识点ENK010101 包含200个题目
存储为excel 格式为
knowledge_code knowledge count
'''
import pymysql
import json


def get_answer_info(sub):
    result = {}
    # 打开数据库连接
    conn = pymysql.connect('172.18.136.94', 'readuser', 'gaojj2019', 'fep-tuoming')
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()  # 游标对象用于执行查询和获取结果
    # 使用execute()方法执行SQL，如果表存在则将其删除
    # cursor.execute(sql)
    # 查询当前学科的全部题目及其接受的答案 构建qid 和aid
    question_id_path = './../download_data_from_mysql/' + sub + '_clean_valid'
    for record in json.load(open(question_id_path, encoding='utf-8')):
        # curr_question_id = record['question_id']
        sql = 'SELECT * FROM t_partner_answer WHERE question_id = \'{}\' AND is_accepted=1'.format(
            record['question_id'])
        cursor.execute(sql)
        for x in cursor.fetchall():
            # 根据答案id获取该题目的知识点code
            curr_ans_id = x[0]
            sql2 = 'SELECT * FROM t_partner_answer_tag WHERE answer_id = \'{}\';'.format(curr_ans_id)
            cursor.execute(sql2)
            # 统计每个知识点包含多少题目
            for ans_tag in cursor.fetchall():
                curr_knowledge_code = ans_tag[2]
                if curr_knowledge_code not in result:
                    result[curr_knowledge_code] = 1
                else:
                    result[curr_knowledge_code] += 1
                print(ans_tag)

    print()

    json.dump(result, open(sub + '_kn_code_num', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)





def start():
    # 已经处理的科目包括cn 语文，ma 数学
    sub_list = ['cn', 'ma']
    for sub in sub_list:
        get_answer_info(sub)


if __name__ == '__main__':
    start()
    print('end...')