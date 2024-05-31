from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.player = QMediaPlayer(self)                              # !!!
        self.player.setMedia(QMediaContent(QUrl(                      # !!!
            'http://europaplus.hostingradio.ru:8014/ep-top256.mp3'    # !!!
        )))                                                           # !!!
        self.player.setVolume(80) 
        self.player.play()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.resize(420, 600)
    ex.show()
    sys.exit(app.exec_())
