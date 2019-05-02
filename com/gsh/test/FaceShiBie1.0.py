import face_recognition
import cv2

'''
这是运行人脸识别从你的网络摄像头视频演示。
这比那要复杂一点。
其他的例子，但它包含了一些基本的性能调整让事情运行得更快：
1。以1/4分辨率处理每个视频帧（尽管仍以完全分辨率显示）
2。只检测其他视频帧中的人脸。
请注意：这个例子需要OpenCV（的` CV2 `库）将安装只能从摄像头读取。
OpenCV是*不*要求使用face_recognition库。如果你想运行它，只需要它。
具体演示。如果你安装它有困难，试试其他不需要它的演示。
获得参考摄像头# 0（默认）
'''
video_capture = cv2.VideoCapture(0)
# 加载示例图片并学习如何识别它。
face_dir = "/Users/gdd/github/Python3/com/gsh/test/data/in/face/"
people1_image = face_recognition.load_image_file(face_dir + "gsh.png")
# people2_image = face_recognition.load_image_file("/Users/gdd/github/Python3/com/gsh/test/data/wdd/wdd.png")
people2_image = face_recognition.load_image_file(face_dir + "zwj.png")
people1_face_encoding = face_recognition.face_encodings(people1_image)[0]
people2_face_encoding = face_recognition.face_encodings(people2_image)[0]
na = 0
# 初始化一些变量
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # 抓取单帧视频
    ret, frame = video_capture.read()

    # 将视频帧大小调整为1/4大小，以便更快地进行人脸识别处理。
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # 只处理其他视频帧以节省时间
    if process_this_frame:
        # 在目前的视频帧中找到所有的脸和面部编码
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            name = "unknow"
            # 看看面部是否与已知人脸相匹配。
            if face_recognition.compare_faces([people1_face_encoding], face_encoding, tolerance=0.34)[0]:
                name = "管生辉"
            if face_recognition.compare_faces([people2_face_encoding], face_encoding, tolerance=0.34)[0]:
                name = "ZWJ"
            face_names.append(name)
    process_this_frame = not process_this_frame
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
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # 显示结果图像
    cv2.imshow('Video', frame)

    # 在键盘上点击“Q”退出！
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放句柄到摄像头
video_capture.release()
cv2.destroyAllWindows()
