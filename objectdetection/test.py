#Object Detection and Tracking in Video using YOLOv8 and opencv
# pip install ultralytics opencv-python matplotlib lap numpy pandas 
import cv2 
import random 
import numpy as np
import lap
from ultralytics import YOLO
from matplotlib import pyplot as plt

yolo = YOLO("yolov8n.pt") #Load yolo model

#define function to assign colors
# - each class gets a unique RGB color
def getColours(cls_num):
    """Generate unique colors for each class ID"""
    random.seed(cls_num) #makes color consistent across frames
    return tuple(random.randint(0, 255) for _ in range(3))

#load the video
video_path = r"C:\Users\reshu\Desktop\ml_Task\objectdetection\video.mp4"
videoCap = cv2.VideoCapture(video_path)

#process video and detect objects
frame_count = 0

while True:
    ret, frame = videoCap.read()
    if not ret:
        break
    results = yolo.track(frame, stream=True)

    for result in results:
        class_names = result.names
        for box in result.boxes:
            if box.conf[0] > 0.4:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cls = int(box.cls[0])
                class_name = class_names[cls]

                conf = float(box.conf[0])

                colour = getColours(cls)

                cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)

                cv2.putText(frame, f"{class_name} {conf:.2f}",
                            (x1, max(y1 - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, colour, 2)

    if frame_count < 20:
     cv2.imshow("YOLO Detection", frame)
     if cv2.waitKey(1) & 0xFF == ord('q'):
      break

    frame_count += 1

videoCap.release()
cv2.destroyAllWindows()

#Load YOLOv8 model.
#Open video file.
#Loop through frames:
#Detect objects + track them.
#Draw bounding boxes + labels.
#Display frame in a window.
#Exit when video ends or user presses q.
#Clean up resources.

