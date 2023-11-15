from algorithm.object_detector import YOLOv7
from utils.detections import draw
import json
import cv2

# Inicjalizacja detektora
yolov7 = YOLOv7()
ocr_classes = ['tablica']
yolov7.set(ocr_classes=ocr_classes, conf_thres=0.7)  # Ustaw progi pewności na 0.7
yolov7.load('best.weights', classes='classes.yaml', device='gpu')  # Użyj 'gpu' do inferencji na GPU CUDA

# Inicjalizacja kamery
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print('[!] Błąd podczas otwierania kamery')

# Śledzenie wczytanych tablic
detected_plates = set()

# Otwarcie pliku do zapisu
with open('output.txt', 'a') as file:
    try:
        while webcam.isOpened():
            ret, frame = webcam.read()
            if ret:
                # Wykrywanie obiektów na klatce
                detections = yolov7.detect(frame, track=True)

                # Sprawdzanie i zapisywanie tekstu, jeśli istnieje
                for detection in detections:
                    if detection['class'] in ocr_classes:
                        detection_id = detection['id']
                        text = detection.get('text', '')  # Użyj get(), aby uniknąć KeyError

                        if text and detection_id not in detected_plates:
                            detected_plates.add(detection_id)
                            # Zapisz tekst w pliku tylko raz
                            file.write(f'Detected license plate: {text}\n')

                detected_frame = draw(frame, detections)
                cv2.imshow('webcam', detected_frame)
                cv2.waitKey(1)
            else:
                break
    except KeyboardInterrupt:
        pass

webcam.release()
print('[+] Zamknięto kamerę')
yolov7.unload()
