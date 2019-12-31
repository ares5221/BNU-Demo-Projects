#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from utils import save_supplement_data
from download_gaokao_file import download_gaokaowang_page
from download_xueke_file import download_xuekewang_page
from download_zhongguojiaoyu_file import download_jiaoyu_page
from text_analysis import text_content_analysis
import os

def input_key_word():
    website_url_dict = {'gaokaowang': 'http://tiku.gaokao.com/search/type0/',
                        # 'xuekewang': 'http://search.zxxk.com/books/?level=1&kw=',
                        'zhongguojiaoyu': 'http://www.zzstep.com/chuzhong_search.php?key='
                        }
    while True:
        key_word = input('Input Key Word:')
        if True:
            kw = key_word
            curr_save_key_dir = os.path.join('./../data_v2/source', kw)
            if not os.path.exists(curr_save_key_dir):
                os.makedirs(curr_save_key_dir)
            for web_name in website_url_dict:
                curr_website = web_name
                if True:
                    if curr_website == 'gaokaowang':
                        download_gaokaowang_page(kw, website_url_dict[curr_website])
                    elif curr_website == 'xuekewang':
                        download_xuekewang_page(kw, website_url_dict[curr_website])
                    elif curr_website == 'zhongguojiaoyu':
                        download_jiaoyu_page(kw, website_url_dict[curr_website])
                    else:
                        # todo download other web，可以考虑配置信息
                        print('输入网址有误，请确认url信息。')
                        pass

                    print('已经爬取该关键字在目标网站的所有资源', curr_website, '\n\n')
            print('\n \n \n资源爬取完成，开始对文件进行分析并分类...\n \n \n')
            text_content_analysis(kw)


# start
if __name__ == '__main__':
    # main()
    input_key_word()
