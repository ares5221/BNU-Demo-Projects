#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import rarfile

path = r"testrar.rar"
path2 = r"./new"

rf = rarfile.RarFile(path)
rf.extractall(path2)  # 解压指定文件路径
rf.close()


'''
运行后报错缺少unrar进入第三部。　
3.配置环境

　　需要WinRAR软件提供的UnRAR.exe文件（rar非开源所以必须使用winrar的文件）,以下三种方法。

　　WinRAR下载地址： http://www.winrar.com.cn

　　(1).据winrar的目录中的UnRAR.exe，拷贝到我的python脚本目录下，再执行就ok了；
　　(2).环境变量path中加入unrar.exe所在目录；(未成功)
　　(3).PyCharm的话，可以将unrar.exe复制到项目的venv/Scripts下。（未测试）

4.问题参考

　　https://blog.csdn.net/big_talent/article/details/52367184
　　https://blog.csdn.net/luoye7422/article/details/41873499
'''