from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit, QComboBox, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPixmap, QStandardItemModel
from PyQt5.QtCore import QRect, Qt
import sys
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtCore
import numpy as np
from yolo import yolo_car_checker

class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.filters = []
        self.foundObjects = []

        self.counter = 20
        self.setWindowTitle("Item checker")
        self.setFixedWidth(810)
        self.setFixedHeight(800)

        # создаем первое видео (верхнее левое)
        self.original_video_label = QLabel(self)
        # self.original_video_label.resize(370, 210)
        self.original_video_label.setGeometry(QRect(20, 10, 380, 220))

        # создаем второе видео (верхнее правое)
        self.recognition_layout = QLabel(self)
        # self.recognition_layout.resize(370, 210)
        self.recognition_layout.setGeometry(QRect(410, 10, 380, 220))

        # создаем третье видео (нижнее левое)
        self.recognition_with_filters_layout = QLabel(self)
        # self.recognition_with_filters_layout.resize(740, 420)
        self.recognition_with_filters_layout.setGeometry(QRect(20, 240, 770, 420))

        # Создаем кнопку для начала детекта
        self.previous_frame_button = QPushButton(self)
        self.previous_frame_button.setText('Пред')
        self.previous_frame_button.setGeometry(QtCore.QRect(40, 700, 100, 25))
        self.previous_frame_button.setObjectName("previous_frame")
        self.previous_frame_button.clicked.connect(self.go_back)
        self.next_frame_button = QPushButton(self)
        self.next_frame_button.setText('След')
        self.next_frame_button.setGeometry(QtCore.QRect(160, 700, 100, 25))
        self.next_frame_button.setObjectName("start_button")
        self.next_frame_button.clicked.connect(self.run)

        
        self.filter_label = QLabel(f'Кадр {self.counter}', self)
        self.filter_label.setGeometry(QtCore.QRect(20, 740, 100, 25))  # Позиция и размеры фильтр-лейбла
        self.filter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ComboBox = QComboBox(self)
        self.ComboBox.addItem('None')
        self.ComboBox.setGeometry(QtCore.QRect(40, 670, 218, 20))
        self.ComboBox.activated.connect(self.comboboxChanged)
        self.cv_img = None
        self.sqr_arr = None

    def comboboxChanged(self, index: int):
        print(self.ComboBox.itemText(index))
        self.filters = [self.ComboBox.itemText(index)]
        self.use_filter()
    

    @pyqtSlot(np.ndarray)
    def process_image(self):
        """Обрабатывает и выводит в приложение все изображения"""

        # Обработка через нейронку (модель YoloV8)
        self.foundObjects, yolo_mat_img, self.sqr_arr = yolo_car_checker(self.cv_img.copy())
        self.ComboBox.addItems(set(self.foundObjects))

        # Вывод всех изображений
        self.original_video_label.setPixmap(self.convert_cv_qt(self.cv_img))             # Ориг кадр
        self.recognition_layout.setPixmap(self.convert_cv_qt(yolo_mat_img))         # Кадр с квадратиками авто
        self.recognition_with_filters_layout.setPixmap(self.convert_cv_qt(self.cv_img, 770, 440))# Кадр с квадратиками авто с фильтрами

    def use_filter(self):
        filtered_img = self.cv_img.copy()
        for i in range(len(self.foundObjects)):                         # Нанесение квадратиков на изображение с фильтрами
            if self.foundObjects[i] in self.filters:
                cv2.rectangle(filtered_img, self.sqr_arr[i][0], self.sqr_arr[i][1], (255, 0, 255), 3)  # Нанесение квадратика на изображение с фильтрами
        self.recognition_with_filters_layout.setPixmap(self.convert_cv_qt(filtered_img, 770, 440))



    def convert_cv_qt(self, cv_img, width = 380, height = 220):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(width, height, Qt.KeepAspectRatio)
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
            self.cv_img = cv_img
            self.process_image()
            self.counter += 1
        else:
            print('Не хорошо(((')
        
        self.filter_label.setText(f'Кадр {self.counter}') 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
