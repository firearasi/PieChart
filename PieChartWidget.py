from PySide2.QtWidgets import QTableView, QSplitter, QWidget, QPushButton, QGridLayout
from PySide2.QtWidgets import QMessageBox, QFileDialog
from PySide2 import QtWidgets
from PySide2.QtCore import QFile, QDataStream, QIODevice, Qt

from PyChartDataModel import PieChartDataModel
from PlotCanvas import PlotCanvas

from SpinBoxDelegate import SpinBoxDelegate

class PieChartWidget(QWidget): 
    needSave = False
    fileName = None
    def __init__(self,  parent = None):
        super(PieChartWidget, self).__init__(parent)
        self.title = 'PyQt5 matplotlib PieChart'
        self.width = 1500
        self.height = 600
        self.left = (1920-self.width)/2
        self.top = (1080-self.height)/2
     
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        layout=QGridLayout()
        splitter = QSplitter(self)
        self.myModel = PieChartDataModel(
            labels=['Frogs', 'Hogs', 'Dogs', 'Logs'],
            data=[22, 30, 45, 10],
            explodes=[0, 0, 10, 0])
        self.myModel.dataChanged.connect(self.dataChangedSlot)
        self.table = QTableView(self)
        self.table.setModel(self.myModel)
        self.delegate=SpinBoxDelegate()
        self.table.setItemDelegate(self.delegate)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch);
       
        splitter.addWidget(self.table)
        self.canvas = PlotCanvas(self.myModel, width=5, height=4, parent = self)
        splitter.addWidget(self.canvas)
        
        layout.addWidget(splitter,0,0,5,12)
        
        appendButton=QPushButton('追加',self)
        appendButton.clicked.connect(self.append)
        layout.addWidget(appendButton,5,0)
        
        insertButton=QPushButton('插入',self)
        insertButton.clicked.connect(self.insert)
        layout.addWidget(insertButton,5,1)
        
        removeButton=QPushButton('删除',self)
        removeButton.clicked.connect(self.removeSth)
        layout.addWidget(removeButton,5,3)
        
        self.setLayout(layout)
        
    def append(self):
        self.myModel.insertRow(self.myModel.rowCount())         
        return

    def insert(self):
        select = self.table.selectionModel().selectedIndexes()
        index = select[0].row() if len(select)>0 else 0
        self.myModel.insertRow(index)
        return
    
    def removeSth(self):
        select = self.table.selectionModel().selectedIndexes()
        selectedRows = [index.row() for index in select]
        for row in reversed(selectedRows):
            self.myModel.removeRow(row)
        return
        
    def closeEvent(self, event):
        if not self.needSave:
            event.accept()
            return
        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save);
        ret = msgBox.exec()
        if ret == QMessageBox.Discard:
            event.accept()
            self.parent().closeEvent(event)
        elif ret == QMessageBox.Save:
            if self.save():
                event.accept()
                self.parent().closeEvent(event)
            else:
                event.ignore()
        else:
            event.ignore()
    
    def save(self):
        if self.fileName is None:
            return self.saveAs()
        print('Saving to {}'.format(self.fileName))
        self.dataSavedSlot()
        self.parent().setWindowTitle(self.fileName)
        file = QFile(self.fileName)
        if not file.open(QIODevice.WriteOnly):
            QMessageBox.information(self, "Unable to open file",
                file.errorString())
            return False
        out = QDataStream(file)
        out.setVersion(QDataStream.Qt_4_5)
        out.writeInt32(self.myModel.rowCount())
        for i in  range(self.myModel.rowCount()):
            out.writeQString(self.myModel.data(self.myModel.index(i, 0), Qt.DisplayRole))
            out.writeFloat(self.myModel.data(self.myModel.index(i, 1), Qt.DisplayRole))
            out.writeFloat(self.myModel.data(self.myModel.index(i, 2), Qt.DisplayRole))
            
        return True
        
        
    def saveAs(self):
        fileName = QFileDialog.getSaveFileName(self,
        "Save PieChart Data", self.parent().windowTitle(),
        "PieChart Data (*.pct);;All Files (*)");
        print('filename is ', fileName[0])
        if fileName is not None and fileName[0]!='':
            self.fileName = fileName[0]
            return self.save()
        return False
    
    def open(self):
        #check if need save
        if self.needSave:
            msgBox = QMessageBox()
            msgBox.setText("The document has been modified.")
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Save);
            ret = msgBox.exec()
            if ret == QMessageBox.Save:
                self.save()
                
        fileName = QFileDialog.getOpenFileName(self,
                "Open PieChart Data", "",
                "PieChart Data (*.pct);;All Files (*)");
       
        if fileName is not None and fileName[0] != '':
            print('Opening  ', fileName[0])
            file = QFile(fileName[0])
            if not file.open(QIODevice.ReadOnly):
                QMessageBox.information(self, "Unable to open file",
                    file.errorString())
                return 
            stream = QDataStream(file)
            stream.setVersion(QDataStream.Qt_4_5)
            rows = stream.readInt32()
            label = []
            amount = []
            explodes = []
            
            for i in range(rows):
                label.append(stream.readQString())
                amount.append(stream.readFloat())
                explodes.append(stream.readFloat())
            self.myModel = PieChartDataModel(
                label,
                amount,
                explodes)
            self.myModel.dataChanged.connect(self.dataChangedSlot)
            self.table.setModel(self.myModel)
            self.canvas.setModel(self.myModel)
            self.fileName = fileName[0]
            self.parent().setWindowTitle(self.fileName)
    
    def dataSavedSlot(self):
        self.needSave = False
        
    def dataChangedSlot(self):
        self.needSave = True
