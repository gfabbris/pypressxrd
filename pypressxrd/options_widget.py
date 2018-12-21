'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

from PyQt5.QtWidgets import QApplication, QWidget,QGroupBox,QComboBox
from PyQt5.QtWidgets import QLabel,QTextEdit,QPushButton,QRadioButton
from PyQt5.QtWidgets import QGridLayout,QVBoxLayout,QHBoxLayout

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QFont

class OptionsWidget(QWidget):

    def __init__(self):
        super(OptionsWidget,self).__init__()
        
        self.spec = SpecWidget()
        self.scan = ScanWidget([''])
        self.fit  = FitWidget()
        self.pressure = PressureWidget()
        
        self._layout = QVBoxLayout()
        self._layout.addWidget(self.spec)
        self._layout.addWidget(self.scan)
        self._layout.addWidget(self.fit)
        self._layout.addWidget(self.pressure)
        self.setLayout(self._layout)

class SpecWidget(QGroupBox):

    def __init__(self,title='Spec File',fontsize=18):
        
        super(SpecWidget,self).__init__(title)
        
        self.build_widgets()
        self.build_layout()
        
        self.spec_fname = 'test'
        
    def build_widgets(self):

        self.load_button = QPushButton('Load')
        self.reload_button = QPushButton('Reload')
        self.fname_label = QLabel('File name:')
        self.fname = QLabel('')
    
    def build_layout(self):

        self._layout = QGridLayout()
        self._layout.addWidget(self.load_button,0,0)
        self._layout.addWidget(self.reload_button,0,1)
        self._layout.addWidget(self.fname_label,1,0)
        self._layout.addWidget(self.fname,1,1)
        
        self.setLayout(self._layout)

class ScanWidget(QGroupBox):
    
    def __init__(self,scan_list,title='Scan Options'):
        
        super(ScanWidget,self).__init__(title)
        
        self.build_widgets(scan_list)
        self.build_layout()
        
    def build_widgets(self,scan_list):

        self.scans_box = QComboBox()
        self.scans_box.addItems(scan_list)

        self.x_label = QLabel('tth column:')
        self.x_box = QComboBox()

        self.y_label = QLabel('y column:')
        self.y_box = QComboBox()
        
        self.temp_label = QLabel('Temp.:')
        self.temp_label.setMaximumWidth(50)
        self.temp_box = QComboBox()
        self.temp_read = QTextEdit('300.0')
        self.temp_read.setMaximumHeight(25)
        self.temp_read.setMaximumWidth(50)
        self.temp_read_unit = QLabel('K')
        
        self.energy_label = QLabel('Energy:')
        self.energy_read = QTextEdit('10.0')
        self.energy_read.setMaximumHeight(25)
        self.energy_read.setMaximumWidth(100)
        self.energy_read_unit = QLabel('keV')
    
    def build_layout(self):

        self._layout = QGridLayout()
        self._layout.addWidget(self.scans_box,0,0,1,3)
        
        self._layout.addWidget(self.x_label,1,0)
        self._layout.addWidget(self.x_box,1,1,1,2)
    
        self._layout.addWidget(self.y_label,2,0)
        self._layout.addWidget(self.y_box,2,1,1,2)
        
        self._layout.addWidget(self.temp_label,5,0)
        self._layout.addWidget(self.temp_box,5,1)
        self._layout.addWidget(self.temp_read,5,2)
        self._layout.addWidget(self.temp_read_unit,5,3)
        
        self._layout.addWidget(self.energy_label,6,0)
        self._layout.addWidget(self.energy_read,6,1)
        self._layout.addWidget(self.energy_read_unit,6,2)
        
        self.setLayout(self._layout)


class FitWidget(QGroupBox):
    
    def __init__(self,title='Fit Parameters'):
        
        super(FitWidget,self).__init__(title)
        
        self.build_widgets()
        self.build_layout()
        
    def build_widgets(self):

        self.pseudovoigt = QRadioButton('Pseudo-Voigt')
        self.gauss = QRadioButton('Gaussian')
        self.lorentz = QRadioButton('Lorentzian')
        
        self.tth_value_label = QLabel('tth:')
        self.tth_value_label.setMaximumWidth(42)
        
        self.tth_value = QTextEdit('')
        self.tth_value.setMaximumHeight(25)
        self.tth_value.setMaximumWidth(61)
        
        self.amplitude_value_label = QLabel('amplitude:')
        self.amplitude_value_label.setMaximumWidth(65)
        
        self.amplitude_value = QTextEdit('')
        self.amplitude_value.setMaximumHeight(25)
        self.amplitude_value.setMaximumWidth(61)
        
        self.sigma_value_label = QLabel('sigma:')
        self.sigma_value_label.setMaximumWidth(42)
        
        self.sigma_value = QTextEdit('')
        self.sigma_value.setMaximumHeight(25)
        self.sigma_value.setMaximumWidth(61)
        
        self.constant_value_label = QLabel('constant:')
        self.constant_value_label.setMaximumWidth(65)
        
        self.constant_value = QTextEdit('')
        self.constant_value.setMaximumHeight(25)
        self.constant_value.setMaximumWidth(61)
        
        self.alpha_value_label = QLabel('weight:')
        self.alpha_value_label.setMaximumWidth(42)
        
        self.alpha_value = QTextEdit('')
        self.alpha_value.setMaximumHeight(25)
        self.alpha_value.setMaximumWidth(61)
          
        self.pseudovoigt.setChecked(True)
        
        self.fit_button = QPushButton('Fit')
        self.reset_button = QPushButton('Reset Params.')
        
    def build_layout(self):

        self._layout = QGridLayout()

        self._layout.addWidget(self.pseudovoigt,0,0,1,2)
        self._layout.addWidget(self.gauss,0,2,1,2)
        self._layout.addWidget(self.lorentz,1,0,1,2)
        
        
        self._layout.addWidget(self.tth_value_label,2,0)
        self._layout.addWidget(self.tth_value,2,1)

        self._layout.addWidget(self.amplitude_value_label,2,2)
        self._layout.addWidget(self.amplitude_value,2,3)

        self._layout.addWidget(self.sigma_value_label,3,0)
        self._layout.addWidget(self.sigma_value,3,1)

        self._layout.addWidget(self.constant_value_label,3,2)
        self._layout.addWidget(self.constant_value,3,3)

        self._layout.addWidget(self.alpha_value_label,4,0)
        self._layout.addWidget(self.alpha_value,4,1)
        
        
        self._layout.addWidget(self.reset_button,5,0,1,2)
        self._layout.addWidget(self.fit_button,5,2,1,2)
        
        self.setLayout(self._layout)
        

class PressureWidget(QGroupBox):
    
    def __init__(self,title='Pressure Calibration'):
        
        super(PressureWidget,self).__init__(title)
        
        self.build_widgets()
        self.build_layout()
        
    def build_widgets(self):
        
        #select bragg peak
        #Write pressure
        #Select which manomenter
        
        
        self.au = QRadioButton('Au')
        self.ag = QRadioButton('Ag')
        self.au.setChecked(True)
        
        self.tth_offset_label = QLabel('tth offset:')
        self.tth_offset_value = QTextEdit('0.000')
        self.tth_offset_value.setMaximumHeight(25)
        self.tth_offset_value.setMaximumWidth(50)
        
        self.hkl_label = QLabel('Bragg Peak (HKL):')
        self.hkl_box = QComboBox()
        self.hkl_box.addItems(['111','200','220'])
        
        self.pressure_button = QPushButton('Calculate Pressure')
        
        self.print_pressure = QLabel('')
        self.print_pressure.setStyleSheet('color: red')
        self.print_pressure.setFont(QFont("Times",30,QFont.Bold))
        self.print_pressure.setAlignment(Qt.AlignCenter)
        
    def build_layout(self):

        self._layout = QVBoxLayout()
        
        self._mano_layout = QHBoxLayout()
        self._mano_layout.addWidget(self.au)
        self._mano_layout.addWidget(self.ag)
        self._mano_layout.addWidget(self.tth_offset_label)
        self._mano_layout.addWidget(self.tth_offset_value)
        
        self._hkl_layout = QHBoxLayout()        
        self._hkl_layout.addWidget(self.hkl_label)
        self._hkl_layout.addWidget(self.hkl_box)
            
        self._layout.addLayout(self._mano_layout)
        self._layout.addLayout(self._hkl_layout)
        self._layout.addWidget(self.pressure_button)
        self._layout.addWidget(self.print_pressure)
        
        self.setLayout(self._layout)
        

if __name__ == '__main__':
    app = QApplication([])
    widget = OptionsWidget(parent=None)
    widget.show()
    app.exec_()
