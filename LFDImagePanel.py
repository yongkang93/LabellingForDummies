from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon, QPixmap
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

rect1 = []   # Start position of label
rect2 = []   # End position of label

class LFDImagePanel(QWidget):
    def __init__(self):
        super().__init__()

        self.filename = None
        self.signals  = {}

        self.begin    = QtCore.QPoint()
        self.end      = QtCore.QPoint()


    def addSignal(self, signal):
        self.signals.update(signal)


    def setImage(self, imageName):
        if type(imageName) is str:
            self.filename = imageName
        else:
            self.filename = imageName.text()

        self.update()


    # Get initial position
    def mousePressEvent(self, event):
        self.setFocus()
        w = self.geometry().width()
        h = self.geometry().height()

        self.begin = event.pos()
        self.end = event.pos()

        # Add position if list is empty
        if (len(rect1)<=0):
            rect1.append(event.pos())
        else:
            removed_file = False
            for i in range(0, len(rect1)):
                # Check if the place you click is inside the labelled rectangle

                """BUG HERE, STARTING POSITION MAYBE BIGGER THAN ENDING POSTION"""
                if (rect1[i].x() < event.pos().x() < rect2[i].x()) and (rect1[i].y() < event.pos().y() < rect2[i].y()):
                    # Remove entry if in labelled rectangle
                    rect1.pop(i)
                    rect2.pop(i)
                    removed_file = True
                    break

            # Add starting position of label
            if not removed_file:
                rect1.append(event.pos())

        self.update()


    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()


   #Get end position
    def mouseReleaseEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        
        # Add end position only if starting position present
        if len(rect1)>0:
            rect2.append(event.pos())
        self.update()
        
        #print("Starting Coordinates: X = %d Y=%d"%(rect1[-1].x(), rect1[-1].y()))
        #print("Ending Coordinates: X = %d Y=%d"%(rect2[-1].x(), rect2[-1].y()))
        coord = [rect1[-1].x(), rect1[-1].y(), rect2[-1].x(), rect2[-1].y()]
        self.signals['coord2table'].emit(coord)


    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        
        #get image
        pixmap = QPixmap(self.filename)
        qp.drawPixmap(self.rect(), pixmap)

        #brush colour
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
        qp.setBrush(br)

        qp.drawRect(QtCore.QRect(self.begin, self.end))

        #Draw a permanent rectangle on canvas that you paint/drag
        for i in range(0,len(rect1)):
            if len(rect2) > i:
                qp.drawRect(rect1[i].x(),rect1[i].y(),rect2[i].x()-rect1[i].x(),rect2[i].y()-rect1[i].y())
