from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, \
    QAction, QPushButton, QLineEdit
from PyQt5.QtCore import QSize, pyqtSlot, QTimer
from PyQt5 import QtMultimedia


sound = QtMultimedia.QSound('beep.wav')
# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса

    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(480, 320))    # Устанавливаем размеры
        self.setMaximumSize(QSize(480, 320))    # Устанавливаем размеры
        self.setWindowTitle("The timer!!!")
        central_widget = QWidget(self)          # Создаём центральный виджет
        self.setCentralWidget(central_widget)   # Устанавливаем центральный виджет

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
        self.setup_state()
        self.setup_buttons()
        self.setup_display()
        self.setup_input()

    def setup_state(self):
        self.timer_connected = False
        self.timer_value = 60*20
        self.timer = QTimer()
        assert not self.timer.isActive()

    def setup_buttons(self):
        self.start_button = QPushButton('Стартуем', self)
        self.start_button.resize(100, 100)
        self.start_button.setToolTip('Старт')
        self.start_button.move(10,10)
        self.start_button.clicked.connect(self.setup_timer)

        self.stop_button = QPushButton('Стоп', self)
        self.stop_button.resize(100, 100)
        self.stop_button.setToolTip('Стоп')
        self.stop_button.move(120,10)
        self.stop_button.clicked.connect(self.stop_timer)

    def setup_display(self):
        self.display = QLabel(self)
        self.display.setAlignment(Qt.Qt.AlignCenter)
        self.display.setText("20:00")
        self.display.setFont(QtGui.QFont("Helvetica", 102))
        self.display.resize(470, 200)
        self.display.move(10, 110)

    def init_timer(self):
        try:
            minutes = int(self.minutes.text())
        except ValueError:
            minutes = 0

        try:
            seconds = int(self.seconds.text())
        except ValueError:
            seconds = 0

        self.timer_value = min(60, minutes) * 60 + seconds
        self.display.setText(f"{minutes}:{seconds}")

    def setup_input(self):
        self.minutes = QLineEdit(self)
        self.minutes.setText("25")
        self.minutes.setFont(QtGui.QFont("Helvetica", 72))
        self.minutes.resize(100, 100)
        self.minutes.move(230,10)
        self.minutes.textChanged.connect(self.init_timer)

        self.seconds = QLineEdit(self)
        self.seconds.setText("00")
        self.seconds.setFont(QtGui.QFont("Helvetica", 72))
        self.seconds.resize(100, 100)
        self.seconds.move(340,10)
        self.seconds.textChanged.connect(self.init_timer)

    @pyqtSlot()
    def setup_timer(self):
        if not self.timer_connected:
            self.timer.timeout.connect(self.tick)
        self.timer_connected = True
        self.timer.start(1000)
        self.tick()

    @pyqtSlot()
    def stop_timer(self):
        self.timer.stop()
        self.init_timer()

    @pyqtSlot()
    def beep(self):
        print("beep")
        sound.play()
        print("beeped")

    @pyqtSlot()
    def tick(self):
        if self.timer_value:
            print(self.timer_value)
            self.timer_value -= 1
            minutes = self.timer_value // 60
            secs = self.timer_value % 60
            self.display.setText(f"{minutes}:{secs}")
        else:
            self.beep()
            self.timer.stop()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
