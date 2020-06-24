#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import zipfile

filename = r'G:\Download\Key_Word_Crower_Demo\src\test\testzip\aa.zip'
z =zipfile.ZipFile(filename, 'r')
# 这里的第二个参数用r表示是读取zip文件，w是创建一个zip文件
for f in z.namelist():
    print (f)