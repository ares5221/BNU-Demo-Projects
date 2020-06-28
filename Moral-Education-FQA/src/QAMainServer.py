#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from aiohttp import web
import asyncio
from bertClient import getBestAnswer
import time, os, csv
import json

root_path = os.path.abspath('./../data/')



def is_Chinese(word):
    '''判断是否是汉字'''
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def formatting_question_info(question):
    if len(question) < 3:
        question = '学生' + question + '怎么办？'

    # if '厌学' in question:
    #     question = '孩子厌学'
    # if '打架' in question:
    #     question = '应该怎么处理学生打架的问题？'
    # if '早恋' in question or '谈恋爱' in question:
    #     question = '早恋怎么办？'
    # if '不交作业' in question:
    #     question = '不交作业怎么办？'
    # if '睡觉' in question  or '学生睡觉' in question:
    #     question = '上课睡觉怎么办？'
    print(question)
    return question


async def handle(request):
    '''当前handle question的方法'''
    varDict = request.query
    question = varDict['question']
    question = formatting_question_info(question)
    res1, res2, res3,res4 = getBestAnswer(question)  # 比较余弦相似度查找相似问题
    # ss = {'res1': res1, 'res2': res2}
    forum_reply = str(res1) + ' ' + res2+ ' ' + res3+ ' ' + res4
    print('Query Finished. Current time is:',
          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # return web.json_response(ss)
    return web.Response(text=forum_reply)


async def result(request):
    '''
    save log data
    :param request:
    :return:
    '''
    log_path = root_path + '/log/resultLog.csv'
    varDict = request.query
    question = varDict['question']
    similaryQuestion = varDict['simQue']
    similaryValue = varDict['value']
    curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    news = [question, similaryQuestion, similaryValue, curr_time]
    with open(log_path, 'a', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(news)
    return web.Response(text='回传信息已经保存!')


async def init_app():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/result', result)  # 用来处理回传的情况
    return app

# Start position
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app,port='9002')
