#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import rarfile

path = r"G:\Download\Key_Word_Crower_Demo\src\test\testrar.rar"
path2 = r"G:\New"

rf = rarfile.RarFile(path)
rf.extractall(path2)  # 解压指定文件路径