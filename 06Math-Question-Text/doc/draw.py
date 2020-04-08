import os
import csv
import numpy as np



path = './../01cal_ques_similary/result1'
for fname in os.listdir(path):
    print(fname)
    dir = os.path.join(path, fname)
    with open(dir, 'r', encoding='utf-8') as csv_read:
        cs = csv.reader(csv_read)
        res = []
        for row in cs:
            # print(row[0])
            res.append(row[0])
        res = res[4:-2]
        tmp = []
        for tt in res:
            tmp.append(float(tt))

        print(np.mean(tmp))
