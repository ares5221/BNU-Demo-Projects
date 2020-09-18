#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import pysolr

# use test server
# solr = pysolr.Solr('http://172.18.136.89:18983/solr/fqa2', always_commit=True, timeout=10)


# use 247 local server
solr = pysolr.Solr('http://172.24.227.247:18993/solr/doubleteacher', always_commit=True, timeout=10)


# Do a health check.
# print(solr.ping())

def search_by_keywords(key, topK=20):
    '''
    根据关键字搜索问题
    :param key:
    :param topK:
    :return:
    '''
    solr_key = 'ques:' + key
    key_results = solr.search(solr_key, **{'wt': 'json', 'rows': str(topK)})
    res = []
    for tmp2 in key_results:
        sub_tmp = {}
        sub_tmp['id'] = tmp2['id']
        # todo 新版的solr存储的ques为字符串格式，旧版的ques带[]，因此这里手动给添加一个[]
        sub_tmp['ques'] = [tmp2['ques']]
        sub_tmp['ans'] = tmp2['ans']
        sub_tmp['raw_title'] = tmp2['raw_title']
        sub_tmp['raw_content'] = tmp2['raw_content']
        if 'clean_title' in tmp2:
            sub_tmp['clean_title'] = tmp2['clean_title']
        else:
            sub_tmp['clean_title'] = []
        if 'clean_content' in tmp2:
            sub_tmp['clean_content'] = tmp2['clean_content']
        else:
            sub_tmp['clean_content'] = []
        res.append(sub_tmp)
    return res


def search_by_id(id, topK=1):
    '''
    根据id搜索solr中的问题
    :param id:
    :param topK:
    :return:
    '''
    res = {}
    if id:
        solr_id = 'id:' + id
        id_results = solr.search(solr_id, **{'wt': 'json', 'rows': str(topK)})
        for tmp in id_results:
            res['id'] = tmp['id']
            res['ques'] = tmp['ques']
            res['ans'] = tmp['ans']
        return res
    else:
        return res


if __name__ == '__main__':
    input_key = '三国演义的主题是什么'
    input_key = '哈哈'
    # input_key = input('input search key>')
    res = search_by_keywords(input_key)
    print(res)
    # input_id = input('input search id>')
    # res2 = search_by_id(input_id)
    # print(res2)
