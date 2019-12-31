import pickle
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.svm import NuSVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_curve, auc, roc_auc_score
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def process(record, tag):
    # 读入数据
    with open('records.dat', 'rb') as f1:
        records = pickle.load(f1)
    with open('disease_tag.dat', 'rb') as f2:
        disease_tag_old = pickle.load(f2)

    # eg:disease:归属和爱的需求→ id:0
    diseases = list(set(disease_tag_old))
    disease2id = dict()
    for i in range(len(diseases)):
        disease2id[diseases[i]] = i
    disease_tag = [disease2id[d] for d in disease_tag_old]
    # shuffle
    records = np.array(records)
    disease_tag = np.array(disease_tag)
    indices = np.arange(records.shape[0])

    np.random.shuffle(indices)
    # print(indices)
    records = records[indices]
    disease_tag = disease_tag[indices]
    return records, disease_tag


# 决策树分类器
def DT(data_train, id_train, data_test, id_test, ofile):
    dtc = tree.DecisionTreeClassifier(criterion="entropy", max_depth=10)
    clf = dtc.fit(data_train, id_train)
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='macro')
    recall = recall_score(id_test, id_predict, average='macro')
    fscore = f1_score(id_test, id_predict, average='macro')
    acc_score = accuracy_score(id_test, id_predict)

    kappa_score = cohen_kappa_score(id_test, id_predict)
    fpr, tpr, thresholds = roc_curve(id_test, id_predict, pos_label=5)
    auc_score = auc(fpr, tpr)
    # print('#####', roc_auc_score(id_test, id_predict))
    # print('\033[1;31;0mDT:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score, kappa_score, auc_score, file=ofile)


# KNN分类器
def KNN(data_train, id_train, data_test, id_test, ofile):
    knn = KNeighborsClassifier(n_neighbors=3, p=2)
    clf = knn.fit(data_train, id_train)
    # print(clf.predict(data_test))
    id_predict = clf.predict(data_test)
    precision = precision_score(id_test, id_predict, average='macro')
    recall = recall_score(id_test, id_predict, average='macro')
    fscore = f1_score(id_test, id_predict, average='macro')
    acc_score = accuracy_score(id_test, id_predict)

    kappa_score = cohen_kappa_score(id_test, id_predict)
    fpr, tpr, thresholds = roc_curve(id_test, id_predict, pos_label=5)
    auc_score = auc(fpr, tpr)
    # print('#####', roc_auc_score(id_test, id_predict, average='micro'))
    # print('\033[1;31;0mDT:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score, kappa_score, auc_score, file=ofile)


# SVM分类器
def SVM(data_train, id_train, data_test, id_test, ofile):
    svm = LinearSVC(random_state=1)
    # svm = SVC(kernel='linear', random_state=1)
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
    precision = precision_score(id_test, id_predict, average='macro')
    recall = recall_score(id_test, id_predict, average='macro')
    fscore = f1_score(id_test, id_predict, average='macro')
    acc_score = accuracy_score(id_test, id_predict)

    kappa_score = cohen_kappa_score(id_test, id_predict)
    fpr, tpr, thresholds = roc_curve(id_test, id_predict, pos_label=5)
    auc_score = auc(fpr, tpr)
    # print('\033[1;31;0mDT:precision:%f, recall:%f, fscore:%f\033[0m' % (precision, recall, fscore))
    print(precision, recall, fscore, acc_score, kappa_score, auc_score, file=ofile)
    # print(classification_report(id_test,id_predict))
    # print(confusion_matrix(id_test,id_predict))

# LR分类器
def LR(data_train, id_train, data_test, id_test, ofile):
    # lr = LogisticRegression(random_state=0, solver='lbfgs',
                            # multi_class='multinomial', penalty='l1')
    lr = LogisticRegression( penalty='l1')
    clf = lr.fit(data_train, id_train)
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
    print(precision, recall, fscore, acc_score, kappa_score, auc_score, file=ofile)


# NB分类器
def NB(data_train, id_train, data_test, id_test, ofile):
    # bayes=GaussianNB()
    bayes=MultinomialNB()
    # bayes = BernoulliNB()
    clf = bayes.fit(data_train, id_train)
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
    print(precision, recall, fscore, acc_score, kappa_score, auc_score, file=ofile)


# MLP分类器
def MLP(data_train, id_train, data_test, id_test, ofile):
    mlp = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(32, 16))
    clf = mlp.fit(data_train, id_train)
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
    print(precision, recall, fscore, acc_score, kappa_score, auc_score, file=ofile)

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

    for split_num in range(5,10):
        ofile = open('./ProcessResult/single_classifer/multi-classifier-'+str(split_num)+'.txt', 'w')
        for i in range(10):
            # 读取进来的全部数据及对应label，shuffle后的结果629条
            trains, labels = process('records.dat', 'disease_tag.dat')
            #给不同切分比例设置相同的test数据
            # split train/test data set
            split = int(len(trains) * 0.9)
            data_test = trains[split:]
            id_test = labels[split:]
            data_train, id_train = get_train_data(trains, labels,split_num)
            print('-------------------------第 %d 组数据------------------------------------------' % i, file=ofile)
            LR(data_train, id_train, data_test, id_test, ofile)
            KNN(data_train, id_train, data_test, id_test, ofile)
            DT(data_train, id_train, data_test, id_test, ofile)
            SVM(data_train, id_train, data_test, id_test, ofile)
            NB(data_train, id_train, data_test, id_test, ofile)
            MLP(data_train, id_train, data_test, id_test, ofile)
            # RF(data_train, id_train, data_test, id_test)
            # AdaBoost(data_train, id_train, data_test, id_test)
            # GradientBoosting(data_train, id_train, data_test, id_test)
        # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$切分情况  %s $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$' % split_num)
