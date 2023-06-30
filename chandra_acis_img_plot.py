from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import argparse
import gzip


def image_plotter(input_gz,output_fits):
    #PLOT THE ACIS fits image with this function
    
    #uncompress the data first
    with gzip.open(input_gz, 'rb') as f_in:
        with open(output_fits, 'wb') as f_out:
            f_out.write(f_in.read())
    img_fits=fits.open(output_fits)
    
    print(img_fits.info())
    
    #THIS IS THE NON CONTRASTED DATA
    img=img_fits[0].data
    
    #do a 1d intensity level distribution accros pixels to get a magnified image from 
    #NON CONTRASTED DATA
    intensity_distribution = np.mean(img, axis=1)
    minvalue=np.min(np.where(intensity_distribution>0)[0]) - 100
    maxvalue=np.max(np.where(intensity_distribution>0)[0])+ 100
    
    #DO CONTRAST CORRECTION
    img = img.astype(float)  # Convert to floating-point for accurate calculations
    img = (img - np.min(img)) / (np.max(img) - np.min(img))
    # Step 2: Define the contrast stretch parameters
    contrast_min = 0.3 # Lower bound of the desired contrast range (adjust this value)
    contrast_max = 1.0  # Upper bound of the desired contrast range (adjust this value)
    # Step 3: Apply the contrast stretch
    contrast_stretched_image = (img - contrast_min) / (contrast_max - contrast_min)
    contrast_stretched_image = np.clip(contrast_stretched_image, 0.0, 1.0)  # Ensure values are within the valid range
    
    
    #PLOT THE IMAGES SIDE-BY-SIDE
    plt.figure(figsize=(20,10))
    plt.subplot(1, 2, 1)
    plt.title('Chandra acis image')
    #
    plt.imshow(img[minvalue:maxvalue,minvalue:maxvalue],cmap='plasma')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.title('Chandra acis image, contrasted')
    plt.imshow(contrast_stretched_image[minvalue:maxvalue,minvalue:maxvalue],cmap='plasma')
    plt.axis('off')
    plt.savefig('chandra_acis.jpg')
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input_gz', type=str, 
                       help='Path to the image .gz fits file')
    parser.add_argument('output_fits', type=str, 
                       help='Out path to the image fits file')
    args = parser.parse_args()    
    
    input_gz=args.input_gz
    output_fits=args.output_fits
    
    print('This simple code takes the .gz fits file and plots the image.')
    print('Processing the .gz fits file from acis instrument onboard chandra xray telescope.')
    print('Saving the image.')
    
    #Run the image processing function
    image_plotter(input_gz,output_fits)