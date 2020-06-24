#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from utils import save_supplement_data
from download_gaokao_file import download_gaokaowang_page
from download_xueke_file import download_xuekewang_page
from download_zhongguojiaoyu_file import download_jiaoyu_page
from download_haokejian_file import download_haokejian_page
from text_analysis import text_content_analysis
import os


def input_key_word():
    website_url_dict = {
        # 'xuekewang_xiaoxue': 'http://search.zxxk.com/books/channel1/?level=1&kw=',
        # 'gaokaowang': 'http://tiku.gaokao.com/search/type0/',
        'zhongguojiaoyu': 'http://www.zzstep.com/chuzhong_search.php?key=',
        # 'dashi': 'http://www.xiexingcun.com/search.asps',
        # 'haokejian': 'http://www.goodkejian.com/search.asp?keyword=',
    }
    while True:
        # key_word = input('Input Key Word:')
        # if True:
        # key_words_list = [  '花的学校','不懂就要问',  '山行', '赠刘景文', '口语交际：我的暑假生活', '习作：猜猜他是谁','夜书所见', '铺满金色巴掌的水泥道',
        #                   '秋天的雨', '听听，秋的声音', '习作：写日记', '去年的树', '那一定会很好', '在牛肚子里旅行', '一块奶酪', '习作：我来编童话', '快乐读书吧',
        #                   '总也倒不了的老屋', '胡萝卜先生的长胡子', '不会叫的狗', '口语交际：名字里的故事', '习作：续写故事', '搭船的鸟', '金色的草地', '我家的小狗',
        #                   '我爱故乡的杨梅', '习作：我们眼中的缤纷世界', '望天门山', '饮湖上初晴后雨', '望洞庭', '富饶的西沙群岛', '海滨小镇', '美丽的小兴安岭', '习作：这儿真美',
        #                   '大自然的声音', '父亲、树林和鸟', '带刺的朋友', '口语交际：身边的“小事”', '习作：我有一个想法', '司马光', '掌声', '灰雀', '手术台就是阵地',
        #                   '口语交际：请教', '习作：那次玩得真高兴', '部编版小学语文三年级上', '部编版三年级上','大青树下的小学','花的学校',]
        key_words_list = ['花的学校','不懂就要问',  '山行']
        for curr_key in key_words_list:
            kw = curr_key
            curr_save_key_dir = os.path.join('./../crawler_data/source', kw)
            if not os.path.exists(curr_save_key_dir):
                os.makedirs(curr_save_key_dir)
            for web_name in website_url_dict:
                curr_website = web_name
                if True:
                    if curr_website == 'xuekewang_xiaoxue':
                        # pass
                        download_xuekewang_page(kw, website_url_dict[curr_website])
                    elif curr_website == 'gaokaowang':
                        pass
                        download_gaokaowang_page(kw, website_url_dict[curr_website])
                    elif curr_website == 'haokejian':
                        pass
                        download_haokejian_page(kw, website_url_dict[curr_website])
                    elif curr_website == 'zhongguojiaoyu':
                        pass
                        download_jiaoyu_page(kw, website_url_dict[curr_website])
                    else:
                        # todo download other web，可以考虑配置信息
                        print('输入网址有误，请确认url信息。')
                        pass

                    # print('已经爬取该关键字在目标网站的所有资源', curr_website, '\n\n')
            print('\n \n \n资源爬取完成，开始对文件进行分析并分类...\n \n \n')
            text_content_analysis(kw)
        break


# start
if __name__ == '__main__':
    # main()
    input_key_word()
