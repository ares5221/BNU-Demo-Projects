import pickle
import xlrd
import random


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
              '成员不顾家','成员打麻将','成员坐牢','成员酗酒','成员看电视','成员打游戏','成员赌博','成员欠钱不还','成员吸毒','成员打牌',
              '同伴接纳受欢迎','同伴接纳一般型','同伴接纳被拒绝','同伴接纳被忽视','同伴接纳矛盾型',
              '大众传媒的影响','网络媒体','影视节目',
              '读书无用'     
              ]
     
    all_data = [[] for i in range(sheet.nrows-4)]
    disease_tag = []
    for i in range(4, sheet.nrows):
        disease = sheet.cell(i,23).value
        if '，' not in disease:
            disease_tag.append(disease.strip())
        else:
            disease_tag.append(random.choice(disease.strip().split('，')))
        label_data = []
        for j in range(2, 22):
            if len(sheet.cell(i,j).value.replace(' ', '')) > 0:
                label_data.append(sheet.cell(i,j).value)      
        all_data[i-4] = label_data
    
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

if __name__ == '__main__':
    #records存储每条案例的特征；disease_tag存储每条案例的根本原因的label
    records, disease_tag = preprocess(r'data整理.xlsx')
    with open('records.dat', 'wb') as f1:
        pickle.dump(records, f1)
    with open('disease_tag.dat', 'wb') as f2:
        pickle.dump(disease_tag, f2)

