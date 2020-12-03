#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import tensorflow as tf

a = tf.constant([1.0, 2.0])  # constant()代表定义常数
b = tf.constant([3.0, 4.0])

result = a + b
print(result)

# Fetch概念 在session中同时运行多个op
input1 = tf.constant(3.0)  # constant()是常量不用进行init初始化
input2 = tf.constant(2.0)
input3 = tf.constant(5.0)

add = tf.add(input2, input3)
mul = tf.multiply(input1, add)

with tf.Session() as sess:
    result = sess.run([mul, add])  # 这里的[]就是Fetch操作
    print(result)

# Feed
# 创建占位符
input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)
# 定义乘法op，op被调用时可通过Feed的方式将input1、input2传入
output = tf.multiply(input1, input2)

with tf.Session() as sess:
    # feed的数据以字典的形式传入
    print(sess.run(output, feed_dict={input1: [7.], input2: [2.]}))