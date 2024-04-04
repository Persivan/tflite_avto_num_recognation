import time
from NumberRecognition import getFuckingNuumber
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect
import sys
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtCore
import numpy as np
from yolo import yolo_car_checker

# class VideoThread(QThread):
#     change_pixmap_signal = pyqtSignal(np.ndarray)

#     def run(self):
#         # capture from web cam
#         cap = cv2.VideoCapture('./Object_Detection/test/video.mp4')
#         while True:
#             ret, cv_img = cap.read()
#             if ret:
#                 self.change_pixmap_signal.emit(cv_img)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.display_width = 370
        self.display_height = 210

        # создаем первое видео (верхнее левое)
        self.original_video_label = QLabel(self)
        self.original_video_label.resize(self.display_width, self.display_height)
        self.original_video_label.setGeometry(QRect(20, 10, 390, 220))

        # создаем второе видео (верхнее правое)
        self.recognition_layout = QLabel(self)
        self.recognition_layout.resize(self.display_width, self.display_height)
        self.recognition_layout.setGeometry(QRect(410, 10, 790, 220))

        # создаем третье видео (нижнее левое)
        self.changeme_layout = QLabel(self)
        self.changeme_layout.resize(self.display_width, self.display_height)
        self.changeme_layout.setGeometry(QRect(20, 230, 790, 220))

        # создаем блок информации
        self.information_label = QLabel(self)
        self.information_label.setGeometry(410, 160, 790, 160)
        self.information_label.setText('Информация')

        self.plate_number_layout = QLabel(self)
        self.plate_number_layout.setGeometry(410, 175, 790, 175)
        self.plate_number_layout.setText('тута ваня')

        # Создаем кнопку для начала детекта
        self.start_button = QPushButton(self)
        self.start_button.setGeometry(QtCore.QRect(410, 500, 100, 20))
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.run)

        # # create the video capture thread
        # self.thread = VideoThread()
        # # connect its signal to the update_image slot
        # self.thread.change_pixmap_signal.connect(self.process_image)
        # # start the thread
        # self.thread.run()

    @pyqtSlot(np.ndarray)
    def process_image(self, cv_img):
        """Обрабатывает и выводит в приложение все изображения"""
        print(1111)
        self.original_video_label.setPixmap(self.convert_cv_qt(cv_img))
        return

        # Обработка через нейронку
        # Получение обрезанных автомобилей
        cars, yolo_mat_img, sqr_arr = yolo_car_checker(cv_img)
        #sqr_arr.append(tuple((xmin, ymin), (xmax, ymax)))

        # Защита если Серега вернул хуйню
        if (len(cars[0]) != len(cars[1])):
            print('Серега вернул хуйню')
            exit(-1)

        # Получение автомобильных номеров
        cars.append([])
        for i in range(len(cars[0])):
            # Добавление в массив номера автомобиля
            cars[2].append(getFuckingNuumber(cars[1][i]))

        # Наложение фильтров @todo
        carsFiltered = [[], list(), []]
        hardcode_filter = 'car'
        car_detected_cv = cars[1]
        buf = []
        filtered_img = cv_img.copy()
        for i in range(len(car_detected_cv)):
            if (cars[0][i] == hardcode_filter):
                carsFiltered[0].append(cars[0][i])
                carsFiltered[1].append(cars[1][i])
                carsFiltered[2].append(cars[2][i])
                # buf.append(cv2.resize(i, (64,64)))
                cv2.rectangle(filtered_img, sqr_arr[i][0], sqr_arr[i][1], (255, 0, 255), 3)  # box

        # Вывод для дебага
        print('===Без фильтров===')
        print('Типы автомобилей:', cars[0])
        print('Номерной знак автомобилей:', cars[2])
        print('===С фильтрами====')
        print('Типы автомобилей:', carsFiltered[0])
        print('Номерной знак автомобилей:', carsFiltered[2])

        # Вывод всех изображений
        #self.original_video_label.setPixmap(self.convert_cv_qt(cv_img))        # Ориг кадр
        self.recognition_layout.setPixmap(self.convert_cv_qt(yolo_mat_img))     # Кадр с квадратиками авто
        self.changeme_layout.setPixmap(self.convert_cv_qt(filtered_img))        # Кадр с квадратиками авто с фильтрами
        print('function ended')

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    # Это наш мейн
    def run(self):
        # capture from video
        cap = cv2.VideoCapture('./Object_Detection/test/vehicle-counting.mp4')
        while True:
            ret, cv_img = cap.read()
            if ret:
                print(123)
                self.process_image(cv_img)
            else:
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    # t = QtCore.QTimer()
    # t.singleShot(0,a.run)
    sys.exit(app.exec_())
