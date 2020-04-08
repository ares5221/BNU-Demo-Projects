#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import matplotlib.pyplot as plt

name_list = ['Levenshtein', 'Difflib', 'Jaccard', 'BM25','Word2vec','TF-IDF','BERT']
num_list = [60, 10, 5, 50, 100,120,200]
num_list1 = [0.9, 0.95, 0.7, 0.65,0.52,0.54,0.53]
x = list(range(len(num_list)))
total_width, n = 0.8, 2
width = total_width / n

# plt.bar(x, num_list, width=width, label='Time', fc='purple')
# for i in range(len(x)):
#     x[i] = x[i] + width
# plt.bar(x, num_list1, width=width, label='Accury', tick_label=name_list, fc='r')
# plt.legend()
# plt.show()


fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.bar(x, num_list, width=width, label='Time', fc='purple')
ax1.set_ylabel('Time')

for i in range(len(x)):
    x[i] = x[i] + width
ax2 = ax1.twinx()  # this is the important function
ax2.bar(x, num_list1, width=width, label='Accury', tick_label=name_list, fc='r')
ax2.set_xlim([-0.5, 7])
ax2.set_ylabel('Auc')
fig.legend()

plt.savefig('result.png')
plt.show()