import sys

import PyQt6
import requests
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel

MAP_FILE = "map.png"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.setFixedSize(600, 450)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.setGeometry(300, 300, 500, 400)
        self.ll = "149,-35"
        self.spn = "50,50"
        self.init_ui()

    def init_ui(self):
        self.get_image()
        pass

    def get_image(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={self.ll}&spn={self.spn}'

        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        with open(MAP_FILE, "wb") as file:
            file.write(response.content)

        pixmap = QPixmap("map.png")

        if pixmap.isNull():
            print("Ошибка: не удалось загрузить изображение. Проверьте путь.")
            return

        self.label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            x = list(map(int, self.spn.split(",")))[0]
            if x > 10:
                self.spn = f"{x - 10},{x - 10}"
                self.get_image()
        if key == Qt.Key.Key_PageDown:
            x = list(map(int, self.spn.split(",")))[0]
            if x < 80:
                self.spn = f"{x + 10},{x + 10}"
                self.get_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
    
