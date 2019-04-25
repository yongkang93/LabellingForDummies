import sys

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class LFDLabelKeybinds(QWidget):
    def __init__(self):
        super().__init__()

        self.keybinds = {}
        self.signals  = {}
        self.initializeWindow()


    def initializeWindow(self):
        form = QFormLayout()

        form.addRow('Keys', QLabel('Labels'))

        for i in range(1, 11):
            self.keybinds.update([(str(i), QLineEdit())])
            self.keybinds[str(i)].textChanged.connect(self.updateLabelKeybind)
            form.addRow(str(i % 10), self.keybinds[str(i)])

        self.setLayout(form)
        self.setWindowTitle('LFD Label Keybinding')


    def lateInitialize(self):
        self.signals['updateLabelKeybinds'].emit(self.keybinds)


    def addSignals(self, signal):
        self.signals.update(signal)


    def updateLabelKeybind(self, label):
       self.signals['updateLabelKeybinds'].emit(self.keybinds)
