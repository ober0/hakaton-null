from datetime import datetime, timedelta
from io import BytesIO
import matplotlib.pyplot as plt
import pytz
from celery import shared_task
import time
import cv2
import numpy as np
from .models import PeopleData
import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline



@shared_task
def count_people(place, filename, file_content, time):
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

            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.2)
    try:
        num_people = sum(1 for i in indices if class_ids[i] == 0)
    except AttributeError:
        num_people = 0
    try:
        people_data = PeopleData(place=place, people_count=num_people, datetime=datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        people_data.save()
        return {'success': True, 'num_people': num_people}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@shared_task
def doModel(place, data):
    df = pd.DataFrame(data)

    df.set_index("time", inplace=True)

    # Добавляем целевые значения для прогноза на 5 и 15 минут вперед
    df["people_count_5min"] = df["people"].shift(-30)  # Сдвиг на 5 минут (30 интервалов по 10 секунд)
    df["people_count_15min"] = df["people"].shift(-90)  # Сдвиг на 15 минут (90 интервалов по 10 секунд)
    df.dropna(inplace=True)  # Удаляем строки с NaN, возникающими из-за сдвига

    X = df[["people"]].values  # Используем текущее количество людей как признак
    y_5min = df["people_count_5min"].values  # Целевое значение для прогноза через 5 минут
    y_15min = df["people_count_15min"].values

    # Создаем и обучаем модели для предсказаний через 5 и 15 минут
    model_5min = make_pipeline(StandardScaler(), SGDRegressor())
    model_15min = make_pipeline(StandardScaler(), SGDRegressor())

    model_5min.fit(X, y_5min)
    model_15min.fit(X, y_15min)


    current_count = [[df["people"].iloc[-1]]]
    prediction_5min = model_5min.predict(current_count)[0]
    prediction_15min = model_15min.predict(current_count)[0]

    return {
        'success': True,
        '5m': int(prediction_5min),
        '15m': int(prediction_15min)
    }
