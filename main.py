from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction, QPushButton
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5 import QtMultimedia


sound = QtMultimedia.QSound('beep.wav')
# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса

    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(480, 320))    # Устанавливаем размеры
        self.setWindowTitle("Hello world!!!")   # Устанавливаем заголовок окна
        central_widget = QWidget(self)          # Создаём центральный виджет
        self.setCentralWidget(central_widget)   # Устанавливаем центральный виджет

        grid_layout = QGridLayout(self)         # Создаём QGridLayout
        central_widget.setLayout(grid_layout)   # Устанавливаем данное размещение в центральный виджет

        title = QLabel("Hello World on the PyQt5", self)    # Создаём лейбл
        title.setAlignment(QtCore.Qt.AlignCenter)   # Устанавливаем позиционирование текста
        grid_layout.addWidget(title, 0, 0)          # и добавляем его в размещение

        exit_action = QAction("&Exit", self)    # Создаём Action с помощью которого будем выходить из приложения
        exit_action.setShortcut('Ctrl+Q')       # Задаём для него хоткей
        # Подключаем сигнал triggered к слоту quit у qApp.
        # синтаксис сигналов и слотов в PyQt5 заметно отличается от того,
        # который используется Qt5 C++
        exit_action.triggered.connect(qApp.quit)
        # Устанавливаем в панель меню данный Action.
        # Отдельного меню создавать пока не будем.
        file_menu = self.menuBar()
        file_menu.addAction(exit_action)

        button = QPushButton('Button', self)
        button.setToolTip('Beep')
        button.move(100,70)
        button.clicked.connect(self.beep)

    @pyqtSlot()
    def beep(self):
        sound.play()
        # print("beep")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())

