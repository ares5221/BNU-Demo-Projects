#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import xlwt


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
    print('data count:', len(parameters), len(res), len(avgs))
    print(parameters)
    print(res)
    print(avgs)
    return parameters, res, avgs


def write_para_res(parameters, res, i):
    #将参数与十次实验结果写入excel
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    for index in range(len(parameters)):
        sheet1.write(index * 10, 0, parameters[index][0].split('| ')[1])
        for second in range(10):
            for ls in range(3):
                sheet1.write(index *10 + second, ls+1, res[index *10 + second][ls])
    res_name = 'parameter_result' + str(i) + '.xls'
    book.save(res_name)


def write_para_ave(parameters, avgs, i):
    # 将参数与十次实验的平均结果写入excel
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    for index in range(len(parameters)):
        para = parameters[index][0].split('| ')[1].split(',')
        for lp in range(len(para)):
            sheet1.write(index, lp, para[lp])
        for ls in range(3):
            sheet1.write(index, ls+5, avgs[index][ls])
    avgs_name = 'parameter_avgs' + str(i) + '.xls'
    book.save(avgs_name)


if __name__ == '__main__':
    for i in range(1,6):
        parameters, res, avgs = readtest(i)
        write_para_res(parameters, res, i)
        write_para_ave(parameters, avgs, i)

