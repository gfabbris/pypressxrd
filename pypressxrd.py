'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

import sys
from pypressxrd.main_widget import MainWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
