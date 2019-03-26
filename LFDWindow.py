import sys

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

from LFDTable      import LFDTable
from LFDFileList   import LFDFileList
from LFDImagePanel import LFDImagePanel
from LFDSignals    import LFDSignals


class LFDWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.mainWindow  = None

        self.tableDock   = None
        self.listDock    = None
        self.imageDock   = None

        self.tableWidget = None
        self.listWidget  = None
        self.imageWidget = None

        self.signals     = None

        self.initializeWindow()
        self.initializeMenuBar()
        self.initializeDockable()
        self.initializeCommunication()
        self.show()


    def initializeWindow(self):
        self.setWindowTitle('Labelling for Dummies')
        self.setGeometry(0, 0, 700, 700)

        self.imageWidget = LFDImagePanel()
        self.mainWindow  = QVBoxLayout()
        self.mainWindow.addWidget(self.imageWidget)
        self.setCentralWidget(self.imageWidget)


    def initializeMenuBar(self):
        menuBar = self.menuBar()
        if sys.platform != 'darwin':
            menuBar.setNativeMenuBar(False)
        file_menu = menuBar.addMenu('&File')

        ''' creating and connecting buttons with functions '''
        sample_action = QAction('&Sample Button 01', self)
        sample_action.setShortcut('Ctrl+W')
        sample_action.triggered.connect(self.sampleButton01Action)

        new_csv_action = QAction('&New CSV', self)
        new_csv_action.setShortcut('Ctrl+N')
        new_csv_action.triggered.connect(self.newCSV)

        open_csv_action = QAction('&Open CSV', self)
        open_csv_action.setShortcut('Ctrl+O')
        open_csv_action.triggered.connect(self.openCSV)

        save_csv_action = QAction('&Save CSV', self)
        save_csv_action.setShortcut('Ctrl+S')
        save_csv_action.triggered.connect(self.saveCSV)

        save_csv_as_action = QAction('&Save CSV as...', self)
        save_csv_as_action.setShortcut('Shift+Ctrl+S')
        save_csv_as_action.triggered.connect(self.saveCSVas)
        
        open_image_action = QAction('&Open Image', self)
        open_image_action.setShortcut('Ctrl+I')
        open_image_action.triggered.connect(self.openImage)

        open_directory_action = QAction('&Open Image Directory', self)
        open_directory_action.setShortcut('Ctrl+D')
        open_directory_action.triggered.connect(self.openImageDirectory)

        ''' formatting layout of menu buttons '''
        file_menu.addAction(sample_action)
        file_menu.addSeparator()
        file_menu.addAction(new_csv_action)
        file_menu.addAction(open_csv_action)
        file_menu.addSeparator()
        file_menu.addAction(save_csv_action)
        file_menu.addAction(save_csv_as_action)
        file_menu.addSeparator()
        file_menu.addAction(open_image_action)
        file_menu.addAction(open_directory_action)


    def initializeDockable(self):
        ''' creating widget objects '''
        self.tableWidget = LFDTable()
        self.listWidget  = LFDFileList() 

        ''' creating and setting dockable windows with widget '''
        self.tableDock = QDockWidget('LFD Table', self)
        self.tableDock.setFeatures(QDockWidget.DockWidgetMovable)
        self.tableDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.tableDock.setWidget(self.tableWidget)

        self.listDock = QDockWidget('LFD File List', self)
        self.listDock.setFeatures(QDockWidget.DockWidgetMovable)
        self.listDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.listDock.setWidget(self.listWidget)

        ''' formatting initial layout of dockable windows '''
        self.addDockWidget(Qt.LeftDockWidgetArea, self.tableDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.listDock)


    def initializeCommunication(self):
        self.signals = LFDSignals()

        ''' self.signals.<LFDSignal VARIABLE>[FUNC INPUT TYPE].connect(self.<LFDTable/FileList/ImagePanel>.FUNC) '''
        self.signals.setActiveImageOnTable[str].connect(self.tableWidget.setImage)
        self.listWidget.addSignal([('setActiveImageOnTable', self.signals.setActiveImageOnTable)])

        self.signals.setActiveImageOnImagePanel[str].connect(self.imageWidget.setImage)
        self.listWidget.addSignal([('setActiveImageOnImagePanel', self.signals.setActiveImageOnImagePanel)])

        self.signals.coord2table[list].connect(self.tableWidget.append2Table)
        self.imageWidget.addSignal([('coord2table', self.signals.coord2table)])

        self.listWidget.currentItemChanged.connect(self.tableWidget.setImage)
        self.listWidget.currentItemChanged.connect(self.imageWidget.setImage)


    def sampleButton01Action(self):
        print('SampleButton01Action')


    def newCSV(self):
        print('newCSV')


    def openCSV(self):
        print('openCSV')


    def saveCSV(self):
        print('saveCSV')


    def saveCSVas(self):
        print('saveCSVas')


    def openImage(self):
        self.listWidget.openImage()


    def openImageDirectory(self):
        print('openImageDirectory')


app = QApplication(sys.argv)
LFDWin = LFDWindow()
sys.exit(app.exec_())
