from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # self.centralWidget = QWidget()                               
        # self.setCentralWidget(self.centralWidget)                    
        
        # self.lbl = QtWidgets.QLabel()
        # self.pix = QtGui.QPixmap("image.png").scaled(400, 400)          # ваше фото
        # self.lbl.setPixmap(self.pix)
        
        # self.btn = QPushButton()
        # self.btn.setText("Кнопка")
        # self.btn.setStyleSheet("""
        #     background: pink; 
        #     color: black; 
        #     border-radius: 34px;
        # """)
        # self.btn.setFont(QtGui.QFont("Pusia-Bold.otf", 17, QtGui.QFont.Bold))
        # self.btn.setFixedSize(300, 150)
        # self.btn.setCheckable(True)
        # self.btn.clicked.connect(self.show_image)

        # layout = QGridLayout(self.centralWidget)
        # layout.addWidget(self.lbl, 0, 0, Qt.AlignCenter)
        # layout.addWidget(self.btn, 1, 0, Qt.AlignHCenter | Qt.AlignBottom)
        
        # self.eff = QGraphicsOpacityEffect()
        # self.eff.setOpacity(0.0)        
        # self.lbl.setGraphicsEffect(self.eff)
        
        # self.animation = QPropertyAnimation(self.eff, b'opacity')
        # self.animation.setDuration(1000)  

        self.player = QMediaPlayer(self)                              # !!!
        self.player.setMedia(QMediaContent(QUrl(                      # !!!
            'http://europaplus.hostingradio.ru:8014/ep-top256.mp3'    # !!!
        )))                                                           # !!!
        self.player.setVolume(80) 
        self.player.play()
        
    # def show_image(self):
    #     if not self.btn.isChecked():       
    #         self.animation.setStartValue(1)
    #         self.animation.setEndValue(0)
    #         self.player.stop()                                            # !!!
    #     else:    
    #         self.player.play()                                            # !!!
    #         self.animation.setStartValue(0)
    #         self.animation.setEndValue(1)            
    #     self.animation.start() 


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.resize(420, 600)
    ex.show()
    sys.exit(app.exec_())