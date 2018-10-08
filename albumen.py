# -*- coding: utf-8 -*-

import sys
import urllib.request

from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QApplication, QHBoxLayout, 
    QVBoxLayout, QPushButton, QLineEdit, QLabel)
from PyQt5.QtGui import QIcon, QImage, QPixmap


class Albumen(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addWidget(QLineEdit(self), 3)
        hbox.addWidget(QPushButton("Search"), 1)


        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        
        url = 'https://lastfm-img2.akamaized.net/i/u/300x300/17ea9e6cf87d4c04a622b5bf7ba241be.png'
        data = urllib.request.urlopen(url).read()
        image = QImage()
        image.loadFromData(data)
        lbl = QLabel(self)
        lbl.setScaledContents(True)
        lbl.setPixmap(QPixmap(image))
        vbox.addWidget(lbl)
        #vbox.addStretch(1)

        self.setLayout(vbox) 

        self.resize(500, 500)
        self.center()
        self.setWindowTitle('Albumen')
        self.setWindowIcon(QIcon('icon.png'))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Albumen()
    sys.exit(app.exec_())