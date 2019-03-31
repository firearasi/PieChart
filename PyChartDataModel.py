from PySide2 import QtCore
class PieChartDataModel(QtCore.QAbstractTableModel):
    def __init__(self, labels, data, explodes, parent = None):
        super(PieChartDataModel,self).__init__(parent)
        self.columns=3
        self.labels=labels
        self.amount=data
        self.explodes=explodes
        
    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.labels)
    def columnCount(self, parent =  QtCore.QModelIndex()):
        return self.columns
    def data(self,index,role=QtCore.Qt.DisplayRole):
        row = index.row()
        column = index.column()
        #if role != QtCore.Qt.DisplayRole or role!=QtCore.Qt.EditRole:
        #    return None
        if row >= self.rowCount() or row < 0 or column >= self.columns or column < 0:
            return None;
        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignRight
        if index.column()==0:
            return self.labels[index.row()]
        elif index.column()==1:
            return float(self.amount[index.row()])
        elif index.column()==2:
            return float(self.explodes[index.row()])
        else:
            return None
    def headerData(self,section,orientation,role):
        if role != QtCore.Qt.DisplayRole:
            return None;
        if orientation==QtCore.Qt.Horizontal:
            if section == 0:
                return 'Labels'
            elif section == 1:
                return 'Data'
            elif section == 2:
                return 'Explodes'
            else:
                return None
        else:
            return 'Item {}'.format(section)
        
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
            self.amount[row] = toNumber(value)
        elif column==2:
            self.explodes[row] = toNumber(value)
        self.dataChanged.emit(index, index, [QtCore.Qt.EditRole, QtCore.Qt.DisplayRole])
        return True
        
    def insertRow(self, row, parent = QtCore.QModelIndex()):
        if row < 0 or row > self.rowCount():
            return
        self.beginInsertRows(parent, row, row);
        self.labels.insert(row, 'Item {}'.format(row))
        self.amount.insert(row, 20)
        self.explodes.insert(row, 0)
        self.endInsertRows()
        topLeft = self.index(row, 0)
        bottomRight = self.index(row, 2)
        self.dataChanged.emit(topLeft, 
            bottomRight, 
            [QtCore.Qt.EditRole, QtCore.Qt.DisplayRole])
        return
    
    def removeRow(self, row, parent = QtCore.QModelIndex()):
        if row < 0 or row >= self.rowCount():
            return
        self.beginRemoveRows(parent, row, row);
        self.labels.pop(row)
        self.amount.pop(row)
        self.explodes.pop(row)
        self.endRemoveRows()
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
