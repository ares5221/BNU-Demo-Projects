#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import matplotlib.pyplot as plt
import numpy as np

'''统计案例的段落情况'''

def get_case_para_info(case_path):
    case_count = 0
    for curr_case_name in os.listdir(case_path):
        if curr_case_name[-4:] == '.txt':
            if curr_case_name != 'a0000001.txt':
                break
            # print(curr_case_name)
            curr_case_path = os.path.join(case_path, curr_case_name)
            case_content = ''
            count = 0
            with open(curr_case_path, 'r', encoding='utf-8') as txt_read:
                for line in txt_read.readlines():
                    # print(line.strip())
                    if '\n' in line:
                        count +=1
                    case_content += line
                # print(case_content)
                if count <8:
                    print(curr_case_name)
                    case_count +=1
            # print('curr ', len(case_content))
            # if '\n' not in case_content:
            #     print(curr_case_name)

    print(case_count)
    # draw_len_info(len_info)



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
    get_case_para_info(case_path)
