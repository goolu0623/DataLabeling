import enum
import os.path
import threading
import matplotlib.pyplot as plt
import math
import numpy as np
import tkinter as tk
from tkinter import ttk
import cv2
from tkinter import filedialog
import shutil


# 變數全小寫 _ 分隔
# class CamelCase
# function camelCase


# class ButtonType(enum.Enum):
#     ask_dir = 3
#     movie_path = 9
#     complete = 87


class Button:
    def __init__(self):
        # button區的檔案屬性
        root = tk.Tk()
        root.withdraw()
        self.work_directory = filedialog.askdirectory(parent=root, initialdir='~/VibrationLabeler-master', title='choose the root directory')
        self.select_movie_path = filedialog.askopenfilename(parent=root, initialdir='~/VibrationLabeler-master', title='select the video')
        self.complete_data_path = os.path.join(self.work_directory + '/complete.txt')
        self.symmetric_data_path = os.path.join(self.work_directory + '/symmetry.txt')
        self.nonsymmetric_data_path = os.path.join(self.work_directory + '/nonsymmetry.txt')
        root.destroy()

        # 控制影片的參數
        self.start_frame = 0
        self.end_frame = 0
        self.graph_type = 0
        self.playing_movie = Movie(self)
        with open(self.complete_data_path, 'r') as f:
            self.total_length = len(f.readlines())
        # print(ButtonType(3))
        # print(ButtonType.complete == 87)
        # print(ButtonType.complete)
        # ButtonType.complete

    def buttonPlayPauseClick(self):
        if self.playing_movie.is_play:
            self.playing_movie.pause()
        else:
            self.playing_movie.play()

    def buttonExitClick(self, root):
        if self.playing_movie is not None:
            self.playing_movie.exit()
        image_path = os.path.join(self.work_directory + '/controller_plot.png')
        if os.path.exists(image_path) is True:
            os.remove(image_path)
        root.quit()

    def buttonApplyClick(self):
        self.playing_movie.exit()
        self.playing_movie = Movie(self, start_frame=self.start_frame, end_frame=self.end_frame)
        t2 = threading.Thread(target=self.playing_movie.mainThread)
        t2.start()

    def buttonSpeedLevelChange(self, sv):
        self.playing_movie.speedChange(float(sv.get()))

    def buttonRecordClick(self, event_entry):
        name_of_event = event_entry.get()
        events_path = os.path.join(self.work_directory + '/documents/events.txt')
        org_image_path = os.path.join(self.work_directory + '/controller_plot.png')
        new_image_path = os.path.join(self.work_directory + '/documents/' + name_of_event + '.png')
        documents_dir_path = os.path.join(self.work_directory + '/documents/')
        # 創資料夾
        if os.path.exists(documents_dir_path) is False:
            os.mkdir(documents_dir_path)
        # 複製影像
        shutil.copyfile(org_image_path, new_image_path)

        with open(events_path, 'a') as f:
            f.writelines(name_of_event + ' ' + str(self.start_frame) + ' ' + str(self.end_frame) + '\n')

    def buttonAskDirectoryClick(self, root):
        self.work_directory = filedialog.askdirectory(parent=root, initialdir='~/VibrationLabeler-master', title='choose the root directory')

    def buttonSelectVideoPathClick(self, root):
        self.select_movie_path = filedialog.askopenfilename(parent=root, initialdir='~/VibrationLabeler-master', title='select the video')

    def buttonSelectCompleteDataPathClick(self, root):
        self.complete_data_path = filedialog.askopenfilename(parent=root, initialdir='~/VibrationLabeler-master', title='select the complete datalog')
        with open(self.complete_data_path, 'r') as f:
            self.total_length = len(f.readlines())

    def buttonSelectSymmetricDataPathClick(self, root):
        self.symmetric_data_path = filedialog.askopenfilename(parent=root, initialdir='~/VibrationLabeler-master', title='select the symmetric datalog')
        with open(self.symmetric_data_path, 'r') as f:
            self.total_length = len(f.readlines())

    def buttonSelectNonSymmetricDataPathClick(self, root):
        self.nonsymmetric_data_path = filedialog.askopenfilename(parent=root, initialdir='~/VibrationLabeler-master', title='select the nonsymmetric datalog')
        with open(self.nonsymmetric_data_path, 'r') as f:
            self.total_length = len(f.readlines())

    def entryStartFrameChange(self, sv):
        if sv.get() == '':
            self.start_frame = 0
        else:
            self.start_frame = int(sv.get())

    def entryEndFrameChange(self, sv):
        if sv.get() == '':
            self.end_frame = 0
        else:
            self.end_frame = int(sv.get())

    def buttonSelectGraphType(self, sv):
        if sv.get() == 'complete':
            self.graph_type = 0
        elif sv.get() == 'symmetric':
            self.graph_type = 1
        else:
            self.graph_type = 2

    def mainThread(self):
        # print('button mainThread start, id= ', threading.get_ident())

        # 設定基本tk window的屬性
        root = tk.Tk()
        root.title('Buttons')  # 視窗命名
        root.geometry('390x200')  # 定義寬高
        root.geometry('+500+500')  # 定義離左上多遠

        # 基本按鈕
        play_puase_button = tk.Button(master=root, text='play/pause', command=self.buttonPlayPauseClick, width=10)
        exit_button = tk.Button(master=root, text='exit', command=lambda: self.buttonExitClick(root), width=10)
        apply_button = tk.Button(root, text='apply', command=self.buttonApplyClick, width=10)

        # 選播放速度

        speed_level_label = tk.Label(root, text='play speed')
        speed_level_var = tk.StringVar()
        speed_level_var.trace('w', lambda name, index, mode, var=speed_level_var: self.buttonSpeedLevelChange(var))
        speed_level_box = ttk.Combobox(root, textvariable=speed_level_var, values=[0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2])

        # 選檔案路徑
        ask_directory_button = tk.Button(master=root, text='work directory', command=lambda: self.buttonAskDirectoryClick(root), width=12)  # TBD------------
        select_video_button = tk.Button(master=root, text='video path', command=lambda: self.buttonSelectVideoPathClick(root), width=12)  # TBD------------
        select_datalog_button = tk.Button(master=root, text='datalog path', command=lambda: self.buttonSelectCompleteDataPathClick(root), width=12)  # TBD------------
        select_nonsymmetric_datalog_button = tk.Button(master=root, text='nonsymmetric path', command=lambda: self.buttonSelectNonSymmetricDataPathClick(root), width=12)  # TBD------------
        select_symmetric_datalog_button = tk.Button(master=root, text='symmetric path', command=lambda: self.buttonSelectSymmetricDataPathClick(root), width=12)  # TBD------------

        # 選作圖型態
        graph_type_label = tk.Label(root, text='graph type')
        graph_type_var = tk.StringVar()
        graph_type_var.trace('w', lambda name, index, mode, var=graph_type_var: self.buttonSelectGraphType(var))
        graph_type_box = ttk.Combobox(root, textvariable=graph_type_var, values=['complete', 'symmetric', 'nonsymmetric'])

        # 影片時間軸相關button

        start_frame_label = tk.Label(root, text='start of frame')
        start_frame_variable = tk.StringVar()
        start_frame_variable.trace('w', lambda name, index, mode, var=start_frame_variable: self.entryStartFrameChange(var))
        start_frame_entry = tk.Entry(root, textvariable=start_frame_variable)
        # start_frame_entry = tk.Entry(root)

        end_frame_label = tk.Label(root, text='end of frame')
        end_frame_variable = tk.StringVar()
        end_frame_variable.trace('w', lambda name, index, mode, var=end_frame_variable: self.entryEndFrameChange(var))
        end_frame_entry = tk.Entry(root, textvariable=end_frame_variable)

        total_length_label = tk.Label(root, text='total data length : ' + str(self.total_length))

        # record按鈕
        event_name_label = tk.Label(root, text='event name')
        event_entry = tk.Entry(root)
        record_button = tk.Button(root, text='record', command=lambda: self.buttonRecordClick(event_entry), width=10)

        # 按鈕排列
        play_puase_button.grid(row=0, column=0, rowspan=4, columnspan=4)
        exit_button.grid(row=0, column=4, rowspan=4, columnspan=4)
        apply_button.grid(row=0, column=8, rowspan=4, columnspan=4)

        ask_directory_button.grid(row=14, column=0, rowspan=2, columnspan=4)
        select_video_button.grid(row=14, column=4, rowspan=2, columnspan=4)
        select_datalog_button.grid(row=16, column=0, rowspan=2, columnspan=4)
        select_nonsymmetric_datalog_button.grid(row=16, column=4, rowspan=2, columnspan=4)
        select_symmetric_datalog_button.grid(row=16, column=8, rowspan=2, columnspan=4)

        start_frame_label.grid(row=4, column=0, rowspan=2, columnspan=4)
        start_frame_entry.grid(row=4, column=4, rowspan=2, columnspan=4)
        end_frame_label.grid(row=6, column=0, rowspan=2, columnspan=4)
        end_frame_entry.grid(row=6, column=4, rowspan=2, columnspan=4)
        total_length_label.grid(row=4, column=8, rowspan=4, columnspan=4)

        event_name_label.grid(row=8, column=0, rowspan=2, columnspan=4)
        event_entry.grid(row=8, column=4, rowspan=2, columnspan=4)
        record_button.grid(row=8, column=8, rowspan=2, columnspan=4)

        graph_type_label.grid(row=20, column=0, rowspan=2, columnspan=4)
        graph_type_box.grid(row=20, column=4, rowspan=2, columnspan=4)

        speed_level_label.grid(row=22, column=0, rowspan=2, columnspan=4)
        speed_level_box.grid(row=22, column=4, rowspan=2, columnspan=4)

        # 測試trace空白格
        # test_string = tk.StringVar()
        # test_string.trace('w', lambda name, index, mode, var=test_string: self.test(var))
        # test_entry = tk.Entry(root, textvariable=test_string)
        # test_entry.grid(row=28, column=0)

        # 循環
        root.mainloop()
        # print('button mainThread end, id= ', threading.get_ident())


class Movie:

    def __init__(self, parent, start_frame=0, end_frame=1000, play_speed=1):

        # 母button物件
        self.parent_button_object = parent

        # 影片播放屬性
        self.play_speed = play_speed
        self.start_frame = start_frame  # 起始影格
        self.end_frame = end_frame  # 結束影格
        self.graph_type = parent.graph_type  # [0, 1 ,2] = [都要, 對稱, 非對稱]

        # 影片流程控制
        self.is_play = True
        self.is_exit = False

        # 影片檔案屬性
        self.movie_path = self.parent_button_object.select_movie_path
        self.work_directory = self.parent_button_object.work_directory
        self.complete_data_path = self.parent_button_object.complete_data_path
        self.symmetric_data_path = self.parent_button_object.symmetric_data_path
        self.nonsymmetric_data_path = self.parent_button_object.nonsymmetric_data_path

        video_capture = cv2.VideoCapture(self.movie_path)
        self.frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
        self.running_frame_delay = math.ceil(1000 / (self.frame_rate * self.play_speed))
        video_capture.release()
        # 母視窗

    def play(self):
        self.is_play = True

    def pause(self):
        self.is_play = False

    def exit(self):
        self.is_exit = True

    def speedChange(self, targetSpeed=1.0):
        self.play_speed = targetSpeed
        self.running_frame_delay = math.ceil(1000 / (self.frame_rate * self.play_speed))

    def dataPlot(self):
        datalog_type_select = 0
        if self.graph_type == 0:
            datalog_type_select = self.complete_data_path
        elif self.graph_type == 1:
            datalog_type_select = self.symmetric_data_path
        elif self.graph_type == 2:
            datalog_type_select = self.nonsymmetric_data_path

        with open(datalog_type_select, 'r') as f:
            data = f.readlines()
        lx, ly, rx, ry = [], [], [], []

        data_start_time, data_end_time = (data[0].split())[1], (data[len(data) - 1].split())[1]  # 全部整個檔案的頭最尾
        target_start_time, target_end_time = (data[self.start_frame].split())[1], (data[self.end_frame].split())[1]  # 目標時間軸的頭尾
        prev_data_time = 0
        left_modified = False
        right_modified = False
        for each in data[self.start_frame + 1:self.end_frame]:
            temp = each.split()

            if 'Left' in each or 'Right' in each:
                if prev_data_time == 0:
                    pass
                    # print("error: data not start with HMD")
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
        x_major_locator = plt.MultipleLocator((self.end_frame - self.start_frame) / 6)
        ax[0].xaxis.set_major_locator(x_major_locator)
        ax[1].xaxis.set_major_locator(x_major_locator)
        ax[0].set_ylim([0, 1.1])
        ax[1].set_ylim([0, 1.1])

        plt.tight_layout()
        controller_plot_path = os.path.join(self.work_directory + '/controller_plot.png')
        plt.savefig(controller_plot_path)
        return data_start_time, data_end_time, target_start_time, target_end_time

        pass

    def mainThread(self):
        # print('movie mainThread start, id= ', threading.get_ident())

        # 讀影片資料
        video_capture = cv2.VideoCapture(self.movie_path)

        # 算input區間段的data_signal 並且回傳那個"真實時間點" 用來對應影片時間點
        start_of_full_data_time, end_of_full_data_time, start_of_target_data_time, end_of_target_data_time = self.dataPlot()

        # 拆成 hour:minute:second:frame 的格式
        sth, stm, sts_and_stms = start_of_target_data_time.split(':')
        sts, stms = sts_and_stms.split('.')
        eth, etm, ets_and_etms = end_of_target_data_time.split(':')
        ets, etms = ets_and_etms.split('.')
        sdh, sdm, sds_and_sdms = start_of_full_data_time.split(':')
        sds, sdms = sds_and_sdms.split('.')
        # edh, edm, eds, edf = end_of_full_data_time.split(':')

        # 計算出目標偵的對應影片點
        target_video_frame = ((int(sth) * 60 * 60 + int(stm) * 60 + int(sts)) - (int(sdh) * 60 * 60 + int(sdm) * 60 + int(sds))) * self.frame_rate
        end_video_frame = ((int(eth) * 60 * 60 + int(etm) * 60 + int(ets)) - (int(sdh) * 60 * 60 + int(sdm) * 60 + int(sds))) * self.frame_rate

        # 算好以後設定video 開始點
        video_capture.set(1, target_video_frame - 1)

        # 吃前面partial算完存的圖
        controller_plot_path = os.path.join(self.work_directory + '/controller_plot.png')
        controller_plot = cv2.imread(controller_plot_path)

        # pre process會把整個完整的全部vibration data做成一張圖 在這邊load進來
        full_image_path = os.path.join(self.work_directory + '/full_image.png')
        full_image = cv2.imread(full_image_path)
        full_image = cv2.resize(full_image, (controller_plot.shape[1], controller_plot.shape[0]), interpolation=cv2.INTER_NEAREST)
        count, length = 0, end_video_frame - target_video_frame
        while self.is_exit is False:
            # 影片播放範圍
            if count > length:
                while self.is_exit is False:
                    pass
                break
            count += 1
            # 用spinlock暫停播放
            while self.is_play is False:
                if self.is_exit is True:
                    break
                continue
            # 組合要放出來的畫面
            ret, video_frame = video_capture.read()
            video_frame = cv2.resize(video_frame, (1080, 800), interpolation=cv2.INTER_NEAREST)

            h1, w1 = video_frame.shape[:2]
            h2, w2 = controller_plot.shape[:2]
            h3, w3 = full_image.shape[:2]
            img_3 = np.zeros((max(h1, h2 + h3), w1 + max(w2, w3), 3), dtype=np.uint8)

            img_3[:h1, :w1, :3] = video_frame
            img_3[:h2, w1:w1 + w2, :3] = controller_plot
            img_3[h2:h2 + h3, w1:w1 + w3, :3] = full_image
            cv2.imshow('Data Labeling', img_3)

            # 利用waitkey的機制控制播放速度
            cv2.waitKey(self.running_frame_delay)

        # 結束整個thread
        cv2.destroyAllWindows()
        video_capture.release()
        # print('movie mainThread end, id= ', threading.get_ident())
