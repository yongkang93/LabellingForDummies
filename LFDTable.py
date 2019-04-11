import os
import modin.pandas as pd

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class LFDTable(QTableWidget):
    def __init__(self, r = 1, c = 6):
        super().__init__(r, c)

        self.csvName          = None
        self.currentImageName = None
        self.tableBuffer      = {}
        self.signals          = {}

        #self.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def addSignal(self, signal):
        self.signals.update(signal)


    def setActiveImageOnTable(self, imageName):
        if type(imageName) is not str:
            imageName = imageName.text()

        self.currentImageName = os.path.split(imageName)[1]

        if self.currentImageName not in self.tableBuffer:
            self.tableBuffer.update([(self.currentImageName, ([], []))])


    def newCSV(self):
        self.csvName, _ = QFileDialog.getSaveFileName(
                          self, 'Save CSV', '',
                          #'All Files (*);;CSV Files (*.csv)')
                          'CSV Files (*.csv)')


    def openCSV(self):
        options = QFileDialog.Options()
        self.csvName, _ = QFileDialog.getOpenFileName(
                          self, 'Open CSV', '',
                          'CSV Files (*.csv)', options = options)

        # return if user closes the file dialog without selecting a csv file
        if self.csvName is '':
            return

        df = pd.read_csv(self.csvName, index_col = 0)
        for index, row in df.iterrows():
            entry = list(row)
            self.insertEntry(entry)


    def saveCSV(self):
        if self.csvName is None:
            self.saveCSVas()
        else:
            self.save()


    def saveCSVas(self):
        self.newCSV()
        self.save()


    def save(self):
        rows = self.rowCount()
        cols = self.columnCount()
        
        labels = []
        # get row 0 as column name for DataFrame
        for col in range(cols):
            attribute = self.item(0, col)
            if attribute is None:
                labels.append('Unnamed Column')
            else:
                labels.append(attribute.text())

        entries = []
        # skipping row 0 as it is the column name
        for row in range(1, rows):
            entry = []
            for col in range(cols):
                attribute = self.item(row, col)
                if attribute is None:
                    entry.append(None)
                else:
                    entry.append(attribute.text())

            entries.append(entry)

        df = pd.DataFrame.from_records(entries)
        df.columns = labels
        df.to_csv(self.csvName)


    def append2table(self, coords):
        if self.currentImageName is None or coords is None:
            return

        entry = [self.currentImageName] + coords
        self.insertEntry(entry)


    def insertEntry(self, entry):
        currentRowCount = self.rowCount()
        self.insertRow(currentRowCount)

        coords = []
        for i in range(len(entry)):
            coords.append(entry[i])
            attribute = str(entry[i])
            item = QTableWidgetItem(attribute)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.setItem(currentRowCount, i, item)

        imageName = entry[0]
        if imageName not in self.tableBuffer:
            self.tableBuffer.update([(imageName, ([], []))])
        
        self.tableBuffer[imageName][0].append(coords[1:])


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
