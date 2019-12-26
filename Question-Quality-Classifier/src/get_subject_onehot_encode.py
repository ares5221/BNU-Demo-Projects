#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
# define example
data = ['语文', '数学', '物理', '化学', '生物', '历史', '地理', '其他']
values = array(data)
print(values)
# integer encode
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(values)
# print(integer_encoded)
# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
print(onehot_encoded.tolist())
# invert first example
inverted = label_encoder.inverse_transform([argmax(onehot_encoded[0, :])])
