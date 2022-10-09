import threading
import module.func as fn

def main():
    # 先在那邊set 一個我要的global用來控thread
    fn.set_global_end_thread(False)
    # 先set start_thread用來控mutex lock
    fn.set_global_start_thread(True)
    # 開thread跑button視窗
    t1 = threading.Thread(target=fn.button_thread)
    t1.start()
    # 開thread跑movie視窗
    t2 = threading.Thread(target=fn.movie_thread, args=[0, 200])
    t2.start()

    return


if __name__ == '__main__':
    main()
