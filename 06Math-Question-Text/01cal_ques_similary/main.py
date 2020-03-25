#encoding:utf-8

import codecs
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
    tmp_dict = {}
    for idx in range(len(data)):
    # for idx in range(0,3):
        if idx % 100 == 0:
            print('已经完成：',idx/len(data) *100,'%')
        for jdx in range(len(data)):
            if idx == jdx:
                continue
            else:
                curr_txt1 = data[idx][1].replace(' ','')
                curr_txt2 = data[jdx][1].replace(' ','')
                simi_val = cal_similarity.ssim(curr_txt1,curr_txt2,model='jaccard')
                # print(simi_val,curr_txt1, curr_txt2)
                curr_str1 = data[idx][0] + ' '+  curr_txt1
                curr_str2 = data[jdx][0] + ' '+  curr_txt2
                tmp_dict[curr_str1 + '<--->' + curr_str2] = simi_val
    # print(tmp_dict)
    top = sorted(tmp_dict.items(), key=lambda x: x[1], reverse=True)
    with open('result.csv','a', encoding='utf-8',newline='') as csv_write:
        f_csv = csv.writer(csv_write)
        f_csv.writerow(['相似值', '题目对及对应id'])
        for tmp in top:
            f_csv.writerow([tmp[1],tmp[0]])

def test():
    test_data=[u'临床表现及实验室检查即可做出诊断',
               u'面条汤等容易消化吸收的食物为佳',
               u'每天应该摄入足够的维生素A',
               u'视患者情况逐渐恢复日常活动',
               u'术前1天开始预防性运用广谱抗生素']
    model_list=['cosine','idf','bm25','jaccard']
    file_sentence=codecs.open('./data/file_sentence.txt','r',encoding='utf-8')
    train_data=file_sentence.readlines()
    for model in model_list:
        t1 = time.time()
        dataset=dict()
        result=dict()
        for s1 in test_data:
            dataset[s1]=dict()
            for s2 in train_data:
                s2=s2.strip()
                if s1!=s2:
                    sim=similarity.ssim(s1,s2,model=model)
                    dataset[s1][s2]=dataset[s1].get(s2,0)+sim
        for r in dataset:
            top=sorted(dataset[r].items(),key=lambda x:x[1],reverse=True)
            result[r]=top[0]
        with codecs.open('./data/test_result.txt','a') as f:
            f.write('--------------The result of %s method------------------\n '%model)
            f.write('\tThe computing cost %.3f seconds\n'% (time.time() - t1))
            f.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=False))
            f.write('\n\n')

    file_sentence.close()

if __name__ == '__main__':
    data_file = 'data.csv'
    data = read_data(data_file)
    cal_similarity_jaccard(data)


    # test()




