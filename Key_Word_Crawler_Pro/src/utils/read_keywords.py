#!/usr/bin/env python
# _*_ coding:utf-8 _*_

ss = []
with open('keywords.txt','r',encoding='utf-8') as file_to_read:
    while True:
        lines = file_to_read.readline().strip()  # 整行读取数据
        if not lines:
            break
            pass
        ss.append(lines)

print(ss)