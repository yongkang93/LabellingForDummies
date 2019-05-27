import os

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class LFDImagePanel(QWidget):
    def __init__(self):
        super().__init__()

        self.XMIN = 5
        self.YMIN = 5

        self.startPoint           = QPoint()
        self.endPoint             = QPoint()

        self.currentImage         = None
        self.currentImageName     = None
        self.currentImageWidth    = None
        self.currentImageHeight   = None

        self.currentLabelState    = None

        # TODO: (High Priority)
        # change to state design pattern
        # (i.e. self.states = self.LFDStates(1))
        self.isDeleting           = False
        self.isDrawing            = False


        self.startRelativeCoords  = []
        self.endRelativeCoords    = []

        self.keybinds             = {}
        self.signals              = {}


    def addSignal(self, signal):
        self.signals.update(signal)


    def setActiveImageOnImagePanel(self, imageName):
        if type(imageName) is str:
            self.currentImageName = imageName
        else:
            self.currentImageName = imageName.text()

        self.currentImage       = QPixmap(self.currentImageName)
        self.currentImageWidth  = self.currentImage.size().width()
        self.currentImageHeight = self.currentImage.size().height()

        imageName = os.path.split(self.currentImageName)[1]
        self.signals['retrieveImageCoordinates'].emit(imageName)
        self.update()


    def updateImageCoordinates(self, coords):
        self.startRelativeCoords.clear()
        self.endRelativeCoords.clear()

        for i in range(len(coords)):
            startWindowCoordX = (coords[i][0] / self.currentImageWidth)
            startWindowCoordY = (coords[i][1] / self.currentImageHeight)
            endWindowCoordX   = (coords[i][2] / self.currentImageWidth)
            endWindowCoordY   = (coords[i][3] / self.currentImageHeight)

            self.startRelativeCoords.append([startWindowCoordX, startWindowCoordY])
            self.endRelativeCoords.append([endWindowCoordX, endWindowCoordY])

        self.update()


    def updateLabelKeybinds(self, keybinds):
        self.keybinds = keybinds


    def setActiveLabelState(self, state):
        self.currentLabelState = state


    def mousePressEvent(self, event):
        if self.currentImage is None:
            return

        self.isDrawing  = True
        self.startPoint = event.pos()
        self.endPoint   = event.pos()

        startPointX = self.startPoint.x() / self.geometry().width()
        startPointY = self.startPoint.y() / self.geometry().height()

        if self.isDeleting is True:
            for i in range(len(self.startRelativeCoords)):
                xCoords = sorted([(self.startRelativeCoords[i][0]),
                                  (self.endRelativeCoords[i][0])])
                yCoords = sorted([(self.startRelativeCoords[i][1]),
                                  (self.endRelativeCoords[i][1])])

                # verify if clicked position is within a bounding box
                if (xCoords[0] < startPointX < xCoords[1]) and \
                   (yCoords[0] < startPointY < yCoords[1]) and self.isDeleting == True:
                   self.startRelativeCoords.pop(i)
                   self.endRelativeCoords.pop(i)

                   self.signals['deleteTableCoordinates'].emit(i)
                   return
        else:
            self.startRelativeCoords.append([startPointX, startPointY])

        self.update()


    def mouseMoveEvent(self, event):
        if self.currentImage is None:
            return

        self.setFocus()
        self.endPoint = event.pos()
        self.update()


    def mouseReleaseEvent(self, event):
        if self.currentImage is None:
            return

        # reject drawing of bounding boxes that are too small
        if self.isDeleting is False and \
           (abs(event.pos().x() - self.startPoint.x()) <= self.XMIN or \
            abs(event.pos().y() - self.startPoint.y()) <= self.YMIN):
            self.startRelativeCoords.pop()
            return

        self.isDrawing  = False
        self.startPoint = event.pos()
        self.endPoint   = event.pos()

        endPointX = self.endPoint.x() / self.geometry().width()
        endPointY = self.endPoint.y() / self.geometry().height()

        if len(self.startRelativeCoords) > len(self.endRelativeCoords):
            self.endRelativeCoords.append([endPointX,endPointY])

        if self.isDeleting is False:
            # sort the coordinate s.t. it is arranged as xMin, xMax, yMin, yMax
            xCoords = sorted([(self.startRelativeCoords[-1][0]),
                                  (self.endRelativeCoords[-1][0])])
            yCoords = sorted([(self.startRelativeCoords[-1][1]),
                                  (self.endRelativeCoords[-1][1])])

            if self.currentLabelState is None:
                coords = [int(xCoords[0] * self.currentImageWidth) ,
                          int(yCoords[0] * self.currentImageHeight),
                          int(xCoords[1] * self.currentImageWidth) ,
                          int(yCoords[1] * self.currentImageHeight), '']
            else:
                coords = [int(xCoords[0] * self.currentImageWidth) ,
                          int(yCoords[0] * self.currentImageHeight),
                          int(xCoords[1] * self.currentImageWidth) ,
                          int(yCoords[1] * self.currentImageHeight),
                          str(self.keybinds[str(self.currentLabelState)].text())]

            self.signals['append2table'].emit(coords)

        self.update()


    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier and event.key() == Qt.Key_D:
            self.isDeleting = True

        if event.key() == Qt.Key_1:
            self.currentLabelState = 1
        elif event.key() == Qt.Key_2:
            self.currentLabelState = 2
        elif event.key() == Qt.Key_3:
            self.currentLabelState = 3
        elif event.key() == Qt.Key_4:
            self.currentLabelState = 4
        elif event.key() == Qt.Key_5:
            self.currentLabelState = 5
        elif event.key() == Qt.Key_6:
            self.currentLabelState = 6
        elif event.key() == Qt.Key_7:
            self.currentLabelState = 7
        elif event.key() == Qt.Key_8:
            self.currentLabelState = 8
        elif event.key() == Qt.Key_9:
            self.currentLabelState = 9
        elif event.key() == Qt.Key_0:
            self.currentLabelState = 0


    def keyReleaseEvent(self, event):
        if event.modifiers() != Qt.ShiftModifier or event.key() == Qt.Key_D:
            self.isDeleting = False


    def paintEvent(self, event):
        if self.currentImage is None:
            return

        qPainter = QPainter(self)
        qBrush   = QBrush(QColor(100, 10, 10, 40))

        qPainter.drawPixmap(self.rect(), self.currentImage)
        qPainter.setBrush(qBrush)


        # reject drawing of bounding boxes that are too small
        if self.isDrawing is True and \
           abs(self.endPoint.x() - self.startPoint.x()) > self.XMIN and \
           abs(self.endPoint.y() - self.startPoint.y()) > self.YMIN:
                qPainter.drawRect(QRect(self.startPoint, self.endPoint))

        for i in range(len(self.startRelativeCoords)):
            if len(self.endRelativeCoords) > i:
                qPainter.drawRect(self.startRelativeCoords[i][0] * self.geometry().width(),
                                  self.startRelativeCoords[i][1] * self.geometry().height(),
                                  (self.endRelativeCoords[i][0]  - self.startRelativeCoords[i][0]) *
                                  self.geometry().width(),
                                  (self.endRelativeCoords[i][1]  - self.startRelativeCoords[i][1]) *
                                  self.geometry().height())
