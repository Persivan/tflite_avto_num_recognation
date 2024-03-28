import time
from ui import getFuckingNuumber
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from yolo import yolo_car_checker

cap = cv2.VideoCapture('https://docs.google.com/uc?export=download&confirm=&id=1pz68D1Gsx80MoPg-_q-IbEdESEmyVLm-')
while True:
    # yolo work
    cv_img, car_detected_cv = yolo_car_checker(cap)
    # Combine detected car array
    buf = []
    for i in car_detected_cv:
         buf.append(cv2.resize(i, (64,64)))
    union = np.hstack(buf)
    # Show result
    cv2.imshow('1', cv2.resize(cv_img, (1024, 576)))
    cv2.imshow('2', union)
    if cv2.waitKey(1) == ord('q'):
        break
    # ret, cv_img = frame.read()
# class VideoThread(QThread):
#     change_pixmap_signal = pyqtSignal(np.ndarray)
#
#     def run(self):
#         # capture from web cam
#         cap = cv2.VideoCapture('https://docs.google.com/uc?export=download&confirm=&id=1pz68D1Gsx80MoPg-_q-IbEdESEmyVLm-')
#         while True:
#             ret, cv_img = cap.read()
#             time.sleep(0.035)
#             if ret:
#                 self.change_pixmap_signal.emit(cv_img)
#
#
# class App(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Qt live label demo")
#         self.setFixedWidth(800)
#         self.setFixedHeight(600)
#         self.display_width = 370
#         self.display_height = 210
#         self.number = ""
#
#         # create the label that holds the image
#         self.original_video_label = QLabel(self)
#         self.original_video_label.resize(self.display_width, self.display_height)
#         self.original_video_label.setGeometry(QRect(20, 10, 390, 220))
#         # create the video capture thread
#         self.thread = VideoThread()
#         # connect its signal to the update_image slot
#         self.thread.change_pixmap_signal.connect(self.update_image)
#         # start the thread
#         self.thread.start()
#
#         # создаем второе видео
#         self.recognition_layout = QLabel(self)
#         self.recognition_layout.resize(self.display_width, self.display_height)
#         self.recognition_layout.setGeometry(QRect(410, 10, 790, 220))
#
#         # создаем третье видео
#         self.changeme_layout = QLabel(self)
#         self.changeme_layout.resize(self.display_width, self.display_height)
#         self.changeme_layout.setGeometry(QRect(410, 10, 790, 220))
#
#         # создаем блок информации
#         self.information_label = QLabel(self)
#         self.information_label.setGeometry(410, 160, 790, 160)
#         self.information_label.setText('Информация')
#
#         self.plate_number_layout = QLabel(self)
#         self.plate_number_layout.setGeometry(410, 175, 790, 175)
#         self.plate_number_layout.setText('тута ваня')
#
#     @pyqtSlot(np.ndarray)
#     def update_image(self, cv_img):
#         """Updates the image_label with a new opencv image"""
#         qt_img = self.convert_cv_qt(cv_img)
#         self.original_video_label.setPixmap(qt_img)
#         self.recognition_layout.setPixmap(qt_img)
#         self.number = getFuckingNuumber(cv_img)
#         # self.number = ['zsscncnskj']
#         print(f'{self.number[0]}')
#         self.plate_number_layout.setText(self.number[0])
#         self.changeme_layout.setPixmap(qt_img)
#         # ТУТА МАНИПУЛЯПУЛЯЦИИ
#
#     def convert_cv_qt(self, cv_img):
#         """Convert from an opencv image to QPixmap"""
#         rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
#         h, w, ch = rgb_image.shape
#         bytes_per_line = ch * w
#         convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
#         p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
#         return QPixmap.fromImage(p)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     a = App()
#     a.show()
#     sys.exit(app.exec_())