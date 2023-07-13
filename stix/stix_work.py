from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import gzip
from astropy.modeling import models, fitting
import argparse

def spectrum_plot(stix_spec_fits):
    
    print('This code will simply plot the spectra from solo_L1_stix-sci-xray-spec*****.fits files')
    print('\n')
    print(stix_spec_fits.info())
    print('\n')
    
    #data hdu contains details of counts from the source
    Data=stix_spec_fits[2].data
    counts=Data['counts'][0]  #there are 7 arrays in the list so I selected any one of them as they donthave much diff
    print('Printing column info of data hdu', Data.columns)
    print('\n')
    #energy hdu contains the energy,channel information
    energy=stix_spec_fits[4].data
    energy_low=energy['e_low']
    energy_high=energy['e_high']
    avg_energy=0.5*(energy_low+energy_high)
    channels=energy['channel']
    print('Printing column info of the data hdu', energy.columns)
    
    plt.figure(figsize=(15,5))
    plt.subplot(1,2,1)
    plt.title('Channel vs counts plot/Spectra from STIX')
    plt.xlabel('channel')
    plt.ylabel('counts')
    plt.plot(channels,counts)
    plt.scatter(channels,counts,c='red', marker='*')
    
    plt.subplot(1,2,2)
    plt.title('Energy vs counts plot/Spectra from STIX')
    plt.xlabel('energies in kev')
    plt.ylabel('counts')
    plt.plot(avg_energy,counts)
    plt.scatter(avg_energy,counts,c='red', marker='*')
    
    plt.savefig('Spectra.jpg')
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('fits_path', type=str,
        help='Path to solo_L1_stix-sci-xray-spec*****.fits file')
    
    args = parser.parse_args()
    
    fits_path=args.fits_path
    #load the fits
    stix_spec_fits=fits.open(fits_path)
    #run the func
    spectrum_plot(stix_spec_fits)