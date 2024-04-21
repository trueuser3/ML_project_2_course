from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import sys
import cv2

#input_video_path = '/home/anastasia/Desktop/project_dataset/Shoplifting1.mp4'

'''
example of usage: python3 cv_qt.py test.mp4 (assuming code and video are in the same directory)
'''

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Unable to open video source {video_path}")
            return
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        frame_time = int((1.0 / fps) * 1000)

        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
                QThread.msleep(frame_time)
            else:
                break
        cap.release()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.disply_width = 600
        self.display_height = 600
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        self.textLabel = QLabel('AntiWor')
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        self.setLayout(vbox)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB) # cv2 use BGR format
        hight, width, ch = rgb_image.shape
        bytes_per_line = ch * width
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, width, hight, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__=="__main__":
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        sys.exit(1)
    a = App()
    a.show()
    sys.exit(app.exec_())
