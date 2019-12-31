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
    return int(-50*temp)

# setup the figure and axes
fig = plt.figure(figsize=(5, 5))  # 画布宽长比例
ax1 = fig.add_subplot(111, projection='3d')
ax1.grid(True, linestyle='-.')
_x = np.arange(1, 5)
_y = np.arange(1, 5)
print(_x, _y)
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel() #ravel扁平化

top = [4.1967,4.1016,4.0032,4 ,12.3509, 4.2809, 4.0634, 4.054,
       11.9144,5.0176,4.3716,4.1603, 29.3873,8.9111,5.2508,4.3619]
bottom = np.zeros_like(top)#每个柱的起始位置
width = depth = 0.34 #x,y方向的宽厚

new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']
for fail in range(1, 5):
    color = new_colors[fail-1]
    for success in range(1, 5):
        ax1.bar3d(success-0.1, fail-0.25, 0, width, depth,
                  top[(fail-1)*4 + (success-1)], color=color, shade=True)   #每次画一个柱


xmajorLocator = MultipleLocator(1) #将x主刻度标签设置为1的倍数
ymajorLocator = MultipleLocator(1) #将x主刻度标签设置为1的倍数

ax1.xaxis.set_major_locator(xmajorLocator)
ax1.yaxis.set_major_locator(ymajorLocator)
ax1.xaxis.set_major_formatter(FuncFormatter(to_zoomX1))#将X,Y,Z轴的坐标轴放大50倍
ax1.yaxis.set_major_formatter(FuncFormatter(to_zoomX2))
ax1.set_xlabel('reward_for_success',fontsize=12, fontweight="bold")
plt.xticks(fontsize=12, fontweight="bold")
ax1.set_ylabel('reward_for_fail',fontsize=12, fontweight="bold")
plt.yticks(fontsize=12, fontweight="bold")
ax1.set_zlabel('ave turns',fontsize=12, fontweight="bold")
plt.ticklabel_format(fontsize=12, fontweight="bold") #可以通过修改ticklabel_format来修改xy轴的字体大小及粗体，但这是在plt上修改的，无法修改z轴
plt.savefig("3d.pdf")
# ax1.grid(True, linestyle="-.") #无法修改网格背景为虚线
plt.show()