import os

from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, \
    QAction, QPushButton, QLineEdit, QSystemTrayIcon, QMenu
from PyQt5.QtCore import QSize, pyqtSlot, QTimer
from PyQt5 import QtMultimedia


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class SystemTrayIcon(QSystemTrayIcon):
  tray_icon = True
  def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.tray_icon = QSystemTrayIcon(self)
        menu = QMenu(parent)
        quit_action = QAction("Exit", self)
        menu.addAction(quit_action)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        self.iconLabel = QLabel("TEST")
        tray_menu.addAction(quit_action)
        self.setContextMenu(tray_menu)
        self.show()


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса

    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)
        self.sound = QtMultimedia.QSound(resource_path('assets/beep.wav'))
        self.setWindowIcon(QtGui.QIcon(resource_path('assets/icon.png')))
        trayIcon = SystemTrayIcon(QtGui.QIcon(resource_path("assets/icon.png")), self)
        trayIcon.show()

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
        self.setup_initial_state()
        self.setup_buttons()
        self.setup_display()
        self.setup_input()
        self.process_state_changes()

    def setup_initial_state(self):
        self.timer_connected = False
        self.timer_value = 60*25
        self.timer = QTimer()
        assert not self.timer.isActive()

    def setup_buttons(self):
        self.start_button = QPushButton('Стартуем', self)
        self.start_button.resize(100, 100)
        self.start_button.setToolTip('Старт')
        self.start_button.move(10,30)
        self.start_button.clicked.connect(self.setup_timer)

        self.stop_button = QPushButton('Стоп', self)
        self.stop_button.resize(100, 100)
        self.stop_button.setToolTip('Стоп')
        self.stop_button.move(120,30)
        self.stop_button.clicked.connect(self.stop_timer)

    def setup_display(self):
        self.display = QLabel(self)
        self.display.setAlignment(Qt.Qt.AlignCenter)
        self.display.setText("20:00")
        self.display.setFont(QtGui.QFont("Helvetica", 102))
        self.display.resize(470, 200)
        self.display.move(10, 110)

    def process_timer(self):
        try:
            minutes = int(self.minutes.text())
        except ValueError:
            minutes = 0

        try:
            seconds = int(self.seconds.text())
        except ValueError:
            seconds = 0
        minutes = max(0, min(59, minutes))
        seconds = max(0, min(59, seconds))
        self.minutes.setText(str(minutes))
        self.seconds.setText(str(seconds))

        self.timer_value = minutes * 60 + seconds
        self.display.setText(f"{minutes:02d}:{seconds:02d}")

    def setup_input(self):
        self.minutes = QLineEdit(self)
        self.minutes.setText("25")
        self.minutes.setFont(QtGui.QFont("Helvetica", 64))
        self.minutes.resize(100, 100)
        self.minutes.move(230, 30)
        self.minutes.textChanged.connect(self.process_timer)

        self.seconds = QLineEdit(self)
        self.seconds.setText("00")
        self.seconds.setFont(QtGui.QFont("Helvetica", 64))
        self.seconds.resize(100, 100)
        self.seconds.move(340, 30)
        self.seconds.textChanged.connect(self.process_timer)

    def process_state_changes(self):
        if self.timer.isActive():
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.minutes.setReadOnly(True)
            self.seconds.setReadOnly(True)
        else:
            self.minutes.setReadOnly(False)
            self.seconds.setReadOnly(False)
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

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
        self.sound.stop()
        self.process_timer()
        self.process_state_changes()

    @pyqtSlot()
    def beep(self):
        print("beep")
        self.sound.play()
        print("beeped")

    @pyqtSlot()
    def tick(self):
        if self.timer_value:
            print(self.timer_value)
            self.timer_value -= 1
            minutes = self.timer_value // 60
            seconds = self.timer_value % 60
            self.display.setText(f"{minutes:02d}:{seconds:02d}")
            if not self.timer_value:
                self.beep()
        self.process_state_changes()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
