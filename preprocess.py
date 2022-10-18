import numpy as np
import matplotlib.pyplot as plt
from time import sleep
# from tqdm import tqdm

def data_preprocess():
    # 先讀資料
    with open('./documents/test_log.txt', 'r') as f:
        data = f.readlines()

    # 有空白行的部分清掉
    i = 0
    while i < len(data):
        if data[i] == '\n':
            data.pop(i)
        else:
            i += 1
    # 寫回不含空白行的
    with open('./documents/test_log_modified.txt', 'w') as f:
        for each in data:
            f.writelines(each)
    # 根據每HMD定義偵數 然後先刪掉所有無關vib的資料
    with open('./documents/test_log_only_vib_and_HMD.txt', 'w') as f:
        for each in data:
            if 'HMD' in each or 'Vibration' in each:
                f.writelines(each)

    with open('./documents/test_log_only_vib_and_HMD.txt', 'r') as f:
        data = f.readlines()
    with open('./documents/test_log_only_vib_and_time.txt', 'w') as f:
        for each in data:
            if 'HMD' in each:
                temp = each.split('  :HMD')
                f.write(temp[0] + '\n')
            else:
                f.writelines(each)
    with open('./documents/test_log_only_vib_and_time.txt', 'r') as f:
        data = f.readlines()
    with open('./documents/text_log_only_vib_extend_timestamp.txt', 'w') as f:
        time_stamp, frame_number = 0, 0

        for each in data:
            each_list = each.split()
            if len(each_list) == 2:
                if time_stamp != each_list[1]:
                    time_stamp = each_list[1]
                    frame_number = 0
                else:
                    frame_number += 1
                f.write(each_list[0] + ' ' + each_list[1] + ':' + str(frame_number) + '\n')
            else:
                f.write(each_list[0] + ' ' + each_list[1] + ':' + str(frame_number))
                for elements in each_list[2:]:
                    f.write(' ' + elements)
                f.write('\n')
    return


def full_data_log():
    with open('documents/text_log_only_vib_extend_timestamp.txt', 'r') as f:
        data = f.readlines()
    start_frame, end_frame = 0, len(data) - 1
    lx, ly, rx, ry = [], [], [], []
    previous = data[start_frame]
    for each in np.array(data[start_frame + 1:end_frame]):
        temp = previous.split()
        if 'Left' in each or 'Right' in each:
            if 'Left' in previous:
                lx = np.append(lx, temp[1])
                ly = np.append(ly, float(temp[3]))
            elif 'Right' in previous:
                rx = np.append(rx, temp[1])
                ry = np.append(ry, float(temp[3]))
        else:
            if 'Left' in previous:
                lx = np.append(lx, temp[1])
                ly = np.append(ly, float(temp[3]))
                rx = np.append(rx, temp[1])
                ry = np.append(ry, [0.0])
            elif 'Right' in previous:
                lx = np.append(lx, temp[1])
                ly = np.append(ly, [0.0])
                rx = np.append(rx, temp[1])
                ry = np.append(ry, float(temp[3]))
            else:
                lx = np.append(lx, temp[1])
                ly = np.append(ly, [0.0])
                rx = np.append(rx, temp[1])
                ry = np.append(ry, [0.0])
        previous = each
    fig, ax = plt.subplots(2, 1,figsize=(10,4))
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
    plt.savefig('./documents/full_image2.png')

    return


def split_symmetry_data():
    with open('documents/text_log_only_vib_extend_timestamp.txt', 'r') as f:
        data = f.readlines()

    with open('documents/text_log_only_vib_without_symmetry.txt', 'w') as f:

        all_list = []
        for each in data:
            each_list = each.split(' ', 3) 
            all_list.append(each_list)

        for i in range(len(all_list)-1):
            first = all_list[i]
            second = all_list[i+1]
            
            if len(first) == 4 and len(second) == 4 and first[1] == second[1] and first[3] == second[3] :
                if 'Right' in data[i] and 'Left' in data[i + 1] or 'Left' in data[i] and 'Right' in data[i + 1]:
                    data[i] = ['']
                    data[i + 1] = ['']
                    f.writelines(data[i])
                    f.writelines(data[i+1])
                else:    
                    f.writelines(data[i])
            else:
                f.writelines(data[i])
    


def only_symmetry_data():
    with open('documents/text_log_only_vib_extend_timestamp.txt', 'r') as f:
        data = f.readlines()

    with open('documents/text_log_only_vib_only_symmetry.txt', 'w') as f:

        all_list = []
        for each in data:
            each_list = each.split(' ', 3) 
            all_list.append(each_list)

        for i in range(len(all_list)-1):
            first = all_list[i]
            second = all_list[i+1]
            
            if len(first) == 2:
                f.writelines(data[i])    
            else:              
                if len(first) == 4 and len(second) == 4 and first[1] == second[1] and first[3] == second[3] :
                    if 'Right' in data[i] and 'Left' in data[i + 1] or 'Left' in data[i] and 'Right' in data[i + 1]:
                        f.writelines(data[i])
                        f.writelines(data[i+1])
                    else:    
                        data[i] = [(all_list[i])[0] , ' ', (all_list[i])[1]]
                        f.writelines(data[i])
                        f.writelines('\n')                        
                else:
                    data[i] = [(all_list[i])[0] , ' ', (all_list[i])[1]]
                    f.writelines(data[i])   
                    f.writelines('\n')                             
    




# # # Progress Bar
# for i in tqdm(range(1, 101)):

#     # split_symmetry_data()
#     # full_data_log()
#     only_symmetry_data()


#     sleep(0.01)
# sleep(0.5)



if __name__ == '__main__':
    full_data_log()
