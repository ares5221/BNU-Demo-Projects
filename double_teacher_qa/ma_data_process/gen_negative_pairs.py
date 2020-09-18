#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import random
import csv


def read_data():
    print('随机选取问题，构造语义不相似的句子对')
    question_list = []
    with open('double_teacher_math_question.csv', 'r',encoding='utf-8') as csv_read:
        reader = csv.reader(csv_read)
        for line in reader:
            ques = line[0].split('\t')[1]
            # print(ques)
            if ques == 'ques':
                continue
            question_list.append(ques)
    print(len(question_list))
    return question_list

def gen_negative_pairs(data_list):
    count_start = 6332
    with open('negative_pairs.csv', 'a', encoding='utf-8', newline='') as csv_write:
        count = 0
        csv_write = csv.writer(csv_write)
        for idx in range(len(data_list)):
            random_ques = random.sample(data_list,2)
            csv_write.writerow([str(idx+count_start) + '\t' + random_ques[0] + '\t' + random_ques[1] + '\t' + str(0)])
            count +=1
            if count >5000:
                break


if __name__ =='__main__':
    question_list = read_data()
    gen_negative_pairs(question_list)
    print('generate negative data end!!!')