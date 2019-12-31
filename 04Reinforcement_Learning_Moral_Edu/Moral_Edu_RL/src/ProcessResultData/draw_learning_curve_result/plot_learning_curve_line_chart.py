# -*- coding:utf-8 -*-
import os
import matplotlib.pyplot as plt
import pickle

'''
"#9467bd"紫色
"#ff7f0e"橙色
'#1f77b4'蓝色
'#2ca02c'绿色
'#d62728'红色
'''


class Ploter(object):
    def __init__(self, performance_file1, performance_file2, performance_file3):
        self.performance_file1 = performance_file1
        self.performance_file2 = performance_file2
        self.performance_file3 = performance_file3

        self.performance1 = pickle.load(file=open(self.performance_file1, "rb"))
        self.performance2 = pickle.load(file=open(self.performance_file2, "rb"))
        self.performance3 = pickle.load(file=open(self.performance_file3, "rb"))
        self.epoch_index = []
        self.success_rate = []
        self.average_reward = []
        self.average_wrong_disease = []
        self.__prepare_data()

    def __prepare_data(self, epoch_size=50):
        epoch_size = max(epoch_size, len(self.performance1.keys()))
        for epoch_index in range(0, epoch_size, 1):
            self.epoch_index.append(epoch_index)
            self.success_rate.append(
                (self.performance1[epoch_index]["success_rate"] + self.performance2[epoch_index]["success_rate"] +
                 self.performance3[epoch_index]["success_rate"]) / 3.0)
            self.average_reward.append(self.performance1[epoch_index]["average_reward"])
            self.average_wrong_disease.append(self.performance1[epoch_index]["average_wrong_disease"])

    def plot(self, save_name):
        size = 2000
        plt.plot(self.epoch_index[0:size], self.success_rate[0:size], color='#9467bd', label="DQN Agent", linewidth=1)
        plt.xlabel("Simulation Epoch", fontsize=12, fontweight="bold")
        plt.xticks(fontsize=12, fontweight="bold")
        plt.ylabel("Success Rate", fontsize=12, fontweight="bold")
        plt.yticks(fontsize=12, fontweight="bold")
        # plt.title("Learning Curve")
        plt.hlines(0.288, 0, size, label="Rule Agent", linewidth=3, colors="#2ca02c")
        plt.hlines(0.2182, 0, size, label="Random Agent", linewidth=3, colors="#ff7f0e")
        plt.grid(True, linestyle="-.")
        plt.legend(loc="lower right")
        # plt.legend(loc='center right')
        plt.savefig(save_name, dpi=400)
        plt.show()


if __name__ == "__main__":
    print(os.path.abspath('.'))
    file_name1 = "./learning_rate1_1999.p"
    file_name2 = "./learning_rate2_1999.p"
    file_name3 = "./learning_rate3_1999.p"

    save_name = "Learning Curve.pdf"
    ploter = Ploter(file_name1, file_name2, file_name3)
    ploter.plot(save_name)
