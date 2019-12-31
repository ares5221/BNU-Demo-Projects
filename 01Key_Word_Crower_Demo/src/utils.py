#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import json
import uuid



def save_supplement_data(key_word, titles, middle_websites, introduction_contents):
    '''
    将爬取的信息保存在字典后实例化到json文件种
    :param key_word:
    :param curr_titles:
    :param curr_middle_websites:
    :param curr_introduction_contents:
    :return:
    '''

    supplement_info_json_path = './../data_v2/supplement_data/supplement_info.json'
    if os.path.exists(supplement_info_json_path):
        with open(supplement_info_json_path, "r") as file_obj:
            info_json = json.load(file_obj)
        if key_word in info_json:
            print(info_json[key_word])

            for index in range(len(titles)):
                uid_str = str(uuid.uuid1())
                curr_dict = {}
                curr_dict['title'] = titles[index]
                curr_dict['web_site'] = middle_websites[index]
                curr_dict['intro'] = introduction_contents[index]
                info_json[key_word][uid_str] = curr_dict
            print(info_json)
            with open(supplement_info_json_path, 'w') as json_write:
                json.dump(info_json, json_write, indent=4, ensure_ascii=False)
        else:
            info_json[key_word] = {}
            for index in range(len(titles)):
                uid_str = str(uuid.uuid1())
                curr_dict = {}
                curr_dict['title'] = titles[index]
                curr_dict['web_site'] = middle_websites[index]
                curr_dict['intro'] = introduction_contents[index]
                info_json[key_word][uid_str] = curr_dict
            print(info_json)
            with open(supplement_info_json_path, 'w') as json_write:
                json.dump(info_json, json_write, indent=4, ensure_ascii=False)

    else:
        info_json = {}
        info_json[key_word] = {}
        for index in range(len(titles)):
            uid_str = str(uuid.uuid1())
            curr_dict = {}
            curr_dict['title'] = titles[index]
            curr_dict['web_site'] = middle_websites[index]
            curr_dict['intro'] = introduction_contents[index]
            info_json[key_word][uid_str] = curr_dict
        with open(supplement_info_json_path, 'w') as json_write:
            json.dump(info_json, json_write, indent=4, ensure_ascii=False)





if __name__ == '__main__':
    save_supplement_data('hahaaa', ['aasa'],['bbs'],['cc'])