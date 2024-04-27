from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image

def crop_image(image, box):
    x_min, y_min, x_max, y_max = box
    width, height = image.size
    box_width = x_max - x_min
    box_height = y_max - y_min
    x_min_2 = max(0, x_min - box_width/3)
    y_min_2 = max(0, y_min - box_height/3)
    x_max_2 = min(width, x_max + box_width/3)
    y_max_2 = min(height, y_max + box_height/3)
    area = (x_min_2, y_min_2, x_max_2, y_max_2)
    cropped_img = image.crop(area)
    return cropped_img
    

def recieve_box(image):
    model = YOLO('yolov8n.pt')
    model.classes = [0]
    results = model(source = image, classes=0, show = False, imgsz=640, conf=0.3, iou=0.4, save = False)
    boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
    cropped_images = []
    for box in boxes:
        cropped_images.append(crop_image(image, box))
    return cropped_images
