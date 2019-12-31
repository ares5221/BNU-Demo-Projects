#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter,FuncFormatter
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
'''
"#9467bd"紫色
"#ff7f0e"橙色
'#1f77b4'蓝色
'#2ca02c'绿色
'#d62728'红色
'''
def to_zoomX1(temp, position):
    return int(50*temp)
def to_zoomX2(temp, position):
    return int(50*temp)

fig = plt.figure(figsize=(5, 5))  # 画布宽长比例
axes3d = Axes3D(fig)
axes3d.grid(True, linestyle='-.')

top = [29.3873,11.9144, 12.3509, 4.1967,
8.9111,5.0176,  4.2809,  4.1016,
5.2508, 4.3716, 4.0634,4.0032,
4.3619,4.1603,  4.054,4, ]


bottom = np.zeros_like(top)#每个柱的起始位置
width = depth = 0.34 #x,y方向的宽厚

new_colors = ['#9467bd', '#ff7f0e', '#2ca02c', '#1f77b4']
'''
若要调整x y轴起始数据，可以调整其从range(-4,0, 1)
'''
for fail in range(1,5,1):
    # color = new_colors[fail-1]
    for success in range(-4,0, 1):
        if success == -4:
            color = new_colors[success]
        elif success == -3:
            color = new_colors[success]
        elif success == -2:
            color = new_colors[success]
        else:
            color = new_colors[success]
        axes3d.bar3d(success-0.1, fail-0.25, 0, width, depth,
                  top[(fail-1)*4 + (success+4)], color=color, shade=True)   #每次画一个柱

xmajorLocator = MultipleLocator(1) #将x主刻度标签设置为1的倍数
ymajorLocator = MultipleLocator(1) #将x主刻度标签设置为1的倍数

axes3d.xaxis.set_major_locator(xmajorLocator)
axes3d.yaxis.set_major_locator(ymajorLocator)
axes3d.xaxis.set_major_formatter(FuncFormatter(to_zoomX2))#将X,Y,Z轴的坐标轴放大50倍
axes3d.yaxis.set_major_formatter(FuncFormatter(to_zoomX1))

plt.tick_params(labelsize=12)
labels = axes3d.get_xticklabels() + axes3d.get_yticklabels() + axes3d.get_zticklabels()
[label.set_fontsize(12) for label in labels]
[label.set_fontweight('bold') for label in labels]

axes3d.set_xlabel('Negative Rewards',fontsize=12, fontweight="bold", labelpad=8.2)
axes3d.set_ylabel('Postive Rewards',fontsize=12, fontweight="bold", labelpad=4.2)
axes3d.set_zlabel('Average Turns',fontsize=12, fontweight="bold")
plt.savefig("3d.pdf")
plt.show()