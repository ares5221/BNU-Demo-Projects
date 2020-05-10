import xlrd, xlwt
import xlutils.copy
import os
import time

math_path = './../../data_source/math_source0409.xls'
chinese_path = './../../data_source/chinese_source0409.xls'
physical_path = './../../data_source/physical_source0422.xls'
history_path = './../../data_source/history_source0422.xls'
english_path = './../../data_source/english_source0429.xls'

math_target_path = './../../data_split/math_split0409.xls'
chinese_target_path = './../../data_split/chinese_split0409.xls'
physical_target_path = './../../data_split/physical_split0422.xls'
history_target_path = './../../data_split/history_split0422.xls'
english_target_path = './../../data_split/english_split0429.xls'

def split(src_path, tar_path):
    rb = xlrd.open_workbook(src_path)

    wb = xlutils.copy.copy(rb)
    table_1 = rb.sheets()[0]
    table_2 = wb.add_sheet('套题')
    table_3 = wb.add_sheet('正常')
    table_4 = wb.add_sheet('不正常')

    j = 0
    pre_not_null_kind = None
    # 提取套题
    for i in range(2, table_1.nrows):
        row = table_1.row_values(i)
        kind = row[1]
        if kind != '':
            pre_not_null_kind = kind

        if kind == '套题':
            for a in range(18):
                table_2.write(j, a, row[a])
            j += 1
        if kind == '' and pre_not_null_kind == '套题':
            for a in range(18):
                table_2.write(j, a, row[a])
            j += 1

    # 不正常多行题目
    j = 0
    pre_not_null_kind = None

    for i in range(2, table_1.nrows - 1):
        row = table_1.row_values(i)
        kind = row[1]

        if kind == '套题':
            pre_not_null_kind = kind

        if kind != '套题' and kind != '' and table_1.row_values(i + 1)[1] == '':
            for a in range(18):
                table_4.write(j, a, row[a])
            j += 1
            pre_not_null_kind = kind

        if kind == '' and pre_not_null_kind != '套题':
            for a in range(18):
                table_4.write(j, a, row[a])
            j += 1

    # 正常题目
    k = 0
    pre_row = table_1.row_values(1)
    for i in range(2, table_1.nrows):
        row = table_1.row_values(i)
        kind = row[1]
        if kind != '' and pre_row[1] != '' and pre_row[1] != '套题':
            for a in range(18):
                table_3.write(k, a, pre_row[a])
            k += 1
        pre_row = row
    wb.save(tar_path)


if __name__ == '__main__':
    print(os.path.abspath('.'))
    print('start split...')
    # deal math
    split(math_path, math_target_path)
    # deal chinese
    # split(chinese_path, chinese_target_path)
    # deal physical
    # split(physical_path, physical_target_path)
    # deal history
    # split(history_path, history_target_path)
    # deal english
    # split(english_path, english_target_path)
    print('end split. ')
    print('curr time: ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
