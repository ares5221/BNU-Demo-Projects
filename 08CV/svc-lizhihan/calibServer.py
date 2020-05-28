#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from aiohttp import web
import asyncio
import time, os
import json
from calibration import calib
import requests


async def handle(request):
    '''当前handle 处理请求,规定用户发送请求及参数
http://172.24.227.247:9011/?str=xxx
    '''
    varDict = request.query
    calib_str = varDict['str']
    # calib_str = download_pic(calib_str)
    print('calib_str:', calib_str)
    res1, res2 = calib(calib_str)
    res1 = str(res1)
    res2 = str(res2)
    if not res1 or not res2:
        ss = {'res1': 'res1 is none', 'res2': 'res2 is none'}
    if res1 and res2:
        ss = {'res1': res1, 'res2': res2}
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
    web.run_app(app, port='9011')
