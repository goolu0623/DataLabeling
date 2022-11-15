import threading
from objects import Button
from objects import Movie


def main():
    button_object = Button()
    t1 = threading.Thread(target=button_object.mainThread)
    t1.start()


if __name__ == '__main__':
    main()
