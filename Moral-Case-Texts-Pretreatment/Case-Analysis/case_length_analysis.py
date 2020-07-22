#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import matplotlib.pyplot as plt
import numpy as np

'''统计案例的字数占比情况'''


def get_max_min_case_id(case_path):
    max_size,min_size = 0,99999
    max_id, min_id = '',''
    for curr_case_name in os.listdir(case_path):
        if curr_case_name[-4:] =='.txt':
            print(curr_case_name)
            curr_case_path = os.path.join(case_path,curr_case_name)
            case_content = ''
            with open(curr_case_path,'r',encoding='utf-8') as txt_read:
                for line in txt_read.readlines():
                    case_content +=line
            print('curr ', len(case_content))
            curr_len = len(case_content)
            if curr_len >max_size:
                max_size = curr_len
                max_id = curr_case_name
            if curr_len <min_size:
                min_size = curr_len
                min_id = curr_case_name
    print('案例最长的情况',max_id, max_size)
    print('案例最短的情况',min_id, min_size)


def get_case_len_info(case_path):
    len_info = [0 for i in range(9)]
    for curr_case_name in os.listdir(case_path):
        if curr_case_name[-4:] == '.txt':
            print(curr_case_name)
            curr_case_path = os.path.join(case_path, curr_case_name)
            case_content = ''
            with open(curr_case_path, 'r', encoding='utf-8') as txt_read:
                for line in txt_read.readlines():
                    case_content += line
            print('curr ', len(case_content))
            curr_len = len(case_content)
            if curr_len < 500:
                len_info[0] +=1
            elif curr_len >=500 and curr_len < 1000:
                len_info[1] +=1
            elif curr_len >=1000 and curr_len < 1500:
                len_info[2] +=1
            elif curr_len >=1500 and curr_len <2000:
                len_info[3] +=1
            elif curr_len >=2000 and curr_len < 2500:
                len_info[4] +=1
            elif curr_len >=2500 and curr_len <3000:
                len_info[5] +=1
            elif curr_len >3000 and curr_len <3500:
                len_info[6] +=1
            elif curr_len >3500 and curr_len <4000:
                len_info[7] +=1
            else:
                len_info[8] +=1

    print(len_info)
    draw_len_info(len_info)



def draw_len_info(info):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10, 10), dpi=80)
    # 再创建一个规格为 1 x 1 的子图
    # plt.subplot(1, 1, 1)
    # 柱子总数
    N = 9
    # 包含每个柱子对应值的序列
    values = info
    # 包含每个柱子下标的序列
    index = np.arange(N)
    # 柱子的宽度
    width = 0.45
    # 绘制柱状图, 每根柱子的颜色为紫罗兰色
    p2 = plt.bar(index, values, width, label="num", color="#87CEFA")
    # 设置横轴标签
    plt.xlabel('字数分布区间')
    # 设置纵轴标签
    plt.ylabel('案例个数')
    # 添加标题
    plt.title('统计案例字数大小所占比例')
    # 添加纵横轴的刻度
    plt.xticks(index, (
    '<500', '[500,1000]', '[1000,1500]', '[1500,2000]', '[2000,2500]',
    '[2500,3000]', '[3000,3500]', '[3500,4000]', '>4000'))
    # plt.yticks(np.arange(0, 10000, 10))
    # 添加图例
    plt.legend(loc="upper right")
    plt.show()



if __name__ == '__main__':
    case_path = './../Save-AnnInfo-to-Excel/data'

    get_max_min_case_id(case_path)
    # get_case_len_info(case_path)
