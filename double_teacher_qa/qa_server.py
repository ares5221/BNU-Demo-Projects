#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from aiohttp import web
import asyncio
from BERTFineTuningClient import sorl_bert_finetuning_query
import time, os, csv
from utils import replace_punctuation
import datetime
import sys
import json
from BERTFineTuningClient import solr_only
from math_BERTFineTuningClient import math_sorl_bert_finetuning_query
from math_BERTFineTuningClient import math_solr_only

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(os.path.split(rootPath)[0])


async def cn_handle(request):
    '''
    handle chinese query
    :param request:
    :return:
    '''
    start_time = time.time()
    query = request.query['query']
    question = replace_punctuation(query)
    response_json = sorl_bert_finetuning_query(question)
    reply = json.dumps(response_json, ensure_ascii=False, indent=4)
    forumQA_log_save(question, response_json)
    print('查询结束， Current time is:',
          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ' 耗时:', time.time() - start_time)
    return web.Response(text=reply)


async def cn_solr_only_handle(request):
    '''
    handle chinese query with solr only
    :param request:
    :return:
    '''
    start_time = time.time()
    query = request.query['query']
    question = replace_punctuation(query)
    response_json = solr_only(question)
    reply = json.dumps(response_json, ensure_ascii=False, indent=4)
    forumQA_log_save(question, response_json)
    print('查询结束， Current time is:',
          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ' 耗时:', time.time() - start_time)
    return web.Response(text=reply)


def forumQA_log_save(query, response_json):
    '''
    log save
    :param query:
    :param response_json:
    :return:
    '''
    curr_data = datetime.datetime.now().strftime('%Y_%m_%d')
    log_save_path = os.path.join('./../log_save/', 'log_' + str(curr_data) + '.csv')
    if not os.path.exists('./../log_save/'):
        os.makedirs('./../log_save/')
    if not os.path.exists(log_save_path):
        with open(log_save_path, "a", newline="", encoding='utf-8') as csv_write:
            spamwriter = csv.writer(csv_write)
            spamwriter.writerow(["query", "FQA_replay", "response_time", ])

    with open(log_save_path, "a", newline="", encoding='utf-8') as csv_write:
        spamwriter = csv.writer(csv_write)
        spamwriter.writerow(
            [query, str(response_json), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))])


async def ma_handle(request):
    '''
    todo handle math query
    :param request:
    :return:
    '''
    start_time = time.time()
    query = request.query['query']
    question = replace_punctuation(query)
    # todo
    response_json= math_sorl_bert_finetuning_query(question)
    reply = json.dumps(response_json, ensure_ascii=False, indent=4)
    forumQA_log_save(query, response_json)
    print('查询结束， Current time is:',
          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ' 耗时:', time.time() - start_time)
    return web.Response(text=reply)


async def ma_solr_only_handle(request):
    '''
    handle chinese query with solr only
    :param request:
    :return:
    '''
    start_time = time.time()
    query = request.query['query']
    question = replace_punctuation(query)
    response_json = math_solr_only(question)
    reply = json.dumps(response_json, ensure_ascii=False, indent=4)
    forumQA_log_save(question, response_json)
    print('查询结束， Current time is:',
          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ' 耗时:', time.time() - start_time)
    return web.Response(text=reply)


async def init_app():
    app = web.Application()
    app.router.add_get('/chinese', cn_handle)
    app.router.add_get('/chinese/solr_only', cn_solr_only_handle)
    app.router.add_get('/math', ma_handle)
    app.router.add_get('/math/solr_only', ma_solr_only_handle)
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, port='9099')
