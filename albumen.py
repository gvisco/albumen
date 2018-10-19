# -*- coding: utf-8 -*-

import sys, os
import urllib.request
import webbrowser
import pylast
import configparser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QApplication, QHBoxLayout, 
    QVBoxLayout, QPushButton, QLineEdit, QLabel, QInputDialog)
from PyQt5.QtGui import QIcon, QImage, QPixmap

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(ROOT_DIR, 'config.ini')

IMG_PATH = os.path.join(ROOT_DIR, 'pics')
ICON_PATH = os.path.join(IMG_PATH, 'icon.png')
NOARTIST_PATH = os.path.join(IMG_PATH, 'noartist.jpg')
NOALBUM_PATH = os.path.join(IMG_PATH, 'noalbum.jpg')
ERROR_PATH = os.path.join(IMG_PATH, 'error.jpg')

class Albumen(QWidget):
    
    def __init__(self):
        super().__init__()
        self.albums = []
        self.artist = '-'
        self.index = 0
        self.network = self.initLastFM()
        self.initUI()

    def initLastFM(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        API_KEY = config['DEFAULT']['API_KEY']
        network = pylast.LastFMNetwork(api_key=API_KEY)
        return network

    def initUI(self):
        self.setLayout(self.initLayout()) 
        self.setFixedSize(500, 500)
        self.centerWindow()
        self.setWindowIcon(QIcon(ICON_PATH))
        self.show()
        self.searchDialog()

    def initLayout(self):
        mainbox = QVBoxLayout()
        self.mainlabel = QLabel(self)
        mainbox.addWidget(self.mainlabel)
        self.updateContent()
        return mainbox

    def updateContent(self):
        image = QImage()
        if self.albums:
            try:
                album = self.albums[self.index].item
                url = album.get_cover_image()
                if url:
                    data = urllib.request.urlopen(url).read()
                    image.loadFromData(data)
                else:
                    image.load(NOALBUM_PATH)
                title = '%s - #%i %s' % (self.artist, self.index + 1, album.get_title())
            except Exception as e:
                print("[ERR] Cannot get album: %r" % e)
                image.load(ERROR_PATH)
                title = '%s - #%i - ERR' % (self.artist, self.index + 1)
        else:
            image.load(NOARTIST_PATH)
            title = self.artist

        self.mainlabel.setScaledContents(True)
        self.mainlabel.setPixmap(QPixmap(image))
        self.setWindowTitle(title)

    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.closeApplication()
        elif e.key() == Qt.Key_Return:
            self.searchDialog()
        elif e.key() == Qt.Key_Right:
            self.nextAlbum()
        elif e.key() == Qt.Key_Left:
            self.previousAlbum()
        elif e.key() == Qt.Key_I:
            self.albumInfo()

    def searchDialog(self):
        text, ok = QInputDialog.getText(self, 'Search', 'Search top album')
        if ok: 
            self.searchAlbums(text)

    def nextAlbum(self):
        if self.albums:
            self.index = (self.index + 1) % len(self.albums) 
            self.updateContent()

    def previousAlbum(self):
        if self.albums:
            self.index = (self.index - 1) % len(self.albums) 
            self.updateContent()

    def albumInfo(self):
        if self.albums:
            album = self.albums[self.index].item
            webbrowser.open(album.get_url())

    def searchAlbums(self, name, limit=5):
        result = self.network.get_artist(name)
        
        try:
            self.artist = result.get_correction()
            self.albums = result.get_top_albums(limit)
        except pylast.WSError as e:
            print("[ERR] Cannot get artist: %r" % e)
            self.artist = name
            self.albums = []
        
        self.index = 0
        topalbum = self.albums[self.index].item if self.albums else None
        self.updateContent()

    def closeApplication(self):
        QApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Albumen()
    sys.exit(app.exec_())