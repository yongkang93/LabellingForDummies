import os

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class LFDTable(QTableWidget):
    def __init__(self, r = 1, c = 6):
        super().__init__(r, c)

        self.currentImageName = None
        self.tableBuffer      = {}
        self.signals          = {}


    def addSignal(self, signal):
        self.signals.update(signal)


    def setActiveImageOnTable(self, imageName):
        if type(imageName) is not str:
            imageName = imageName.text()

        self.currentImageName = os.path.split(imageName)[1]

        if self.currentImageName not in self.tableBuffer:
            self.tableBuffer.update([(self.currentImageName, ([], []))])


    def append2table(self, coords):
        if self.currentImageName is None or coords is None:
            return

        self.tableBuffer[self.currentImageName][0].append(coords)

        entry = [self.currentImageName] + coords
        currentRowCount = self.rowCount()
        self.insertRow(currentRowCount)

        for i in range(len(entry)):
            attribute = str(entry[i])
            self.setItem(currentRowCount, i, QTableWidgetItem(attribute))


    def deleteTableCoordinates(self, index):
        coords = self.tableBuffer[self.currentImageName][0].pop(index)
        self.tableBuffer[self.currentImageName][1].append(coords)

        removeEntryRow = self.findItems(self.currentImageName, Qt.MatchExactly)[index].row()
        self.removeRow(removeEntryRow)


    def retrieveImageCoordinates(self, imageName):
        coords = []
        if imageName in self.tableBuffer:
            coords = self.tableBuffer[imageName][0]

        self.signals['updateImageCoordinates'].emit(coords)


    def undo(self):
        if len(self.tableBuffer) is 0:
            return 

        currentImageUndoBuffer = self.tableBuffer[self.currentImageName][0]
        if len(currentImageUndoBuffer) is 0:
            return

        coords = self.tableBuffer[self.currentImageName][0].pop()
        self.tableBuffer[self.currentImageName][1].append(coords)

        undoEntryRow = self.findItems(self.currentImageName, Qt.MatchExactly)[-1].row()
        self.removeRow(undoEntryRow)

        self.signals['updateImageCoordinates'].emit(self.tableBuffer[self.currentImageName][0])


    def redo(self):
        if len(self.tableBuffer) is 0:
            return 

        currentImageRedoBuffer = self.tableBuffer[self.currentImageName][1]
        if len(currentImageRedoBuffer) is 0:
            return

        coords = self.tableBuffer[self.currentImageName][1].pop()
        self.tableBuffer[self.currentImageName][0].append(coords)

        currentImageEntries = self.findItems(self.currentImageName, Qt.MatchExactly)
        if len(currentImageEntries) is 0:
            redoEntryRow = currentImageLastEntryRow = self.rowCount()
            self.insertRow(redoEntryRow)
        else:
            currentImageLastEntryRow = currentImageEntries[-1].row()
            redoEntryRow = currentImageLastEntryRow + 1
            self.insertRow(redoEntryRow)

        entry = [self.currentImageName] + coords

        for i in range(len(entry)):
            attribute = str(entry[i])
            self.setItem(redoEntryRow, i, QTableWidgetItem(attribute))

        self.signals['updateImageCoordinates'].emit(self.tableBuffer[self.currentImageName][0])
