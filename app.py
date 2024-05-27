from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from PyQt5.Qt import *

import sys
import torch
import cv2
import os
from transformers import ViTImageProcessor
from transformers import ViTForImageClassification
from ultralytics import YOLO
from PIL import Image
from pipeline_for_app import process_video_with_tracking

import pipeline_for_app

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):

        self.flag = 0

        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("VideoPlayer")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)


        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.playButton)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)

    def music_on(self):
        self.player = QMediaPlayer(self)                              # !!!
        self.player.setMedia(QMediaContent(QUrl(                      # !!!
            'http://europaplus.hostingradio.ru:8014/ep-top256.mp3'    # !!!
        )))                                                           # !!!
        self.player.setVolume(80) 
        self.player.play() 


    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        
        if not fileName:
            print("No file selected.")
            return
        print(f"Selected file: {fileName}")
        
        try:
            model = YOLO('yolov8n.pt')
            model.fuse()
            current_dir = os.path.dirname(os.path.realpath(__file__))
            output_dir = os.path.join(current_dir, 'output')
            os.makedirs(output_dir, exist_ok=True)
            output_file_name = os.path.join(output_dir, 'output_video.mp4')
            
            ##process_video_with_tracking(model, input_video_path=fileName, show_video=False, save_video=True, output_video_path=output_file_name)



            #####################################
            # Open the input video file
            cap = cv2.VideoCapture(fileName)

            temp_frame_count = 1

            if not cap.isOpened():
                raise Exception("Error: Could not open video file.")

            # Get input video frame rate and dimensions
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Define the output video writer
            if True:
                fourcc = cv2.VideoWriter_fourcc(*'avc1')
                out = cv2.VideoWriter(output_file_name, fourcc, fps, (frame_width, frame_height))



            #Считаем количество кадров у видео
            cap_2 = cv2.VideoCapture(fileName)

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
                results = model.track(frame, iou=0.4, conf=0.25, persist=True, imgsz=608, verbose=False, tracker="bytetrack.yaml", classes=0)

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

                        prob = pipeline_for_app.image_to_prob(cropped_img)

                        print(prob, end = ' ')
                        if (prob > 0.1 and self.flag == 0):
                            self.music_on()
                            self.flag = 1

                        colour = pipeline_for_app.get_color(prob)


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

                if True:
                    out.write(frame)

                if False:
                    frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
                    # cv2.imshow("frame", frame)
                    cv2_imshow(frame)

            # Release the input video capture and output video writer
            cap.release()
            if True:
                out.release()
            return results
            #####################################



            print("Video processing completed.")
        except Exception as e:
            print(f"Error processing video: {e}")
            return
    
        if os.path.exists(output_file_name):
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(output_file_name)))
            self.playButton.setEnabled(True)
            print("Media loaded successfully.")
        else:
            print(f"Output file not found: {output_file_name}")


    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(400, 300)
    player.show()
    sys.exit(app.exec_())
