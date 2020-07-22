#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv
import xlrd


def read_data(data_path):
    workbook = xlrd.open_workbook(data_path)
    sheet = workbook.sheet_by_index(4)  # 索引的方式，从0开始
    print(sheet.name, sheet.nrows, sheet.ncols)  # 获取当前sheet页的名称，行数，列数，都从1开始
    id_idx = 0
    for row in range(4, sheet.nrows):
        id = sheet.cell(row, id_idx).value
        print(id)
        case_explain = get_explain(sheet, row)
        write_csv(id,case_explain)


def write_csv(id,content):
    with open('case_exolain.csv', 'a', encoding='utf-8', newline='') as csv_write:
        f_csv = csv.writer(csv_write)
        f_csv.writerow([id,content])



def get_explain(sheet, row):
    problem_behavie = get_problem_behavie(sheet, row)
    healty_status = get_healty_status(sheet, row)
    social_group = get_social_group(sheet, row)
    famaly_type = get_famaly_type(sheet, row)
    edu_type = get_edu_type(sheet, row)
    eco_type = get_eco_type(sheet, row)
    clutre_type = get_clutre_type(sheet, row)
    crime_type = get_crime_type(sheet, row)
    company_type = get_company_type(sheet, row)
    demand_type = get_demand_type(sheet, row)
    solution_type = get_solution(sheet, row)

    content = content_compose(problem_behavie, healty_status, social_group, famaly_type, edu_type, eco_type,
                              clutre_type, crime_type, company_type, demand_type, solution_type)
    return content


def content_compose(problem_behavie, healty_status, social_group, famaly_type, edu_type, eco_type, clutre_type,
                    crime_type, company_type, demand_type, solution_type):
    content = '本案例中教师通过了解学生存在的'
    pb = ''
    for pb_idx in range(len(problem_behavie)):
        if pb_idx < len(problem_behavie) - 1:
            pb += problem_behavie[pb_idx] + '、'
        else:
            pb += problem_behavie[pb_idx] + '等问题行为，开始调查学生出现问题行为可能存在的内外部影响因素，案例中的学生'
    content += pb
    if healty_status and healty_status[0]:
        content += '有' + healty_status[0] + '；'
    if social_group and social_group[0]:
        content += '属于' + social_group[0] + '；'
    if famaly_type and famaly_type[0]:
        content += '所在的家庭是' + famaly_type[0] + '；'
    if edu_type and edu_type[0]:
        content += '家庭教养方式不良，属于' +edu_type[0] +'；'
    if eco_type and eco_type[0]:
        content += eco_type[0] +'；'
    if clutre_type and clutre_type[0]:
        content += clutre_type[0] + '；'
    if crime_type and crime_type[0]:
        content += crime_type[0] + '；'
    if company_type and company_type[0]:
        content += '同伴接纳处于' + company_type[0] + '的状态等。'
    content += '基于已经收集到的相关影响因素，教师综合分析发现学生可能是由于'
    if demand_type:
        content += demand_type[0] +'而出现一系列的问题行为，针对综合的因素，教师采取了'
    if solution_type:
        content += solution_type[0] +'等育人措施以满足学生的心理需求，矫正学生的问题行为。'
    print(content)

    return content


def get_problem_behavie(sheet, row_idx):
    problem_behavie = []
    for col in range(2, 10):
        curr = sheet.cell(row_idx, col).value
        if curr:
            if '，' in curr:
                curr = curr.split('，')
                problem_behavie += curr
            else:
                problem_behavie.append(curr)
    if not problem_behavie:
        # 防止问题行为为空
        problem_behavie.append('注意力问题')
    # print(problem_behavie)
    return problem_behavie


def get_healty_status(sheet, row):
    healty_status = []
    curr = sheet.cell(row, 12).value
    if curr:
        healty_status.append(curr.replace('健康', ''))
    return healty_status


def get_social_group(sheet, row):
    social_group = []
    curr = sheet.cell(row, 13).value
    if curr:
        social_group.append(curr.replace('一般儿童', ''))
    return social_group


def get_famaly_type(sheet, row):
    famaly_type = []
    curr = sheet.cell(row, 21).value
    if curr:
        famaly_type.append(curr.replace('完整家庭', ''))
    return famaly_type


def get_edu_type(sheet, row):
    edu_type = []
    curr = sheet.cell(row, 22).value
    if curr:
        edu_type.append(curr.replace('教养方式', ''))
    return edu_type


def get_eco_type(sheet, row):
    eco_type = []
    curr = sheet.cell(row, 27).value
    if curr:
        eco_type.append('家庭经济' + curr)
    return eco_type


def get_clutre_type(sheet, row):
    clutre_type = []
    curr = sheet.cell(row, 25).value
    if curr:
        clutre_type.append('家庭成员' + curr)
    return clutre_type


def get_crime_type(sheet, row):
    crime_type = []
    curr = sheet.cell(row, 28).value
    if curr:
        crime_type.append('家庭成员存在不良行为')
    return crime_type


def get_company_type(sheet, row):
    company_type = []
    curr = sheet.cell(row, 34).value
    if curr:
        company_type.append(curr)
    if not company_type:
        # 防止问题行为为空
        company_type.append('被忽视')
    return company_type


def get_demand_type(sheet, row):
    demand_type = []
    curr = sheet.cell(row, 38).value
    if curr:
        demand_type.append(curr)
    if not demand_type:
        # 防止为空
        demand_type.append('缺少正确教育引导')
    return demand_type


def get_solution(sheet, row):
    solution_type = []
    curr = sheet.cell(row, 39).value
    if curr:
        solution_type.append(curr)
    if not solution_type:
        # 防止为空
        solution_type.append('主动谈心说服')
    return solution_type


if __name__ == '__main__':
    print('start read excel data...')
    read_data('./data.xlsx')
    print('end...')
