#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import xlwt
# 在\MCB-Diff-Prop-2\MCB-55\src\multi-classifier 通过不同切分比例的数据生成的train test数据，然后通过
# 不同的分类器对数据进行分类，将console得到的结果复制保存到 \MCB-Diff-Prop-2\ProcessResultData\多分类结果处理
# 该路径下，通过执行本文件将结果保存在excel中

def readResTxt():
    line_num = 0
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    title = ['Train/Test', 'AdaBoost-LR', 'AdaBoost-NB', 'AdaBoost-DT', 'AdaBoost-SVM', 'Bagging-LR', 'Bagging-NB', 'Bagging-DT', 'Bagging-SVM', 'GradientBoosting', 'RF']
    for ti in range(len(title)):
        sheet1.write(line_num, ti, title[ti])
        
    for fname in os.listdir('.'):
        if fname[-4:] == '.txt':
            with open(fname, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                res_data = lines[2:-2] #去除数据中开头和结尾无效的数据
                count = 0
                sum_Ada_LR_acc = 0
                sum_Ada_NB_acc = 0
                sum_Ada_DT_acc = 0
                sum_Ada_SVM_acc = 0
                sum_Bag_LR_acc = 0
                sum_Bag_NB_acc = 0
                sum_Bag_DT_acc = 0
                sum_Bag_SVM_acc = 0
                sum_GradientBoosting_acc = 0
                sum_RF_acc = 0
                for index in range(len(res_data)):
                    if count <=10:
                        if count ==1:
                            sum_Ada_LR_acc += float(res_data[index].split(' ')[0])
                        if count ==2:
                            sum_Ada_NB_acc += float(res_data[index].split(' ')[0])
                        if count ==3:
                            sum_Ada_DT_acc += float(res_data[index].split(' ')[0])
                        if count ==4:
                            sum_Ada_SVM_acc += float(res_data[index].split(' ')[0])
                        if count ==5:
                            sum_Bag_LR_acc += float(res_data[index].split(' ')[0])
                        if count ==6:
                            sum_Bag_NB_acc += float(res_data[index].split(' ')[0])
                        if count ==7:
                            sum_Bag_DT_acc += float(res_data[index].split(' ')[0])
                        if count ==8:
                            sum_Bag_SVM_acc += float(res_data[index].split(' ')[0])
                        if count ==9:
                            sum_GradientBoosting_acc += float(res_data[index].split(' ')[0])
                        if count ==10:
                            sum_RF_acc += float(res_data[index].split(' ')[0])
                        count += 1
                        if count == 11:
                            count = 0
                avg_AdaLR_acc = sum_Ada_LR_acc /10.0
                avg_AdaNB_acc = sum_Ada_NB_acc/ 10.0
                avg_AdaDT_acc = sum_Ada_DT_acc/ 10.0
                avg_AdaSVM_acc = sum_Ada_SVM_acc /10.0
                avg_BagLR_acc = sum_Bag_LR_acc / 10.0
                avg_BagNB_acc = sum_Bag_NB_acc / 10.0
                avg_BagDT_acc = sum_Bag_DT_acc/ 10.0
                avg_BagSVM_acc = sum_Bag_SVM_acc/ 10.0
                avg_GradientBoosting_acc = sum_GradientBoosting_acc/ 10.0
                avg_RF_acc = sum_RF_acc/ 10.0
                avg_val = [avg_AdaLR_acc, avg_AdaNB_acc, avg_AdaDT_acc, avg_AdaSVM_acc, avg_BagLR_acc, avg_BagNB_acc, avg_BagDT_acc,
                           avg_BagSVM_acc, avg_GradientBoosting_acc, avg_RF_acc]
                line_num +=1
                # 将参数与十次实验结果写入excel
                sheet1.write(line_num, 0, fname[-6:-4])
                for clomus in range(1,11):
                    sheet1.write(line_num, clomus, avg_val[clomus-1])
                res_name = 'multi_classifier_precisoon' + '.xls'
                book.save(res_name)


def readResTxt2():
    line_num = 0
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    title = ['Train/Test', 'AdaBoost-LR', 'AdaBoost-NB', 'AdaBoost-DT', 'AdaBoost-SVM', 'Bagging-LR', 'Bagging-NB',
             'Bagging-DT', 'Bagging-SVM', 'GradientBoosting', 'RF']
    for ti in range(len(title)):
        sheet1.write(line_num, ti, title[ti])

    for fname in os.listdir('.'):
        if fname[-4:] == '.txt':
            with open(fname, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                res_data = lines[2:-2]  # 去除数据中开头和结尾无效的数据
                count = 0
                sum_Ada_LR_acc = 0
                sum_Ada_NB_acc = 0
                sum_Ada_DT_acc = 0
                sum_Ada_SVM_acc = 0
                sum_Bag_LR_acc = 0
                sum_Bag_NB_acc = 0
                sum_Bag_DT_acc = 0
                sum_Bag_SVM_acc = 0
                sum_GradientBoosting_acc = 0
                sum_RF_acc = 0
                for index in range(len(res_data)):
                    if count <= 10:
                        if count == 1:
                            sum_Ada_LR_acc += float(res_data[index].split(' ')[1])
                        if count == 2:
                            sum_Ada_NB_acc += float(res_data[index].split(' ')[1])
                        if count == 3:
                            sum_Ada_DT_acc += float(res_data[index].split(' ')[1])
                        if count == 4:
                            sum_Ada_SVM_acc += float(res_data[index].split(' ')[1])
                        if count == 5:
                            sum_Bag_LR_acc += float(res_data[index].split(' ')[1])
                        if count == 6:
                            sum_Bag_NB_acc += float(res_data[index].split(' ')[1])
                        if count == 7:
                            sum_Bag_DT_acc += float(res_data[index].split(' ')[1])
                        if count == 8:
                            sum_Bag_SVM_acc += float(res_data[index].split(' ')[1])
                        if count == 9:
                            sum_GradientBoosting_acc += float(res_data[index].split(' ')[1])
                        if count == 10:
                            sum_RF_acc += float(res_data[index].split(' ')[1])
                        count += 1
                        if count == 11:
                            count = 0
                avg_AdaLR_acc = sum_Ada_LR_acc / 10.0
                avg_AdaNB_acc = sum_Ada_NB_acc / 10.0
                avg_AdaDT_acc = sum_Ada_DT_acc / 10.0
                avg_AdaSVM_acc = sum_Ada_SVM_acc / 10.0
                avg_BagLR_acc = sum_Bag_LR_acc / 10.0
                avg_BagNB_acc = sum_Bag_NB_acc / 10.0
                avg_BagDT_acc = sum_Bag_DT_acc / 10.0
                avg_BagSVM_acc = sum_Bag_SVM_acc / 10.0
                avg_GradientBoosting_acc = sum_GradientBoosting_acc / 10.0
                avg_RF_acc = sum_RF_acc / 10.0
                avg_val = [avg_AdaLR_acc, avg_AdaNB_acc, avg_AdaDT_acc, avg_AdaSVM_acc, avg_BagLR_acc, avg_BagNB_acc,
                           avg_BagDT_acc,
                           avg_BagSVM_acc, avg_GradientBoosting_acc, avg_RF_acc]
                line_num += 1
                # 将参数与十次实验结果写入excel
                sheet1.write(line_num, 0, fname[-6:-4])
                for clomus in range(1, 11):
                    sheet1.write(line_num, clomus, avg_val[clomus - 1])
                res_name = 'multi_classifier_recall' + '.xls'
                book.save(res_name)


def readResTxt3():
    line_num = 0
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    title = ['Train/Test', 'AdaBoost-LR', 'AdaBoost-NB', 'AdaBoost-DT', 'AdaBoost-SVM', 'Bagging-LR', 'Bagging-NB',
             'Bagging-DT', 'Bagging-SVM', 'GradientBoosting', 'RF']
    for ti in range(len(title)):
        sheet1.write(line_num, ti, title[ti])

    for fname in os.listdir('.'):
        if fname[-4:] == '.txt':
            with open(fname, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                res_data = lines[2:-2]  # 去除数据中开头和结尾无效的数据
                count = 0
                sum_Ada_LR_acc = 0
                sum_Ada_NB_acc = 0
                sum_Ada_DT_acc = 0
                sum_Ada_SVM_acc = 0
                sum_Bag_LR_acc = 0
                sum_Bag_NB_acc = 0
                sum_Bag_DT_acc = 0
                sum_Bag_SVM_acc = 0
                sum_GradientBoosting_acc = 0
                sum_RF_acc = 0
                for index in range(len(res_data)):
                    if count <= 10:
                        if count == 1:
                            sum_Ada_LR_acc += float(res_data[index].split(' ')[2])
                        if count == 2:
                            sum_Ada_NB_acc += float(res_data[index].split(' ')[2])
                        if count == 3:
                            sum_Ada_DT_acc += float(res_data[index].split(' ')[2])
                        if count == 4:
                            sum_Ada_SVM_acc += float(res_data[index].split(' ')[2])
                        if count == 5:
                            sum_Bag_LR_acc += float(res_data[index].split(' ')[2])
                        if count == 6:
                            sum_Bag_NB_acc += float(res_data[index].split(' ')[2])
                        if count == 7:
                            sum_Bag_DT_acc += float(res_data[index].split(' ')[2])
                        if count == 8:
                            sum_Bag_SVM_acc += float(res_data[index].split(' ')[2])
                        if count == 9:
                            sum_GradientBoosting_acc += float(res_data[index].split(' ')[2])
                        if count == 10:
                            sum_RF_acc += float(res_data[index].split(' ')[2])
                        count += 1
                        if count == 11:
                            count = 0
                avg_AdaLR_acc = sum_Ada_LR_acc / 10.0
                avg_AdaNB_acc = sum_Ada_NB_acc / 10.0
                avg_AdaDT_acc = sum_Ada_DT_acc / 10.0
                avg_AdaSVM_acc = sum_Ada_SVM_acc / 10.0
                avg_BagLR_acc = sum_Bag_LR_acc / 10.0
                avg_BagNB_acc = sum_Bag_NB_acc / 10.0
                avg_BagDT_acc = sum_Bag_DT_acc / 10.0
                avg_BagSVM_acc = sum_Bag_SVM_acc / 10.0
                avg_GradientBoosting_acc = sum_GradientBoosting_acc / 10.0
                avg_RF_acc = sum_RF_acc / 10.0
                avg_val = [avg_AdaLR_acc, avg_AdaNB_acc, avg_AdaDT_acc, avg_AdaSVM_acc, avg_BagLR_acc, avg_BagNB_acc,
                           avg_BagDT_acc,
                           avg_BagSVM_acc, avg_GradientBoosting_acc, avg_RF_acc]
                line_num += 1
                # 将参数与十次实验结果写入excel
                sheet1.write(line_num, 0, fname[-6:-4])
                for clomus in range(1, 11):
                    sheet1.write(line_num, clomus, avg_val[clomus - 1])
                res_name = 'multi_classifier_fscore' + '.xls'
                book.save(res_name)


def readResTxt4():
    line_num = 0
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    title = ['Train/Test', 'AdaBoost-LR', 'AdaBoost-NB', 'AdaBoost-DT', 'AdaBoost-SVM', 'Bagging-LR', 'Bagging-NB',
             'Bagging-DT', 'Bagging-SVM', 'GradientBoosting', 'RF']
    for ti in range(len(title)):
        sheet1.write(line_num, ti, title[ti])

    for fname in os.listdir('.'):
        if fname[-4:] == '.txt':
            with open(fname, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                res_data = lines[2:-2]  # 去除数据中开头和结尾无效的数据
                count = 0
                sum_Ada_LR_acc = 0
                sum_Ada_NB_acc = 0
                sum_Ada_DT_acc = 0
                sum_Ada_SVM_acc = 0
                sum_Bag_LR_acc = 0
                sum_Bag_NB_acc = 0
                sum_Bag_DT_acc = 0
                sum_Bag_SVM_acc = 0
                sum_GradientBoosting_acc = 0
                sum_RF_acc = 0
                for index in range(len(res_data)):
                    if count <= 10:
                        if count == 1:
                            sum_Ada_LR_acc += float(res_data[index].split(' ')[3])
                        if count == 2:
                            sum_Ada_NB_acc += float(res_data[index].split(' ')[3])
                        if count == 3:
                            sum_Ada_DT_acc += float(res_data[index].split(' ')[3])
                        if count == 4:
                            sum_Ada_SVM_acc += float(res_data[index].split(' ')[3])
                        if count == 5:
                            sum_Bag_LR_acc += float(res_data[index].split(' ')[3])
                        if count == 6:
                            sum_Bag_NB_acc += float(res_data[index].split(' ')[3])
                        if count == 7:
                            sum_Bag_DT_acc += float(res_data[index].split(' ')[3])
                        if count == 8:
                            sum_Bag_SVM_acc += float(res_data[index].split(' ')[3])
                        if count == 9:
                            sum_GradientBoosting_acc += float(res_data[index].split(' ')[3])
                        if count == 10:
                            sum_RF_acc += float(res_data[index].split(' ')[3])
                        count += 1
                        if count == 11:
                            count = 0
                avg_AdaLR_acc = sum_Ada_LR_acc / 10.0
                avg_AdaNB_acc = sum_Ada_NB_acc / 10.0
                avg_AdaDT_acc = sum_Ada_DT_acc / 10.0
                avg_AdaSVM_acc = sum_Ada_SVM_acc / 10.0
                avg_BagLR_acc = sum_Bag_LR_acc / 10.0
                avg_BagNB_acc = sum_Bag_NB_acc / 10.0
                avg_BagDT_acc = sum_Bag_DT_acc / 10.0
                avg_BagSVM_acc = sum_Bag_SVM_acc / 10.0
                avg_GradientBoosting_acc = sum_GradientBoosting_acc / 10.0
                avg_RF_acc = sum_RF_acc / 10.0
                avg_val = [avg_AdaLR_acc, avg_AdaNB_acc, avg_AdaDT_acc, avg_AdaSVM_acc, avg_BagLR_acc, avg_BagNB_acc,
                           avg_BagDT_acc,
                           avg_BagSVM_acc, avg_GradientBoosting_acc, avg_RF_acc]
                line_num += 1
                # 将参数与十次实验结果写入excel
                sheet1.write(line_num, 0, fname[-6:-4])
                for clomus in range(1, 11):
                    sheet1.write(line_num, clomus, avg_val[clomus - 1])
                res_name = 'multi_classifier_acc_score' + '.xls'
                book.save(res_name)


if __name__ == '__main__':
    readResTxt()
    readResTxt2()
    readResTxt3()
    readResTxt4()
    print('save accuracy_score in excel success')