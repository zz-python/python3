#pip install numpy
#pip install opencv-python
import numpy as np
import cv2

# 创建一个图像作为背景图，size:512*512，channel:3
img = np.zeros((512, 512, 3), np.uint8)

# 1.画蓝色对角线
img = cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 5)


# 显示并回收资源
cv2.imshow('draw',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
