import pickle
import xlrd
import random
import os
# todo 依次去除一个特征后，比较分类器的分类效果
# 以此来判断那些特征是不重要的，可以忽略考虑


def preprocess(file):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_name(workbook.sheet_names()[1])
    print(sheet.ncols, sheet.nrows)
    labels = ['身体攻击行为', '言语攻击行为', '关系攻击行为',
              '隐蔽性违反课堂纪律行为','扰乱课堂秩序行为','违反课外纪律行为',
              '欺骗行为','偷盗行为', '背德行为',
              '言语型退缩','行为型退缩','心理型退缩',
              '抑郁问题','焦虑问题',
              '自我吹嘘型问题', '执拗型问题', '自私型问题', 
              '学习能力问题','学习方法问题','学习态度问题','注意力问题',
              '沉迷行为','早恋行为','极端行为',
              '男','女',
              '小学','初中','高中',
              '健康','生理疾病','心理疾病',
              '一般儿童','留守儿童','流动儿童','孤困儿童',
              '寄养家庭','重组家庭','单亲家庭','完整家庭',
              '权威型教养方式','专制型教养方式','溺爱型教养方式','忽视型教养方式',
              '冲突型家庭气氛','离散型家庭气氛','和谐型家庭气氛','平静型家庭气氛',
              '成员文化程度低','成员文化程度高',
              '成员健康','成员生理疾病','成员心理疾病',
              '家庭经济低收入','家庭经济高收入',
              '同伴接纳受欢迎','同伴接纳一般型','同伴接纳被拒绝','同伴接纳被忽视','同伴接纳矛盾型',
              ]
     
    all_data = [[] for i in range(sheet.nrows-4)]
    disease_tag = []
    for i in range(4, sheet.nrows):
        disease = sheet.cell(i,21).value
        if '，' not in disease:
            disease_tag.append(disease.strip())
        else:
            disease_tag.append(random.choice(disease.strip().split('，')))
        label_data = []
        for j in range(2, 21):
            if len(sheet.cell(i,j).value.replace(' ', '')) > 0:
                label_data.append(sheet.cell(i,j).value)      
        all_data[i-4] = label_data
    print(all_data[0])
    labels2id = dict()
    for i in range(len(labels)):
        labels2id[labels[i]] = i
    
    records = []
    for data in all_data:
        record = [0]*len(labels)
        for d in data:
            if '，' not in d:
                index =  labels2id[d]
                record[index] = 1
            else:
                d = d.strip().split('，')
                for dd in d:
                     index =  labels2id[dd]
                     record[index] = 1
        records.append(record)
    return records, disease_tag


def save_single_data(records, index):
    tmp_record = []
    if index ==0:
        for i in range(len(records)):
            tmp_record.append(records[i][3:])
    if index ==1:
        for i in range(len(records)):
            tmp_record.append(records[i][:3] + records[i][6:])
    if index == 2:
        for i in range(len(records)):
            tmp_record.append(records[i][:6] + records[i][9:])
    if index == 3:
        for i in range(len(records)):
            tmp_record.append(records[i][:9] + records[i][12:])
    if index == 4:
        for i in range(len(records)):
            tmp_record.append(records[i][:12] + records[i][14:])
    if index ==5:
        for i in range(len(records)):
            tmp_record.append(records[i][:14] + records[i][17:])
    if index == 6:
        for i in range(len(records)):
            tmp_record.append(records[i][:17] + records[i][21:])
    if index == 7:
        for i in range(len(records)):
            tmp_record.append(records[i][:21] + records[i][24:])
    if index == 8:
        for i in range(len(records)):
            tmp_record.append(records[i][:24] + records[i][26:])
    if index ==9:
        for i in range(len(records)):
            tmp_record.append(records[i][:26] + records[i][29:])
    if index == 10:
        for i in range(len(records)):
            tmp_record.append(records[i][:29] + records[i][32:])
    if index == 11:
        for i in range(len(records)):
            tmp_record.append(records[i][:32] + records[i][36:])
    if index == 12:
        for i in range(len(records)):
            tmp_record.append(records[i][:36] + records[i][40:])
    if index ==13:
        for i in range(len(records)):
            tmp_record.append(records[i][:40] + records[i][44:])
    if index == 14:
        for i in range(len(records)):
            tmp_record.append(records[i][:44] + records[i][48:])
    if index == 15:
        for i in range(len(records)):
            tmp_record.append(records[i][:48] + records[i][50:])
    if index == 16:
        for i in range(len(records)):
            tmp_record.append(records[i][:50] + records[i][53:])
    if index ==17:
        for i in range(len(records)):
            tmp_record.append(records[i][:53] + records[i][55:])
    if index == 18:
        for i in range(len(records)):
            tmp_record.append(records[i][:55])
    # if index == 19:
    #     for i in range(len(records)):
    #         tmp_record.append(records[i][:9] + records[i][12:])

    print(records[0])
    print(tmp_record[0])
    data_name = str(index) + '_records.dat'
    if not os.path.exists(data_name):
        with open(data_name, 'wb') as f1:
            pickle.dump(tmp_record, f1)


if __name__ == '__main__':
    #records存储每条案例的特征；disease_tag存储每条案例的根本原因的label
    records, disease_tag = preprocess(r'data整理2.xlsx')
    print(len(records[0]),records[0])
    print(len(disease_tag))
    # 总共20个维度
    for index in range(19):
        save_single_data(records, index)

    if not os.path.exists('disease_tag.dat'):
        with open('disease_tag.dat', 'wb') as f2:
            pickle.dump(disease_tag, f2)

