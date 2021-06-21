import queue
import threading
import cv2 as cv
import subprocess as sp
from PIL import ImageGrab
import numpy as np


class Live(object):
    def __init__(self):
        self.frame_queue = queue.Queue()
        self.command = ""
        # 自行设置
        # self.rtmpUrl = "rtmp://192.168.112.51:1935/demo/gsh"
        self.rtmp_url = "rtmp://10.16.32.165:31663/demo/luping"

    def read_frame(self):
        print("开启推流")
        # 延时录制
        start = 3
        fps = 20
        # 获取屏幕对象
        cur_screen = ImageGrab.grab()
        height, width = cur_screen.size

        # ffmpeg command
        self.command = ['ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        # S rtsp
                        # '-f', 'rtsp',
                        # self.rtspUrl,
                        # E rtsp
                        self.rtmp_url]

        # read webcamera
        image_num = 0
        p = sp.Popen(self.command, stdin=sp.PIPE)
        while True:
            image_num += 1
            # 抓取屏幕
            capture_image = ImageGrab.grab()
            frame = cv.cvtColor(np.array(capture_image), cv.COLOR_RGB2BGR)
            if image_num > fps:
                p.stdin.write(frame.tostring())


    def push_frame(self):
        # 防止多线程时 command 未被设置
        while True:
            if len(self.command) > 0:
                # 管道配置
                p = sp.Popen(self.command, stdin=sp.PIPE)
                break

        while True:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                # process frame
                # 你处理图片的代码
                # write to pipe
                p.stdin.write(frame.tostring())

    def run(self):
        thread_read_frame = threading.Thread(target=Live.read_frame, args=([self]))
        thread_read_frame.daemon = True
        thread_read_frame.start()


if __name__ == '__main__':
    live = Live()
    live.read_frame()
