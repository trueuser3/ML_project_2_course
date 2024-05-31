# Shoplifting-Detection

#### Project creators
-  Емельянова Анастасия
-  Цирульников Владислав
-  Шахонин Егор

## Motivation

Воровство в магазинах составляет от 30% до 40% от общего объема потерь в розничной торговле, что делает задачу детекции шоплифтинга крайне актуальной для каждого магазина страны. Среди существующих решений есть либо плохо работающие opensource проекты, либо полностью коммерческие.


## Introduction 

Приложение для детекции шоплифтинга, анализирующее поведение покупателя с помощью нейросетей, таких как Vision Transformer и YOLOv8. При обнаружении подозрительного поведения, сотрудники магазинов получают уведомления о деталях кражи в режиме реального времени. 

Основные функции: 
- Автоматическое определение вероятности совершения кражи в реальном времени.
- Активация уведомления персонала при превышении установленного порога вероятности шоплифтинга.
- Возможность сохранить результат, отслеживание передвижения посетителей

---


# App-videoplayer

Разработаное на PyQT приложение для взаимодействия с обученной на детекцию краж нейронной сетью. 

### Description

В видеоплеер загружается видео, далее оно обрабатывается, затем полученную запись можно воспроизвести и на моменте кражи включится уведомление.

![metrics](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/player1.jpg)
![metrics](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/player2.jpg)

![metrics](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/player3.jpg)
![metrics](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/player4.jpg)
![metrics](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/player5.jpg)

### System reqirements

+   Python 3.11.5
+   библиотека GUI - PyQt 5 (pip install pyqt5)
+   ultralytics
+   cv2
+   torch

### Decomposition:

 + app.py - главное окно приложения
 + pipeline_for_app.py - функция обработки видео

### example of launching the application
    python3 program.py

### install dependencies 
    pip install -r requirements.txt
    

### Examples of interaction:

![example](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/video_result.mp4)

## Data 
---
#### Data collection

Для обучения нейронной сети были использованы следующие наборы данных:

- Из [датасета](https://disk.yandex.ru/d/_vjY_E84Bs1p-Q) с записями камер видеонаблюдения были извлечены и преобразованы моменты краж. Затем все кадры были обрезаны по yolo боксам и размечены. [Итоговый датасет](https://drive.google.com/drive/folders/1YTx-Rj6D7dj0WFRjYTJHJ6_gOz8KsCh5) на 12 000 кадров.
  
- Также были взяты [искусственно созданные датасеты](https://universe.roboflow.com/theft-detection-poc/shoplifting-detection-tqzfb/dataset/1), а еще [тык](https://universe.roboflow.com/vit-oru5x/shoplifting_theft_detection2/dataset/7). К ним были применены различные аугментации, такие как поворот и отзеркаливание.

- Для учета последовательство действий покупателя были созданы [датасеты](https://drive.google.com/drive/folders/1_PVQkCOosGOxXistgBOYBDgtWUZbdSEn) с 4 действиями, вручную размеченные.

- Для дообучения yolov8m используется [датасет](https://universe.roboflow.com/projecthuman/human-tracking-krcgm/dataset/3) c кадрами, похожими на CCTV. Датасет размечен на 18 классов для уменьшения вероятности спутывания человека с другими объектами.
---

## Model architecture

![architecture](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/image.png)

## Model training && Evaluation

![metrics](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/image.png)

### Метрики аналогов ViT

![metrics](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/screen.png)

## YOLOv8m дообучение pretrain модели для задачи детекции и трекинга человека на CCTV-кадрах

### Полученные метрики:

![metrcis](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/results.png)

![metrics](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/R_curve.png)

### Examples of human detection

![examples](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/train_batch5880.jpg)

### Сравнение по метрике Intersection over Union c дефолт моделью

На тестовом датасете с CCTV-кадрами было проведено сравнение качества выделенных bounding boxes по метрике mean IoU с дефолт yolov8m. Прирост составил 20%

![iou](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/iou_metrics.jpg)


## Input-Output
![SL_event_record_1__ (1)](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/output/output_grad_1.gif)
