#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 23:44:38 2019

@author: yan
"""

import sys
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QApplication
from PieChartWidget import PieChartWidget
from PySide2.QtGui import QIcon
        
if __name__ == '__main__':
    print('main')
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('pie2.png'))
    ex = PieChartWidget()
    sys.exit(app.exec_())
