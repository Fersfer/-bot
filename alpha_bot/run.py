import cv2
from sympy.printing.pretty.pretty_symbology import annotated
from ultralytics import YOLO


model = YOLO('D:/mob_detector/mob_detector/yolov8n_mob22/weights/best.pt')
cap = cv2.VideoCapture(0)

i = 0
while True:
    i +=1

    ret, frame = cap.read()
    results = model.predict(frame)
    annotated_frame = results[0].plot()
    cv2.imwrite(f'{i}.png', annotated_frame)
    cv2.imshow("Yolov12",annotated_frame)
    if cv2.waitKey(1) ==27:
        break