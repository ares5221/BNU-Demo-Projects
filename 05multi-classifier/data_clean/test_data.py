import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from collections import Counter

def check_data():
    print('check data')
    # step 1: read data
    with open('records.dat', 'rb') as f1:
        records = pickle.load(f1)
    with open('disease_tag.dat', 'rb') as f2:
        tag = pickle.load(f2)

    records = np.array(records)


    count = 0
    for i in range(len(records)):
        for j in range(i+1, len(records)):
            
            diff = sum(records[i]!=records[j])
            if diff < 10 and tag[i] != tag[j]:
                print(i, j, tag[i], tag[j])
                count += 1
    print(count)
    print(type(records))


def read_data():
    # data = pd.read_excel(open('标注结果.xlsx', 'rb'), sheet_name='4_案例标注629-3.0_2', dtype=str)
    data = pd.read_excel(open('标注结果.xlsx', 'rb'), sheet_name='label_5_classes', dtype=str)
    # print(data.dtype)
    data = data.set_index('ID')
    data = data.drop(columns=['标题', '具体方法'])
    label = data['需求缺失类别']
    # print(type(label.array), label.array)
    data = data.drop(columns=['需求缺失类别'])
    # count = 0
    # idset = set()
    # for i in range(data.shape[0]-1):
    #     for j in range(i+1, data.shape[0]):
    #         # value = sum(data.iloc[i]!=data.iloc[j])
    #         value = compare(data.iloc[i], data.iloc[j])
    #         # print(value)
    #         if value == 0:
    #             idset.add(i)
    #             idset.add(j)
    #             print(i, j, label.iloc[i], label.iloc[j])
    #             count += 1
    # print('count', count)
    # print('set', idset)
    data = data.drop(columns=['年级', '不良品行', '自我中心', '特殊问题'])
    data2 = data.applymap(lambda x: sorted(str(x).replace(' ', '').split('，'))[0])
    # print(data.columns)
    # print(data2)
    cols = data.columns
    data2 = data2[cols[:15]]
    print(data2)
    print(label)
    enc = OneHotEncoder(dtype=int, sparse=False)
    data3 = enc.fit_transform(data2)
    # print(type(data3), data3.shape)
    print(type(label))
    label_a = [str(x).replace(' ', '').split('，') for x in label]
    label_a = [sorted(x) for x in label_a]
    print('label_1', label_a)

    # step 2: compare each case and make the label consistant
    y = consistent_data(data3, label_a)
    cols = data2.columns
    data4 = data2[cols[:]]
    enc2 = OneHotEncoder(dtype=int, sparse=False)
    x = enc2.fit_transform(data4)
    print(y)
    return x, y

def consistent_data(data_x, label_y):
    # step 1: find the similar cases
    idset = set()
    group = []
    for i in range(data_x.shape[0]-1):
        for j in range(i+1, data_x.shape[0]):
            if (data_x[i] == data_x[j]).all():
                # check whether in any group
                exist = False
                for g in group:
                    if i in g:
                        exist=True
                        # add in 
                        g.add(j)
                        break
                if not exist:
                    group.append({i, j})

                # count all case id
                idset.add(i)
                idset.add(j)
    print(len(group))

    # step 2: find the most common tag for similar cases
    new_tag = {}
    for g in group:
        tag_list = [y for x in g for y in label_y[x]]
        tag = Counter(tag_list).most_common(1)
        for cid in g:
            new_tag[cid] = tag[0][0]
    # print('new tag list', new_tag)

    for g in group:
        g = sorted(g)
        # print([x+1 for x in g], [label_y[x] for x in g])
    print(len(idset))

    # step 3: create new tag list
    new_label_y = label_y.copy()
    for i in range(len(label_y)):
        if i in new_tag:
            new_label_y[i] = new_tag[i]
        else:
            # print(i, label_y[i][-1])
            new_label_y[i] = label_y[i][-1]

    # print('disease_tag', new_label_y)
    """
    '认知的需求': 305, '归属和爱的需求': 166, '尊重的需求': 102, '生理的需求': 29, '安全的需求': 27
    """
    print('label counter', Counter(new_label_y))
    print(len(new_label_y))
    return new_label_y

def compare(row_a, row_b):
    assert len(row_a) == len(row_b)
    value = 0
    for i in range(len(row_a)):
        if pd.isna(row_a[i]) and pd.isna(row_b[i]):
            value += 1
        elif row_a[i] == row_b[i]:
            value += 1
    diff = int(len(row_a)-value)
    return diff


def generate_data_file():
    # check_data()
    #records存储每条案例的特征；disease_tag存储每条案例的根本原因的label
    records, disease_tag  = read_data()
    # print(disease_tag)
    # print(records)
    with open('records.dat', 'wb') as f1:
        pickle.dump(records, f1)
    with open('disease_tag.dat', 'wb') as f2:
        pickle.dump(disease_tag, f2)

def start():
    # check_data()
    # read_data()
    generate_data_file()

if __name__ == '__main__':
    start()