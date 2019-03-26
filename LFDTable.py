import os

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class LFDTable(QTableWidget):
    def __init__(self, r = 1, c = 6):
        super().__init__(r, c)

        self.currentImage = None
        self.tableBuffer  = {}
        self.signals      = {}


    def addSignal(self, signal):
        self.signals.update(signal)


    def setImage(self, imageName):
        if type(imageName) is not str:
            imageName = imageName.text()

        self.currentImage = os.path.split(imageName)[1]
        print(self.currentImage)
        if self.currentImage not in self.tableBuffer:
            self.tableBuffer.update([(self.currentImage, [])])


    def append2Table(self, coords):
        if self.currentImage is None or coords is None:
            return

        self.tableBuffer[self.currentImage].append(coords)

        entry = [self.currentImage] + coords
        currentRowCount = self.rowCount()
        self.insertRow(currentRowCount)

        for i in range(len(entry)):
            attribute = str(entry[i])
            self.setItem(currentRowCount, i, QTableWidgetItem(attribute))
