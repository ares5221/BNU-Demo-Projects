#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import shutil
import random
import csv

before_shuffle_data_path = 'double_teacher_math_train_data.csv'
shuffle_data_path = './../bert_fine_tuning/data/math/'
def cpmpat_positive_negative():
    with open(before_shuffle_data_path, 'a',encoding='utf-8',newline='') as csv_write:
        csv_write = csv.writer(csv_write)
        with open('postive_pairs.csv', 'r',encoding='utf-8') as csv_read:
            reader = csv.reader(csv_read)
            for line in reader:
                csv_write.writerow(line)
        with open('negative_pairs.csv', 'r', encoding='utf-8') as csv_read2:
            reader2 = csv.reader(csv_read2)
            for line in reader2:
                csv_write.writerow(line)


def shuffle_data():
    print('开始shuffle数据')
    with open(shuffle_data_path+'train.csv', 'a',encoding='utf-8',newline='') as csv_write:
        csv_write = csv.writer(csv_write)
        data_list = []
        with open(before_shuffle_data_path, 'r',encoding='utf-8') as csv_read:
            reader = csv.reader(csv_read)
            for line in reader:
                data_list.append(line)
        print(data_list)
        print(random.shuffle(data_list))
        print(data_list)
        for tmp in data_list:
            csv_write.writerow(tmp)
    shutil.copyfile(shuffle_data_path+'train.csv', shuffle_data_path+'dev.csv')


def main():
    cpmpat_positive_negative()
    shuffle_data()


if __name__ =='__main__':
    main()
    print('end...')