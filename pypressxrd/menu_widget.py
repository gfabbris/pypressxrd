'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

from PyQt5.QtWidgets import QMainWindow, QAction

class MenuWidget(QMainWindow.menuBar):

    def __init__(self):
        super(MenuWidget,self).__init__()

        file_menu = self.addMenu('File')

        newAct = QAction('Load spec file', self)
        file_menu.addAction(newAct)
