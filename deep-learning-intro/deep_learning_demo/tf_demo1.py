#!/usr/bin/env python
# _*_ coding:utf-8 _*_



import tensorflow as tf
a = tf.constant([1.0, 2.0])  # constant()代表定义常数
b = tf.constant([3.0, 4.0])
result = tf.add(a,b)
print(result)

m1 = tf.constant([[3.0,3.0]])  # constant()代表定义常数
m2 = tf.constant([[2.0], [3.0]])
product = tf.matmul(m1,m2)#创建一个矩阵乘法op，把m1和m2传入
print(product)

# 定义会话的方式（常用）
with tf.Session() as sess:
    add_result=sess.run(result)
    print(add_result)

# 旧版本定义一个会话 启动默认图
sess=tf.Session()  #
product_res =sess.run(product)
print(product_res)
sess.close()

import tensorflow as tf

x = tf.Variable([1, 2])
a = tf.constant([3, 3])

sub = tf.subtract(x, a)  # 增加一个减法op
add = tf.add(x, sub)  # 增加一个加法op

# 注意变量再使用之前要再sess中做初始化，但是下边这种初始化方法不会指定变量的初始化顺序
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    print(sess.run(sub))
    print(sess.run(add))

#################分割线#####################
# 创建一个名字为‘counter’的变量 初始化0
state = tf.Variable(0, name='counter')
new_value = tf.add(state, 1)  # 创建一个op，作用是使state加1
update = tf.assign(state, new_value)  # 赋值op
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print(sess.run(state))
    for _ in range(5):
        sess.run(update)
        print(sess.run(state))

import tensorflow as tf
import numpy as np

# 使用numpy生成100个随机点
x_data = np.random.rand(100)
y_data = x_data * 0.1 + 0.2  # 这里我们设定已知直线的k为0.1 b为0.2得到y_data

# 构造一个线性模型
b = tf.Variable(0.)
k = tf.Variable(0.)
y = k * x_data + b

# 二次代价函数（白话：两数之差平方后取 平均值）
loss = tf.reduce_mean(tf.square(y_data - y))
# 定义一个梯度下降法来进行训练的优化器（其实就是按梯度下降的方法改变线性模型k和b的值，注意这里的k和b一开始初始化都为0.0，后来慢慢向0.1、0.2靠近）
optimizer = tf.train.GradientDescentOptimizer(0.2)  # 这里的0.2是梯度下降的系数也可以是0.3...
# 最小化代价函数(训练的方式就是使loss值最小，loss值可能是随机初始化100个点与模型拟合出的100个点差的平方相加...等方法)
train = optimizer.minimize(loss)

# 初始化变量
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    for step in range(201):
        sess.run(train)
        if step % 20 == 0:
            print(step, sess.run([k, b]))  # 这里使用fetch的方式只是打印k、b的值，每20次打印一下，改变k、b的值是梯度下降优化器的工作