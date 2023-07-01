"""
Author: Kevin Luke
Date created: 24th October 2020
Date modified: 1st July 2023
"""
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import argparse
import gzip
from astropy.modeling import models, fitting


def model_to_spectra(events, min_ener, max_ener):
    energy=events['energy'] #it is in ev 
    energy_min = min_ener*1000 #0.0  # Minimum energy in eV
    energy_max = max_ener*1000  # Maximum energy in eV
    selected_events = events[(energy >= energy_min) & (energy <= energy_max)]
    counts, _ = np.histogram(selected_events['ENERGY'], 
                               bins=100, 
                               range=(energy_min, energy_max))
    energy_binned = np.linspace(energy_min, energy_max, num=101)[:-1] + 0.5 * (energy_max - energy_min) / 100
    
    make_model = models.Gaussian1D()
    energy_log = np.log(energy_binned)
    fitter = fitting.LevMarLSQFitter()
    model_fit = fitter(make_model, energy_log, counts)
    
    energy_fit = np.linspace(np.min(energy_log), np.max(energy_log))
    counts_fit = model_fit(energy_fit)
    
    
    plt.figure(figsize=(8, 5))
    plt.plot(energy_fit, counts_fit, label='Gaussian Fit', color='red')
    plt.scatter(energy_log, counts, label='Data',marker='o')
    plt.xlabel('Log(Energy in ev)')
    plt.ylabel('Counts')
    plt.title('X-ray Spectrum')
    plt.legend()
    plt.savefig('Model_fit_to_spectra.jpg')

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('events_gzfits_file', type=str, 
                       help='Path to the events .gz fits file')
    
    args = parser.parse_args()
    events_gzfits_file=args.events_gzfits_file
    
    print('Give the overview of the fits files\n')
    
    #decompress the .gz fits file
    inpath=events_gzfits_file
    outpath=inpath[:-3]
    
    with gzip.open(inpath, 'rb') as f_in:
        with open(outpath, 'wb') as f_out:
            f_out.write(f_in.read())
    out_fits=fits.open(outpath)
    
    out_fits.info()
    events=out_fits['EVENTS'].data
    print(out_fits['EVENTS'].data.names)
    
    model_to_spectra(events,0.0,10.0)