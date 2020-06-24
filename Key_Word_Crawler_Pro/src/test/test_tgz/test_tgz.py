#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import tarfile

path = r"aa.tgz"
path2 = r"./new"

tar = tarfile.open(path)
tar.extractall(path2)  # 解压指定文件路径
tar.close()
