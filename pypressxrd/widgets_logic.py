'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

from PyQt5.QtWidgets import QFileDialog,QApplication
from PyQt5.QtCore import QObject

from spec2nexus.spec import SpecDataFile

from pypressxrd.logic import load_scan,plot_data,fit_pseudo_voigt,pseudo_voigt
from pypressxrd.logic import calculate_pressure

from numpy import abs as np_abs

import time

class LogicWidgets(QObject):
    def __init__(self,status,options,plot):
        
        super(LogicWidgets, self).__init__()
        
        self.status = status
        self.spec = options.spec
        self.scan = options.scan
        self.fit = options.fit
        self.pressure = options.pressure
        self.plot = plot
        
        self.prepare_pseudovoigt()
        self.au_selected()
        
        self.popt = None
        self.fit_line = []
        self.axv_line = None
        self.spec_fname = ''
        
        self.make_connections()

    def make_connections(self):
        
        self.spec.load_button.clicked.connect(self.get_spec_fname)
        self.spec.load_button.clicked.connect(self.load_spec_file)
        self.spec.reload_button.clicked.connect(self.load_spec_file)
        
        self.scan.scans_box.activated[str].connect(self.selected_scan)
        
        self.scan.x_box.activated[str].connect(self.load_scan_wrap)
        self.scan.y_box.activated[str].connect(self.load_scan_wrap)
        
        self.scan.temp_box.activated[str].connect(self.update_temp)
        
        self.fit.pseudovoigt.toggled.connect(self.prepare_pseudovoigt)
        self.fit.gauss.toggled.connect(self.prepare_gauss)
        self.fit.lorentz.toggled.connect(self.prepare_lorentz)
        
        self.fit.fit_button.clicked.connect(self.fit_data)
        self.fit.reset_button.clicked.connect(self.reset_parameters)
        
        self.pressure.au.toggled.connect(self.au_selected)
        self.pressure.ag.toggled.connect(self.ag_selected)
        
        self.pressure.pressure_button.clicked.connect(self.pressure_calculator)
     
    def get_spec_fname(self):
        
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.spec_fname, _ = QFileDialog.getOpenFileName(self.spec,"QFileDialog.getOpenFileName()", "","All Files (*);;Spec Files (*.spec)", options=options)
            self.spec.fname.setText('{}'.format(self.spec_fname.split('/')[-1]))
     
    def load_spec_file(self):
        
        if self.spec_fname == '':
            self.status.showMessage('No file was loaded')
            return
        
        self.scan.scans_box.clear()
        try:
            self._spec_file = SpecDataFile(self.spec_fname)
            
            self._commands_list = self._spec_file.getScanCommands()
            for i in range(len(self._commands_list)):
                if '#S' in self._commands_list[i]:
                    self._commands_list[i] = self._commands_list[i].strip('#S ')
                self.scan.scans_box.addItem(self._commands_list[i])
                
            self.scan.scans_box.setCurrentIndex(len(self._commands_list)-1)
            
            self.selected_scan(self._commands_list[-1])
            self.make_plot()
            self.pressure.print_pressure.setText('')
        except:
            self.status.showMessage('{} is not a spec file!!'.format(self.spec.fname.text()))

  
    def selected_scan(self,text):
        self._scan_number = int(text.split()[0])
        self._columns = self._spec_file.getScan(self._scan_number).L
        firstcol = self._spec_file.getScan(self._scan_number).column_first
        lastcol = self._spec_file.getScan(self._scan_number).column_last
    
        self.scan.x_box.clear()
        self.scan.x_box.addItems(self._columns)
        self.scan.x_box.setCurrentText(firstcol)
        
        self.scan.y_box.clear()
        self.scan.y_box.addItems(self._columns)
        self.scan.y_box.setCurrentText(lastcol)
    
        self.load_scan_wrap()
        
    def load_scan_wrap(self):
        try:
            self.x,self.y,self.temperature,self.energy = load_scan(self._spec_file,
                                                                   self._scan_number,
                                                                   self.scan.x_box.currentText(),
                                                                   self.scan.y_box.currentText())
            
            self.scan.energy_read.setText('{:0.4f}'.format(self.energy))
            
            self.scan.temp_box.clear()
            temp_list = list(self.temperature.keys())
            temp_list.sort()
            self.scan.temp_box.addItems(temp_list)
            self.scan.temp_box.setCurrentIndex(1)
            self.scan.temp_read.setText('{:0.1f}'.format(self.temperature[self.scan.temp_box.currentText()]))
            self.make_plot()
            self.popt = None
            self.fit_line = []
            self.axv_line = None
            self.update_params()
            self.status.showMessage('Loaded scan #{:d}'.format(self._scan_number))
        except:
            self.status.showMessage('Could not load scan #{:d}!!'.format(self._scan_number))
    
    def update_temp(self,text):
        self.scan.temp_read.setText('{:0.2f}'.format(self.temperature[text]))    

    def make_plot(self):
        self.ax = plot_data(self.plot.figure,self.plot.canvas,self.x,self.y,
                       xlabel=self.scan.x_box.currentText(),
                       ylabel=self.scan.y_box.currentText())
    
    def update_params(self):
        if self.popt is None:
            self.fit.tth_value.setText('{:.3f}'.format((self.x.max()+self.x.min())/2.))
            self.fit.amplitude_value.setText('{:.3f}'.format(self.y.max()))
            self.fit.sigma_value.setText('{:.3f}'.format(np_abs((self.x.max()-self.x.min())/6.)))
            self.fit.constant_value.setText('{:.3f}'.format((self.y[:5].mean()+self.y[-5:].mean())/2.))
        else:
            self.fit.tth_value.setText('{:.3f}'.format(self.popt[0]))
            self.fit.sigma_value.setText('{:.3f}'.format(self.popt[1]))
            self.fit.amplitude_value.setText('{:.3f}'.format(self.popt[2]))
            self.fit.constant_value.setText('{:.3f}'.format(self.popt[3]))
            self.fit.alpha_value.setText('{:.2f}'.format(self.popt[4]))
            
            
    def prepare_pseudovoigt(self):
        self.fit.alpha_value.setText('0.5')
        self.fit.alpha_value.setDisabled(False)
        self.fit_alpha = True

    def prepare_gauss(self):
        self.fit.alpha_value.setText('0.0')
        self.fit.alpha_value.setDisabled(True)
        self.fit_alpha = False

    def prepare_lorentz(self):
        self.fit.alpha_value.setText('1.0')
        self.fit.alpha_value.setDisabled(True)
        self.fit_alpha = False
        
    def fit_data(self):
        p0 = [float(self.fit.tth_value.toPlainText()),
              float(self.fit.sigma_value.toPlainText()),
              float(self.fit.amplitude_value.toPlainText()),
              float(self.fit.constant_value.toPlainText()),
              float(self.fit.alpha_value.toPlainText())]
        
        try:
            self.popt = fit_pseudo_voigt(self.x,self.y,p0=p0,fit_alpha=self.fit_alpha,
                                    alpha_guess=p0[-1])
         
            self.yfit = pseudo_voigt(self.x,*self.popt)
        
            self.update_params()
            self.plot_fit()
            self.status.showMessage('Fit successful!!')
        except RuntimeError:
            self.status.showMessage('Could not fit the data!!!')
        
    def plot_fit(self):

        for line in self.fit_line:
            self.ax.lines.remove(line)
        
        self.fit_line = self.ax.plot(self.x,self.yfit,color='red')
        
        self.plot_vline(self.popt[0])
        
        self.plot.canvas.draw()
    
    def plot_vline(self,x0):
        if self.axv_line is not None:
            self.ax.lines.remove(self.axv_line)
            
        self.axv_line = self.ax.axvline(x=x0,ls='--',color='grey')
        
    def au_selected(self):
        self.calibrant = 'Au'
        
    def ag_selected(self):
        self.calibrant = 'Ag'
        
    def pressure_calculator(self):
        
        tth = float(self.fit.tth_value.toPlainText())
        temperature = float(self.scan.temp_read.toPlainText())
        energy = float(self.scan.energy_read.toPlainText())
        bragg_peak = self.pressure.hkl_box.currentText()
        calibrant = self.calibrant
        tth_off = float(self.pressure.tth_offset_value.toPlainText())
        
        self.plot_vline(tth)
        self.plot.canvas.draw()
        
        output = calculate_pressure(tth,temperature,energy,bragg_peak,
                                       calibrant,tth_off = tth_off)
        
        if type(output) is str:
            self.status.showMessage(output)
        else:
            self.pressure.print_pressure.setText('P = {:.2f} GPa'.format(output))
            
        time.sleep(0.01)
        QApplication.processEvents()
        
    def reset_parameters(self):
        self.popt=None
        self.update_params()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
