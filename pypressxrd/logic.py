'''
 Copyright (c) 2018, UChicago Argonne, LLC
 See LICENSE file.
'''

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def get_temperature(header):
    """Reads the temperature from the header of a spec file from 4-ID-D.

    Parameters
    -----------
    header: string
        String containing the file header where the temperature is saved.

    temp_source: string
        Name of the temperature to be read. Normal stardard is "Control" or "Sample".

    Returns
    -----------
    temperature: float
        Temperature from the selected source.
    """
    
    temperature = {}
    
    for line in header.split('\n'):
        if line[:2] == '#X':
            raw = line.strip('#X').split()
            for i in range(int(len(raw)/2)):
                temperature[raw[2*i].strip(':')] = float(raw[2*i+1].strip('K'))      
                
    return temperature

def get_energy(header):
    """Reads the x-ray energy from the header of 4-ID-D spec file.

    Parameters
    -----------
    header: string
        String containing the file header where the energy is saved.

    Returns
    -----------
    energy: float
        X-ray energy in keV.
    """

    for line in header.split('\n'):
        if 'Energy' in line:
            return float(line.split('Energy:')[1].split('eV')[0])

def load_scan(spec,scan_number,x_label,y_label,norm_column=None):
    """Loads a scan, temperature and energy from the 4-ID-D spec file.

    Parameters
    -----------
    spec: spec2nexus.spec.SpecDataFile
        Spec file

    scan_number: int
        Number of the scan to be loaded.

    x_label: string
        Name of the column to be loaded as x.

    y_label: string
        Name of the column to be loaded as y.

    norm_column: string (Optional)
        Name of the column to be used as a normalization. If None, then no normalization is done.

    Returns
    -----------
    x: np.ndarray
        Array with x values

    y: np.ndarray
        Array with y values

    energy: float
        X-ray energy in keV.

    temperature: float
        Temperature from the selected source.
    """

    scan = spec.getScan(scan_number)
    x = np.array(scan.data[x_label])
    y = np.array(scan.data[y_label])
    if norm_column:
        y /= np.array(scan.data[norm_column])

    temperature = get_temperature(scan.raw)
    energy = get_energy(scan.raw)

    return x,y,temperature,energy

def pseudo_voigt(x,x0,sigma,amplitude,constant,alpha):
    """Creates a pseudo-voigt peak.

    Parameters
    -----------
    x: np.ndarray
        Array with x values

    x0,sigma,amplitude,constant,alpha : float
        Parameters of the pseudo-voigt function.

    Returns
    -----------
    pseudo-voigt: np.ndarray
        Pseudo-voigt function
    """

    sigma_g = sigma/np.sqrt(2*np.log(2))
    gauss = (1-alpha)*amplitude/sigma_g/np.sqrt(2*np.pi)*np.exp(-1.*(x-x0)**2/2/sigma_g**2)

    lorentz = alpha*amplitude/np.pi*sigma/((x-x0)**2+sigma**2)

    return gauss+lorentz+constant

def fit_pseudo_voigt(x,y,p0=None,fit_alpha=True,alpha_guess=0.5):
    """Fits the data with a pseudo-voigt peak.

    Parameters
    -----------
    x: np.ndarray
        Array with x values

    y: np.ndarray
        Array with y values

    p0: list (Optional)
        It contains a initial guess the for the pseudo-voigt variables, in the order:
    p0 = [x0,sigma,amplitude,constant,alpha]. If None, the code will create a guess.

    fit_alpha: boolean (Optional)
        Option to fit the alpha parameter.

    alpha_guess: float (Optional)
        If alpha is being fitted, then this will be the initial guess. Otherwise it will be the fixed parameter used.
    For lorenzian: alpha = 1, for gaussian: alpha = 0.

    Returns
    -----------
    popt: np.ndarray
        Array with the optimized pseudo-voigt parameters.
    """

    if p0 is None:
        width = (x.max()-x.min())/10.
        index = y == y.max()
        p0 = [x[index][0],width,y.max()*width*np.sqrt(np.pi/np.log(2)),y[0],alpha_guess]

    if fit_alpha is False:
        popt,pcov = curve_fit(lambda x,x0,sigma,amplitude,constant: pseudo_voigt(x,x0,sigma,amplitude,constant,alpha_guess),
                              x,y,p0=p0[:-1])
        popt = np.append(popt,alpha_guess)
    else:
        popt,pcov = curve_fit(pseudo_voigt,x,y,p0=p0)
        

    return popt

def load_ag_params(temperature):
    """Load the Ag parameters for calculating the pressure. These parameters were
    extracted from Holzapfel et al., J. Phys. Chem. Ref. Data 30, 515 (2001).

    Parameters
    -----------
    temperature: float
        Measurement temperature in Kelvin.

    Returns
    -----------
    v0_out,k0_out,kp0_out: float
        Volume, K and K' calibrated parameters.
    """

    v0 = [16.8439,16.8439,16.8512,16.8815,16.9210,16.9644,17.0099,17.057,17.1055,17.1553,17.2063,17.2585]
    k0 = [110.85,110.85,110.31,108.68,106.83,104.91,102.96,101.0,99.03,97.05,95.07,93.07]
    kp0 = [6,6,6.01,6.03,6.05,6.08,6.12,6.15,6.19,6.22,6.26,6.3]
    temp0 = [0,10,50,100,150,200,250,300,350,400,450,500]

    try:
        v0_out = float(interp1d(temp0,v0,kind='linear')(temperature))
        k0_out = float(interp1d(temp0,k0,kind='linear')(temperature))
        kp0_out = float(interp1d(temp0,kp0,kind='linear')(temperature))
        return v0_out,k0_out,kp0_out
    except ValueError:
        print('ERROR! Temperature must be between 5-500K, but {:0.1f} was entered!'.format(temperature))
        return 0

def load_au_params(temperature):
    """Load the Au parameters for calculating the pressure. These parameters were
    extracted from Holzapfel et al., J. Phys. Chem. Ref. Data 30, 515 (2001).

    Parameters
    -----------
    temperature: float
        Measurement temperature in Kelvin.

    Returns
    -----------
    v0_out,k0_out,kp0_out: float
        Volume, K and K' calibrated parameters.
    """

    v0 = [16.7905,16.7906,16.7984,16.8238,16.8550,16.8885,16.9232,16.959,16.9956,17.0329,17.071,17.1098]
    k0 = [180.93,180.93,179.94,177.51,174.86,172.16,169.43,166.7,163.96,161.21,158.46,155.7]
    kp0 = [6.08,6.08,6.09,6.11,6.13,6.15,6.17,6.20,6.23,6.25,6.28,6.31]
    temp0 = [0,10,50,100,150,200,250,300,350,400,450,500]

    try:
        v0_out = float(interp1d(temp0,v0,kind='linear')(temperature))
        k0_out = float(interp1d(temp0,k0,kind='linear')(temperature))
        kp0_out = float(interp1d(temp0,kp0,kind='linear')(temperature))
        return v0_out,k0_out,kp0_out
    except ValueError:
        print('ERROR! Temperature must be between 5-500K, but {:0.1f} was entered!'.format(temperature))
        return 0

def calculate_pressure(tth, temperature, energy, bragg_peak, calibrant, tth_off = 0.0):
    """Calculate the pressure using diffraction from Au or Ag.

    Parameters
    -----------
    tth: float
        Two theta of the selected Bragg peak.

    temperature: float
        Measurement temperature in Kelvin.

    energy: float
        X-ray energy used in keV.

    bragg_peak: string
        Pick the Bragg peak that will be used in the calibration. Current options are
    '111', '200', '220'.

    calibrant: string
        Selects the calibrant used. Options are 'Au' or 'Ag'.

    tth_off: float (Optional)
        Offset between the reference two theta and the measured value.

    Returns
    -----------
    pressure: float
        Calculated pressure in GPa.
    """
    ## Constants ##
    afg = 2337 #GPa.AA^5
    h = 4.135667662E-15 #eV.s
    c = 299792458E10 #AA/s

    ## Loading parameters ##
    if calibrant == 'Au':
        z = 79
        #a0_th = 4.07837
        v0,k0,kp0 = load_au_params(temperature)
    elif calibrant == 'Ag':
        return 'Ag calibrant is not setup yet!!!'
        

    ## Calculate atomic volume
    lamb = h*c/energy/1000.
    d = lamb/2/np.sin((tth-tth_off)/2.*np.pi/180.)

    if bragg_peak == '111':
            a = d*np.sqrt(3)
    elif bragg_peak == '200':
            a = d*2.
    elif bragg_peak == '220':
            a = d*np.sqrt(8)
    else:
        return 'Could not recognize the {} bragg peak. It must be "111", "200", or "220".'.format(bragg_peak)

    v = a**3/4.

    ## Calculate pressure
    x = (v/v0)**0.3333
    pfg0 = afg*(z/v0)**1.6666
    c0 = -1*np.log(3*k0/pfg0)
    c2 = (3/2)*(kp0-3)-c0

    pressure = 3*k0*(1-x)/x**5*np.exp(c0*(1-x))*(1+c2*x*(1-x))

    return pressure

def plot_data(fig,canvas,x,y,clear=True,xlabel='',ylabel=''):
    ''' plot some random stuff '''

    if clear:
        fig.clear()
        ax = fig.add_subplot(111)
    else:
        plt.gca()
    ax.plot(x,y, 'o-')
    ax.tick_params(which='both',direction='in',right=True,top=True)
    ax.set_xlabel(xlabel,fontsize=12)
    ax.set_ylabel(ylabel,fontsize=12)
    
    rng = np.abs(x.max()-x.min())*0.05
    ax.set_xlim(x.min()-rng,x.max()+rng)
    
    rng = np.abs(y.max()-y.min())*0.05
    ax.set_ylim(y.min()-rng,y.max()+rng)

    canvas.draw()
    return ax
