# -*- coding: utf-8 -*-

import sys
import urllib.request

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QApplication, QHBoxLayout, 
    QVBoxLayout, QPushButton, QLineEdit, QLabel, QInputDialog)
from PyQt5.QtGui import QIcon, QImage, QPixmap


class Albumen(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):
        self.setLayout(self.initLayout()) 

        self.resize(500, 500)
        self.centerWindow()
        self.setWindowTitle('Albumen')
        self.setWindowIcon(QIcon('icon.png'))

        self.show()


    def initLayout(self):
        mainbox = QVBoxLayout()
        
        url = 'https://lastfm-img2.akamaized.net/i/u/300x300/17ea9e6cf87d4c04a622b5bf7ba241be.png'
        data = urllib.request.urlopen(url).read()
        image = QImage()
        image.loadFromData(data)
        lbl = QLabel(self)
        lbl.setScaledContents(True)
        lbl.setPixmap(QPixmap(image))
        mainbox.addWidget(lbl)
        #mainbox.addStretch(1)
        return mainbox


    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def keyPressEvent(self, e):  
        print(e.key())  
        if e.key() == Qt.Key_Escape:
            self.closeApplication()
        elif e.key() == Qt.Key_Return:
            self.search()

    def search(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Search top albums')
        if ok:
            print(str(text))


    def closeApplication(self):
        QApplication.instance().quit()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Albumen()
    sys.exit(app.exec_())