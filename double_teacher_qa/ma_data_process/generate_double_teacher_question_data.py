#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import csv

def read_save_question_data():
    with open('double_teacher_math_question.csv', 'a', encoding='utf-8', newline='') as csv_write:
        csv_write = csv.writer(csv_write)
        with open('./double_teacher_math_ques_ans.csv', 'r',encoding='utf-8') as csv_read:
            reader = csv.reader(csv_read)
            for line in reader:
                print(line[0])
                print(line[1])





if __name__ =='__main__':
    read_save_question_data()