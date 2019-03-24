import sys

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

from LFDTable     import LFDTable
from LFDFileList  import LFDFileList
from LFDImagePanel import LFDImagePanel

class LFDWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.table_dock = None
        self.list_dock  = None
        self.image_dock = None

        self.table_widget = None
        self.list_widget  = None
        self.image_widget = None

        self.init_gui()


    def init_gui(self):
        self.setWindowTitle('Labelling for Dummies')
        self.setGeometry(0, 0, 700, 700)

        self.table_dock = QDockWidget('LFD Table', self)
        self.table_dock.setFeatures(QDockWidget.DockWidgetMovable)
        self.table_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.table_widget = LFDTable()
        self.table_dock.setWidget(self.table_widget)

        self.list_dock = QDockWidget('LFD File List', self)
        self.list_dock.setFeatures(QDockWidget.DockWidgetMovable)
        self.list_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.list_widget = LFDFileList() 
        self.list_dock.setWidget(self.list_widget)

        self.image_dock = QDockWidget('LFD Draw Panel', self)
        self.image_dock.setFeatures(QDockWidget.DockWidgetMovable)
        self.image_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.image_widget = LFDImagePanel()
        self.image_dock.setWidget(self.image_widget)

        self.addDockWidget(Qt.LeftDockWidgetArea , self.table_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea , self.list_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.image_dock)
        
        self.show()


app = QApplication(sys.argv)
LFDWin = LFDWindow()
sys.exit(app.exec_())
