#encoding:utf-8

import os
import cal_similarity
import json
import time
import csv


def read_data(path):
    data = []
    with open(path, 'r', encoding='utf-8') as csv_read:
        reader = csv.reader(csv_read)
        for row in reader:
            data.append(row)
    return data[1:]

def cal_similarity_jaccard(data):
    # print(len(data)) #3321
    # print(data[0])#['2', '如果一个命题的逆命题是真命题，那么这个命题的(\xa0\xa0\xa0)']
    # print(data[0][1])#如果一个命题的逆命题是真命题，那么这个命题的(   )

    simi_method_list = ['cosine', 'idf', 'bm25', 'jaccard','difflib','editdist', 'bert']
    simi_method_list = ['editdist']
    for func in simi_method_list:
        t1 = time.time()
        tmp_dict = {}
        for idx in range(len(data)):
        # for idx in range(0,3):
            if idx % 100 == 0:
                print(func, '已经完成：',idx/len(data) *100,'%')
            for jdx in range(len(data)):
                if idx == jdx:
                    continue
                else:
                    curr_txt1 = data[idx][1].replace(' ','')
                    curr_txt2 = data[jdx][1].replace(' ','')
                    simi_val = cal_similarity.ssim(curr_txt1,curr_txt2,model=func)

                    curr_str1 = data[idx][0] + ' '+  curr_txt1
                    curr_str2 = data[jdx][0] + ' '+  curr_txt2
                    tmp_dict[curr_str1 + '<--->' + curr_str2] = simi_val
        # print(tmp_dict)
        top = sorted(tmp_dict.items(), key=lambda x: x[1], reverse=True)
        result_name = os.path.join('./result',func+'_result.csv')
        with open(result_name,'a', encoding='utf-8',newline='') as csv_write:
            f_csv = csv.writer(csv_write)
            f_csv.writerow(['--------------The result of %s method------------------' % func])
            f_csv.writerow(['\tThe computing cost %.3f seconds' % (time.time() - t1)])
            f_csv.writerow(['相似值', '题目对及对应id'])
            for tmp in top:
                f_csv.writerow([tmp[1],tmp[0]])
            f_csv.writerow('\n\n')


if __name__ == '__main__':
    data_file = 'data.csv'
    data = read_data(data_file)
    cal_similarity_jaccard(data)


    # test()




