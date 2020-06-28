#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import re

from bert_serving.client import BertClient
import os
import numpy as np
import csv
import Levenshtein

root_path = os.path.abspath('./../data/')
filePath = root_path + '/moral_fqa_data.csv'


def cosine_similarity(vector1, vector2):
    '''计算余弦相似度'''
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0
    else:
        return round(dot_product / ((normA ** 0.5) * (normB ** 0.5)), 2)


def getBestAnswer(qdata):
    '''
    todo 增加判断编辑距离的方法，用来判断是否相同问题，对于不相同的继续找相似问题
    :param qdata:
    :return:
    '''
    most_similarity, index = getSameQuestionByEditDistance(qdata)
    print(most_similarity, index)
    if most_similarity > 0.98:
        similar_val = most_similarity
        similaryQuestion, bestAns = getSimilaryQuestionByIndex(index)
        ans_type = 0
        sys_reply, QA_que = '', ''
        QA_ans = bestAns
        QA_ans = clean_ans(QA_ans)
    else:
        b = np.load(root_path + '/question2vec.npy')
        bc = BertClient()
        testvec = bc.encode(["".join(qdata.split())])
        topk = 10
        score = np.sum(testvec * b, axis=1) / np.linalg.norm(b, axis=1)
        topk_idx = np.argsort(score)[::-1][:topk]
        questionID = topk_idx[0] + 1  # qa-clean-data中问题索引是从1开始的
        similaryQuestion, bestAns = getSimilaryQuestionByIndex(questionID)
        similar_val = cosine_similarity(testvec[0], b[topk_idx[0]])
        if similar_val < 0.9:
            ans_type = 2
            sys_reply = '啊哦，小i还没有掌握这方面的知识呢，我会将您的问题记录下来，并尽快找到专业的答案。'
            QA_que, QA_ans = '', ''
        else:
            ans_type = 1
            sys_reply = '小i没有这个问题的答案呢，给您推荐相似问题及答案以供参考哦~'
            QA_que = similaryQuestion
            QA_ans = bestAns
            QA_ans = clean_ans(QA_ans)
    print('当前输入问题-->', qdata, '<--curr similary val:', similar_val,' SysQue: ', similaryQuestion, ' SysAns: ', bestAns, ' ans_type ', ans_type, ' sys_reply ', sys_reply)
    return ans_type, sys_reply, QA_que, QA_ans


def getSameQuestionByEditDistance(curr_ques):
    '''
    根据编辑距离计算问题库中最相思的问题，返回相似值及索引
    :param curr_ques:
    :return:
    '''
    most_similarity, index = 0, 0
    with open(filePath, 'r', encoding='utf-8') as csvfile:
        ques_ans = csv.reader(csvfile)
        id = 0
        for curr in ques_ans:
            id += 1
            curr_ques = replace_punctuation(curr_ques)
            csv_ques = replace_punctuation(curr[0])
            edit_distance_val = Levenshtein.ratio(csv_ques, curr_ques)
            if edit_distance_val > most_similarity:
                most_similarity = edit_distance_val
                index = id
    return most_similarity, index


def replace_punctuation(line):
    punctuation = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏."
    re_punctuation = "[{}]+".format(punctuation)
    line = re.sub(re_punctuation, "", line)
    punctuation2 = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    re_punctuation2 = "[{}]+".format(punctuation2)
    line = re.sub(re_punctuation2, "", line)
    return line


def getSimilaryQuestionByIndex(index):
    with open(filePath, 'r', encoding='utf-8') as csvfile:
        read = csv.reader(csvfile)
        id = 0
        for i in read:
            id += 1
            if id == index:
                simQuestion = i[0]
                ans = i[1]
    return simQuestion, ans


def clean_ans(str_ans):
    '''清理回答字符串中可能出现的html符号'''
    str_ans = str_ans.replace('??', '')
    str_ans = str_ans.replace('\n', '')
    str_ans = str_ans.replace(' ', '')
    return str_ans.replace('<br>', '')


if __name__ == '__main__':
    print('测试开始，查询问题--->')
    # testQ = ['应该怎么处理学生打架的问题', '不交作业怎么办', '上课睡觉怎么办？',
    #          '如何提高学生上课注意力', '上课注意力不集中怎么办？', '学生打架',
    #          '我怎样才能管住难管的学生？',
    #          '如何教育偷东西的学生']
    testQ = ['学生上课爱睡觉怎么办？']
    for que in testQ:
        getBestAnswer(que)
        print('------------------------------------------------------')
