import os

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class LFDImagePanel(QWidget):
    def __init__(self):
        super().__init__()

        self.startPoint           = QPoint()
        self.endPoint             = QPoint()

        self.currentImage         = None
        self.currentImageName     = None
        self.currentImageWidth    = None
        self.currentImageHeight   = None

        self.isDeleting           = False
        self.isDrawing            = False

        self.startRelativeCoords  = []
        self.endRelativeCoords    = []
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

        self.isDrawing  = False
        self.startPoint = event.pos()
        self.endPoint   = event.pos()

        endPointX = self.endPoint.x() / self.geometry().width()
        endPointY = self.endPoint.y() / self.geometry().height()

        if len(self.startRelativeCoords) > len(self.endRelativeCoords):
            self.endRelativeCoords.append([endPointX,endPointY])

        if self.isDeleting is False:
            coords = [int(self.startRelativeCoords[-1][0] * self.currentImageWidth) ,
                      int(self.startRelativeCoords[-1][1] * self.currentImageHeight),
                      int(self.endRelativeCoords[-1][0]   * self.currentImageWidth) ,
                      int(self.endRelativeCoords[-1][1]   * self.currentImageHeight)]

            self.signals['append2table'].emit(coords)

        self.update()


    def keyPressEvent(self, event):
        if Qt.ShiftModifier and event.key() == Qt.Key_D:
            self.isDeleting = True


    def keyReleaseEvent(self, event):
        if Qt.ShiftModifier and event.key() == Qt.Key_D:
            self.isDeleting = False


    def paintEvent(self, event):
        if self.currentImage is None:
            return

        qPainter = QPainter(self)
        qBrush   = QBrush(QColor(100, 10, 10, 40))

        qPainter.drawPixmap(self.rect(), self.currentImage)
        qPainter.setBrush(qBrush)

        if self.isDrawing is True:
            qPainter.drawRect(QRect(self.startPoint, self.endPoint))

        for i in range(len(self.startRelativeCoords)):
            if len(self.endRelativeCoords) > i:
                qPainter.drawRect(self.startRelativeCoords[i][0] * self.geometry().width(),
                            self.startRelativeCoords[i][1] * self.geometry().height(),
                            (self.endRelativeCoords[i][0]  - self.startRelativeCoords[i][0]) *
                            self.geometry().width(),
                            (self.endRelativeCoords[i][1]  - self.startRelativeCoords[i][1]) *
                            self.geometry().height())
