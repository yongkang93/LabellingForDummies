from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

class LFDTable(QTableWidget):
    def __init__(self, r=20, c=5):
        super().__init__(r, c)
