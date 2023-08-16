# general module
import random
import time
import threading

# 自作モジュール
import download

class SampleThreading(threading.Thread):
    
    def __init__(self, url):
        self.url = str(url)
        threading.Thread.__init__(self)
    
    def __str__(self):
        return str(self.url)
    
    def run(self):
        print('Thread: %s started.' % self)
        download.download_img(self.url)
        print('Thread: %s ended.' % self)


def main():
    # 入力
    input_path = "img_dlp.txt"
    print(input_path)
    with open(input_path,"r") as f:
        input_txt = [s.rstrip() for s in f.readlines()]
    

    for i in range(len(input_txt)):
        if download.is_ok_url(input_txt[i]):
            thread = SampleThreading(input_txt[i])
            thread.start()


if __name__ == '__main__':
    main()
