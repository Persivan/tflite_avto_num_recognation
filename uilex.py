from NumberRecognition import getFuckingNuumber
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect
import sys
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtCore
import numpy as np
from yolo import yolo_car_checker

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.counter = 3
        self.setWindowTitle("Qt live label demo")
        self.setFixedWidth(800)
        self.setFixedHeight(460)
        self.display_width = 370
        self.display_height = 210

        # создаем первое видео (верхнее левое)
        self.original_video_label = QLabel(self)
        self.original_video_label.resize(self.display_width, self.display_height)
        self.original_video_label.setGeometry(QRect(20, 10, 390, 220))

        # создаем второе видео (верхнее правое)
        self.recognition_layout = QLabel(self)
        self.recognition_layout.resize(self.display_width, self.display_height)
        self.recognition_layout.setGeometry(QRect(410, 10, 390, 220))

        # создаем третье видео (нижнее левое)
        self.recognition_with_filters_layout = QLabel(self)
        self.recognition_with_filters_layout.resize(self.display_width, self.display_height)
        self.recognition_with_filters_layout.setGeometry(QRect(20, 230, 390, 220))

        # Создаем кнопку для начала детекта
        self.next_frame = QPushButton(self)
        self.next_frame.setText('След')
        self.next_frame.setGeometry(QtCore.QRect(680, 230, 100, 25))
        self.next_frame.setObjectName("start_button")
        self.next_frame.clicked.connect(self.run)
        self.previous_frame = QPushButton(self)
        self.previous_frame.setText('Пред')
        self.previous_frame.setGeometry(QtCore.QRect(570, 230, 100, 25))
        self.previous_frame.setObjectName("previous_frame")
        self.previous_frame.clicked.connect(self.go_back)

        # # create the video capture thread
        # self.thread = VideoThread()
        # # connect its signal to the update_image slot
        # self.thread.change_pixmap_signal.connect(self.process_image)
        # # start the thread
        # self.thread.run()

        # Фильтры
        self.filters = []
        self.filter_label = QLabel(f'Кадр {self.counter}', self)
        self.filter_label.setGeometry(410, 230, 100, 25)  # Позиция и размеры фильтр-лейбла
        self.filter_input = QLineEdit(self)
        self.filter_input.setGeometry(410, 260, 370, 25)  # Позиция и размеры поля для ввода номерного знака
        self.filter_input.textChanged.connect(self.on_plate_filter_changed)

    # Фильтр
    def on_plate_filter_changed(self, plate_filter):
        self.filters = plate_filter.split()
        print("Новый фильтр:", self.filters)

    @pyqtSlot(np.ndarray)
    def process_image(self, cv_img):
        """Обрабатывает и выводит в приложение все изображения"""

        # Обработка через нейронку
        # Получение обрезанных автомобилей
        cars, yolo_mat_img, sqr_arr = yolo_car_checker(cv_img.copy())
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

        # Наложение фильтров
        cars_filtered = [[], list(), []]
        car_detected_cv = cars[1]
        filtered_img = cv_img.copy()
        for i in range(len(car_detected_cv)):
            if cars[0][i] in self.filters and cars[2][i] in self.filters:
                cars_filtered[0].append(cars[0][i])
                cars_filtered[1].append(cars[1][i])
                cars_filtered[2].append(cars[2][i])
                cv2.rectangle(filtered_img, sqr_arr[i][0], sqr_arr[i][1], (255, 0, 255), 3)  # box
        pink_car = filtered_img.copy()

        # Вывод для дебага
        print('==========Без фильтров========')
        print('Типы автомобилей:', cars[0])
        print('Номерной знак автомобилей:', cars[2])
        print('==========С фильтрами=========')
        print('Типы автомобилей:', cars_filtered[0])
        print('Номерной знак автомобилей:', cars_filtered[2])

        # Вывод в таблицу @todo


        # Вывод всех изображений
        self.original_video_label.setPixmap(self.convert_cv_qt(cv_img))             # Ориг кадр
        self.recognition_layout.setPixmap(self.convert_cv_qt(yolo_mat_img))         # Кадр с квадратиками авто
        self.recognition_with_filters_layout.setPixmap(self.convert_cv_qt(pink_car))# Кадр с квадратиками авто с фильтрами

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    def go_back(self):
        # @todo out of index guard
        self.counter -= 2
        self.run()

    # Это наш мейн
    def run(self):
        self.filter_label.setText(f'В процессе..')
        # capture from video
        cap = cv2.VideoCapture('./Object_Detection/test/Untitled.mp4')
        local_counter = 0
        good = False
        cv_img = 0

        while local_counter <= self.counter:
            # @todo out of index guard
            local_counter += 1
            good, cv_img = cap.read()
        
        print(cv_img)
        
        # иф аут оф индекс
        if good:
            self.process_image(cv_img)
            self.counter += 1
        else:
            print('Не хорошо(((')
        
        self.filter_label.setText(f'Кадр {self.counter}')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
