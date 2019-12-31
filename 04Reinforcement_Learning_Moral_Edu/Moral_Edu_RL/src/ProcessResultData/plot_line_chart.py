import matplotlib.pyplot as plt
import numpy as np

n_data = 6
fig, ax = plt.subplots(nrows=1, ncols=1)
index = np.arange(n_data)
bar_width = 1.25

minus = 0.375
f_size = 12
axis_size = 12
l_width = 3
m_size = 10

# c_ass = 'b'
# c_ma = 'g'
# c_ph = 'k'
# c_ge = 'r'
# c_cm = 'm'

'''
"#9467bd"紫色
"#ff7f0e"橙色
'#1f77b4'蓝色
'#2ca02c'绿色
'#d62728'红色
'''
new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf']

c_ass = new_colors[0]
c_ma = new_colors[1]
c_ph = new_colors[4]
c_ge = new_colors[3]
c_cm = new_colors[2]
# set marker
m_ass = 'd'
m_ma = 'p'
m_ph = 'H'
m_ge = 's'
m_cm = 'o'

title = ""
titlesize = 14
NAME = "C"

x1 = [1, 2, 3, 4, 5, 6]

if NAME == 'C':
    y401_assist = [0.42, 0.3654, 0.3546, 0.4256, 0.4276, 0.4124]
    y901_math = [0.3885, 0.3329, 0.437, 0.4198, 0.4064, 0.4091]
    y1501_physics = [0.3377, 0.3641, 0.4327, 0.3327, 0.4074, 0.3981]
    y1503_geography = [0.3999, 0.3444, 0.3287, 0.4594, 0.3938, 0.2802]
    y1504_chemistry = [0.246, 0.3967, 0.3935, 0.3872, 0.3668, 0.3745]


def draw_AUC():
    plt.grid(True, linestyle="-.")
    plt.plot(x1, y401_assist, color=c_ass, linewidth=l_width, label="50%", marker=m_ass, markersize=m_size)
    plt.plot(x1, y901_math, color=c_ma, linewidth=l_width, label="60%", marker=m_ma, markersize=m_size)
    plt.plot(x1, y1501_physics, color=c_ph, linewidth=l_width, label="70%", marker=m_ph, markersize=m_size)
    plt.plot(x1, y1503_geography, color=c_ge, linewidth=l_width, label="80%", marker=m_ge, markersize=m_size)
    plt.plot(x1, y1504_chemistry, color=c_cm, linewidth=l_width, label="90%", marker=m_cm, markersize=m_size)

    plt.xlabel('Number of DQN Hidden Units', fontsize=f_size, fontweight="bold")
    plt.xticks(index + 1, ('8', '16', '32', '64', '128', '256'), fontsize=axis_size, fontweight="bold")
    plt.ylabel('SR', fontsize=f_size, fontweight="bold")
    plt.yticks(fontsize=axis_size, fontweight="bold")
    plt.ylim(0, 0.5)
    plt.legend(loc="lower center", ncol=5)


def draw():
    # fig.suptitle(title, fontsize=titlesize, ha='center', y=0.9)
    fig.set_size_inches(6, 4, forward=True)
    # draw AUC
    draw_AUC()
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.subplots_adjust(left=0.15, right=0.98)
    plt.savefig(NAME + "dqn_hidden_units.pdf")
    plt.show()


if __name__ == "__main__":
    draw()
