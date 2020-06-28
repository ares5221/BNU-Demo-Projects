#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import docx
import csv


def phrase_book_docx(path):
    document = docx.Document(path)
    ques_ans_dic = {}
    curr_ques = ''
    for paragraph in document.paragraphs:
        curr_type = paragraph.style.name
        curr_content = paragraph.text

        if curr_type != 'Normal':
            curr_ques = curr_content
            ques_ans_dic[curr_ques] = []
        else:
            ques_ans_dic[curr_ques].append(curr_content)
    # print(len(ques_ans_dic),ques_ans_dic)
    return ques_ans_dic


def formate_ques_ans_content(ques_ans_dic):
    clean_ques_ans_dic = {}
    for key, val in ques_ans_dic.items():
        key = key.split('.')[1]
        val = ''.join(val)
        print(key, val)
        clean_ques_ans_dic[key] = val
    return clean_ques_ans_dic


def save_book_data(ques_ans_dic):
    for key, val in ques_ans_dic.items():
        with open('book_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([key, val])


if __name__ == '__main__':
    path = './../../raw_data/book_data/book-work.docx'
    ques_ans_dic = phrase_book_docx(path)
    ques_ans_dic = formate_ques_ans_content(ques_ans_dic)
    save_book_data(ques_ans_dic)
