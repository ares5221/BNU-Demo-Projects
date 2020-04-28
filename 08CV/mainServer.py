#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from aiohttp import web
import asyncio
import time, os, csv
import json


async def handle(request):
    '''当前handle 处理请求,规定用户发送请求及参数
http://172.24.227.247:9010/?question=xxx
    '''
    varDict = request.query
    question = varDict['question']
    print('The query from url parameter:', question)
    
	# 这里调用你的python项目的方法，对java输入的请求做处理即可
    res1 = youFunc(question) 


    ss = {'res1': res1}
    print('Finish！Current time is:',
          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    return web.json_response(ss)


async def init_app():
    app = web.Application()
    app.router.add_get('/', handle)
    return app

# Start position
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app,port='9010')# 这里设置你的服务端口，如果你要在我们的247服务器的话可以用这个9010
