#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tika import parser
parsed = parser.from_file(r'G:\Download\Key_Word_Crower_Demo\src\test\test_tika\aa.pptx')
print(parsed["metadata"]) #To get the meta data of the file
print(parsed["content"]) # To get the content of the file