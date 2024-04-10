from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QComboBox, QFileDialog, QMainWindow
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QRect, Qt
import sys
import cv2
from yolo import detect_obj

class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # Служебные переменные
        self.filter = 'Все'
        self.recognited_objects = []
        self.cv_img = None
        self.sqr_arr = None
        self.filename = None

        # Характеристики окна
        self.setWindowTitle("Item checker")
        self.setFixedWidth(810)
        self.setFixedHeight(800)

        # Вывод оригинального изображения (верхнее левое)
        self.original_image = QLabel(self)
        self.original_image.setGeometry(QRect(20, 10, 380, 220))

        # Вывод изображения со всеми найенными обьектаи (верхнее правое)
        self.recognition_image = QLabel(self)
        self.recognition_image.setGeometry(QRect(410, 10, 380, 220))

        # Вывод изображения с отфильтрованными обьектами (нижнее)
        self.recognition_with_filters_image = QLabel(self)
        self.recognition_with_filters_image.setGeometry(QRect(20, 240, 780, 448))

        # Кнопка выбора изображения
        self.choose_file_button = QPushButton(self)
        self.choose_file_button.setText('Выбрать файл')
        self.choose_file_button.setFont(QFont('Times', 15))
        self.choose_file_button.setGeometry(QtCore.QRect(145, 730, 250, 60))
        self.choose_file_button.setObjectName("choose_file")
        self.choose_file_button.clicked.connect(self.openFileNameDialog)

        # Выпадающий список
        self.itemComboBox = QComboBox(self)
        self.itemComboBox.addItem('Все')
        self.itemComboBox.setGeometry(QtCore.QRect(145, 690, 520, 30))
        self.itemComboBox.setFont(QFont('Times', 14))
        self.itemComboBox.activated.connect(self.comboBoxChanged)

        # Вывод общего количества
        self.total_count_label_text = QLabel(self)
        self.total_count_label_text.setText('Всего:')
        self.total_count_label_text.setFont(QFont('Times', 13))
        self.total_count_label_text.setGeometry(QtCore.QRect(20, 655, 100, 100))
        self.total_count_label = QLabel(self)
        self.total_count_label.setText('0')
        self.total_count_label.setFont(QFont('Times', 13))
        self.total_count_label.setGeometry(QtCore.QRect(20, 675, 100, 100))

        # Кнопка для начала детекта
        self.start_button = QPushButton(self)
        self.start_button.setText('Старт')
        self.start_button.setDisabled(True)
        self.start_button.setGeometry(QtCore.QRect(415, 730, 250, 60))
        self.start_button.setFont(QFont('Times', 15))
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.process_image)

        # Вывод фильтрованного количества
        self.filtered_count_label_text = QLabel(self)
        self.filtered_count_label_text.setText('С фильтром:')
        self.filtered_count_label_text.setFont(QFont('Times', 13))
        self.filtered_count_label_text.setGeometry(QtCore.QRect(680, 655, 150, 100))
        self.filtered_count_label = QLabel(self)
        self.filtered_count_label.setText('0')
        self.filtered_count_label.setFont(QFont('Times', 13))
        self.filtered_count_label.setGeometry(QtCore.QRect(680, 675, 100, 100))

    def openFileNameDialog(self):
        """Диалоговое окно с выбором файла"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open file','c:\'', "Image files (*.jpg, *.png)")
        if fileName:
            self.filename = fileName
            self.start_button.setEnabled(True)

    def comboBoxChanged(self, index: int):
        """Применение фильтра при смене значения в выпадающем списке"""
        print(self.itemComboBox.itemText(index))
        self.filter = self.itemComboBox.itemText(index)
        self.use_filter()
    
    def process_image(self):
        """Обрабатывает и выводит в приложение все изображения"""
        # Очистка переменных
        self.filter = 'Все'
        self.recognited_objects = []
        self.sqr_arr = None
        
        # Открытие изображения
        self.cv_img = cv2.imread(self.filename)

        # Обработка через нейронку (модель YoloV8)
        self.recognited_objects, yolo_mat_img, self.sqr_arr = detect_obj(self.cv_img.copy()) # ['person', 'bicycle', 'person']

        # Выводим количество объектов
        self.total_count_label.setText(str(len(self.recognited_objects)))

        # Очистка выпадающего списка
        self.itemComboBox.clear()
        self.itemComboBox.addItem('Все ' + str(len(self.recognited_objects)) + ' обьектов')

        # Заполнение выпадающего списка
        unique_objects = set(self.recognited_objects)
        dropbox_text = set()
        for val in unique_objects:
            dropbox_text.add(val + " " + str(len(list(filter(lambda x: x == val, self.recognited_objects)))) + " обьект (ов)")
        self.itemComboBox.addItems(dropbox_text)

        # Вывод всех изображений
        self.original_image.setPixmap(self.convert_cv_qt(self.cv_img))              # Ориг кадр
        self.recognition_image.setPixmap(self.convert_cv_qt(yolo_mat_img))          # Кадр с квадратиками

        # Применение фильтра на новое изображение (выведет все обьекты)
        self.use_filter()

    def use_filter(self):
        """Применение фильтров"""
        count = 0
        filtered_img = self.cv_img.copy()
        for i in range(len(self.recognited_objects)):                                                   # Нанесение квадратиков на изображение с фильтрами
            if 'Все' in self.filter or self.recognited_objects[i] in self.filter:
                count += 1
                cv2.rectangle(filtered_img, self.sqr_arr[i][0], self.sqr_arr[i][1], (255, 0, 255), 3)   # Нанесение квадратика на изображение с фильтрами
        cv2.resize(filtered_img, (780, 450))                                                            # Изменяем размер картинки
        self.recognition_with_filters_image.setPixmap(self.convert_cv_qt(filtered_img, 780, 448))       # Кадр с квадратиками с фильтрами

        # Выводим количество отфильтрованных объектов
        self.filtered_count_label.setText(str(count))

    def convert_cv_qt(self, cv_img, width = 380, height = 220):
        """Конвертация CV изображения в QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(width, height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
