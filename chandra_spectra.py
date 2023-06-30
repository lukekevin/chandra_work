"""
Author: Kevin Luke
Date created: 24th October 2020
Date modified: 30th June 2023
"""
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import argparse

def energy_time_hist(events):
    energy=events['energy']
    time=events['time']

    plt.title('Energy Time distribution')
    plt.xlabel('Time in hrs')
    plt.ylabel('Energy in kev')
    plt.hist2d(np.max(time)/3600-time/3600,energy/1000,
               bins=[500,500])
    plt.savefig('energy_time_distribution.jpg')
    
def energy_hist(events, energy_min, energy_max):
    energy=events['energy']/1000 #convert the ev to kev 
    # Filter the energy values within the specified range
    energy_range = energy[(energy >= energy_min) & (energy <= energy_max)]
    plt.title('Energy distribution')
    plt.xlabel('Energy in kev')
    plt.ylabel('Counts')
    plt.hist(energy_range, bins=500)
    plt.savefig('energy_histogram.jpg')

    
def energy_spectrum(events, min_ener, max_ener):
    energy=events['energy'] #it is in ev 
    energy_min = min_ener*1000 #0.0  # Minimum energy in eV
    energy_max = max_ener*1000  # Maximum energy in eV
    selected_events = events[(energy >= energy_min) & (energy <= energy_max)]
    spectrum, _ = np.histogram(selected_events['ENERGY'], bins=100, range=(energy_min, energy_max))
    energy_bins = np.linspace(energy_min, energy_max, num=101)[:-1] + 0.5 * (energy_max - energy_min) / 100
    plt.figure(figsize=(8, 5))
    plt.plot(energy_bins/1000, spectrum, color='black')
    plt.xlabel('Energy (keV)')
    plt.ylabel('Counts')
    plt.title('X-ray Spectrum')
    plt.savefig('energy_spectrum.jpg')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('events_fits_file', type=str, 
                       help='Path to the events fits file')
    
    parser.add_argument('--make_spectra',dest='make_spectra',
                        default=None, action='store_true',
                       help='Do you want a spectra?')
    
    parser.add_argument('--make_energy_hist',dest='make_energy_hist',
                        default=None, action='store_true',
                       help='Do you want an energy histogram')
    
    parser.add_argument('--make_energy_time_hist',dest='make_energy_time_hist',
                        default=None, action='store_true',
                       help='Do you want an energy-time histogram')

    args = parser.parse_args()
    events_fits_file=args.events_fits_file
    make_spectra=args.make_spectra
    make_energy_hist=args.make_energy_hist
    make_energy_time_hist=args.make_energy_time_hist
    
    print('Give the overview of the fits files\n')
    cx_fits=fits.open(events_fits_file)
    cx_fits.info()
    events=cx_fits['EVENTS'].data
    print('\n Give the names of columns in the events table\n')
    print(cx_fits['EVENTS'].data.names)
    print('\nGive detais of the header file')
    print(cx_fits[0].header)
    
    if make_spectra:
        energy_spectrum(events, 1.0,10.0)
    elif make_energy_hist:
        energy_hist(events, 1.0, 10.0)
    elif make_energy_time_hist:
        energy_time_hist(events)
    else:
        energy_spectrum(events, 1.0,10.0)
        energy_hist(events, 1.0, 10.0)
        energy_time_hist(events)  
