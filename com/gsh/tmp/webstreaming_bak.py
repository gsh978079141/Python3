# import the necessary packages
from com.gsh.tmp.singlemotiondetector_bak import SingleMotionDetector as smd
from imutils.video import VideoStream
from flask import Response
from flask import Flask
import face_recognition
import os
import threading
import argparse
import datetime
import imutils
import time
import cv2
from PIL import ImageGrab
import numpy as np
import pyaudio
import wave
outputFrame = None
lock = threading.Lock()
app = Flask(__name__)
# vs = VideoStream(src=0).start()
vs = None
time.sleep(2.0)
CHUNK = 256  # 定义数据流块
FORMAT = pyaudio.paInt16  # 量化位数（音量级划分）
CHANNELS = 1  # 声道数;声道数：可以是单声道或者是双声道
RATE = 8000  # 采样率;采样率：一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz, 11.025kHz, 22.05kHz, 44.1kHz
RECORD_SECONDS = 10  # 录音秒数
sampwidth=2 #两个字节十六位


# 动作识别
def detect_motion(frameCount):
    global vs, outputFrame, lock
    md = smd(accumWeight=0.1)
    total = 0
    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        # face.face_shibie(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)

            # check to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                              (0, 0, 255), 2)

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()




# 人脸识别
def face_shibie(frameCount):
    global vs, outputFrame, lock
    md = smd(accumWeight=0.1)

    total = 0
    # store the accumulated weight factor
    # 加载示例图片并学习如何识别它。
    face_dir = "D:/WorkSpaces/Pycharm_WorkSpace/Python3/com/gsh/test/data/in/face/"
    #  ！！！！！！！修改！！！！！！ #
    people_datas = []
    people_face_encoding = []
    people_names = []
    # 遍历人脸图片文件夹
    filenames = os.listdir(face_dir)
    for filename in filenames:
        people_image = face_recognition.load_image_file(face_dir + filename)
        people_face_encoding = face_recognition.face_encodings(people_image)[0]
        people_name = os.path.splitext(filename)[0]
        people_data = {"name": people_name, "people_face_encoding": people_face_encoding}
        people_datas.append(people_data)
    #  ！！！！！！！修改！！！！！！ #
    na = 0
    # 初始化一些变量
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
        frame = vs.read()
        # 将视频帧大小调整为1/4大小，以便更快地进行人脸识别处理。
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # 只处理其他视频帧以节省时间
        if process_this_frame:
            # 在目前的视频帧中找到所有的脸和面部编码
            face_locations = face_recognition.face_locations(small_frame)
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                name = "No Data"
                #  ！！！！！！！修改！！！！！！ #
                # 看看面部是否与已知人脸相匹配。
                for people_data in people_datas:
                    if face_recognition.compare_faces([people_data.get("people_face_encoding")], face_encoding,
                                                      tolerance=0.5)[0]:
                        name = people_data.get("name")
                        # print(name)
                #  ！！！！！！！修改！！！！！！ #
                face_names.append(name)
        process_this_frame = not process_this_frame
        # S 动作识别
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (7, 7), 0)
        #
        # # grab the current timestamp and draw it on the frame
        # timestamp = datetime.datetime.now()
        # cv2.putText(frame, timestamp.strftime(
        #     "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        #
        # # if the total number of frames has reached a sufficient
        # # number to construct a reasonable background model, then
        # # continue to process the frame
        # if total > frameCount:
        #     # detect motion in the image
        #     motion = md.detect(gray)
        #
        #     # check to see if motion was found in the frame
        #     if motion is not None:
        #         # unpack the tuple and draw the box surrounding the
        #         # "motion area" on the output frame
        #         (thresh, (minX, minY, maxX, maxY)) = motion
        #         cv2.rectangle(frame, (minX, minY), (maxX, maxY),
        #                       (0, 0, 255), 2)
        #
        # # update the background model and increment the total number
        # # of frames read thus far
        # md.update(gray)
        # total += 1
        # E 动作识别

        # 显示结果
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # 缩放面部位置，因为我们检测到的帧被缩放到1/4大小。
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # 在脸上画一个盒子
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # 在脸下面画一个有名字的标签。
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            # #######中文字体#########
            b, g, r, a = 0, 255, 0, 0
            # #######中文字体#########
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        with lock:
            outputFrame = frame.copy()
        # 显示结果图像
        # cv2.imshow('Video', frame)

        # 在键盘上点击“Q”退出！
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # 释放句柄到摄像头
    # cv2.destroyAllWindows()



# 摄像头
def camera(frameCount):
    global vs, outputFrame, lock
    while True:
        # frame = vs.read()
        # outputFrame = frame.copy()
        # 0710 s
        outputFrame = vs.read()
        # 0710 e
        # 显示结果图像
        # cv2.imshow('Video', frame)

        # 在键盘上点击“Q”退出！
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # 释放句柄到摄像头
    # cv2.destroyAllWindows()


#save the date to the wav file
def save_wave_file(filename, data):
    # 二进制写入模式
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    # 两个字节16位
    wf.setsampwidth(sampwidth)
    # 帧速率
    wf.setframerate(RATE)
    # 把数据加进去，就会存到硬盘上去wf.writeframes(b"".join(data))
    wf.writeframes(b"".join(data))
    wf.close()


# 录屏
def luping(frameCount):
    global vs, outputFrame, lock
    fps = 20
    start = 3  # 延时录制
    end = 15  # 自动结束时间
    curScreen = ImageGrab.grab()  # 获取屏幕对象
    height, width = curScreen.size
    # video = cv2.VideoWriter('video02.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (height, width))
    # 显示无图像的窗口
    # cv2.imshow('capturing', np.zeros((1, 255), np.uint8))

    # 控制窗口显示位置，方便通过按键方式退出
    # cv2.moveWindow('capturing', height, width)
    imageNum = 0
    while True:
        imageNum += 1
        captureImage = ImageGrab.grab()  # 抓取屏幕
        frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)
        if imageNum > fps * start:
            outputFrame = frame
            # video.write(frame)
            save_wave_file("D:\\WorkSpaces\\Pycharm_WorkSpace\\Python3\\com\\gsh\\tmp\\data\\test.mp4",frame)

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        # with lock:
        # check if the output frame is available, otherwise skip
        # the iteration of the loop
        if outputFrame is None:
            continue

        # encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

        # ensure the frame was successfully encoded
        if not flag:
            continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o


def audio():
        # S 音频处理
        RECORD_SECONDS = 5
        CHUNK = 1024  # 定义数据流块
        FORMAT = pyaudio.paInt16  # 量化位数（音量级划分）
        CHANNELS = 2  # 声道数;声道数：可以是单声道或者是双声道
        RATE = 44100  # 采样率;采样率：一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz, 11.025kHz, 22.05kHz, 44.1kHz
        sampleRate = 44100
        bitsPerSample = 16
        # WAVE_OUTPUT_FILENAME = filepath  # wav文件路径
        p = pyaudio.PyAudio()  # 实例化
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        wav_header = genHeader(sampleRate, bitsPerSample, CHANNELS)
        # print("*"*10, "开始录音：请在5秒内输入语音")
        # frames = []  # 定义一个列表
        while True:
            # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):  # 循环，采样率11025 / 256 * 5
            data = wav_header + stream.read(CHUNK)  # 读取chunk个字节 保存到data中
            yield data
        # E 音频处理

@app.route("/zhi_bo")
def zhi_bo():
    # return the response generated along with the specific media
    # type (mime type)
    t = threading.Thread(target=camera, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/lu_ping")
def lu_ping():
    # return the response generated along with the specific media
    # type (mime type)
    t = threading.Thread(target=luping, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/audio_feed")
def audio_feed():
    # return Response(audio(), mimetype="audio/mpeg3")
    return Response(audio(), mimetype="audio/x-wav;codec=pcm")


# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    # start a thread that will perform motion detection
    # t = threading.Thread(target=camera, args=(
    t = threading.Thread(target=luping, args=(
        args["frame_count"],))
    t.daemon = True
    # t.start()

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()
