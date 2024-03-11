from ultralytics import YOLO
import cv2
from pathlib import Path

# 模型路径
model_path = Path('../model').resolve()
# 资源路径
asset_path = Path('../assets').resolve()

# 加载预训练模型
model = YOLO(model_path / "yolov8n-cls.pt")
# 推理图片
results = model(asset_path / "bus.jpg")
# print(results)

res = results[0].plot()
cv2.imshow("YOLOv8 Inference", res)
cv2.waitKey(0)









