from algorithm.object_detector import YOLOv7
from utils.detections import draw
import json
import cv2

yolov7 = YOLOv7()
yolov7.set(ocr_classes=['tablica'])
yolov7.load('best.weights', classes='classes.yaml', device='gpu') # use 'gpu' for CUDA GPU inference
image = cv2.imread('Photo/3.jpg')
detections = yolov7.detect(image)
detected_image = draw(image, detections)
cv2.imwrite('Result/image.jpg', detected_image)
print(json.dumps(detections, indent=4))