#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from aiohttp import web
import asyncio
import time, os, csv
import json
from service import gaze_emo
import requests

async def handle(request):
    '''当前handle 处理请求,规定用户发送请求及参数
http://172.24.227.247:9010/?question=xxx
"img.png"
    '''
    varDict = request.query
    img_path = varDict['img_path']
    img_path = download_pic(img_path)
    print('img path:',img_path)
    res1, res2,res3 =gaze_emo(img_path, mirror_label=True)
    res1 = str(res1)
    res2 = str(res2)
    if not res1 or not res2:
        ss = {'res1': 'res1 is none','res2': 'res2 is none'}
    if res1 and res2:
        ss = {'res1': res1,'res2': res2}
    print('Finish！Current time is:',
          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    return web.json_response(ss)


def download_pic(pic_url):
    pic_dir = './pic/'
    if str(pic_url).startswith('http'):
        pic_name = pic_url.split('/')[-1]
        try:
            print('pic url :', pic_url)
            pic = requests.get(pic_url, timeout=5)
            with open(pic_dir + pic_name, 'wb') as f:
                f.write(pic.content)
        except Exception as e:
            print('下载图片失败: %s' % (str(pic_url)))
            print(e)

    else:
        pic_name = pic_url

    return os.path.join(pic_dir + pic_name)



async def init_app():
    app = web.Application()
    app.router.add_get('/', handle)
    return app

# Start position
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app,port='9010')
