from .screen_reader import ScreenReader
from time import sleep

def main():
    sleep(5)
    sr = ScreenReader()
    sr.main_loop()

if __name__ =="__main__":
    main()