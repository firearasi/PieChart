#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 23:44:38 2019

@author: yan
"""

import sys
from PyQt5.QtWidgets import QTableView,QSplitter,QSizePolicy, QApplication, QWidget, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
 
class PieChartDataModel(QtCore.QAbstractTableModel):
    def __init__(self, labels, data, explodes, parent = None):
        super(PieChartDataModel,self).__init__(parent)
        self.columns=3
        self.labels=labels
        self.data=data
        self.explodes=explodes
        
    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.labels)
    def columnCount(self, parent =  QtCore.QModelIndex()):
        return self.columns
    def data(self,index,role=QtCore.Qt.DisplayRole):
        row = index.row()
        column = index.column()
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if row >= self.rowCount() or row < 0 or column >= self.columns or column < 0:
            return QtCore.QVariant();
        if index.column()==0:
            return QtCore.QVariant(self.labels[index.row()])
        elif index.column()==1:
            return QtCore.QVariant(float(self.data[index.row()]))
        elif index.column()==2:
            return QtCore.QVariant(float(self.explodes[index.row()]))
        else:
            return QtCore.QVariant()
    def headerData(self,section,orientation,role):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant();
        if orientation==QtCore.Qt.Horizontal:
            if section == 0:
                return QtCore.QVariant('Labels')
            elif section == 1:
                return QtCore.QVariant('Data')
            elif section == 2:
                return QtCore.QVariant('Explodes')
            else:
                return QtCore.QVariant()
        else:
            return QtCore.QVariant('Item {}'.format(section))
        
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        def toNumber(v):
            try:
                return float(v)
            except:
                return 0
        row = index.row()
        column = index.column()
        if role!=QtCore.Qt.EditRole:
            return False
        if row >= self.rowCount() or row < 0 or column >= self.columns or column < 0:
            return False
        if column == 0:
            self.labels[row] = value
        elif column==1:
            self.data[row] = toNumber(value)
        elif column==2:
            self.explodes[row] = toNumber(value)
        self.dataChanged.emit(index, index, [QtCore.Qt.EditRole, QtCore.Qt.DisplayRole])
        return True
        
    def insertRow(self, row, parent = QtCore.QModelIndex()):
        if row < 0 or row > self.rowCount():
            return
        self.beginInsertRows(parent, row, row);
        self.labels.insert(row, 'Item {}'.format(row))
        self.data.insert(row, 20)
        self.explodes.insert(row, 0)
        self.endInsertRows()
        topLeft = self.index(row, 0)
        bottomRight = self.index(row, 2)
        self.dataChanged.emit(topLeft, 
            bottomRight, 
            [QtCore.Qt.EditRole, QtCore.Qt.DisplayRole])
        return
    
    def flags(self, index):
        flags = super(self.__class__,self).flags(index)
        flags |= QtCore.Qt.ItemIsEditable
        #flags |= QtCore.Qt.ItemIsSelectable
        #flags |= QtCore.Qt.ItemIsEnabled
        return flags
        
    def selectionChanged(self,selected, deselected,aLabel):  
        for index in selected.indexes():
            self.sums += int(self.data(index))
        for index in deselected.indexes():
            self.sums -= int(self.data(index))
            
        aLabel.setText('Sum :{}'.format(self.sums))
        return      

class App(QWidget): 
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
            explodes=[0.1, 0.1, 0, 0])
        self.table = QTableView(self)
        self.table.setModel(self.myModel)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch);
       
        splitter.addWidget(self.table)
        splitter.addWidget(PlotCanvas(self.myModel, width=5, height=4, parent = self))
        
        layout.addWidget(splitter,0,0,5,12)
        
        appendButton=QPushButton('Append',self)
        appendButton.clicked.connect(self.append)
        layout.addWidget(appendButton,5,0)
        
        insertButton=QPushButton('Insert',self)
        insertButton.clicked.connect(self.insert)
        layout.addWidget(insertButton,5,1)
        self.setLayout(layout)
        self.show()
        self.activateWindow() 
    
    def append(self):
        self.myModel.insertRow(self.myModel.rowCount())         
        return

    def insert(self):
        select = self.table.selectionModel().selectedRows()
        index = select[0].row() if len(select)>0 else 0
        self.myModel.insertRow(index)
        return
        
        
class PlotCanvas(FigureCanvas):
    def __init__(self,  model, width=5, height=4, dpi=100,parent=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setModel(model)
    
 
    def setModel(self, model):
        self.model = model
        self.model.dataChanged.connect(self.plotChanged)
        self.plot()
 
    def plot(self):
        rows = self.model.rowCount()
        self.labels = [self.model.index(i, 0).data() for i in range(rows)]
        self.data = [self.model.index(i, 1).data() for i in range(rows)]
        self.explodes = [self.model.index(i, 2).data() for i in range(rows)]
        self.axes.cla()
        ax = self.figure.add_subplot(111)
        ax.pie(self.data, explode=self.explodes, labels=self.labels, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.axis('equal')  
        ax.set_title('PyQt Matplotlib Example')
        self.draw()
    def plotChanged(self, topLeft, bottomRight, roles = [QtCore.Qt.EditRole]):
        if QtCore.Qt.EditRole in roles:
            self.plot()

if __name__ == '__main__':
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('pie2.png'))
    ex = App()
    sys.exit(app.exec_())
