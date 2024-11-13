import cv2
import numpy as np

def count_people(place, filename, file_content):
    # Загрузка YOLOv3
    yolo_net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    layer_names = yolo_net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in yolo_net.getUnconnectedOutLayers()]

    # Загрузка изображения
    image = cv2.imread("photo.jpg")
    height, width, channels = image.shape

    # Преобразуем изображение в формат, подходящий для YOLO
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Прогоняем изображение через сеть
    yolo_net.setInput(blob)
    outs = yolo_net.forward(output_layers)

    # Параметры для детекции людей
    class_ids = []
    confidences = []
    boxes = []

    # Обработка выходных данных YOLO
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.3:  # Повышаем порог уверенности
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Прямоугольник для объектов
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Применяем Non-Maximum Suppression для устранения дублирующихся боксов
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.2)  # Увеличиваем параметры NMS

    # Рисуем результаты, фильтруем только людей (класс 0)
    num_people = 0
    if len(indices) > 0:
        for i in indices.flatten():  # Правильная обработка индексов после NMS
            if class_ids[i] == 0:  # Только люди (класс 0)
                x, y, w, h = boxes[i]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                num_people += 1

    # Показываем изображение с детекцией
    cv2.imshow("Detected People", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Подсчитаем количество людей (класс 0 — это люди)
    print(f"Number of people detected: {num_people}")

    return num_people

with open('photo.jpg', 'rb') as f:
    count_people('floor4', f.name, f.read())
