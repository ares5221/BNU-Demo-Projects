#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import xlwt

'''
生成三个单独的excel表格，存储acc, avg turn

'''
def readtest(index):
    resname = 'test' + str(index) + '.txt'
    parameters = []
    res = []
    avgs = []
    with open(resname, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        count = 0
        sum_simulationSR =0
        sum_reward =0
        sum_turns =0
        for line in lines:
            if line.startswith('Paramaters'):
                parameters.append([line])
            else:
                tmp = (line.split(':')[1]).split(' ')
                res.append([tmp[0], tmp[1], tmp[2]])
                count +=1
                if count <= 10:
                    sum_simulationSR += float(tmp[0])
                    sum_reward += float(tmp[1])
                    sum_turns += float(tmp[2])
                if count == 10:
                    ave_simulationSR = sum_simulationSR/10.0
                    ave_reward = sum_reward/10.0
                    ave_turns = sum_turns /10.0
                    avgs.append([ave_simulationSR, ave_reward, ave_turns])
                    count = 0
                    sum_simulationSR = 0
                    sum_reward = 0
                    sum_turns = 0
    # print('data count:', len(parameters), len(res), len(avgs))
    # print(parameters)
    # print(res)
    # print(avgs)
    return parameters, res, avgs

line = [256,128,64,32,16,8]
rows = ['实验一5-5', '实验二6-4', '实验三7-3', '实验四8-2', '实验五9-1']
def write_simulationSR_ave(data):
    # 将五组实验的平均结果存在excel
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    sheet1.write(0, 0, 'SR_ave')
    for i in range(len(line)):
        sheet1.write(i+1, 0, line[i])
    for j in range(len(rows)):
        sheet1.write(0, j+1, rows[j])

    for index in range(len(data)):
        for sr in range(len(data[0])):
            sheet1.write(sr+1, index+1, data[index][sr][0])
    avgs_name = '1simulationSR_avgs' + '.xls'
    book.save(avgs_name)


def write_reward_ave(data):
    # 将五组实验的平均结果存在excel
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    sheet1.write(0, 0, 'reward_ave')
    for i in range(len(line)):
        sheet1.write(i + 1, 0, line[i])
    for j in range(len(rows)):
        sheet1.write(0, j + 1, rows[j])
    for index in range(len(data)):
        for sr in range(len(data[0])):
            sheet1.write(sr+1, index+1, data[index][sr][1])
    avgs_name = '2reward_avgs' + '.xls'
    book.save(avgs_name)


def write_turns_ave(data):
    # 将五组实验的平均结果存在excel
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    sheet1.write(0, 0, 'SR_ave')
    for i in range(len(line)):
        sheet1.write(i + 1, 0, line[i])
    for j in range(len(rows)):
        sheet1.write(0, j + 1, rows[j])
    for index in range(len(data)):
        for sr in range(len(data[0])):
            sheet1.write(sr+1, index+1, data[index][sr][2])
    avgs_name = '3turns_avgs' + '.xls'
    book.save(avgs_name)


if __name__ == '__main__':
    all_avgs = []
    for i in range(1,6):
        parameters, res, avgs = readtest(i)
        all_avgs.append(avgs)
    print(all_avgs)
    print(len(all_avgs), len(all_avgs[0]), len(all_avgs[0][0]))
    write_simulationSR_ave(all_avgs)
    write_reward_ave(all_avgs)
    write_turns_ave(all_avgs)
        # write_para_ave(parameters, avgs, i)

