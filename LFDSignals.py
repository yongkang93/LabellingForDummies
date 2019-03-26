from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class LFDSignals(QObject):
    csv2table                      = pyqtSignal(str)
    setActiveImageOnTable          = pyqtSignal(str)
    setActiveImageOnImagePanel     = pyqtSignal(str)

    coord2table                    = pyqtSignal(list)