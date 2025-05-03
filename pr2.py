from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QMainWindow, QPushButton,
    QVBoxLayout, QWidget, QMessageBox, QListWidget, QListWidgetItem,
    QFileDialog
)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("График")

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.functions = {} # Словарь для хранения функций {название: функция}
        self.selected_function = None # Выбранная функция
        self.x = None
        self.y = None

        # Виджеты
        self.plot_button = QPushButton("Нарисовать график")
        self.plot_clear_button = QPushButton("Очистить график")
        self.function_label = QLabel("Функция:")
        self.function_input = QLineEdit('x**3') # Поле ввода названия функции
        self.add_function_button = QPushButton("Добавить функцию")
        self.function_list = QListWidget()
        self.range_label = QLabel("Диапазон по оси x:")
        self.range_start_input = QLineEdit('0')
        self.range_end_input = QLineEdit('1')
        self.plot_point_count_label = QLabel("Количество точек:")
        self.num_points_input = QLineEdit('50')
        self.save_plot_points_button = QPushButton("Сохранить точки")


        # Макет
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Добавление виджетов на макет
        layout.addWidget(self.canvas)
        layout.addWidget(self.function_label)
        layout.addWidget(self.function_input)
        layout.addWidget(self.add_function_button)
        layout.addWidget(self.function_list)
        layout.addWidget(self.range_label)
        layout.addWidget(self.range_start_input)
        layout.addWidget(self.range_end_input)
        layout.addWidget(self.plot_point_count_label)
        layout.addWidget(self.num_points_input)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.plot_clear_button)
        layout.addWidget(self.save_plot_points_button)


        self.setCentralWidget(central_widget)

        #
        self.plot_button.clicked.connect(self.plot_data)
        self.plot_clear_button.clicked.connect(self.clear_plot)
        self.add_function_button.clicked.connect(self.add_function)
        self.function_list.itemSelectionChanged.connect(self.update_selected_function)
        self.save_plot_points_button.clicked.connect(self.save_plot_points)

        self.add_function()


    def add_function(self):
        try:
            expression = self.function_input.text()
            # Создаем лямбда-функцию в безопасном окружении  проверить, можно ли вычислить функцию с каким-либо значением,
            # и выбросить исключение до того, как функция будет добавлена
            func = eval(f"lambda x: {expression}", {"__builtins__": None}, {"x": None, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, \
                        "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi}) # add more functions as needed

            # Тестируем функцию, чтобы выявить ошибки
            test_value = 0
            func(test_value) # Вызываем функцию для проверки

            self.functions[expression] = func
            item = QListWidgetItem(expression)
            self.function_list.addItem(item)
            self.function_list.setCurrentItem(item) # Выбираем добавленную функцию

        except (SyntaxError, NameError, TypeError, ValueError, ZeroDivisionError, OverflowError) as e:
            QMessageBox.warning(self, "Ошибка", f"Функция введена не верно: {e}")
        except Exception as e: # Ловим другие потенциальные ошибки
            QMessageBox.warning(self, "Ошибка", f"Функция не может быть вычислена: {e}")


    def update_selected_function(self):
        selected_items = self.function_list.selectedItems()
        if selected_items:
            self.selected_function = self.functions[selected_items[0].text()]
        else:
            self.selected_function = None

        if self.selected_function is None:
            QMessageBox.warning(self, "Ошибка", "Выберите функцию")
            return
        range_start = float(self.range_start_input.text())
        range_end = float(self.range_end_input.text())
        num_point = int(self.num_points_input.text())
        x = np.linspace(range_start, range_end, num_point)
        y = self.selected_function(x)
        self.x = x
        self.y = y


    def plot_data(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(self.x, self.y)
        ax.grid(True)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'График функции: {self.function_input.text()}')
        self.canvas.draw()


    def clear_plot(self):
        self.figure.clear()
        self.canvas.draw()


    def save_plot_points(self):
        # Открываем диалоговое окно "Сохранить как..."
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить точки графика в файл", "plot_data.txt")

        # Если пользователь нажал "Отмена", filename будет пустой строкой
        if not filename:
            return

        # Добавляем расширение .txt, если пользователь его не указал
        if not filename.endswith(".txt"):
            filename += ".txt"

        with open(filename, "w") as f:
            for i in range(len(self.x)):
                f.write(f"{self.x[i]:.6f}\t{self.y[i]:.6f}\n")
            QMessageBox.information(self, "Успешно", f"Данные графика успешно сохранены в файл {filename}")


# Создать приложение QApplication
app = QApplication([])
# Создать окно приложения
main_window = MainWindow()
main_window.show()
# Запустить приложение
app.exec_()
