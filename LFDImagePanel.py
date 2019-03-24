from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon, QPixmap
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

rect1 = []   # Start position of label
rect2 = []   # End position of label
filename=""

class LFDImagePanel(QWidget):
    def __init__(self):
        super().__init__()

        """"Choose File to open"""
        self.filename=self.openFile()
        self.button = QPushButton("File")
        self.button.clicked.connect(self.openFile)

        """Initialize"""
        self.title = 'PyQt5 image'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.setWindowTitle('Testing123')

        """Set Menu"""
        chooseAct = QAction(QIcon('choose.png'), '&Choose File', self)
        chooseAct.setShortcut('Ctrl+Q')
        chooseAct.setStatusTip('Choose File')
        chooseAct.triggered.connect(self.openFile)

        """Set drawing rectangle"""
        self.setGeometry(self.left, self.top, self.width, self.height)

        #set points
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()


    def openFile(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;JPG (*.jpg)", options=options)
        self.filename=fileName.split('/')[-1]
        self.update()
        print(filename)
        return self.filename


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
        for i in range(0, len(rect1)):
            print("Starting Coordinates: X = %d Y=%d"%(rect1[i].x(), rect1[i].y()))
            print("Ending Coordinates: X = %d Y=%d"%(rect2[i].x(), rect2[i].y()))


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
