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
'''
color1 = "#fcce10"
color2 = "#c1232b"
color3 = "#27727b"
color4 = "#e87c25"
color5 = "#b5c334"
'''
color1 = "#7f1874"
color2 = "#c1232b"
color3 = "#0098d9"
color4 = "#de8100"
color5 = "#2b821d"

# c_ass = 'b'
# c_ma = 'g'
# c_ph = 'k'
# c_ge = 'r'
# c_cm = 'm'

new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf']

c_dt = new_colors[0]
c_knn = new_colors[1]
c_svm = new_colors[2]
c_lr = new_colors[8]
c_nb = new_colors[4]
c_rf = new_colors[5]
c_ada = new_colors[6]
c_gradb = new_colors[7]
c_ds = new_colors[3]


m_dt = 'd'
m_knn = 'p'
m_svm = 'H'
m_lr = 's'
m_nb = 'o'
m_rf = '^'
m_ada = '*'
m_gradb = 'P'
m_ds = 'D'

opacity1 = 1
opacity2 = 1
opacity3 = 0.9
opacity4 = 1
opacity5 = 1
# dataset = "geography"
title = ""
titlesize = 14
NAME = "C"

x1 = [1, 2, 3, 4, 5]

if NAME == 'C':
    yDT = [0.349206,0.331746,0.35873,0.347619,0.368254]
    yKNN = [0.371429,0.357143,0.390476,0.38254,0.393651]
    ySVM = [0.438095,0.422222,0.446032,0.415873,0.415873]
    yLR = [0.442857,0.404762,0.447619,0.4,0.44127]
    yNB = [0.403175,0.388889,0.450794,0.396825,0.419048]
    yRF = [0.385714,0.37619,0.425397,0.371429,0.420635]
    yAdaBoost = [0.365079,0.35873,0.357143,0.366667,0.38254]
    yGradientBoosting = [0.393651,0.365079,0.393651,0.404762,0.419048]
    yDialogueSystem = [0.4136,0.4285,0.430778,0.435625,0.444429]
elif NAME == 'E':
    y401_assist = [0.811261246, 0.813158142, 0.813924387, 0.813165431, 0.81219811, 0.808349123]
    y901_math = [0.808937832, 0.811444557, 0.812279888, 0.810413351, 0.808562321, 0.80374303]
    y1501_physics = [0.809669653, 0.810775027, 0.811227336, 0.811223345, 0.80940019, 0.807067823]
    y1503_geography = [0.841415896, 0.842017892, 0.842017479, 0.841760691, 0.84118277, 0.838793638]
    y1504_chemistry = [0.84453393, 0.845892481, 0.846317941, 0.84657443, 0.845846821, 0.843690655]


def draw_AUC():
    plt.grid(True, linestyle="-.")

    plt.plot(x1, yDT, color=c_dt, linewidth=l_width, label="DT", marker=m_dt, markersize=m_size)
    plt.plot(x1, yKNN, color=c_knn, linewidth=l_width, label="KNN", marker=m_knn, markersize=m_size)
    plt.plot(x1, ySVM, color=c_svm, linewidth=l_width, label="SVM", marker=m_svm, markersize=m_size)
    plt.plot(x1, yLR, color=c_lr, linewidth=l_width, label="LR", marker=m_lr, markersize=m_size)
    plt.plot(x1, yNB, color=c_nb, linewidth=l_width, label="NB", marker=m_nb, markersize=m_size)
    plt.plot(x1, yRF, color=c_rf, linewidth=l_width, label="RF", marker=m_rf, markersize=m_size)
    plt.plot(x1, yAdaBoost, color=c_ada, linewidth=l_width, label="AdaBoost", marker=m_ada, markersize=m_size)
    plt.plot(x1, yGradientBoosting, color=c_gradb, linewidth=l_width, label="GradientBoosting", marker=m_gradb, markersize=m_size)
    plt.plot(x1, yDialogueSystem, color=c_ds, linewidth=l_width, label="DialogueSystem", marker=m_ds, markersize=m_size)

    plt.xlabel('Number of DQN Hidden Units', fontsize=f_size, fontweight="bold")
    plt.xticks(index + 1, ('5:5', '6:4', '7:3', '8:2', '9:1'), fontsize=axis_size, fontweight="bold")
    plt.ylabel('SR', fontsize=f_size, fontweight="bold")
    plt.yticks(fontsize=axis_size, fontweight="bold")
    plt.ylim(0.2, 0.5)
    plt.legend(loc="lower center", ncol=5)


def draw():
    '''
    color1 = "#c12e34"
    color2 = "#e6b600"
    color3 = "#0098d9"
    color4 = "#2b821d"
    '''

    # fig.suptitle(title, fontsize=titlesize, ha='center', y=0.9)
    fig.set_size_inches(6, 4, forward=True)
    # draw AUC
    draw_AUC()
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.subplots_adjust(left=0.15, right=0.98)
    plt.savefig(NAME + "_hidden_units.pdf")
    plt.show()


if __name__ == "__main__":
    draw()
