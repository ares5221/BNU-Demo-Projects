#!/usr/bin/env python
# _*_ coding:utf-8 _*_
dd = {"q":1}
d2 = {}
d3 = {}
for i in [dd,d2,d3]:
    if i==dd:
        print('11')
    elif i == d2:
        print('22')
    else:
        print('33')
