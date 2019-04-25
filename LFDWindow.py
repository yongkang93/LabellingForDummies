import sys

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

from LFDTable         import LFDTable
from LFDFileList      import LFDFileList
from LFDImagePanel    import LFDImagePanel
from LFDLabelKeybinds import LFDLabelKeybinds
from LFDSignals       import LFDSignals


class LFDWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.mainWindow    = None

        self.tableDock     = None
        self.listDock      = None
        self.imageDock     = None

        self.tableWidget   = None
        self.listWidget    = None
        self.imageWidget   = None

        self.keybindWindow = None

        self.signals       = None

        self.initializeWindow()
        self.initializeMenuBar()
        self.initializeDockable()
        self.initializeCommunication()
        self.lateInitialize()
        self.show()


    def initializeWindow(self):
        self.setWindowTitle('Labelling for Dummies')
        self.setGeometry(0, 0, 700, 700)
        self.statusBar().showMessage('Labelling for Dummies - Future of Labelling Starts Today')

        self.imageWidget = LFDImagePanel()
        self.mainWindow  = QVBoxLayout()
        self.mainWindow.addWidget(self.imageWidget)
        self.setCentralWidget(self.imageWidget)

        self.keybindWindow = LFDLabelKeybinds()


    def initializeMenuBar(self):
        menuBar = self.menuBar()
        if sys.platform != 'darwin':
            menuBar.setNativeMenuBar(False)

        file_menu    = menuBar.addMenu('&File')
        edit_menu    = menuBar.addMenu('&Edit')

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

        undo_action = QAction('&Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.undo)

        redo_action = QAction('&Redo', self)
        redo_action.setShortcut('Shift+Ctrl+Z')
        redo_action.triggered.connect(self.redo)

        show_keybind_action = QAction('&Keybinds', self)
        show_keybind_action.setShortcut('Ctrl+K')
        show_keybind_action.triggered.connect(self.openKeybinding)

        ''' formatting layout of file buttons '''
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

        ''' formatting layout of edit buttons '''
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(show_keybind_action)


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

        ''' LFDTable Signals '''
        self.signals.updateImageCoordinates[list].connect(self.imageWidget.updateImageCoordinates)
        self.tableWidget.addSignal([('updateImageCoordinates', self.signals.updateImageCoordinates)])


        ''' LFDFileList Signals '''
        self.signals.setActiveImageOnTable[str].connect(self.tableWidget.setActiveImageOnTable)
        self.listWidget.addSignal([('setActiveImageOnTable', self.signals.setActiveImageOnTable)])

        self.signals.setActiveImageOnImagePanel[str].connect(self.imageWidget.setActiveImageOnImagePanel)
        self.listWidget.addSignal([('setActiveImageOnImagePanel', self.signals.setActiveImageOnImagePanel)])


        ''' LFDImagePanel Signals '''
        self.signals.deleteTableCoordinates[int].connect(self.tableWidget.deleteTableCoordinates)
        self.imageWidget.addSignal([('deleteTableCoordinates', self.signals.deleteTableCoordinates)])

        self.signals.retrieveImageCoordinates[str].connect(self.tableWidget.retrieveImageCoordinates)
        self.imageWidget.addSignal([('retrieveImageCoordinates', self.signals.retrieveImageCoordinates)])

        self.signals.append2table[list].connect(self.tableWidget.append2table)
        self.imageWidget.addSignal([('append2table', self.signals.append2table)])


        ''' LFDLabelKeybinds Signals '''
        self.signals.updateLabelKeybinds[dict].connect(self.imageWidget.updateLabelKeybinds)
        self.keybindWindow.addSignals([('updateLabelKeybinds', self.signals.updateLabelKeybinds)])


        ''' PyQt5 Built-In Signals '''
        self.listWidget.currentItemChanged.connect(self.tableWidget.setActiveImageOnTable)
        self.listWidget.currentItemChanged.connect(self.imageWidget.setActiveImageOnImagePanel)


    def lateInitialize(self):
        self.keybindWindow.lateInitialize()


    def sampleButton01Action(self):
        print('SampleButton01Action')


    def newCSV(self):
        self.tableWidget.newCSV()


    def openCSV(self):
        self.tableWidget.openCSV()


    def saveCSV(self):
        self.tableWidget.saveCSV()


    def saveCSVas(self):
        self.tableWidget.saveCSVas()


    def openImage(self):
        self.listWidget.openImage()


    def openImageDirectory(self):
        self.listWidget.openImageDirectory()


    def undo(self):
        self.tableWidget.undo()


    def redo(self):
        self.tableWidget.redo()


    def openKeybinding(self):
        self.keybindWindow.show()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            self.currentLabelState = 1
            print('1')
        elif event.key() == Qt.Key_2:
            self.currentLabelState = 2
            print('2')
        elif event.key() == Qt.Key_3:
            self.currentLabelState = 3
            print('3')
        elif event.key() == Qt.Key_4:
            self.currentLabelState = 4
            print('4')
        elif event.key() == Qt.Key_5:
            self.currentLabelState = 5
            print('5')
        elif event.key() == Qt.Key_6:
            self.currentLabelState = 6
            print('6')
        elif event.key() == Qt.Key_7:
            self.currentLabelState = 7
            print('7')
        elif event.key() == Qt.Key_8:
            self.currentLabelState = 8
            print('8')
        elif event.key() == Qt.Key_9:
            self.currentLabelState = 9
            print('9')
        elif event.key() == Qt.Key_0:
            self.currentLabelState = 0
            print('0')

        #if event.key() == Qt.Key_Up:
        #    self.listWidget.setSelectedItem('UP')
        
        #if event.key() == Qt.Key_Down:
        #    self.listWidget.setSelectedItem('DOWN')


app = QApplication(sys.argv)
LFDWin = LFDWindow()
sys.exit(app.exec_())
