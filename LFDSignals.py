from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class LFDSignals(QObject):
    ''' LFDTable Signals '''
    updateImageCoordinates         = pyqtSignal(list)


    ''' LFDFileList Signals '''
    setActiveImageOnTable          = pyqtSignal(str)
    setActiveImageOnImagePanel     = pyqtSignal(str)


    ''' LFDImagePanel Signals '''
    deleteTableCoordinates         = pyqtSignal(int)
    retrieveImageCoordinates       = pyqtSignal(str)
    append2table                   = pyqtSignal(list)


    ''' LFDLabelKeybind Signals '''
    updateLabelKeybinds            = pyqtSignal(dict)
