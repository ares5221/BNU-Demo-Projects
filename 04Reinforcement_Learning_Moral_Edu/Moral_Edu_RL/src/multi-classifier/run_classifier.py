# -*- coding:utf-8 -*-
import random
import pickle
import os
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.svm import NuSVC
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import warnings
warnings.filterwarnings("ignore")
'''
机器学习的分类器结果作为baseline，将来与通过RL得到的结果比较。
'''
DISEASES = ['安全的需求', '尊重的需求', '归属和爱的需求', '生理的需求', '认知的需求']
INFORM_LABELS = ['身体攻击行为', '言语攻击行为', '关系攻击行为',
                 '隐蔽性违反课堂纪律行为', '扰乱课堂秩序行为', '违反课外纪律行为',
                 '欺骗行为', '偷盗行为', '背德行为',
                 '言语型退缩', '行为型退缩', '心理型退缩',
                 '抑郁问题', '焦虑问题',
                 '自我吹嘘型问题', '执拗型问题', '自私型问题',
                 '学习能力问题', '学习方法问题', '学习态度问题', '注意力问题',
                 '沉迷行为', '早恋行为', '极端行为',
                 '男', '女',
                 '小学', '初中', '高中',
                 '健康', '生理疾病', '心理疾病',
                 '一般儿童', '留守儿童', '流动儿童', '孤困儿童',
                 '寄养家庭', '重组家庭', '单亲家庭', '完整家庭',
                 '权威型教养方式', '专制型教养方式', '溺爱型教养方式', '忽视型教养方式',
                 '冲突型家庭气氛', '离散型家庭气氛', '和谐型家庭气氛', '平静型家庭气氛',
                 '成员文化程度低', '成员文化程度高',
                 '成员健康', '成员生理疾病', '成员心理疾病',
                 '家庭经济低收入', '家庭经济高收入',
                 '成员不顾家', '成员打麻将', '成员坐牢', '成员酗酒', '成员看电视', '成员打游戏', '成员赌博', '成员欠钱不还', '成员吸毒', '成员打牌',
                 '同伴接纳受欢迎', '同伴接纳一般型', '同伴接纳被拒绝', '同伴接纳被忽视', '同伴接纳矛盾型',
                 '大众传媒的影响', '网络媒体', '影视节目', '读书无用'
                 ]


def get_vector(data_dict):
    labels2id = dict()
    for i in range(len(INFORM_LABELS)):
        labels2id[INFORM_LABELS[i]] = i
    vector = [0 for i in range(len(INFORM_LABELS))]
    for eis, eis_val in data_dict['goal']['explicit_inform_slots'].items():
        vector[labels2id[eis]] = 1 if eis_val else 0
    for iis, iis_val in data_dict['goal']['implicit_inform_slots'].items():
        vector[labels2id[iis]] = 1 if iis_val else 0
    return vector


def get_label(data_dict):
    disease = data_dict['disease_tag']
    if len(disease) > 1:
        disease_tag = random.choice(disease)
    else:
        disease_tag = disease[0]
    return DISEASES.index(disease_tag)


def get_vectors_repe(data_list):
    vectors, labels = [], []
    for index in range(len(data_list)):
        vectors.append(get_vector(data_list[index]))
        labels.append(get_label(data_list[index]))
    return vectors, labels


def parper_data(index):
    # 1 get file goal_set.p
    data_path = os.path.abspath('./../dialogue_system/data/data_') + str(index)
    # print(data_path)
    goal_set = pickle.load(file=open(data_path + "/goal_set.p", "rb"))
    # print(goal_set)
    # 2 get train data
    train = goal_set['train']
    train_data, train_lable = get_vectors_repe(train)
    # print(len(train_data), train_data[0], train_lable[0])
    # 3 get test data
    test = goal_set['test']
    test_data, test_label = get_vectors_repe(test)
    # print(len(test_data), test_data[0], test_label[0])
    return train_data, train_lable, test_data, test_label


# 决策树分类器
def DT(data_train, id_train, data_test, id_test):
    dtc = tree.DecisionTreeClassifier(criterion="entropy")
    clf = dtc.fit(data_train, id_train)
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='weighted')
    recall = recall_score(id_test, id_predict, average='weighted')
    fscore = f1_score(id_test, id_predict, average='weighted')
    acc_score = accuracy_score(id_test, id_predict)
    # print('\033[1;31;0mDT:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print( precision, recall, fscore, acc_score)


# KNN分类器
def KNN(data_train, id_train, data_test, id_test):
    knn = KNeighborsClassifier(n_neighbors=5, p=2)
    clf = knn.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='weighted')
    recall = recall_score(id_test, id_predict, average='weighted')
    fscore = f1_score(id_test, id_predict, average='weighted')
    acc_score = accuracy_score(id_test, id_predict)
    # print('\033[1;32;0mKNN:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score)


# SVM分类器
def SVM(data_train, id_train, data_test, id_test):
    # svm = LinearSVC(random_state=1)
    svm = SVC(kernel='linear', random_state=1)
    # svm = SVC(kernel = 'poly',random_state=1)
    # svm = SVC(kernel = 'rbf',random_state=1)
    # svm = SVC(kernel = 'sigmoid',random_state=1)

    # svm = NuSVC(kernel = 'linear',random_state=1)
    # svm = NuSVC(kernel = 'poly',random_state=1)
    # svm = NuSVC(kernel = 'rbf',random_state=1)
    # svm = NuSVC(kernel = 'sigmoid',random_state=1)
    clf = svm.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='weighted')
    recall = recall_score(id_test, id_predict, average='weighted')
    fscore = f1_score(id_test, id_predict, average='weighted')
    acc_score = accuracy_score(id_test, id_predict)
    # print('\033[1;33;0mSVM:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score)


# LR分类器
def LR(data_train, id_train, data_test, id_test):
    lr = LogisticRegression(random_state=0, solver='lbfgs',
                            multi_class='multinomial', penalty='l2')
    clf = lr.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='weighted')
    recall = recall_score(id_test, id_predict, average='weighted')
    fscore = f1_score(id_test, id_predict, average='weighted')
    acc_score = accuracy_score(id_test, id_predict)
    # print('\033[1;34;0mLR:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score)


# NB分类器
def NB(data_train, id_train, data_test, id_test):
    # bayes=GaussianNB()
    # bayes=MultinomialNB()
    bayes = BernoulliNB()
    clf = bayes.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='weighted')
    recall = recall_score(id_test, id_predict, average='weighted')
    fscore = f1_score(id_test, id_predict, average='weighted')
    acc_score = accuracy_score(id_test, id_predict)
    # print('\033[1;34;0NB:precision:%f, recall:%f, fscore:%f\033[0m' %(precision, recall, fscore))
    print(precision, recall, fscore, acc_score)

# RF分类器
def RF(data_train, id_train, data_test, id_test):
    rf = RandomForestClassifier(n_estimators=10)
    clf = rf.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='weighted')
    recall = recall_score(id_test, id_predict, average='weighted')
    fscore = f1_score(id_test, id_predict, average='weighted')
    acc_score = accuracy_score(id_test, id_predict)
    # print('\033[1;36;0mRF:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score)


# AdaBoost分类器
def AdaBoost(data_train, id_train, data_test, id_test):
    rf = AdaBoostClassifier(n_estimators=10)
    clf = rf.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='weighted')
    recall = recall_score(id_test, id_predict, average='weighted')
    fscore = f1_score(id_test, id_predict, average='weighted')
    acc_score = accuracy_score(id_test, id_predict)
    # print('\033[1;36;0mRF:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score)


# GradientBoosting分类器
def GradientBoosting(data_train, id_train, data_test, id_test):
    rf = GradientBoostingClassifier(n_estimators=10)
    clf = rf.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='weighted')
    recall = recall_score(id_test, id_predict, average='weighted')
    fscore = f1_score(id_test, id_predict, average='weighted')
    acc_score = accuracy_score(id_test, id_predict)
    # print('\033[1;36;0mRF:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score)



def run():
    '''
    读取切分比例为5：5情况下随机出来的十组数据，向量化表示为多分类数据
       train_data:训练集每条案例的特征表示
       train_lable: 训练集每条案例对应根本原因的标签
       test_data:测试集每条案例的特征表示
       test_label: 测试集每条案例对应根本原因的标签
       '''
    print('多分类器依次为：DT, KNN, SVM, LR, NB, RF, AdaBoost, GradientBoosting')
    for i in range(10):
        # 依次读取不同切分比例下的十组数据
        train_data, train_lable, test_data, test_label = parper_data(i)
        print('-------------------------第 %d 组数据------------------------------------------'%i)
        DT(train_data, train_lable, test_data, test_label)
        KNN(train_data, train_lable, test_data, test_label)
        SVM(train_data, train_lable, test_data, test_label)
        LR(train_data, train_lable, test_data, test_label)
        NB(train_data, train_lable, test_data, test_label)
        RF(train_data, train_lable, test_data, test_label)
        AdaBoost(train_data, train_lable, test_data, test_label)
        GradientBoosting(train_data, train_lable, test_data, test_label)


if __name__ == "__main__":
    run()
