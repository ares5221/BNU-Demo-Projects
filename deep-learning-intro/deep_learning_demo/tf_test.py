#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import tensorflow as tf

a = tf.constant([1.0, 2.0])  # constant()代表定义常数
b = tf.constant([3.0, 4.0])

result = a + b
print(result)
