import os.path
import threading
import matplotlib.pyplot as plt
import math
import numpy as np
import tkinter as tk
import cv2
from tkinter import filedialog
# from ffpyplayer.player import MediaPlayer


def set_global_end_thread(status):
    global end_thread
    end_thread = status
    return


def set_global_start_thread(status):
    global start_thread
    start_thread = status
    return


def button_thread():
    global root, start_frame_entry, end_frame_entry, event_entry, end_thread
    # 創建button的外框
    root = tk.Tk()
    root.title('Buttons')  # 視窗命名
    root.geometry('400x200')  # 定義寬高
    root.geometry('+0+200')  # 定義離左上多遠

    # 基本button
    play_button = tk.Button(root, text='play', command=button_play, width=10).grid(row=0, column=0, rowspan=4, columnspan=4)
    pause_button = tk.Button(root, text='pause', command=button_pause, width=10).grid(row=0, column=4, rowspan=4, columnspan=4)
    exit_button = tk.Button(root, text='exit', command=button_exit, width=10).grid(row=0, column=8, rowspan=4, columnspan=4)
    speedup_button = tk.Button(root, text='+', command=button_speedup, width=25).grid(row=12, column=0, rowspan=2, columnspan=6)
    speeddown_button = tk.Button(root, text='-', command=button_speeddown, width=25).grid(row=12, column=6, rowspan=2, columnspan=6)
    askdirectory_button=tk.Button(root, text='work directory',command=button_workdirectory, width=12).grid(row=14, column=0, rowspan=2, columnspan=4)
    selectvideo_button = tk.Button(root, text='select video',command=button_selectvideo, width=12).grid(row=14, column=4, rowspan=2,columnspan=4)
    selectdatalog_button = tk.Button(root, text='select datalog',command=button_selectdatalog, width=12).grid(row=14, column=8, rowspan=2, columnspan=4)

    # 影片時間軸相關button
    start_frame_Label = tk.Label(root, text='start of frame').grid(row=4, column=0, rowspan=2, columnspan=4)
    start_frame_entry = tk.Entry(root)
    start_frame_entry.grid(row=4, column=4, rowspan=2, columnspan=4)
    end_frame_Label = tk.Label(root, text='end of frame').grid(row=6, column=0, rowspan=2, columnspan=4)
    end_frame_entry = tk.Entry(root)
    end_frame_entry.grid(row=6, column=4, rowspan=2, columnspan=4)
    apply_button = tk.Button(root, text='apply', command=button_apply, width=10).grid(row=4, column=8, rowspan=4, columnspan=4)
    current_frame = tk.Label(root, text='current frame').grid(row=16, column=0, rowspan=4, columnspan=4)
    current_frame = tk.Label(root, text='1').grid(row=16, column=4, rowspan=4, columnspan=4)

    # 紀錄事件相關button
    event_name_Label = tk.Label(root, text='event name').grid(row=8, column=0, rowspan=4, columnspan=4)
    event_entry = tk.Entry(root)
    event_entry.grid(row=8, column=4, rowspan=4, columnspan=4)
    record_button = tk.Button(root, text='record', command=button_record, width=10).grid(row=8, column=8, rowspan=4, columnspan=4)

    # 循環吃button狀態
    root.mainloop()



def movie_thread(start_frame, end_frame):
    global end_thread, start_thread
    global workdirectory, selectvideo, selectdatalog, controller_plot_path, full_image_path
    # mutex lock 卡一下thread 避免沒關成功
    while not start_thread:
        pass
    start_thread = False



    # 讀影片資料
    video_capture = cv2.VideoCapture(selectvideo)
    # video_length = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)

    # 讀聲音資料
    # player = MediaPlayer('./documents/test_video.mp4')

    # 用在影片的para們
    global video_frame_rate, running_frame_delay, speedup, pause
    pause = False
    speedup = 1
    video_frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    running_frame_delay = math.ceil(1000 / (video_frame_rate * speedup))

    # 算input區間段的data_signal 並且回傳那個"真實時間點" 用來對應影片時間點
    start_of_full_data_time, end_of_full_data_time, start_of_target_data_time, end_of_target_data_time = partial_data_log(start_frame, end_frame)
    # print(start_of_target_data_time, end_of_target_data_time, start_of_full_data_time, end_of_full_data_time)
    # 拆成 hour:minute:second:frame 的格式
    sth, stm, sts, stf = start_of_target_data_time.split(':')
    eth, etm, ets, etf = end_of_target_data_time.split(':')
    sdh, sdm, sds, sdf = start_of_full_data_time.split(':')
    # edh, edm, eds, edf = end_of_full_data_time.split(':')
    # 計算出目標偵的對應影片點
    target_video_frame = ((int(sth) * 60 * 60 + int(stm) * 60 + int(sts)) - (int(sdh) * 60 * 60 + int(sdm) * 60 + int(sds))) * video_frame_rate
    end_video_frame = ((int(eth) * 60 * 60 + int(etm) * 60 + int(ets)) - (int(sdh) * 60 * 60 + int(sdm) * 60 + int(sds))) * video_frame_rate
    # print(target_video_frame)
    # print(end_video_frame)
    # 算好以後設定video 開始點
    video_capture.set(1, target_video_frame-1)

    # 處理聲音
    # player = MediaPlayer('./documents/test_video.mp4')

    # 吃前面partial算完存的圖
    #controller_plot_path=os.path.join(workdirectory + '/controller_plot.png')
    controller_plot = cv2.imread(controller_plot_path)
    # controller_plot = cv2.resize(controller_plot, (480, 360), interpolation=cv2.INTER_NEAREST)

    # pre process會把整個完整的全部vibration data做成一張圖 在這邊load進來
    full_image_path=os.path.join(workdirectory + '/full_image2.png')
    full_image = cv2.imread(full_image_path)
    full_image = cv2.resize(full_image, (controller_plot.shape[1], controller_plot.shape[0]), interpolation=cv2.INTER_NEAREST)

    # 用一個while迴圈控制這個thread的結束
    count, length = 0, end_video_frame - target_video_frame
    while not end_thread:
        if count > length:
            while not end_thread:
                pass
            break

        # 底下這坨是在組合前面拿到的各個影像
        ret, video_frame = video_capture.read()
        # x, y = video_frame.shape[:2]
        video_frame = cv2.resize(video_frame, (1080, 800), interpolation=cv2.INTER_NEAREST)

        h1, w1 = video_frame.shape[:2]
        h2, w2 = controller_plot.shape[:2]
        h3, w3 = full_image.shape[:2]
        img_3 = np.zeros((max(h1, h2 + h3), w1 + max(w2, w3), 3), dtype=np.uint8)

        img_3[:h1, :w1, :3] = video_frame
        img_3[:h2, w1:w1 + w2, :3] = controller_plot
        img_3[h2:h2 + h3, w1:w1 + w3, :3] = full_image
        cv2.imshow('Data Labeling', img_3)
        count += 1
        while pause:
            if end_thread:
                break
            continue
        cv2.waitKey(running_frame_delay)  # 利用這邊wait key的waiting time(ms)來控制後續movie_log裡面的播放速度(偵)

    cv2.destroyAllWindows()
    video_capture.release()
    start_thread = True
    end_thread = False
    return


def partial_data_log(start_frame, end_frame):
    global workdirectory, selectvideo, selectdatalog, controller_plot_path
    controller_plot_path = os.path.join(workdirectory + '/controller_plot.png')
    with open(selectdatalog, 'r') as f:
        data = f.readlines()
    lx, ly, rx, ry = [], [], [], []
    previous = data[start_frame]
    data_start_time, data_end_time = (data[0].split())[1], (data[len(data) - 1].split())[1]
    target_start_time, target_end_time = (data[start_frame].split())[1], (data[end_frame].split())[1]
    prev_data_time = 0
    left_modified = False
    right_modified = False
    for each in np.array(data[start_frame + 1:end_frame]):
        temp = each.split()
        if 'Left' in each or 'Right' in each: # 現在是左右手訊號
            if prev_data_time == 0:
                print("error: data no start with HMD")
            elif 'Left' in each:
                lx = np.append(lx, temp[1])
                ly = np.append(ly, float(temp[3]))
                left_modified = True
            elif 'Right' in each:
                rx = np.append(rx, temp[1])
                ry = np.append(ry, float(temp[3]))
                right_modified = True
        else:
            if prev_data_time == 0:
                pass
            elif left_modified or right_modified: # 兩手有資料
                if left_modified and right_modified:
                    pass
                elif left_modified:
                    rx = np.append(rx, prev_data_time)
                    ry = np.append(ry, [0.0])
                elif right_modified:
                    lx = np.append(lx, prev_data_time)
                    ly = np.append(ly, [0.0])
            else: # 兩手都沒資料 各塞一個空值進去
                lx = np.append(lx, prev_data_time)
                ly = np.append(ly, [0.0])
                rx = np.append(rx, prev_data_time)
                ry = np.append(ry, [0.0])
            prev_data_time = temp[1]
            left_modified = False
            right_modified = False
        # temp = previous.split()
        # if 'Left' in each or 'Right' in each: # 現在是左右手訊號
        #     if 'Left' in previous:
        #         lx = np.append(lx, temp[1])
        #         ly = np.append(ly, float(temp[3]))
        #     elif 'Right' in previous:
        #         rx = np.append(rx, temp[1])
        #         ry = np.append(ry, float(temp[3]))
        # else: # 現在不是左右手訊號
        #     if 'Left' in previous:
        #         lx = np.append(lx, temp[1])
        #         ly = np.append(ly, float(temp[3]))
        #         rx = np.append(rx, temp[1])
        #         ry = np.append(ry, [0.0])
        #     elif 'Right' in previous:
        #         lx = np.append(lx, temp[1])
        #         ly = np.append(ly, [0.0])
        #         rx = np.append(rx, temp[1])
        #         ry = np.append(ry, float(temp[3]))
        #     else:
        #         lx = np.append(lx, temp[1])
        #         ly = np.append(ly, [0.0])
        #         rx = np.append(rx, temp[1])
        #         ry = np.append(ry, [0.0])
        # previous = each
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
    plt.savefig(controller_plot_path)
    # plt.show()
    return data_start_time, data_end_time, target_start_time, target_end_time

#Save img 抓controller_plot 重新改檔名

def button_workdirectory():
    global workdirectory
    root2 = tk.Tk()
    root2.withdraw()
    workdirectory= filedialog.askdirectory(parent=root2, initialdir='~/VibrationLabeler-master')
    return workdirectory

def button_selectvideo():
    global selectvideo
    root2 = tk.Tk()
    root2.withdraw()
    selectvideo = filedialog.askopenfilename(parent=root2, initialdir='~/VibrationLabeler-master')
    return selectvideo

def button_selectdatalog():
    global selectdatalog
    root2 = tk.Tk()
    root2.withdraw()
    selectdatalog = filedialog.askopenfilename(parent=root2, initialdir='~/VibrationLabeler-master')
    return selectdatalog

def button_record():
    global event_entry
    name_of_event = event_entry.get()
    with open('./documents/events.txt', 'a') as f:
        f.writelines(name_of_event + ' ' + start_frame_entry.get() + ' ' + end_frame_entry.get() + '\n')
    return


def button_apply():
    global start_frame_entry, end_frame_entry, end_thread
    start_frame = int(start_frame_entry.get())
    end_frame = int(end_frame_entry.get())
    # mutex lock 卡thread 避免重複執行
    if not start_thread:
        end_thread = True
    else:
        end_thread = False
    t2 = threading.Thread(target=movie_thread, args=[start_frame, end_frame])
    t2.start()

    return


def button_exit():
    global end_thread
    end_thread = True
    root.quit()
    return


def button_pause():
    global pause
    pause = True
    return


def button_play():
    global pause
    pause = False
    return


def button_speedup():
    global speedup, running_frame_delay
    speedup *= 2
    running_frame_delay = math.ceil(1000 / (video_frame_rate * speedup))
    return


def button_speeddown():
    global speedup, running_frame_delay
    speedup /= 2
    running_frame_delay = math.ceil(1000 / (video_frame_rate * speedup))
    return
