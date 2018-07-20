
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.io import fits, ascii
import numpy as np 
import os

#make a list of files out of the directory (folder) where you're keeping them
list_of_files = (os.listdir('/home/pystudent/Desktop/Summer18_Research/FITS_files'))

#move the handling cursor to the same folder so we can look at them
os.chdir('/home/pystudent/Desktop/Summer18_Research/FITS_files') 


#this opens the file into a list like a normal python list
#hdulist = fits.open('HD41117_w346_n12_20150927_B.fits')

#run a for loop that will go through all the files in the desired folder
for file_number in range(len(list_of_files)):

    #set the name to the name of the current file from the list
    file_name = list_of_files[file_number]

    #the leading segment of the file name contains where in the sky the measurements were taken
    location = file_name.split("_")

    #open the desired FITS file in a list and then make it as a single object (hdu)
    hdulist = fits.open(file_name)
    hdu = hdulist[0]

    #this displays all information such as relevant dates and equipment 
    #print(hdu.header)

    #outputs a table that catalogues all of the HDU of the FITS files in the HDU List
    #hdulist.info()

    #outputs a specific 'card' of the specified HDU 
    print(hdu.header)

    # this sets the data component of the HDU to a variable called data
    # data = hdu.data
    # then print it, with the option of specifying and index i.e. print(data[234])
    # note to self: non-zero data starts very far in so it appears to be all zero but is actually a sneaky snake
    # print(data)

    #pull out where the wavelengths start in the file
    start = hdu.header['CRVAL1']
    print (start)
    #pull out the resolution/step size of the file
    step = hdu.header['CDELT1']

    #ask for the length of the data file, how many data points it stores
    length = len(hdu.data)
    #print (length)
    #the place where the wavelengths stop is implicitly certain
    #it can be calculated as follows
    stop = start + step*length
    #print (stop)
    #makes x values for all the data points by taking the range and dividing it into equal parts according to the length of the file
    array = np.linspace(start, stop, length)

    #plot the array of x values vs the actual data then set up the labels and such
    plt.plot(array, hdu.data, label = file_name)
    
plt.xlabel('Wavelength (Angstroms)')
plt.ylabel('Flux')
plt.title('Spectrum of ' + location[0])
plt.grid(which = 'both')
plt.legend()
plt.show()