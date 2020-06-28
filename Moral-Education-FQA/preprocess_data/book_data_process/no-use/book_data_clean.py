#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import docx
import csv


def read_data():
    book2_title = ['管理上课不带学习用具的学生', '管理学生不良言语', '学生对上课不感兴趣','学生在课堂感到无聊',
                   '小学生注意力时间短','学生不能独立自觉','学习无助感容易放弃的学生',
                   '学生不能在课堂上完成作业', '学习没有动力的学生','学生不能完成家庭作业','管理女生行为问题',
                   '代课老师怎么进行班级管理','应对不给予支持的家长','管理顶嘴的学生',
                   '巧管理课堂上的小打小闹','管理不停闲聊的学生','管理话多、吵闹的班级',
                   '如何在15秒或更短的时间内让课堂安静','管理迟到、不守时的学生','管理说脏话的学生','如何让学生听从你的指示',
                   '如何处理学生愚蠢的行为','管理课堂上喜欢开玩笑捣乱的学生','管理愤怒、目中无人的学生','管理特别难管的班级',
                   '如何鼓励缺乏自尊的学生', '管理学生争斗和严重的事件','管理学生手机使用',
                   '管理来自“外星"的班级','学生迟到','不参与课堂任务的学生','学生不参与小组活动', '寻求被关注',
                   '咒骂、说粗话','在课程开始的时候学生还没有静下心','对抗','搞破坏','无视你',
                   '不带学习用具','缺乏学习动力','开小差','挑衅滋事','大声叫喊','学生放屁','不听从指示',
                    '第一阶段：对触发点的回应','第二阶段：学生极度痛苦和焦虑','让学生重新回到学习任务的五个步骤',
                   '帮助你保持冷静，控制情绪的3个要求技巧','让捣蛋学生听话的魔术语','如何在不引起争论的情况下对学生说不','能减少一半课堂干扰的简单语言'
                   ]
    full_text = []
    txt = [[] for i in range(55)]
    path = 'clean_docx.docx'
    document = docx.Document(path)
    title_index = 0
    for paragraph in document.paragraphs:
        linetxt = paragraph.text
        full_text.append(linetxt)
    print(len(full_text), full_text)
    buttle = False
    for full_text_index in range(len(full_text)):
        curr_title = book2_title[title_index]
        if curr_title in full_text[full_text_index]:
            buttle = True
            title_index += 1
            if title_index >= 51:
                title_index = 51
        if buttle:
            txt[title_index].append(full_text[full_text_index])

    for inde in range(len(txt)):
        print(inde, txt[inde])


    # start_index = 0
    # for cc in range(len(txt)):
    #     if txt[cc]:
    #         savename = './../data/test_txt_file/book3/' + str(cc + start_index).zfill(4) + '.txt'
    #         for cont in txt[cc]:
    #             with open(savename, 'a', encoding='utf-8') as ff:
    #                 ff.write(cont)
    #                 ff.write('\n')




if __name__ == '__main__':
    read_data()
