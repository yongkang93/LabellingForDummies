import os
import pandas as pd

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

        self.initialize()


    def initialize(self):
        imageItem = QTableWidgetItem('image')
        imageItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        xMinItem = QTableWidgetItem('xMin')
        xMinItem.setFlags(Qt.ItemIsSelectable  | Qt.ItemIsEnabled)
        yMinItem = QTableWidgetItem('yMin')
        yMinItem.setFlags(Qt.ItemIsSelectable  | Qt.ItemIsEnabled)
        xMaxItem = QTableWidgetItem('xMax')
        xMaxItem.setFlags(Qt.ItemIsSelectable  | Qt.ItemIsEnabled)
        yMaxItem = QTableWidgetItem('yMax')
        yMaxItem.setFlags(Qt.ItemIsSelectable  | Qt.ItemIsEnabled)
        labelItem = QTableWidgetItem('label')
        labelItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.setItem(0, 0, imageItem)
        self.setItem(0, 1, xMinItem)
        self.setItem(0, 2, yMinItem)
        self.setItem(0, 3, xMaxItem)
        self.setItem(0, 4, yMaxItem)
        self.setItem(0, 5, labelItem)


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

        #df = pd.read_csv(self.csvName, index_col = 0)
        df = pd.read_csv(self.csvName)
        for index, row in df.iterrows():
            entry = list(row)
            self.insertEntry(entry)


    def saveCSV(self):
        # if there is no selected csv file to save to
        if self.csvName is None or self.csvName is '':
            self.saveCSVas()
        else:
            self.save()


    def saveCSVas(self):
        self.newCSV()

        # if there is no selected csv file to save to
        if self.csvName is None or self.csvName is '':
            return

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

        df = pd.DataFrame.from_records(entries, columns=labels)
        df = df.set_index('image')
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

            # disable editing of cell for everything except label column
            if i is not len(entry) - 1:
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

        # check if image bounding box information already exists
        if imageName in self.tableBuffer:
            coords = self.tableBuffer[imageName][0]

        self.signals['updateImageCoordinates'].emit(coords)


    def undo(self):
        if len(self.tableBuffer) is 0:
            return 

        if len(self.tableBuffer[self.currentImageName][0]) is 0:
            return

        coords = self.tableBuffer[self.currentImageName][0].pop()
        self.tableBuffer[self.currentImageName][1].append(coords)

        undoEntryRow = self.findItems(self.currentImageName, Qt.MatchExactly)[-1].row()
        self.removeRow(undoEntryRow)

        self.signals['updateImageCoordinates'].emit(self.tableBuffer[self.currentImageName][0])


    def redo(self):
        if len(self.tableBuffer) is 0:
            return 

        if len(self.tableBuffer[self.currentImageName][1]) is 0:
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


    def keyPressEvent(self, event):
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
