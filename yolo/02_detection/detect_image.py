from ultralytics import YOLO
import cv2
from pathlib import Path

# 模型路径
model_path = Path('../model').resolve()
# 资源路径
asset_path = Path('../assets').resolve()

# 加载预训练模型 task参数也可以不填写，它会根据模型去识别相应任务类别
model = YOLO(model_path / "yolov8n.pt", task='detect')
# 推理图片
results = model(asset_path / "bus.jpg")
res = results[0].plot()
cv2.imshow("YOLOv8 Inference", res)
cv2.waitKey(0)









