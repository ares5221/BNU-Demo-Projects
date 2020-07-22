#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os

# 设置最长段落字数
max_papagraph_len = 300
'''
拆分长段落的案例
'''
def split_long_paragraph(case_path):
    for curr_case_name in os.listdir(case_path):
        if curr_case_name[-4:] == '.txt':
            # if curr_case_name != 'a0000035.txt':
            #     continue
            curr_case_path = os.path.join(case_path, curr_case_name)
            case_content = ''
            with open(curr_case_path, 'r', encoding='utf-8') as txt_read:
                for line in txt_read.readlines():
                    curr_para = line.strip()
                    curr_para_len = len(line)
                    if curr_para_len < max_papagraph_len:
                        case_content +=curr_para + '\n'
                    else:
                        curr_para = split_para(curr_para)
                        case_content += curr_para + '\n'
            print('@@@@@@@@@@',case_content)
            save_path = os.path.join('./split_paragraph_res',curr_case_name)
            with open(save_path,'a', encoding='utf-8') as txt_write:
                txt_write.write(case_content)  # 写入
                txt_write.write('\n')

def split_para(curr_str):
    split_num = int(len(curr_str)/max_papagraph_len)+1
    print(split_num)
    # 拆分段落
    res = [[] for i in range(split_num)]
    for idx in range(split_num):
        if max_papagraph_len*(idx+1) <len(curr_str):
            res[idx] = curr_str[max_papagraph_len*idx:max_papagraph_len*(idx+1)]
        else:
            res[idx] = curr_str[max_papagraph_len*idx:]
    formter_res = [[] for i in range(split_num)]
    replace_str = ''
    for idx in range(len(res)):
        curr_part = res[idx]
        if curr_part:
            if len(replace_str) >0:
                curr_part = str(curr_part).replace(replace_str,'')
            if idx ==len(res)-1:
                formter_res[idx] = curr_part
                break
            if str(curr_part).endswith('。'):
                formter_res[idx] = res[idx] +'\n'
            else:
                next_part = res[idx+1]
                if '。' in next_part:
                    start,end = next_part.split('。',1)
                    formter_res[idx] = curr_part + start + '。\n'
                    replace_str = start

    final_res = ''
    for tt in formter_res:
        if str(tt).startswith('。'):

            final_res += tt[1:]
        else:
            final_res +=str(tt)
    # print(final_res)
    return  final_res









if __name__ == '__main__':
    case_path = './../Save-AnnInfo-to-Excel/data'
    split_long_paragraph(case_path)