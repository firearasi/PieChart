from PieChartWidget import PieChartWidget
from PySide2.QtWidgets import QMainWindow, QMdiArea, QAction, QMdiSubWindow
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtCore import Qt
class MainWindow(QMainWindow):
    count = 0
    def __init__(self, viewMode=QMdiArea.SubWindowView, parent = None):
        super(MainWindow, self).__init__(parent)
        self.viewMode = viewMode
        self.setupUi()
        self.setGeometry(200, 100, 1600, 900)
        self.show()
        self.menuAction(QAction('New'))
        self.activateWindow()

        
    def setupUi(self):
        self.mdi = QMdiArea()
        self.mdi.setViewMode(self.viewMode)
        self.setCentralWidget(self.mdi)
        self.menuBar = self.menuBar()
        
        actNew = QAction('New', self)
        actNew.setIcon(QIcon.fromTheme('document-new', QIcon('icons/maia/document-new.svg')))
        actNew.setShortcuts(QKeySequence.New)
        actOpen = QAction('Open...', self)
        actOpen.setIcon(QIcon.fromTheme('document-open', QIcon('icons/maia/document-open.svg')))
        actOpen.setShortcuts(QKeySequence.Open)
        actOpenRecent = QAction('OpenRecent', self)
        actOpenRecent.setIcon(QIcon.fromTheme('document-open-recent', QIcon('icons/maia/document-open-recent.svg')))
        actSave = QAction('Save', self)
        actSave.setShortcuts(QKeySequence.Save)
        actSave.setIcon(QIcon.fromTheme('document-save', QIcon('icons/maia/document-save.svg')))
        actSaveAs = QAction('Save as...', self)
        actSaveAs.setIcon(QIcon.fromTheme('document-save-as', QIcon('icons/maia/document-save-as.svg')))
        actSaveAs.setShortcuts(QKeySequence.SaveAs)
        actSaveAll = QAction('Save all', self)
        actSaveAll.setIcon(QIcon.fromTheme('document-save-all', QIcon('icons/maia/document-save-all.svg')))
        actClose = QAction('Close', self)
        actClose.setIcon(QIcon.fromTheme('document-close', QIcon('icons/maia/document-close.svg')))
        actClose.setShortcuts(QKeySequence.Close)
        actQuit = QAction('Quit', self)
        actQuit.setIcon(QIcon.fromTheme('application-exit'))
        actQuit.setShortcuts(QKeySequence.Quit)
        fileMenu = self.menuBar.addMenu('文件')
        fileMenu.addAction(actNew)
        fileMenu.addSeparator()
        fileMenu.addAction(actOpen)
        fileMenu.addAction(actOpenRecent)
        fileMenu.addSeparator()
        fileMenu.addAction(actSave)
        fileMenu.addAction(actSaveAs)
        fileMenu.addAction(actSaveAll)
        fileMenu.addSeparator()
        fileMenu.addAction(actClose)
        fileMenu.addSeparator()
        fileMenu.addAction(actQuit)
        
        fileMenu.triggered[QAction].connect(self.menuAction)
        windowMenu = self.menuBar.addMenu('窗口')
        windowMenu.addAction('Cascade')
        windowMenu.addAction('Tile')
        
        self.actTabbed = QAction('Tabbed', self)
        self.actTabbed.setCheckable(True)
        self.actTabbed.setChecked(self.viewMode == QMdiArea.TabbedView)
        windowMenu.addAction(self.actTabbed)
        windowMenu.triggered[QAction].connect(self.menuAction)
        
        tb = self.addToolBar('File')
        tb.addAction(actNew)
        tb.addSeparator()
        tb.addAction(actOpen)
        tb.addAction(actSave)
        tb.addAction(actSaveAs)
        tb.addSeparator()
        tb.addAction(actClose)
        
        
        self.statusBar()
        
    def menuAction(self,act):
        print(act.text())
        if act.text() == 'New':
            self.count += 1
            sub = QMdiSubWindow(self.mdi)
            sub.setBaseSize(800, 400)
            sub.setAttribute(Qt.WA_DeleteOnClose);
            pie = PieChartWidget(sub)
            sub.setWidget(pie)
            sub.setWindowTitle('Untitled{}.pct'.format(self.count))
            self.mdi.addSubWindow(sub)
            sub.show()
        
        if act.text() == 'Open...':
            self.mdi.activeSubWindow().widget().open()
        if act.text() == 'Save':
            self.mdi.activeSubWindow().widget().save()
        if act.text() == 'Save as...':
            self.mdi.activeSubWindow().widget().saveAs()
        if act.text() == 'Save all':
            currentActiveSubWindow = self.mdi.activeSubWindow()
            for subWindow in self.mdi.subWindowList():
                self.mdi.setActiveSubWindow(subWindow)
                subWindow.widget().save()
            self.mdi.setActiveSubWindow(currentActiveSubWindow)
        if act.text() == 'Close':
            if self.mdi.currentSubWindow():
                self.mdi.currentSubWindow().close()
        elif act.text() == 'Cascade':
            self.mdi.cascadeSubWindows()
        elif act.text() == 'Tile':
            self.mdi.tileSubWindows()
        elif act.text() == 'Tabbed':
            self.viewMode = QMdiArea.TabbedView if self.actTabbed.isChecked() else QMdiArea.SubWindowView
            self.mdi.setViewMode(self.viewMode)
        elif act.text() == 'Quit':
            self.close()
        
    def closeEvent(self, event):
        print('MainWindow close event')
        for subWindow in self.mdi.subWindowList():
                subWindow.close()
        if len(self.mdi.subWindowList()) == 0:
            event.accept()
        else:
            event.ignore()
        
       
        
            
