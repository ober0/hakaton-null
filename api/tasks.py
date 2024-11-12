from datetime import datetime
import pytz
from celery import shared_task
import time
import cv2
import numpy as np
from .models import PeopleData


@shared_task
def count_people(place, filename, file_content):
    # return str(settings.BASE_DIR)

    yolov3_weights = 'static/cfg/yolov3.weights'
    yolov3_cfg = 'static/cfg/yolov3.cfg'

    yolo_net = cv2.dnn.readNet(yolov3_weights, yolov3_cfg)
    layer_names = yolo_net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in yolo_net.getUnconnectedOutLayers()]

    # Декодируем изображение из содержимого файла
    image_array = np.frombuffer(file_content, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Проверяем, что изображение загружено
    if image is None:
        return {'success': False, 'error': 'Ошибка загрузки изображения'}

    height, width, channels = image.shape

    # Преобразуем изображение для YOLO
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    yolo_net.setInput(blob)
    outs = yolo_net.forward(output_layers)

    # Параметры для детекции
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.6:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.6, 0.4)
    num_people = sum(1 for i in indices.flatten() if class_ids[i] == 0)

    try:
        people_data = PeopleData(place=place, people_count=num_people, datetime=datetime.now(pytz.timezone('Europe/Moscow')))
        people_data.save()
        return {'success': True, 'num_people': num_people}
    except Exception as e:
        return {'success': False, 'error': str(e)}