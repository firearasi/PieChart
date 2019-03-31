from PySide2.QtWidgets import QTableView, QSplitter, QWidget, QPushButton, QGridLayout
from PySide2 import QtWidgets

from PyChartDataModel import PieChartDataModel
from PlotCanvas import PlotCanvas

from SpinBoxDelegate import SpinBoxDelegate

class PieChartWidget(QWidget): 
    def __init__(self):
        super().__init__()
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
        self.table = QTableView(self)
        self.table.setModel(self.myModel)
        self.delegate=SpinBoxDelegate()
        self.table.setItemDelegate(self.delegate)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch);
       
        splitter.addWidget(self.table)
        self.canvas = PlotCanvas(self.myModel, width=5, height=4, parent = self)
        splitter.addWidget(self.canvas)
        
        layout.addWidget(splitter,0,0,5,12)
        
        appendButton=QPushButton('Append',self)
        appendButton.clicked.connect(self.append)
        layout.addWidget(appendButton,5,0)
        
        insertButton=QPushButton('Insert',self)
        insertButton.clicked.connect(self.insert)
        layout.addWidget(insertButton,5,1)
        
        removeButton=QPushButton('Remove',self)
        removeButton.clicked.connect(self.removeSth)
        layout.addWidget(removeButton,5,3)
        
        self.setLayout(layout)
        self.show()
        self.activateWindow() 
    
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
