import os
import sys
from io import BytesIO

from pydantic import BaseModel
from PyQt6.QtCore import Qt
from load_dotenv import load_dotenv
import requests
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QApplication

load_dotenv()

class MapParams(BaseModel):
    ll:

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
        self.delta = [0, 0]

        self.map_params = self.load_map_params('Байкал')

        self.update_map()

    def get_scaling(self, toponym):
        delta_long = str(abs(float(toponym['boundedBy']['Envelope']['lowerCorner'].split(" ")[0]) -
                             float(toponym['boundedBy']['Envelope']['upperCorner'].split(" ")[0])))
        delta_lat = str(abs(float(toponym['boundedBy']['Envelope']['lowerCorner'].split(" ")[1]) -
                            float(toponym['boundedBy']['Envelope']['upperCorner'].split(" ")[1])))
        return ",".join([delta_long, delta_lat])

    def get_coords(self, toponym):
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = list(map(float, toponym_coodrinates.split(" ")))
        return ",".join(str(x) for x in [toponym_longitude, toponym_lattitude])

    def update_map(self):
        pixmap = self.get_map(self.map_params)
        self.set_pixmap(pixmap)

    def update_params(self):


    def load_map_params(self, name):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "geocode": name,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params).json()
        toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        params = {
            'spn' : self.get_scaling(toponym),
            'll': self.get_coords(toponym),
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
        return pixmap

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            self.scale -= 0.1
            self.update_map()
        if key == Qt.Key.Key_PageDown:
            self.scale += 0.1
            self.update_map()
        if key == Qt.Key.Key_Left:
            if self.delta[0] < 180:
                self.delta[0] -= 10
                self.update_map()
        if key == Qt.Key.Key_Right:
            if self.delta[0] > -180:
                self.delta[0] += 10
                self.update_map()
        if key == Qt.Key.Key_Up:
            if self.delta[1] < 90:
                self.delta[1] += 10
                self.update_map()
        if key == Qt.Key.Key_Down:
            if self.delta[1] > -90:
                self.delta[1] -= 10
                self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())