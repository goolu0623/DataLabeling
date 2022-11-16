import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog


def selectdirectory():
    # 讀資料位置
    root = tk.Tk()
    root.withdraw()
    log_directory = filedialog.askdirectory(parent=root, initialdir='~/VibrationLabeler-master')
    root.destroy()
    return log_directory


def data_preprocess(logdirectory):
    # 讀資料
    with open(os.path.join(logdirectory + '/log.txt'), 'r') as f:
        data = f.readlines()

    # 有空白行的部分清掉
    i = 0
    while i < len(data):
        if data[i] == '\n':
            data.pop(i)
        else:
            i += 1
    # 寫回不含空白行的
    if debug:
        with open(os.path.join(logdirectory + '/test_log_modified.txt'), 'w') as f:
            for each in data:
                f.writelines(each)

    # 根據每HMD定義偵數 然後先刪掉所有無關vib的資料
    data2 = []
    for each in data:
        if 'HMD' in each or 'Vibration' in each:
            data2.append(each)
    data = data2.copy()
    if debug:
        with open(os.path.join(logdirectory + '/test_log_only_vib_and_HMD.txt'), 'w') as f:
            for each in data:
                f.writelines(each)

    # with open(os.path.join(logdirectory + '/test_log_only_vib_and_HMD.txt'), 'r') as f:
    #     data = f.readlines()

    # Only vib and time
    data_temp = []
    for each in data:
        if 'HMD' in each:
            temp = each.split('  :HMD')
            data_temp.append(temp[0] + '\n')
        else:
            data_temp.append(each)
    data = data_temp.copy()

    if debug:
        with open(os.path.join(logdirectory + '/test_log_only_vib_and_time.txt'), 'w') as f:
            for each in data:
                f.writelines(data)

    # with open(os.path.join(logdirectory + '/test_log_only_vib_and_time.txt'), 'r') as f:
    #     data = f.readlines()

    with open(os.path.join(logdirectory + '/complete.txt'), 'w') as f:
        time_stamp, frame_number = 0, 0

        for each in data:
            each_list = each.split()
            if len(each_list) == 2:
                timetemp = each_list[1].split('.')
                if time_stamp != timetemp[0]:
                    time_stamp = timetemp[0]
                    frame_number = 0
                else:
                    frame_number += 1
                f.write(each_list[0] + ' ' + each_list[1] + ' [' + str(frame_number) + ']' + '\n')
            else:
                f.write(each_list[0] + ' ' + each_list[1] + ' [' + str(frame_number) + ']')
                for elements in each_list[2:]:
                    f.write(' ' + elements)
                f.write('\n')
    return


def full_data_log(log_directory):
    with open(os.path.join(log_directory + '/complete.txt'), 'r') as f:
        data = f.readlines()
    start_frame, end_frame = 0, len(data) - 1
    lx, ly, rx, ry = [], [], [], []
    prev_data_time = 0
    left_modified = False
    right_modified = False
    for each in data[start_frame + 1:end_frame]:
        temp = each.split()
        if 'Left' in each or 'Right' in each:
            if prev_data_time == 0:
                print("error: data not start with HMD")
            elif 'Left' in each:
                lx.append(temp[1])
                ly.append(float(temp[4]))
                left_modified = True
            elif 'Right' in each:
                rx.append(temp[1])
                ry.append(float(temp[4]))
                right_modified = True

        else:
            if prev_data_time == 0:
                pass
            elif left_modified or right_modified:
                if left_modified and right_modified:
                    pass
                elif left_modified:
                    rx.append(prev_data_time)
                    ry.append(0.0)
                elif right_modified:
                    lx.append(prev_data_time)
                    ly.append(0.0)
            else:
                lx.append(prev_data_time)
                ly.append(0.0)
                rx.append(prev_data_time)
                ry.append(0.0)
            prev_data_time = temp[1]
            left_modified = False
            right_modified = False
    lx, ly, rx, ry = np.array(lx), np.array(ly), np.array(rx), np.array(ry)
    fig, ax = plt.subplots(2, 1, figsize=(10, 4))
    ax[0].set_title('Left Controller')
    ax[0].plot(lx, ly)
    ax[1].set_title('Right Controller')
    ax[1].plot(rx, ry)
    x_major_locator = plt.MultipleLocator((end_frame - start_frame) / 6)
    ax[0].xaxis.set_major_locator(x_major_locator)
    ax[1].xaxis.set_major_locator(x_major_locator)
    ax[0].set_ylim([0, 1.1])
    ax[1].set_ylim([0, 1.1])

    plt.tight_layout()
    plt.savefig(os.path.join(log_directory + '/full_image.png'))

    return


def symmetric_data(log_directory):
    with open(os.path.join(log_directory + '/complete.txt'), 'r') as f:
        data = f.readlines()

    with open(os.path.join(log_directory + '/symmetry.txt'), 'w') as f:
        p_date, p_time, p_frame, p_hand, p_vib_value, p_freq, p_freq_value, p_dur, p_dur_value = 0, 0, 0, 0, 0, 0, 0, 0, 0
        prev_each = 0
        for index, each in enumerate(data):
            temp = each.split()
            if index == len(data) - 1:  # 檔案尾 全存
                if p_date != 0:
                    f.writelines(p_date + ' ' + p_time + ' ' + p_frame + '\n')
                f.writelines(each)
            else:
                if len(temp) == 3:  # 某個HMD 暫時假設對稱訊號不會跨過HMD 那在這個階段的時候 前一個訊號必定當作不是對稱
                    if p_date != 0:
                        f.writelines(p_date + ' ' + p_time + ' ' + p_frame + '\n')
                        p_date, p_time, p_frame, p_hand, p_vib_value, p_freq, p_freq_value, p_dur, p_dur_value = 0, 0, 0, 0, 0, 0, 0, 0, 0
                        prev_each = 0
                    f.writelines(each)

                else:
                    n_date, n_time, n_frame, n_hand, n_vib_value, n_freq, n_freq_value, n_dur, n_dur_value = temp
                    # 判斷全相同就兩個都寫入 prev清空
                    # 判斷不同的話 前一個寫入 再補上後一個
                    if n_vib_value == p_vib_value and n_freq_value == p_freq_value and n_dur_value == p_dur_value:
                        n_ms, p_ms = int((n_time.split('.'))[1]), int((p_time.split('.'))[1])
                        if n_hand != p_hand and (abs(n_ms - p_ms) <= time_window or abs(n_ms - p_ms + 1000) <= time_window):
                            f.writelines(prev_each)
                            f.writelines(each)
                            p_date, p_time, p_frame, p_hand, p_vib_value, p_freq, p_freq_value, p_dur, p_dur_value = 0, 0, 0, 0, 0, 0, 0, 0, 0
                            prev_each = 0
                            continue
                    if p_date != 0:
                        f.writelines(p_date + ' ' + p_time + ' ' + p_frame + '\n')
                    prev_each = each
                    p_date, p_time, p_frame, p_hand, p_vib_value, p_freq, p_freq_value, p_dur, p_dur_value = temp.copy()


def nonsymmetric_data(log_directory):
    with open(os.path.join(log_directory + '/complete.txt'), 'r') as f:
        data = f.readlines()

    with open(os.path.join(log_directory + '/nonsymmetry.txt'), 'w') as f:
        p_date, p_time, p_frame, p_hand, p_vib_value, p_freq, p_freq_value, p_dur, p_dur_value = 0, 0, 0, 0, 0, 0, 0, 0, 0
        prev_each = 0
        for index, each in enumerate(data):
            temp = each.split()
            if index == len(data) - 1:
                if p_date != 0:
                    f.writelines(prev_each)
                f.writelines(each)
            else:
                if len(temp) == 3:
                    if p_date != 0:
                        f.writelines(prev_each)
                        p_date, p_time, p_frame, p_hand, p_vib_value, p_freq, p_freq_value, p_dur, p_dur_value = 0, 0, 0, 0, 0, 0, 0, 0, 0
                        prev_each = 0
                    f.writelines(each)

                else:
                    n_date, n_time, n_frame, n_hand, n_vib_value, n_freq, n_freq_value, n_dur, n_dur_value = temp
                    # 判斷全相同就兩個都寫入 prev清空
                    # 判斷不同的話 前一個寫入 再補上後一個
                    if n_vib_value == p_vib_value and n_freq_value == p_freq_value and n_dur_value == p_dur_value:
                        n_ms, p_ms = int((n_time.split('.'))[1]), int((p_time.split('.'))[1])
                        if n_hand != p_hand and (abs(n_ms - p_ms) <= time_window or abs(n_ms - p_ms + 1000) <= time_window):
                            f.writelines(p_date + ' ' + p_time + ' ' + p_frame + '\n')
                            f.writelines(n_date + ' ' + n_time + ' ' + n_frame + '\n')
                            p_date, p_time, p_frame, p_hand, p_vib_value, p_freq, p_freq_value, p_dur, p_dur_value = 0, 0, 0, 0, 0, 0, 0, 0, 0
                            prev_each = 0
                            continue
                    if p_date != 0:
                        f.writelines(prev_each)
                    prev_each = each
                    p_date, p_time, p_frame, p_hand, p_vib_value, p_freq, p_freq_value, p_dur, p_dur_value = temp.copy()


def validate_test(log_directory):
    with open(os.path.join(log_directory + '/nonsymmetry.txt'), 'r') as f:
        data = f.readlines()
    data2 = []
    for each in data:
        temp = each.split()
        if len(temp) > 3:
            data2.append(each)
    print(len(data2))


debug = False  # debug mode 才會存出其他的txt
time_window = 4  # 2ms以內的都會辨識為對稱訊號
if __name__ == '__main__':
    # print(sys.argv)
    path = selectdirectory()
    data_preprocess(path)
    full_data_log(path)
    symmetric_data(path)
    nonsymmetric_data(path)

    # validate_test(path)
