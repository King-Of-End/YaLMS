import os
import sys
from io import BytesIO

from PyQt6.QtCore import Qt
from load_dotenv import load_dotenv
import requests
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QApplication

from get_scaling import get_scaling, get_coords

load_dotenv()

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

        self.scale: int = 1

        self.load_map()

    def load_map(self):
        map_params = self.get_map_params('Байкал', self.scale)
        self.get_map(map_params)

    def get_map_params(self, name, scale):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "geocode": name,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params).json()
        toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        params = {
            'spn' : get_scaling(toponym, scale),
            'll': get_coords(toponym),
            'apikey': os.getenv("API_KEY")
        }
        return params

    def set_pixmap(self, pixmap):
        self.label.setPixmap(pixmap)

    def get_map(self, map_params):
        map_api_server = "https://static-maps.yandex.ru/v1"
        response = requests.get(map_api_server, params=map_params)
        im = BytesIO(response.content).getvalue()
        opened_image = QImage.fromData(im)
        pixmap = QPixmap.fromImage(opened_image)
        self.set_pixmap(pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            self.scale -= 0.1
            self.load_map()
        if key == Qt.Key.Key_PageDown:
            self.scale += 0.1
            self.load_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())



    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            x = self.spn[0]
            if x > 10:
                self.spn = [x - 10, x - 10]
                self.get_image()
        if key == Qt.Key.Key_PageDown:
            x = self.spn[0]
            if x > 10:
                self.spn = [x + 10, x + 10]
                self.get_image()
        if key == Qt.Key.Key_Left:
            if self.ll[0] > -180:
                self.ll[0] -= 1
                self.get_image()
        if key == Qt.Key.Key_Right:
            if self.ll[0] > -180:
                self.ll[0] += 1
                self.get_image()
        if key == Qt.Key.Key_Up:
            if self.ll[1] < 90:
                self.ll[1] += 1
                self.get_image()
        if key == Qt.Key.Key_Down:
            if self.ll[1] > -90:
                self.ll[1] -= 1
                self.get_image()
