from scipy.optimize import curve_fit
import numpy as np

labelset = np.array(range(5))


def x_pos(x, a, b, c):
    return a * x[0] + b * x[1] + c


def y_pos(x, a, b, c):
    return a * x[0] + b * x[1] + c


def calib(str):
    # data_matrix = np.loadtxt(f_path)
    splited_str = str.split()
    data_matrix = [float(i) for i in splited_str]
    data_matrix = np.reshape(data_matrix, [-1, 5])
    gaze_xpos, gaze_ypos, label, real_xpos, real_ypos = \
        data_matrix[:, 0], data_matrix[:, 1], data_matrix[:, 2], data_matrix[:, 3], data_matrix[:, 4]
    # label_collected = np.unique(label).astype(np.int)
    # label_uncollected = np.setdiff1d(labelset, label_collected)
    # if label_uncollected.size > 0:
    label = label.astype(np.int)
    center_didx = label == 1
    if (sum(center_didx) < 1) and (sum(~center_didx) < 3):
        return None, None
    else:
        gaze_pos = np.concatenate([gaze_xpos[np.newaxis, :], gaze_ypos[np.newaxis, :]], axis=0)
        popt_x, pcov_x = curve_fit(x_pos, gaze_pos, real_xpos)
        popt_y, pcov_y = curve_fit(y_pos, gaze_pos, real_ypos)
        return popt_x, popt_y


if __name__ == "__main__":
    str_data = '0 0 0 3 0 -1 0 1 2 -2 1 0 2 4 2 0 -1 3 1 -1 0 1 4 5 1'
    a, b = calib(str_data)
    # a, b, c = calib('ca.txt')
    print(a, b)
