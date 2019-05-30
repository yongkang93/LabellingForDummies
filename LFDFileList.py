import os
import sys

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class LFDFileList(QListWidget):
    def __init__(self):
        super().__init__()

        self.imageDirectory = None
        self.fileList = []
        self.signals  = {}


    def addSignal(self, signal):
        self.signals.update(signal)


    def openImage(self):
        options = QFileDialog.Options()
        #if sys.platform != 'darwin':
        #    options |= QFileDialog.DontUseNativeDialog
        fullImageName, _ = QFileDialog.getOpenFileName(
                       None, 'Open Image', '',
                       'JPEG Files (*.jpg);;PNG Files (*.png)',
                       options=options)

        # return if user closes the file dialog without selecting an image
        if fullImageName is '':
            return

        self.insertEntry(fullImageName)

        self.signals['setActiveImageOnTable'].emit(fullImageName)
        self.signals['setActiveImageOnImagePanel'].emit(fullImageName)


    def openImageDirectory(self):
        self.imageDirectory = QFileDialog.getExistingDirectory(
                              None, 'Select Image Folder', '',
                              QFileDialog.ShowDirsOnly)

        if self.imageDirectory is '':
            return

        self.get_images(self.imageDirectory)


    def get_images(self, path):
        accepted_format = ['.jpg', 'jpeg', '.png']

        for file in os.listdir(path):
            fullImageName = os.path.join(path, file)
            if os.path.splitext(fullImageName)[1] in accepted_format:
                self.insertEntry(fullImageName, False)


    def insertEntry(self, imageName, setCurrentRow = True):
        # prevent displaying of duplicate items
        if imageName not in self.fileList:
            self.addItem(imageName)

            if setCurrentRow is True:
                self.setCurrentRow(len(self.fileList))

            self.fileList.append(imageName)
        else:
            itemIndex = self.fileList.index(imageName)
            self.setCurrentRow(itemIndex)


    def setSelectedItem(self, direction):
        if len(self.fileList) is 0:
            return

        if direction is 0:
            currentSelection = self.currentItem()
            itemIndex = self.fileList.index(currentSelection.text())
            if itemIndex is not 0:
                itemIndex -= 1
                self.setCurrentRow(itemIndex)

        if direction is 1:
            currentSelection = self.currentItem()
            itemIndex = self.fileList.index(currentSelection.text())
            if itemIndex is not len(self.fileList) - 1:
                itemIndex += 1
                self.setCurrentRow(itemIndex)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            currentSelection = self.currentItem()
            itemIndex = self.fileList.index(currentSelection.text())
            if itemIndex is not 0:
                itemIndex -= 1
                self.setCurrentRow(itemIndex)
        if event.key() == Qt.Key_Down:
            currentSelection = self.currentItem()
            itemIndex = self.fileList.index(currentSelection.text())
            if itemIndex is not len(self.fileList) - 1:
                itemIndex += 1
                self.setCurrentRow(itemIndex)
        if event.key() == Qt.Key_1:
            self.currentLabelState = 1
            self.signals['setActiveLabelState'].emit(self.currentLabelState)
        elif event.key() == Qt.Key_2:
            self.currentLabelState = 2
            self.signals['setActiveLabelState'].emit(self.currentLabelState)
        elif event.key() == Qt.Key_3:
            self.currentLabelState = 3
            self.signals['setActiveLabelState'].emit(self.currentLabelState)
        elif event.key() == Qt.Key_4:
            self.currentLabelState = 4
            self.signals['setActiveLabelState'].emit(self.currentLabelState)
        elif event.key() == Qt.Key_5:
            self.currentLabelState = 5
            self.signals['setActiveLabelState'].emit(self.currentLabelState)
        elif event.key() == Qt.Key_6:
            self.currentLabelState = 6
            self.signals['setActiveLabelState'].emit(self.currentLabelState)
        elif event.key() == Qt.Key_7:
            self.currentLabelState = 7
            self.signals['setActiveLabelState'].emit(self.currentLabelState)
        elif event.key() == Qt.Key_8:
            self.currentLabelState = 8
            self.signals['setActiveLabelState'].emit(self.currentLabelState)
        elif event.key() == Qt.Key_9:
            self.currentLabelState = 9
            self.signals['setActiveLabelState'].emit(self.currentLabelState)
        elif event.key() == Qt.Key_0:
            self.currentLabelState = 0
            self.signals['setActiveLabelState'].emit(self.currentLabelState)
