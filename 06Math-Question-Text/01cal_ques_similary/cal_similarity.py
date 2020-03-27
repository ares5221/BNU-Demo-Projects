#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from __future__ import absolute_import
import jieba
import time
from scipy import spatial
import numpy as np
import difflib
import Levenshtein
from Utils.load_data import *
from bert_serving.client import BertClient

file_voc = './data/voc.txt'
file_idf = './data/idf.txt'
file_userdict = './data/self_jieba_dict.txt'


class SSIM(object):
    def __init__(self):
        t1 = time.time()
        self.voc = load_voc(file_voc)
        print("Loading  word2vec vector cost %.3f seconds...\n" % (time.time() - t1))
        t1 = time.time()
        self.idf = load_idf(file_idf)
        print("Loading  idf data cost %.3f seconds...\n" % (time.time() - t1))
        jieba.load_userdict(file_userdict)

    def M_cosine(self, s1, s2):
        s1_list = jieba.lcut(s1)
        s2_list = jieba.lcut(s2)
        v1 = np.array([self.voc[s] for s in s1_list if s in self.voc])
        v2 = np.array([self.voc[s] for s in s2_list if s in self.voc])
        v1 = v1.sum(axis=0)
        v2 = v2.sum(axis=0)
        sim = 1 - spatial.distance.cosine(v1, v2)
        return sim

    def M_idf(self, s1, s2):
        v1, v2 = [], []
        s1_list = jieba.lcut(s1)
        s2_list = jieba.lcut(s2)
        for s in s1_list:
            idf_v = self.idf.get(s, 1)
            if s in self.voc:
                v1.append(1.0 * idf_v * self.voc[s])
        for s in s2_list:
            idf_v = self.idf.get(s, 1)
            if s in self.voc:
                v2.append(1.0 * idf_v * self.voc[s])
        v1 = np.array(v1).sum(axis=0)
        v2 = np.array(v2).sum(axis=0)
        sim = 1 - spatial.distance.cosine(v1, v2)
        return sim

    def M_bm25(self, s1, s2, s_avg=10, k1=2.0, b=0.75):
        bm25 = 0
        s1_list = jieba.lcut(s1)
        for w in s1_list:
            idf_s = self.idf.get(w, 1)
            bm25_ra = s2.count(w) * (k1 + 1)
            bm25_rb = s2.count(w) + k1 * (1 - b + b * len(s2) / s_avg)
            bm25 += idf_s * (bm25_ra / bm25_rb)
        return bm25

    def M_jaccard(self, s1, s2):
        s1 = set(s1)
        s2 = set(s2)
        ret1 = s1.intersection(s2)
        ret2 = s1.union(s2)
        jaccard = 1.0 * len(ret1) / max(len(ret2),0.000000001)
        return jaccard

    def M_difflib(self, s1, s2):
        # SequenceMatcher 第一个参数为一个函数，主要用来去掉自己不想算在内的元素；如果没有，可以写None，有的话写 lambda x: x == " ",或者lambda x: x in '主要'
        # 后面两个参数就是需要比较的两个对象了
        difflib_value = difflib.SequenceMatcher(None, s1, s2).quick_ratio()
        return difflib_value

    def M_edit_dist(self, s1, s2):
        # 计算编辑距离
        len1 = len(s1)
        len2 = len(s2)
        dp = np.zeros((len1 + 1, len2 + 1))
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                delta = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j - 1] + delta, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
        return dp[len1][len2]

    def M_Levenshtein_dist_pro(self, s1, s2):
        # 采用Levenshtein包直接计算编辑距离
        leven_dist = Levenshtein.distance(s1, s2)
        return leven_dist

    def M_Levenshtein_dist_ratio(self, s1, s2):
        # 采用Levenshtein包直接计算ratio,区间[0-1]越接近1越相似
        leven_dist = Levenshtein.ratio(s1, s2)
        return leven_dist

    def M_bert_cosine(self, s1, s2):
        bc = BertClient()
        if len(s1)>0 and len(s2)>0:
            vec1 = bc.encode([s1]).tolist()[0]
            vec2 = bc.encode([s2]).tolist()[0]
            dist1 = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        else:
            print(s1,s2)
            dist1 = 0 #如果有一个为空，则不相似
        return dist1

    def ssim(self, s1, s2, model='cosine'):
        if model == 'idf':
            f_ssim = self.M_idf
        elif model == 'bm25':
            f_ssim = self.M_bm25
        elif model == 'jaccard':
            f_ssim = self.M_jaccard
        elif model == 'difflib':
            f_ssim = self.M_difflib
        elif model == 'editdist':
            f_ssim = self.M_Levenshtein_dist_pro
        elif model == 'Leven_ratio':
            f_ssim = self.M_Levenshtein_dist_ratio

        elif model == 'bert':
            f_ssim = self.M_bert_cosine
        else:
            f_ssim = self.M_cosine

        sim = f_ssim(s1, s2)
        return sim


sm = SSIM()
ssim = sm.ssim

if __name__ == '__main__':
    print('test')
