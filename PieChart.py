#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 23:44:38 2019

@author: yan
"""

import sys
from PyQt5.QtWidgets import QTableView,QSplitter, QApplication, QWidget, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QStyledItemDelegate, QSpinBox
from PyQt5.QtCore import Qt
from PyChartDataModel import PieChartDataModel
from PlotCanvas import PlotCanvas


class SpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(SpinBoxDelegate, self).__init__(parent)
        return
        
    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor
        
    def setEditorData(self, editor, index):
        if index.column() > 0:
            value = index.model().data(index, Qt.EditRole)
            editor.setValue(value)
        return
        
    def setModelData(self, editor, model, index):
        if index.column() > 0:
            editor.interpretText()
            value=float(editor.value())
            model.setData(index, value, Qt.EditRole)
        return
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        

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
        self.delegate=SpinBoxDelegate()
        self.table.setItemDelegate(self.delegate)
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
        


if __name__ == '__main__':
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('pie2.png'))
    ex = App()
    sys.exit(app.exec_())
