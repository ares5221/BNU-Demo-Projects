#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os,sys
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(os.path.split(rootPath)[0])


from bert_fine_tuning.predict_demo_math import predict_test
from utils import replace_punctuation
import Levenshtein
from search_solr.solr_math import search_by_keywords

def math_sorl_bert_finetuning_query(input_text):
    '''
    采用solr + finetuning的方式查询相似问题
    :param input_text:
    :return:
    '''
    clean_input_text = replace_punctuation(input_text)

    solr_res_dict = search_by_keywords(clean_input_text)
    if len(solr_res_dict) == 0 or len(clean_input_text) <= 1:
        QA_query = ''
        QA_answer = '没有找到相关问题及答案。'
        response_json = {'答案': QA_answer}
        return response_json
    else:
        if True:
            ques = []
            for tmp in solr_res_dict:
                ques.append(tmp['ques'])
            simi_res = predict_test(input_text, ques)
            sort_info = [i for i, v in sorted(enumerate(simi_res), key=lambda x: x[1])]
            top_similarity = simi_res[sort_info[-1]]
            top_ques = solr_res_dict[sort_info[-1]]['ques']
            input_ques = replace_punctuation(input_text)
            top_ques = replace_punctuation(top_ques[0])
            edit_distance_val = Levenshtein.ratio(input_ques, top_ques)
            print('model_similarity: ', top_similarity, ' Levenshtein_similarity: ', edit_distance_val)
            response_json = formating_resutl(top_similarity, edit_distance_val,
                                                   input_text,
                                                   solr_res_dict[sort_info[-1]])
            return response_json


def formating_resutl(model_val, leven_val, query, result):
    if leven_val >= 0.5 or model_val >= 0.8:
        QA_query = result['ques'][0]
        QA_answer = result['ans'][0]
        raw_title = result['raw_title'][0]
        raw_content = result['raw_content'][0]
        clean_title = result['clean_title'][0]
        clean_content = result['clean_content'][0]
        response_json = {'答案': QA_answer, '原始题目标题': raw_title,
                         '原始题目内容': raw_content, '清理后题目标题': clean_title, '清理后题目内容': clean_content}
        return response_json
    else:
        QA_query = ''
        QA_answer = '没有找到相关问题及答案'
        response_json = {'答案': QA_answer}
        return response_json


def math_solr_only(input_text):
    '''
    采用solr的方式直接搜索
    :param input_text:
    :return:
    '''
    clean_input_text = replace_punctuation(input_text)
    solr_res_dict = search_by_keywords(clean_input_text)
    if len(solr_res_dict) == 0 or len(clean_input_text) <= 1:
        QA_query = ''
        QA_answer = '没有找到相关问题及答案。'
        response_json = {'答案': QA_answer}
        return response_json
    else:
        if True:
            print(solr_res_dict[0])
            result = solr_res_dict[0]
            QA_query = result['ques'][0]
            QA_answer = result['ans'][0]
            if len(result['raw_title']) >0:
                raw_title = result['raw_title'][0]
            else:
                raw_title = ''
            if len(result['raw_content']) >0:
                raw_content = result['raw_content'][0]
            else:
                raw_content = ''
            if len(result['clean_title']):
                clean_title = result['clean_title'][0]
            else:
                clean_title = ''
            if len(result['clean_content']) >0:
                clean_content = result['clean_content'][0]
            else:
                clean_content = ''
            # response_json = {'QA_query': QA_query, 'QA_answer': QA_answer, 'raw_title': raw_title,
            #                  'raw_content': raw_content, 'clean_title': clean_title, 'clean_content': clean_content}
            response_json = {'答案': QA_answer, '原始题目标题': raw_title,
                             '原始题目内容': raw_content, '清理后题目标题': clean_title, '清理后题目内容': clean_content}
            return response_json


if __name__ == '__main__':
    print('测试开始，查询问题--->')
    testQ = ['直角三角形']
    for que in testQ:
        # math_sorl_bert_finetuning_query(que)
        print('------------------------------------------------------')
        math_solr_only(que)
