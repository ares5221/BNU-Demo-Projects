#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import xlwt
# 在src\multi-classifier 通过不同切分比例的数据生成的train test数据，然后通过
# 不同的分类器对数据进行分类，将console得到的结果复制保存到该路径下，通过执行本文件将结果保存在excel中

def readResTxt():
    line_num = 0
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    title = ['Train/Test', 'DT', 'KNN', 'SVM', 'LR', 'NB', 'RF', 'AdaBoost', 'GradientBoosting']
    for ti in range(len(title)):
        sheet1.write(line_num, ti, title[ti])
    for fname in os.listdir('.'):
        if fname[-4:] == '.txt':
            with open(fname, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                res_data = lines[2:-2] #去除数据中开头和结尾无效的数据
                # print(res_data)
                count = 0
                sum_DT_acc = 0
                sum_KNN_acc = 0
                sum_SVM_acc = 0
                sum_LR_acc = 0
                sum_NB_acc = 0
                sum_RF_acc = 0
                sum_AdaBoost_acc = 0
                sum_GradientBoosting_acc = 0
                for index in range(len(res_data)):
                    if count <=8:
                        if count ==1:
                            sum_DT_acc += float(res_data[index].split(' ')[3])
                        if count ==2:
                            sum_KNN_acc += float(res_data[index].split(' ')[3])
                        if count ==3:
                            sum_SVM_acc += float(res_data[index].split(' ')[3])
                        if count ==4:
                            sum_LR_acc += float(res_data[index].split(' ')[3])
                        if count ==5:
                            sum_NB_acc += float(res_data[index].split(' ')[3])
                        if count ==6:
                            sum_RF_acc += float(res_data[index].split(' ')[3])
                        if count ==7:
                            sum_AdaBoost_acc += float(res_data[index].split(' ')[3])
                        if count ==8:
                            sum_GradientBoosting_acc += float(res_data[index].split(' ')[3])
                        count += 1
                        if count == 9:
                            count = 0
                avg_DT_acc = sum_DT_acc /10.0
                avg_KNN_acc = sum_KNN_acc/ 10.0
                avg_SVM_acc = sum_SVM_acc/ 10.0
                avg_LR_acc = sum_LR_acc /10.0
                avg_NB_acc = sum_NB_acc / 10.0
                avg_RF_acc = sum_RF_acc / 10.0
                avg_AdaBoost_acc = sum_AdaBoost_acc/ 10.0
                avg_GradientBoosting_acc = sum_GradientBoosting_acc/ 10.0
                avg_val = [avg_DT_acc, avg_KNN_acc, avg_SVM_acc, avg_LR_acc, avg_NB_acc, avg_RF_acc, avg_AdaBoost_acc, avg_GradientBoosting_acc]
                line_num +=1
                # 将参数与十次实验结果写入excel
                sheet1.write(line_num, 0, fname[-6:-4])
                for clomus in range(1,9):
                    sheet1.write(line_num, clomus, avg_val[clomus-1])
                res_name = 'multi_classifier_result' + '.xls'
                book.save(res_name)


if __name__ == '__main__':
    readResTxt()
    print('save accuracy_score in excel success')