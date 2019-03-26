import sys 

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class LFDFileList(QListWidget):
    def __init__(self):
        super().__init__()
        
        self.fileList = []
        self.signals  = {}


    def addSignal(self, signal):
        self.signals.update(signal)


    def openImage(self):
        options = QFileDialog.Options()
        #if sys.platform != 'darwin': 
        #    options |= QFileDialog.DontUseNativeDialog
        imageName, _ = QFileDialog.getOpenFileName(
                      None, "QFileDialog.getOpenFileName()", "",
                      "All Files (*);;Python Files (*.py)", options=options)

        ''' prevent displaying of duplicate items '''
        if imageName not in self.fileList:
            self.addItem(imageName)
            self.setCurrentRow(len(self.fileList))
            self.fileList.append(imageName)
        else:
            itemIndex = self.fileList.index(imageName)
            self.setCurrentRow(itemIndex)

        self.signals['setActiveImageOnTable'].emit(imageName)
        self.signals['setActiveImageOnImagePanel'].emit(imageName)
