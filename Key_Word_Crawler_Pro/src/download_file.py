#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import requests
import wget
import time
from bs4 import BeautifulSoup
import shutil


def download_with_requests(url, file_name):
    base_dir = './../crawler_data'
    save_path = os.path.join(base_dir, file_name)
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(save_path):
        ss = requests.get(url)
        with open(save_path, 'wb') as f:
            f.write(ss.content)
        print(file_name, ' 该文件下载完成 ', 'curr time----> :', curr_time)
    else:
        print(file_name, ' 文件已经存在 ', 'curr time----> :', curr_time)


def download_with_wget(file_name, url, key):
    base_dir = './../crawler_data/source'
    save_dir = os.path.join(base_dir, key)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # filename = wget.download(url, out=save_dir) # 可以直接指定输出路径，但是不确定文件后缀类型
    filename = wget.download(url)  # 中文文件名会出现乱码，但是可以知道文件类型[tiku.gaokao.com]é«ä¿ç»ä¹ .doc
    filename = filename.replace('|', '')
    time.sleep(3)
    suffix_type = '.zip'
    print(filename, suffix_type)
    file_name += suffix_type
    save_path = os.path.join(save_dir, file_name)

    curr_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(save_path):
        try:
            os.rename(filename, save_path)
        except:
            pass
        print(file_name, ' 该文件下载完成 ', 'curr time----> :', curr_time)
    else:
        print(file_name, ' 文件已经存在 存储在backup', 'curr time----> :', curr_time)
        # del_dir = os.path.join('./../crawler_data/backup', filename)
        # shutil.move(filename, del_dir)


def download_file_use_middle_website(search_key, titles, middle_websites):
    download_website = []
    if len(middle_websites) < 1:
        print('获取的中间网页信息有误，请查看网址')
        return
    for curr_url in middle_websites:
        response = requests.get(curr_url)
        web_page = response.content
        soup = BeautifulSoup(web_page, 'html.parser')
        download_info = soup.find_all('a', class_="download lm10 op8")
        for dlw in download_info:
            download_website.append(dlw.get('href'))
    for index in range(len(titles)):
        download_with_wget(titles[index], download_website[index], search_key)


def download_good_kejian_middle_website(search_key, titles, middle_websites):
    download_website = []
    url_base = 'http://www.goodkejian.com'
    if len(middle_websites) < 1:
        print('获取的中间网页信息有误，请查看网址')
        return
    for curr_url in middle_websites:
        response = requests.get(curr_url)
        web_page = response.content
        soup = BeautifulSoup(web_page, 'html.parser')
        download_info = soup.find_all('div', id='soft_zhulixiazai')
        for tmp1 in download_info:
            tmp2 = tmp1.find_all('li')[0]
            for a in tmp2.find_all('a', href=True):
                if a.get_text(strip=True):
                    print(url_base + a['href'][2:])
                    download_website.append(url_base + a['href'][2:])
    for index in range(len(titles)):
        download_with_wget(titles[index], download_website[index], search_key)
        # download_with_requests(download_website[index], titles[index])


if __name__ == '__main__':
    url = 'http://tiku.gaokao.com/download/type6/id7483'
    file_name = '高中生物必修1光合作用同步练习1.docx'
    # test this Func
    download_with_requests(url, file_name)
    # download_with_wget(url, file_name)
