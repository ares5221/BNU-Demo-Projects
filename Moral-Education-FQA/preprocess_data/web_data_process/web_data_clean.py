#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import docx
import csv


def read_data():
    root_path = './../../'
    print(os.path.abspath(root_path))
    web_data_path = os.path.join(root_path, 'raw_data/web_data/教育咨询师常见的10个经典问题解答.docx')

    file = docx.Document(web_data_path)
    data = []
    for p in file.paragraphs:
        print(p.text)
        data.append(p.text)
    print(len(data))

    for idx in range(0, len(data), 2):
        print(idx)
        ques_text = data[idx].split('、')[1]
        ans_text = data[idx + 1]
        with open('web_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([ques_text, ans_text])


if __name__ == '__main__':
    read_data()
