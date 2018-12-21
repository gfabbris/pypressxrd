'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

from PyQt5.QtWidgets import QMainWindow,QAction,QApplication,QWidget,QGridLayout

from pypressxrd.plot_widget import PlotWidget
from pypressxrd.options_widget import OptionsWidget
from pypressxrd.widgets_logic import LogicWidgets


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()

        self.spec_fname= ''
        self.statusBar().showMessage('Ready')

        self.setWindowTitle('XRD Pressure Calibration')
        self.setGeometry(200, 200, 1000, 600)
        
        self.build_menu()
        
        self.plot_widget = PlotWidget()
        self.plot_widget.setFixedWidth(1000-310)
        
        self.options_widget = OptionsWidget()
        self.options_widget.setFixedWidth(310)
        
        #self._layout = QHBoxLayout()
        #self._layout.addWidget(self.options_widget,1)
        #self._layout.addWidget(self.plot_widget,3)
        
        self._layout = QGridLayout()
        self._layout.addWidget(self.options_widget,0,0)
        self._layout.addWidget(self.plot_widget,0,1,1,5)
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(self._layout)
        
        self.connections = LogicWidgets(self.statusBar(),self.options_widget,self.plot_widget)
        
        
    def build_menu(self):

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        newAct = QAction('Load spec file', self)
        file_menu.addAction(newAct)
        #file_menu.triggered.connect(self.get_spec_fname)
        #file_menu.triggered.connect(self.load_spec_file)
        #file_menu.triggered.connect(self.load_scan_wrap)
        
        
    
        

if __name__ == '__main__':
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    app.exec_()

