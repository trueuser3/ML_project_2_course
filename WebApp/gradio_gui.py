# -*- coding: utf-8 -*-
"""gradio_GUI (2).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d2RYp-uQEqYdTL6UkX8DB4vjVQUOydX1

По ссылке https://0e016e93c7a2e2ee67.gradio.live находится видеопроигрыватель: загружаем видео, ждем обработку, получаем результат - видео с детекцией кражи на нем, можем посмотреть или сохранить себе
"""

#from google.colab import drive
#drive.mount('/content/drive/')
#
#!pip install ultralytics
#!pip install accelerate

import torch

if torch.cuda.is_available():
  device = torch.device("cuda")
else:
  device = torch.device("cpu")

from transformers import ViTImageProcessor

processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')

from transformers import ViTForImageClassification

model_clf = ViTForImageClassification.from_pretrained(
    'weights1/'
)

import torch
from transformers import ViTImageProcessor
from transformers import ViTForImageClassification

if torch.cuda.is_available():
  device = torch.device("cuda")
else:
  device = torch.device("cpu")

processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')
model_clf = ViTForImageClassification.from_pretrained('weights1/')
softmax = torch.nn.Softmax()

def image_to_prob(img):
    inputs = processor(img, return_tensors='pt')
    logits = model_clf(inputs['pixel_values']).logits
    return float(softmax(logits)[0][1])

import torch
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image

def crop_image(image, box):
    additional_area = 1/10
    x_min, y_min, x_max, y_max = box
    width, height = image.size
    box_width = x_max - x_min
    box_height = y_max - y_min
    x_min_2 = max(0, x_min - box_width*additional_area)
    y_min_2 = max(0, y_min - box_height*additional_area)
    x_max_2 = min(width, x_max + box_width*additional_area)
    y_max_2 = min(height, y_max + box_height*additional_area)
    area = (x_min_2, y_min_2, x_max_2, y_max_2)
    cropped_img = image.crop(area)
    return cropped_img

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_detect = YOLO('yolov8n.pt').to(device)
model_detect.classes = [0]

def recieve_box(image):
    results = model_detect(source = image, classes=0, show = False, imgsz=640, conf=0.2, iou=0.4, save = False, verbose=False)
    boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
    cropped_images = []
    for box in boxes:
        cropped_images.append(crop_image(image, box))
    return cropped_images

#!pip install opencv-python-headless gradio

#!pip install gradio

"""Тестовый вариант функции для обработки видео для gradio: преобразование в черно-белый формат"""

"""

import cv2
import gradio as gr
import numpy as np

def process_video(input_video):
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        raise Exception("Error: Could not open video file.")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height), isColor=False)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # test: convert frames to black-white ones
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            out.write(gray_frame)
        else:
            break

    cap.release()
    out.release()

    return 'output.mp4'

iface = gr.Interface(
    fn=process_video,
    inputs=gr.Video(label="Загрузите видео"),
    outputs=gr.Video(label="Обработанное видео"),
)
iface.launch()

"""

"""Реализация функции для детекции человека и классификации кражи на кадре. Берется функция из пайплайна, видоизменяется под формат process_video функции для gradio."""

import cv2
import gradio as gr
import numpy as np
from ultralytics import YOLO
from PIL import Image

def get_color(prob):
    # gradient from green to red
    r = int(255 * prob)
    g = int(255 * (1 - prob))
    b = 0
    return (b, g, r)  # BGR format


def process_video(input_video):
    model = YOLO('yolov8n.pt')
    model.fuse()
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        raise Exception("Error: Could not open video file.")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model.track(frame, iou=0.4, conf=0.25, persist=True, imgsz=608, verbose=False, tracker="bytetrack.yaml", classes=0)

        if results[0].boxes.id != None: # this will ensure that id is not None -> exist tracks
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)

            for box, id in zip(boxes, ids):
                color_normal = (0,255,0) # green
                color_theft = (0,0,255) # red
                additional_area = 1/10
                x_min, y_min, x_max, y_max = box
                width, height = frame_width, frame_height
                box_width = x_max - x_min
                box_height = y_max - y_min
                x_min_2 = max(0, x_min - box_width*additional_area)
                y_min_2 = max(0, y_min - box_height*additional_area)
                x_max_2 = min(width, x_max + box_width*additional_area)
                y_max_2 = min(height, y_max + box_height*additional_area)
                area = (x_min_2, y_min_2, x_max_2, y_max_2)
                cropped_img = Image.fromarray(frame, 'RGB').crop(area)

                prob = image_to_prob(cropped_img)
#                if prob >= 0.7:
#                    color = color_theft
#                else:
#                    color = color_normal
                color = get_color(prob)
                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3],), color, 2)
                cv2.putText(
                    frame,
                    f"{prob:.2f}",
                    (box[0], box[1]),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.70,
                    (0, 255, 255),
                    2,
                )

        out.write(frame)
#        if cv2.waitKey(1) & 0xFF == ord("q"):
#            break

    cap.release()
    out.release()

    return 'output.mp4'

iface = gr.Interface(
    fn=process_video,
    inputs=gr.Video(label="Загрузите видео"),
    outputs=gr.Video(label="Обработанное видео"),
)
#iface.launch(share=True)
