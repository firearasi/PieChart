from PySide2 import QtCore
from PySide2.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        self.amount = [self.model.index(i, 1).data() for i in range(rows)]
        self.explodes = [self.model.index(i, 2).data()/100.0 for i in range(rows)]
        self.axes.cla()
        #ax = self.figure.add_subplot(111)
        ax=self.axes
        ax.pie(self.amount, explode=self.explodes, labels=self.labels, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.axis('equal')  
        ax.set_title('PyQt Matplotlib Example')
        self.draw()
    def plotChanged(self, topLeft, bottomRight, roles = [QtCore.Qt.EditRole]):
        if QtCore.Qt.EditRole in roles:
            self.plot()
