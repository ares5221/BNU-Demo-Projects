#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import re
import random


def replace_punctuation(line):
    punctuation = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏."
    re_punctuation = "[{}]+".format(punctuation)
    line = re.sub(re_punctuation, "", line)
    punctuation2 = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    re_punctuation2 = "[{}]+".format(punctuation2)
    line = re.sub(re_punctuation2, "", line)
    return line


def re_filter_str(desstr, restr=''):
    # 除中英文及数字以外的其他字符替换为空字符
    pattern = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
    desstr = desstr.lower()
    res = re.sub(pattern, restr, desstr)
    print(res)
    return res


def rule_based_QA(user_input):
    is_active_rule_base = False
    greeting_user_dia = ['你好', '您好', '早上好', '早安', '早', '中午好', '晚上好', '哈喽', '嗨', '哈啰', 'hello', 'helo', '你好呀',
                         'hi', 'halo', 'nihao', 'ninhao', 'hey']
    greeting_sys_dia = ['你好', '您好', 'Hello', 'Hi']
    info_user_dia = ['你是', '你是谁', '你叫什么', '你叫什么名字', '你是谁呀']
    info_sys_dia = ['我是小未', '我是您的育人助手小未', ]
    info_user_dia_2 = ['你多大了', '你几岁了', '你几岁', '你多大']
    info_sys_dia_2 = ['我年龄小但是本领大', ]
    info_user_dia_3 = ['你真可爱', '你好可爱呀', '你好可爱', '你有点可爱']
    info_sys_dia_3 = ['我不仅可爱还有很多技能哦', '我也觉得自己很可爱呢']
    info_user_dia_4 = ['我喜欢你', '我好喜欢你呀', '我好喜欢你']
    info_sys_dia_4 = ['我也喜欢你', '人家都要不好意思了', '谢谢你']
    info_user_dia_5 = ['你的主人是谁', '你的主人呢']
    info_sys_dia_5 = ['你就是我现在的主人了', '就是你呀', ]
    info_user_dia_6 = ['你是男生吗', '你是女生吗', '你是男的吗', '你是男生还是女生', '你是女的吗', '你是男是女', '你是男的', '你是女的', '你是男生女生', ]
    info_sys_dia_6 = ['我是新新人类']
    chat_user_dia = ['哈哈', '嘿嘿', '哈哈哈']
    chat_sys_dia = ['很高兴认识你']
    chat_user_dia_2 = ['你有什么技能', '你会做什么', '你会什么', '你能干什么', '你有什么能力', '你可以做什么', '你会做什么', '你可以干什么', '你有什么本事', '你是干啥的',
                       '你是干什么的', '你能干啥']
    chat_sys_dia_2 = ['我可以帮您解答育人过程中的困惑', '我可以帮助您解决育人过程中遇到的问题']
    if user_input in greeting_user_dia:
        rule_based_res = random.choice(greeting_sys_dia)
        is_active_rule_base = True
    if user_input in info_user_dia:
        rule_based_res = random.choice(info_sys_dia)
        is_active_rule_base = True
    if user_input in info_user_dia_2:
        rule_based_res = random.choice(info_sys_dia_2)
        is_active_rule_base = True
    if user_input in info_user_dia_2:
        rule_based_res = random.choice(info_sys_dia_2)
        is_active_rule_base = True
    if user_input in info_user_dia_3:
        rule_based_res = random.choice(info_sys_dia_3)
        is_active_rule_base = True
    if user_input in info_user_dia_4:
        rule_based_res = random.choice(info_sys_dia_4)
        is_active_rule_base = True
    if user_input in info_user_dia_5:
        rule_based_res = random.choice(info_sys_dia_5)
        is_active_rule_base = True
    if user_input in info_user_dia_6:
        rule_based_res = random.choice(info_sys_dia_6)
        is_active_rule_base = True
    if user_input in chat_user_dia:
        rule_based_res = random.choice(chat_sys_dia)
        is_active_rule_base = True
    if user_input in chat_user_dia_2:
        rule_based_res = random.choice(chat_sys_dia_2)
        is_active_rule_base = True
    if is_active_rule_base:
        return is_active_rule_base, rule_based_res + '，请问您遇到那些育人相关的问题呢？'
    else:
        return is_active_rule_base, user_input

