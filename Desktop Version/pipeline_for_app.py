import torch
import cv2
from transformers import ViTImageProcessor
from transformers import ViTForImageClassification
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image


processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')
model_clf = ViTForImageClassification.from_pretrained('weights1/')
softmax = torch.nn.Softmax()

def image_to_prob(img):
    inputs = processor(img, return_tensors='pt')
    logits = model_clf(inputs['pixel_values']).logits
    return float(softmax(logits)[0][1])

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




def get_color(prob):
    # gradient from green to red
    r = int(255 * prob)
    g = int(255 * (1 - prob))
    b = 0
    return (b, g, r)  # BGR format



def process_video_with_tracking(model, input_video_path, show_video=True, save_video=False, output_video_path="output_video.mp4"):
    # Open the input video file
    cap = cv2.VideoCapture(input_video_path)

    temp_frame_count = 1

    if not cap.isOpened():
        raise Exception("Error: Could not open video file.")

    # Get input video frame rate and dimensions
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the output video writer
    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))



    #Считаем количество кадров у видео

    cap_2 = cv2.VideoCapture(input_video_path)

    frame_counter = 0
    while True:
        ret, frame = cap_2.read()
        if not ret:
            break
        frame_counter += 1


    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model.track(frame, iou=0.4, conf=0.3, persist=True, imgsz=608, verbose=False, tracker="bytetrack.yaml", classes=0)

        if results[0].boxes.id != None: # this will ensure that id is not None -> exist tracks
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)

            for box, id in zip(boxes, ids):
                #color_normal = (0,255,0) # green
                #color_theft = (0,0,255) # red
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
                colour = get_color(prob)


                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3],), colour, 2)
                cv2.putText(
                    frame,
                    f"{prob:.2f}",
                    (box[0], box[1]),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.70,
                    (0, 255, 255),
                    2,
                )
            print(f"Progress: {temp_frame_count} / {frame_counter}")
            temp_frame_count += 1

        if save_video:
            out.write(frame)

        if show_video:
            frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
            # cv2.imshow("frame", frame)
            cv2_imshow(frame)

    # Release the input video capture and output video writer
    cap.release()
    if save_video:
        out.release()
    return results
