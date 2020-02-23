from imageai.Detection import VideoObjectDetection

detector = VideoObjectDetection()
# 使用轻型模型
# detector.setModelTypeAsTinyYOLOv3()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("./model/yolo.h5")
detector.loadModel()

input_file_path = 0
output_file_path = "test"
detections, extract_detected_objects = detector.detectObjectsFromVideo(input_file_path=input_file_path,output_file_path=output_file_path,video_complete_function=print("detect complete"))
for eachObject in detections:
    print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
