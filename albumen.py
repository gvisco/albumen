# -*- coding: utf-8 -*-

import sys
import urllib.request

import pylast
import configparser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QApplication, QHBoxLayout, 
    QVBoxLayout, QPushButton, QLineEdit, QLabel, QInputDialog)
from PyQt5.QtGui import QIcon, QImage, QPixmap

class Albumen(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.network = self.initLastFM()
                
    def initLastFM(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        API_KEY = config['DEFAULT']['API_KEY']
        network = pylast.LastFMNetwork(api_key=API_KEY)
        return network

    def initUI(self):
        self.setLayout(self.initLayout()) 
        self.setFixedSize(500, 500)
        self.centerWindow()
        self.setWindowIcon(QIcon('icon.png'))
        self.show()

    def initLayout(self):
        mainbox = QVBoxLayout()
        self.mainlabel = QLabel(self)
        mainbox.addWidget(self.mainlabel)
        #mainbox.addStretch(1)
        self.updateContent('-')
        return mainbox

    def updateContent(self, artist, url=None):
        image = QImage()
        if url:
            data = urllib.request.urlopen(url).read()
            image.loadFromData(data)
        else:
            image.load('question-mark.png')
        self.mainlabel.setScaledContents(True)
        self.mainlabel.setPixmap(QPixmap(image))
        self.setWindowTitle(artist)

    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):  
        # print(e.key())  
        if e.key() == Qt.Key_Escape:
            self.closeApplication()
        elif e.key() == Qt.Key_Return:
            self.searchDialog()

    def searchDialog(self):
        text, ok = QInputDialog.getText(self, 'Search', 'Search top album')
        if ok: 
            self.searchAlbums(text)

    def searchAlbums(self, name):
        artist = self.network.get_artist(name)
        topalbum = artist.get_top_albums(1)[0]
        # TODO: error handling
        self.updateContent(name, topalbum.item.get_cover_image())

    def closeApplication(self):
        QApplication.instance().quit()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Albumen()
    sys.exit(app.exec_())