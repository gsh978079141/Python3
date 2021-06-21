import queue
import threading
import cv2 as cv
import subprocess as sp


class Live(object):
    def __init__(self):
        self.frame_queue = queue.Queue()
        self.command = ""
        # 自行设置
        self.rtspUrl = "rtsp://192.168.112.51:10081/"
        # self.rtmpUrl = "rtmp://192.168.112.51:1935/demo/gsh"
        self.rtmpUrl = "rtmp://10.16.32.165:31663/demo/gsh"
        self.camera_path = 0

    def read_frame(self):
        print("开启推流")
        cap = cv.VideoCapture(self.camera_path)

        # Get video information
        fps = int(cap.get(cv.CAP_PROP_FPS))
        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

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
                        self.rtmpUrl]

        # read webcamera
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Opening camera is failed")
                # 说实话这里的break应该替换为：
                # cap = cv.VideoCapture(self.camera_path)
                # 因为我这俩天遇到的项目里出现断流的毛病
                # 特别是拉取rtmp流的时候！！！！
                break

            # put frame into queue
            self.frame_queue.put(frame)

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

    # def run(self):
    #     threads = [
    #         threading.Thread(target=Live.read_frame, args=(self,)),
    #         threading.Thread(target=Live.push_frame, args=(self,))
    #     ]
    #     [thread.setDaemon(True) for thread in threads]
    #     [thread.start() for thread in threads]
    def run(self):
        thread_read_frame = threading.Thread(target=Live.read_frame, args=([self]))
        thread_read_frame.daemon = True
        thread_read_frame.start()


if __name__ == '__main__':
    live = Live()
    live.run()
    live.push_frame()
