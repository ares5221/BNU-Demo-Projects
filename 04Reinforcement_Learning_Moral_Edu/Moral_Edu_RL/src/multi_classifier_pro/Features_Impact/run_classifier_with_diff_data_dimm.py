#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import pickle
import numpy as np
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn import tree
from sklearn.svm import SVC
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_curve, auc
import warnings
warnings.filterwarnings("ignore")

# 每次去除一个维度的数据，对数据进行分类

def process(data_index):
    # 读入数据
    data_name = str(data_index) + '_records.dat'
    with open(data_name, 'rb') as f1:
        records = pickle.load(f1)
    with open('disease_tag.dat', 'rb') as f2:
        disease_tag_old = pickle.load(f2)

    # eg:disease:归属和爱的需求→ id:0
    diseases = list(set(disease_tag_old))
    disease2id = dict()
    for i in range(len(diseases)):
        disease2id[diseases[i]] = i
    disease_tag = [disease2id[d] for d in disease_tag_old]
    # print(disease2id)
    # shuffle
    records = np.array(records)
    disease_tag = np.array(disease_tag)
    indices = np.arange(records.shape[0])

    np.random.shuffle(indices)
    # print(indices)
    records = records[indices]
    disease_tag = disease_tag[indices]
    return records, disease_tag


# AdaBoost分类器
def AdaBoost(data_train, id_train, data_test, id_test, select):
    # rf = AdaBoostClassifier(n_estimators=10)
    if select == 0:
        rf = AdaBoostClassifier(n_estimators=100, base_estimator=LogisticRegression())
    elif select == 1:
        rf = AdaBoostClassifier(n_estimators=100, base_estimator=BernoulliNB())
    elif select ==2:
        rf = AdaBoostClassifier(n_estimators=100, base_estimator=tree.DecisionTreeClassifier())
    else:
        rf = AdaBoostClassifier(n_estimators=100, base_estimator=SVC(), algorithm='SAMME')
    clf = rf.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='macro')
    recall = recall_score(id_test, id_predict, average='macro')
    fscore = f1_score(id_test, id_predict, average='macro')
    acc_score = accuracy_score(id_test, id_predict)
    kappa_score = cohen_kappa_score(id_test, id_predict)
    fpr, tpr, thresholds = roc_curve(id_test, id_predict, pos_label=5)
    auc_score = auc(fpr, tpr)
    # print('\033[1;31;0mDT:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    # print(precision, recall, fscore, acc_score, kappa_score, auc_score)
    return precision, recall, fscore, acc_score

# Bagging分类器
def Bagging(data_train, id_train, data_test, id_test, select):
    if select == 0:
        bc = BaggingClassifier(n_estimators=100, base_estimator=LogisticRegression())
    elif select == 1:
        bc = BaggingClassifier(n_estimators=100, base_estimator=BernoulliNB())
    elif select ==2:
        bc = BaggingClassifier(n_estimators=100, base_estimator=tree.DecisionTreeClassifier())
    else:
        bc = BaggingClassifier(n_estimators=100, base_estimator=SVC())
    clf = bc.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='macro')
    recall = recall_score(id_test, id_predict, average='macro')
    fscore = f1_score(id_test, id_predict, average='macro')
    acc_score = accuracy_score(id_test, id_predict)
    kappa_score = cohen_kappa_score(id_test, id_predict)
    fpr, tpr, thresholds = roc_curve(id_test, id_predict, pos_label=5)
    auc_score = auc(fpr, tpr)
    # print('\033[1;31;0mDT:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score, kappa_score, auc_score)


# GradientBoosting分类器
def GradientBoosting(data_train, id_train, data_test, id_test):
    rf = GradientBoostingClassifier(n_estimators=10)
    clf = rf.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='macro')
    recall = recall_score(id_test, id_predict, average='macro')
    fscore = f1_score(id_test, id_predict, average='macro')
    acc_score = accuracy_score(id_test, id_predict)
    kappa_score = cohen_kappa_score(id_test, id_predict)
    fpr, tpr, thresholds = roc_curve(id_test, id_predict, pos_label=5)
    auc_score = auc(fpr, tpr)
    # print('\033[1;31;0mDT:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score, kappa_score, auc_score)


# RF分类器
def RF(data_train, id_train, data_test, id_test):
    rf = RandomForestClassifier(n_estimators=10)
    clf = rf.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='macro')
    recall = recall_score(id_test, id_predict, average='macro')
    fscore = f1_score(id_test, id_predict, average='macro')
    acc_score = accuracy_score(id_test, id_predict)
    kappa_score = cohen_kappa_score(id_test, id_predict)
    fpr, tpr, thresholds = roc_curve(id_test, id_predict, pos_label=5)
    auc_score = auc(fpr, tpr)
    # print('\033[1;31;0mDT:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score, kappa_score, auc_score)


def get_train_data(trains, labels, split_num):
    split = int(len(trains) * split_num * 0.1)
    data_train = trains[:split]
    id_train = labels[:split]
    # print(id_train)
    indices = np.arange(data_train.shape[0])
    np.random.shuffle(indices)
    data_train = data_train[indices]
    id_train = id_train[indices]
    return data_train, id_train


if __name__ == '__main__':
    '''
    data_train:训练集每条案例的特征表示
    id_train: 训练集每条案例对应根本原因的标签
    data_test:测试集每条案例的特征表示
    id_test: 测试集每条案例对应根本原因的标签
    '''
    for data_idx in range(19):#共有19个维度，生成19份数据
        sum_precision = 0
        sum_recall = 0
        sum_fscore = 0
        sum_acc_score = 0
        count_num = 50
        for i in range(count_num):
            # 读取进来的全部数据及对应label，shuffle后的结果629条
            trains, labels = process(data_idx)
            # 给不同切分比例设置相同的test数据
            # split train/test data set
            split = int(len(trains) * 0.8)

            data_train = trains[:split]
            label_train = labels[:split]
            # data_train, id_train = get_train_data(trains, labels, split_num)
            data_test = trains[split:]
            label_test = labels[split:]

            # print('-------------------------第 %d 组数据------------------------------------------' % i)
            # AdaBoost和BaggingClassifier用LR、NB、DT和SVM做基分类器。
            # for selcet in range(4):
            #     AdaBoost(data_train, id_train, data_test, id_test, selcet)
            #     Bagging(data_train, id_train, data_test, id_test, selcet)
            # GradientBoosting(data_train, id_train, data_test, id_test)
            # RF(data_train, id_train, data_test, id_test)
            select = 0
            precision, recall, fscore, acc_score = AdaBoost(data_train, label_train, data_test, label_test, select)
            sum_precision += precision
            sum_recall += recall
            sum_fscore += fscore
            sum_acc_score += acc_score
        avg_precision = sum_precision /(count_num*1.0)
        avg_recall = sum_recall /(count_num*1.0)
        avg_fscore = sum_fscore/ (count_num*1.0)
        avg_acc_score = sum_acc_score/(count_num*1.0)
        print('第 %s 份数据的分类效果-precision, recall, fscore, acc_score' % data_idx, avg_precision, avg_recall, avg_fscore, avg_acc_score)
