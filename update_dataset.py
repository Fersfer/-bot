import shutil
import os
from ultralytics import YOLO


source_img = r"D:\mob_detector\muto_datasets\images"
source_lbl = r"D:\mob_detector\muto_datasets\labels"

target_img = r"D:\mob_detector\dataset\images\train"
target_lbl = r"D:\mob_detector\dataset\labels\train"

for file in os.listdir(source_img):
    shutil.copy(os.path.join(source_img, file), target_img)

for file in os.listdir(source_lbl):
    shutil.copy(os.path.join(source_lbl, file), target_lbl)

print("✅ Скріни перенесено в датасет")


model = YOLO(r"D:\mob_detector\mob_detector\yolov8n_mob2\weights\best.pt")

model.train(
    data=r"D:\mob_detector\data.yaml",
    epochs=10,
    imgsz=512,
    batch=8,
    project="mob_detector",
    name="yolov8n_mob_retrain",
    exist_ok=True,
    amp=False
)
