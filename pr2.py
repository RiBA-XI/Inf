from PyQt5.QtWidgets import (
 QApplication,
 QLabel,
 QLineEdit,
 QMainWindow,
 QPushButton,
 QVBoxLayout,
 QWidget,
 QMessageBox, QListWidget, QListWidgetItem, QFileDialog

)

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow):
    def plot_data(self):
        if self.selected_function is None:
            QMessageBox.warning(self, "Ошибка", "выберите функцию")
            return

        try:
            expression = self.function_input.text()
        except ValueError:
            expression = "x**3"

        try:
            range_start = float(self.range_start_input.text())
            range_end = float(self.range_end_input.text())
        except ValueError:
            range_start = 0
            range_end = 1

        try:
            num_point = int(self.num_points_input.text())
        except ValueError:
            num_point = 50

        x = np.linspace(range_start, range_end, num_point)
        #functions = {}  # определим словарь функций
        #exec(f"def f(x): return {self.selected_function}", functions)  ###############################
        function = self.selected_function["f"]
        #self.functions  # обращаемся к массиву объекта и получаем из него функции
        y = [function(value) for value in x]

        self.figure.clf()  # Очищаем всю фигуру
        plt.plot(x, y)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('График функции: ' + self.selected_function)
        self.canvas.draw()

        self.x = x
        self.y = y

    def clear_plot(self):
        try:
            self.figure.clf()  # Очищаем всю figure
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при очистке графика: {e}")


    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("График")

        # self.canvas = FigureCanvas(plt.figure()) # Создание полотна Matplotlib
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.functions = []  # Список для хранения функций

        self.plot_button = QPushButton("Нарисовать график")
        self.plot_button.clicked.connect(self.plot_data)
        self.plot_clear_button = QPushButton("очистка графика")
        self.plot_clear_button.clicked.connect(self.clear_plot)
        self.function_label = QLabel("Функция:")
        self.function_input = QLineEdit('x**3')
        self.add_function_button = QPushButton("Добавить функцию")
        self.add_function_button.clicked.connect(self.add_function)
        self.function_list = QListWidget()
        self.function_list.itemSelectionChanged.connect(self.update_selected_function)
        self.range_label = QLabel("Диапазон по оси x:")
        self.range_start_input = QLineEdit('0')
        self.range_end_input = QLineEdit('1')
        self.plot_point_count_label = QLabel("Количество точек для отрисовки графика")
        self.num_points_input = QLineEdit('50')
        self.save_plot_points_button = QPushButton("сохранить точки графика в файл")
        self.save_plot_points_button.clicked.connect(self.save_plot_points)

        # Создание центрального виджета
        central_widget = QWidget()
        layout = QVBoxLayout()  # макет, на который будут добавляться виджеты
        central_widget.setLayout(layout)  # добавление макета на центральный виджет

        # Добавление виджетов на макет
        layout.addWidget(self.canvas)
        layout.addWidget(self.plot_button) #кнопка, при нажатии на которую будет рисоваться график
        layout.addWidget(self.plot_clear_button)
        layout.addWidget(self.function_label)
        layout.addWidget(self.function_input)
        layout.addWidget(self.add_function_button)
        layout.addWidget(self.function_list)
        layout.addWidget(self.range_label)
        layout.addWidget(self.range_start_input)
        layout.addWidget(self.range_end_input)
        layout.addWidget(self.plot_point_count_label)
        layout.addWidget(self.num_points_input)
        layout.addWidget(self.save_plot_points_button)

        # Установка центрального виджета
        self.setCentralWidget(central_widget)
        self.selected_function = None

    def add_function(self):#добовляем функцию в список выбора
        function_text = self.function_input.text()

        #exec(f"def f(x): return {self.selected_function}", functions)
        try:
            function = exec(f"lambda x: {function_text}")
            item = QListWidgetItem(function_text)
            self.function_list.addItem(item)
            self.functions.append(function_text)
            self.function_input.clear()

        except NameError as e:
            QMessageBox.warning(self, "Ошибка", "функция введена не верно exept")
        except SyntaxError as e:
            QMessageBox.warning(self, "Ошибка", "функция введена не верно exept")
        except TypeError as e:
            QMessageBox.warning(self, "Ошибка", "функция введена не верно exept")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", "функция введена не верно exept")
        # except Exception as e:
        #     QMessageBox.warning(self, "Ошибка", "функция введена не верно exept")

        # try:
        #     item = QListWidgetItem(function_text)
        #     self.function_list.addItem(item)
        #     self.functions.append(function_text)
        #     self.function_input.clear()
        # except ***:
        #     QMessageBox.warning(self, "Ошибка", "функция введена не верно")

    def update_selected_function(self):#выбор функции для отрисовки из списка
        selected_items = self.function_list.selectedItems()
        if selected_items:
            self.selected_function = selected_items[0].text()
        else:
            self.selected_function = None

    def save_plot_points(self):
        # Открываем диалоговое окно "Сохранить как..."
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить точки графика в файл", "plot_data.txt")

        # # Если пользователь нажал "Отмена", filename будет пустой строкой
        # if not filename:
        #     return

        if not filename.endswith(".txt"): # Добавляем расширение .txt, если пользователь его не указал
            filename += ".txt"

        with open(filename, "w") as f:
            for i in range(len(self.x)):
                f.write(f"{self.x[i]}\t{self.y[i]}\n")
            QMessageBox.information(self, "Успешно", f"Данные графика успешно сохранены в файл {filename}")


# Создать приложение QApplication
app = QApplication([])
# Создать окно приложения
main_window = MainWindow()
main_window.show()
# Запустить приложение
app.exec_()
