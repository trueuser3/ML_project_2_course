# Shoplifting-Detection

#### Project creators
-  Емельянова Анастасия
-  Цирульников Владислав
-  Шахонин Егор

AntiBOP - приложение для детекции шоплифтинга, анализирующее поведение покупателя с помощью нейросетей, таких как ViT и yolov8. При обнаружении подозрительного поведения, сотрудники магазинов получают уведомления о деталях кражи в режиме реального времени. 

## Introduction 
---

TODO

## Project highlights
---

# App-videoplayer AntiBOP

Приложение разработано для взаимодействия с обученной на детекцию краж нейронной сетью. 

### Description

TODO

### System reqirements

+   Python 3.11.5
+   библиотека GUI - PyQt 5 (pip install pyqt5)

### Decomposition:

TODO

### example of launching the application
    python3 program.py


### Examples of interaction:

TODO

## Data 
---
#### Data collection

Для обучения нейронной сети были использованы следующие наборы данных:

- Из [датасета](https://disk.yandex.ru/d/_vjY_E84Bs1p-Q) с записями камер видеонаблюдения были извлечены и преобразованы моменты краж. Затем все кадры были обрезаны по yolo боксам и размечены. [Итоговый датасет](https://drive.google.com/drive/folders/1YTx-Rj6D7dj0WFRjYTJHJ6_gOz8KsCh5) на 12 000 кадров.
  
- Также были взяты [искусственно созданные датасеты](https://universe.roboflow.com/theft-detection-poc/shoplifting-detection-tqzfb/dataset/1), а еще [тык](https://universe.roboflow.com/vit-oru5x/shoplifting_theft_detection2/dataset/7). К ним были применены различные аугментации, такие как поворот и отзеркаливание.

## Model architecture

TODO

## Model training && Evaluation

TODO

## Input-Output
![SL_event_record_1__ (1)](https://github.com/trueuser3/ML_project_2_course/blob/AnastasiaEmelyanova/samples/output/output_grad_1.gif)
