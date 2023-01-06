import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os


def main():
    # 讀資料位置
    root = tk.Tk()
    root.withdraw()
    log_directory = filedialog.askdirectory(parent=root, initialdir='~/VibrationLabeler-master')
    root.destroy()

    with open(os.path.join(log_directory + '/symmetry.txt'), 'r') as f:
        data = f.readlines()

    new = []
    data_list = [0] * 101
    for each in data:
        if 'Amp' in each:
            temp = each.split()
            value = temp[4]
            round_value = round(float(value), 2)
            if round_value > 1:
                round_value = 1
            new.append(round_value)
            round_value = int(100 * round_value)
            print(round_value)
            data_list[round_value] += 1

    for i in range(100):
        print(i / 100, data_list[i])

    steps = np.arange(0.0, 1, 0.01)
    print(data_list)
    plt.hist(new, bins=100)
    # plt.ylim((0, 100))
    plt.xlim((0, 1))
    plt.savefig('elderscroll_symmetry_event_cnt.png')
    plt.show()


if __name__ == '__main__':
    main()
