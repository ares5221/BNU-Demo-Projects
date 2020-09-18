#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from nlpcda import Similarword
import csv


def main():
    print('开始生成数据增强的问答数据')
    with open('postive_pairs.csv', 'a',encoding='utf-8',newline='') as csv_write:
        csv_write = csv.writer(csv_write)
        count = 0
        with open('double_teacher_math_question.csv', 'r',encoding='utf-8') as csv_read:
            reader = csv.reader(csv_read)
            for line in reader:
                print(line)
                # curr_id = line[0].split('\t')[0]
                curr_ques = line[0].split('\t')[1]
                smw = Similarword(create_num=3, change_rate=0.5)
                simi_ques = smw.replace(curr_ques)
                for curr_simi in simi_ques:
                    if curr_simi and curr_simi!=curr_ques:
                        print('@@@',curr_ques,curr_simi)
                        csv_write.writerow([str(count)+ '\t'+curr_ques+ '\t'+curr_simi+'\t'+str(1)])
                        count +=1
                if count >2500:
                    break


if __name__ =='__main__':
    main()
    print('generate positive data end!!!')