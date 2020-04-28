#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from aiohttp import web
import asyncio
import time, os, csv
import json
from service import gaze_emo

async def handle(request):
    '''当前handle 处理请求,规定用户发送请求及参数
http://172.24.227.247:9010/?question=xxx
"img.png"
    '''
    varDict = request.query
    img_path = varDict['img_path']
    print('The query from url parameter:', img_path)
    res1, res2,res3 =gaze_emo(img_path, mirror_label=True)
    res1 = str(res1)
    res2 = str(res2)
    ss = {'res1': res1,'res2': res2}
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
    web.run_app(app,port='9010')
