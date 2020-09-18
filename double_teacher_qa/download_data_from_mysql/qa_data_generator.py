import json
import re
from collections import Counter
import pymysql

def read_data(sub):
    # 打开数据库连接
    conn = pymysql.connect('172.18.136.94', 'readuser', 'gaojj2019', 'fep-tuoming')
    
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()      # 游标对象用于执行查询和获取结果
    
    # 使用execute()方法执行SQL，如果表存在则将其删除
    sql = 'SELECT * FROM t_partner_question WHERE status = \'resolved\' AND course = \'{}\';'.format(sub.upper())
    cursor.execute(sql)

    # print(type(result), result)

    # csv_file = csv.writer(codecs.open('./data.csv' ,'w','utf_8_sig'),dialect ='excel')
    # csv_file.writerow(['用户名','密码','验证码','结果'])
    # csv_file.writerow(data)

    # question = open('./question.txt','w')
    question = open(sub+'_original','w',encoding='utf-8')

    for x in cursor.fetchall():
        # print(len(x), x)

        # csv_file.writerow(x)
        # x[0]: question_id
        # x[2]: title
        # x[3]: content
        # x[7]: course
        # x[9]: status
        # x[30]: question type
        # if x[9] == 'resolved' and x[7] == 'CN':
        print(x[30])
        qtype = json.loads(x[30])[0]['name'] if x[30] != None else '不确定'
        # qtype = x[30] if x[30] != None else '不确定'
        # if x[22] != None:
        #     qtype = json.loads(x[22])
        print(x[0], x[2].replace('\n', ' '), x[3].replace('\n', ' '), qtype, sep='\t', file=question)

    
    # 关闭数据库连接
    conn.close()

def check_question_type(sub):
    # 打开数据库连接
    conn = pymysql.connect('172.18.136.94', 'readuser', 'gaojj2019', 'fep-tuoming')
    
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()      # 游标对象用于执行查询和获取结果
    
    # 使用execute()方法执行SQL，如果表存在则将其删除
    sql = 'SELECT distinct(question_type) FROM t_partner_question WHERE course = \'{}\';'.format(sub)
    cursor.execute(sql)

    # print(type(result), result) 

    # csv_file = csv.writer(codecs.open('./data.csv' ,'w','utf_8_sig'),dialect ='excel')
    # csv_file.writerow(['用户名','密码','验证码','结果'])
    # csv_file.writerow(data)

    # question = open('./question.txt','w')
    # question = open(sub+'_question_type','w')
    q_raw = open(sub+'_question_type_original','w',encoding='utf-8')

    # all_types = set()
    all_types = []
    for x in cursor.fetchall():
        print(x[0])
        if x[0] != None:
            qtype = json.loads(x[0])
            # print(qtype, file=q_raw)
            all_types.append(qtype)
            # for item in qtype:
                # all_types.add(item['name'])
                # all_types.append(item)
            # print(x[0], x[2].replace('\n', ' '), x[3].replace('\n', ' '), qtype, sep='\t', file=question)

    # for t in all_types:
        # print(t, file=question)
    json.dump(all_types, q_raw, ensure_ascii=False, indent=4)
    # 关闭数据库连接
    conn.close()


def process_question_type(sub):
    data = json.load(open(sub+'_question_type_original',encoding='utf-8'))

    type1 = {}
    type2 = []
    for record in data:
        for item in record:
            code = item['code']
            name = item['name']
            if code in type1:
                type1[code].add(name)
            else:
                type1[code] = {name}
            type2.append(name)
    type3 = Counter(type2)
    type4 = set(type2)


    s2 = '[^\u4e00-\u9fa5]+'
    r2 = re.compile(s2)
    type5 = [r2.sub('', x) for x in type4]
    type5 = [x for x in set(type5) if x]
    
    ofile = open(sub+'_question_type', 'w',encoding='utf-8')
    for x in type5:
        print(x, file=ofile)
    # print(type2)


def clean_sentence(str_in):
    # step 1: remove unnecessary prefix
    # str1 = '2018年石景山区中考语文一模说明文'
    # str1 = '2017-2018语文终结性期末试卷'
    str1 = str_in
    s1 = '[0-9]*.*(模|卷|中考|考试|期末)'
    r1 = re.compile(s1)
    str1 = r1.sub('', str1)
    # print(str1)

    # step 2: punctuation
    # s2 = '[^0-9A-Za-z\u4e00-\u9fa5]+'
    s2 = '[^0-9\u4e00-\u9fa5]+'
    r2 = re.compile(s2)
    str1 = r2.sub('', str1)

    # step 3: 
    s3 = '(谢|在线求解|请|老师们|老师|帮忙一下|看一下|求助|不会|求解|各位|帮忙|辛苦|您好|麻烦)'
    r3 = re.compile(s3)
    str1 = r3.sub('', str1)

    # step 4:
    s4 = '[，。？！,.?!]*'
    r4 = re.compile(s4)
    str1 = r4.sub('', str1)

    return str1

def check_validity(line):
    line = line.strip()
    # valid = True
    if len(line) < 10:
        return False


    # step 1: check subject
    # when subject is cn
    wlist = ['方程', '函数','通知', '版本', '物理', '化学', '生物', '数学', '英语', '地理', '几何']
    # when subject is ma
    wlist = ['通知', '版本', '物理', '化学', '生物', '英语', '地理' ]
    for x in wlist:
        if x in line:
            # valid = False
            # break
            return False

    # step 2: check repetition
    chars = Counter(line)
    for x in chars:
        if chars[x]>0.5*len(chars): #and chars[x]/len(str1) > 0.2:
            # print(str1, file=ofile)
            # valid = False
            # break
            return False
    return True

def generate_question_clean(sub):
    result = []
    ofile = open(sub+'_clean_valid', 'w',encoding='utf-8')
    # ofile2 = open('repeated', 'w')
    ofile3 = open(sub+'_invalid', 'w',encoding='utf-8')
    for line in open(sub+'_original', encoding='utf-8'):
        line = line.strip()
        items = line.split('\t')
        if len(items) < 4:
            print(line)
            continue
        a = items[1]
        b = items[2]
        a = clean_sentence(a)
        b = clean_sentence(b)
        if a and b and b[:len(a)] == a:
            # print(a, b, file=ofile3)
            b = b[len(a):]
        if check_validity(a+b):
            # print(items[0], a, b, items[3], sep='\t', file=ofile)
            record = {'question_id': items[0], 'question_title_original': items[1], 'question_content_original': items[2], 'question_type': items[3],
                        'question_title_clean': a, 'question_content_clean': b }
            result.append(record)
        else:
            print(line, file=ofile3)


    json.dump(result, ofile, ensure_ascii=False, indent=4)


def retrieve_answer(sub):
    result = []
    # 打开数据库连接
    conn = pymysql.connect('172.18.136.94', 'readuser', 'gaojj2019', 'fep-tuoming')
    
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()      # 游标对象用于执行查询和获取结果
    
    # 使用execute()方法执行SQL，如果表存在则将其删除
    # cursor.execute(sql)

    for record in json.load(open(sub+'_clean_valid',encoding='utf-8')):
        # line = line.strip()
        # items = line.split('\t')
        sql = 'SELECT * FROM t_partner_answer WHERE question_id = \'{}\' AND is_accepted=1'.format(record['question_id'])
        print(sql)
        cursor.execute(sql)
        for x in cursor.fetchall():
            print([x[4], x[-1]])
            # print(x[x-1])
            # record = {'question_id': items[0], 'question_title': items[1], 'question_content': items[2], 'question_type': items[3],
            #            'answer_content': x[4] }
            record['answer_content'] = x[4]
            if x[-1] and x[-1] != x[4]:
                record['answer_idea'] = x[-1]
            result.append(record)
        print()
    
    json.dump(result, open(sub+'_qa_data.txt', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


def start():
    # 已经处理的科目包括cn 语文，ma 数学
    sub = 'ma'
    # read_data(sub)
    # check_question_type(sub)
    # process_question_type(sub)
    # generate_question_clean(sub)
    retrieve_answer(sub)


if __name__ == '__main__':
    start()
