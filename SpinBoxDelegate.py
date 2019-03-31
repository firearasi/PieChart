
from PySide2.QtWidgets import QStyledItemDelegate, QSpinBox, QLineEdit, QSlider
from PySide2.QtCore import Qt

class SpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(SpinBoxDelegate, self).__init__(parent)
        return
        
    def createEditor(self, parent, option, index):
        if index.column() == 1: 
            editor = QSpinBox(parent)
            editor.setFrame(False)
            editor.setMinimum(0)
            editor.setMaximum(200)
            valueChangedSlot = lambda x:self.setModelData(editor, index.model(), index)
            editor.valueChanged.connect(valueChangedSlot)
        elif index.column() == 2:
            editor = QSlider(parent, orientation=Qt.Horizontal)
            #editor.setFrame(False) 
            editor.setMinimum(-100)
            editor.setMaximum(100)
            valueChangedSlot = lambda x:self.setModelData(editor, index.model(), index)
            editor.valueChanged.connect(valueChangedSlot)
        else:
            editor = QLineEdit(parent)
            valueChangedSlot = lambda x:self.setModelData(editor, index.model(), index)
            editor.textChanged.connect(valueChangedSlot)
        return editor
        
    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        if index.column() > 0:
            editor.setValue(value)
        else:
            editor.setText(value)
        return
        
    def setModelData(self, editor, model, index):
        if index.column() > 0:
            value=float(editor.value())
            model.setData(index, value, Qt.EditRole)
        else:
            value=editor.text()
            model.setData(index, value, Qt.EditRole)
        return
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
