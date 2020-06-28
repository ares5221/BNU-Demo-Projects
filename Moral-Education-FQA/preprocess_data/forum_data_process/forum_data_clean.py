#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''

生成问题-答案的数据集，及问题句子的npy wmbedding文件
'''
import csv
import xlrd
import os


def read_data():
    root_path = './../../'
    print(os.path.abspath(root_path))
    forum_data_path = os.path.join(root_path, 'raw_data/forum_data/问答数据导出_summary.xlsx')
    data = xlrd.open_workbook(forum_data_path)
    sheet = data.sheet_by_name('Sheet1')
    ques_content_id_dict = {}  # 用于存储问题-ID的字典

    for row_index in range(2, sheet.nrows):
        if sheet.cell(row_index, 0).value not in ques_content_id_dict:
            if sheet.cell(row_index, 2).value is not '':
                que_txt = sheet.cell(row_index, 2).value
            else:
                que_txt = sheet.cell(row_index, 1).value
                ques_content_id_dict[sheet.cell(row_index, 0).value] = que_txt
    print('共搜集到问题个数：', len(ques_content_id_dict))

    que_ans_list_dict = {}  # 用于存储问题-答案列表的字典
    for row_index in range(2, sheet.nrows):
        if sheet.cell(row_index, 0).value in ques_content_id_dict:
            # print(que_ans_list_dict[que_id_dict[sheet.cell(row_index, 0).value]])
            if ques_content_id_dict[sheet.cell(row_index, 0).value] not in que_ans_list_dict:
                ans_list = []
                # que_ans_list_dict[que_id_dict[sheet.cell(row_index, 0).value]] = ans_list
            else:
                ans_list = que_ans_list_dict[ques_content_id_dict[sheet.cell(row_index, 0).value]]

            ans_like_dict = {}  # {'ans demo1':4}存储答案文本及对应点赞数
            ans_txt = sheet.cell(row_index, 13).value  # ans_txt
            ans_like = sheet.cell(row_index, 14).value  # dian zan
            if ans_txt is not '':
                ans_like_dict[ans_txt] = ans_like

            if ans_like_dict:
                ans_list.append(ans_like_dict)
            que_ans_list_dict[ques_content_id_dict[sheet.cell(row_index, 0).value]] = ans_list

    print('start 筛选答案...')
    que_ans_list = []
    for que, answer_list in que_ans_list_dict.items():
        if len(answer_list) > 0:
            max_support = 0
            best_answer = ''
            for index in range(len(answer_list)):
                curr = answer_list[index]
                for key in curr:
                    if curr[key] > max_support:
                        best_answer = key
                        max_support = curr[key]
                    if curr[key] == max_support:
                        if len(key) > len(best_answer):
                            best_answer = key
                            max_support = curr[key]
            que_ans_list.append([que, best_answer])

    print('采集到问答数据共', len(que_ans_list), '存储数据...')
    question_sentences = []
    for q_a in que_ans_list:
        que = clean_str(q_a[0])
        ans = clean_str(q_a[1])
        question_sentences.append(que)
        with open('forum_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([que, ans])

    print('处理后的问答对数据保存在forum_data.csv文件中!!!!!')


def clean_str(str_ans):
    '''清理回答字符串中可能出现的html符号'''
    str_ans = str_ans.replace('??', '')
    str_ans = str_ans.replace('\n', '')
    return str_ans.replace('<br>', '')


if __name__ == '__main__':
    read_data()
