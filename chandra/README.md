# chandra_work
A simple collection of scripts to analyse files from the Chandra x-ray telescope I made during free time during my masters.
You will need numpy, matplotlib, argparse, gzip, astropy to run these codes. The data is at https://cda.harvard.edu/chaser/mainEntry

### 1) chandra_acis_img_plot.py
Take the compressed image fits file and process and output the data. Made for acis instrument onboard chandra. 
<br />
##### Usage
 `python chandra_acis_img_plot.py --args`
 
### 2) chandra_spectra.py 
Take the events fits file (uncompressed) from acis instrument of chandra and obtain the spectram of the targeted object.
<br />
##### Usage
`python chandra_spectra.py  --args`

### 3) model_to_spectra.py 
Fit a gaussian model to the energy spectrum from acis instrument's events fits file.
<br />
##### Usage
`python model_to_spectra.py  --args`
