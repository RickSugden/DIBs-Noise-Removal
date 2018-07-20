
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.io import fits, ascii
import numpy as np 
import os

def colourGenerator():
    yield 'red'
    yield 'green'
    yield 'yellow'
    yield 'orange'
    yield 'cyan'
    yield 'blue'

colour = colourGenerator()

#make a list of files out of the directory (folder) where you're keeping them
list_of_files = (os.listdir('/home/pystudent/Desktop/Summer18_Research/MPI_FITS_files'))

#move the handling cursor to the same folder so we can look at them
os.chdir('/home/pystudent/Desktop/Summer18_Research/MPI_FITS_files') 


#this opens the file into a list like a normal python list
#hdulist = fits.open('HD41117_w346_n12_20150927_B.fits')

#run a for loop that will go through all the files in the desired folder
for file_number in range(len(list_of_files)):

    #set the name to the name of the current file from the list
    file_name = list_of_files[file_number]
    file_type = file_name.split('.')

    if (file_type [-1] == 'fits') :

        #the leading segment of the file name contains where in the sky the measurements were taken
        location = file_name.split("_")

        #open the desired FITS file in a list and then make it as a single object (hdu)
        hdulist = fits.open(file_name)
        hdu = hdulist[0]

        #pull out where the wavelengths start in the file
        start = hdu.header['CRVAL1']

        #pull out the resolution/step size of the file
        step = hdu.header['CDELT1']

        #ask for the length of the data file, how many data points it stores
        length = len(hdu.data)

        #the place where the wavelengths stop is implicitly certain
        #it can be calculated as follows
        stop = start + step*length
        
        #makes x values for all the data points by taking the range and dividing it into equal parts according to the length of the file
        array = np.linspace(start, stop, length)

        plt.ylim(0,400)
        #plot the array of x values vs the actual data then set up the labels and such
        plt.plot(array, hdu.data, label = location[0])

    elif file_type[-1] == 'txt':

        print("elif is running")
        name_split = file_name.split("_")
        molecule = name_split[0]

        XS_list = []
        angstrom_list = []

        # open the file and give it a "pointer" called f
        # this pointer can be used to reference a location in the file but it's not actually the information stored in the file
        # it is like a cursor (pointing at a line) the first line is where it starts
        with open(os.path.join(file_name), "r") as f:
            
        
            for line in f:

                #remove the new line markers and split up the WN and XS into a list called line that contains two strings
                line = line.replace('\n', '')
                line = line.replace('\t', '   ')
                line = line.split('   ')
                
                #separate the list called line into two variables
                
                #wavelength is being read in nm
                wavelength = float(line[0].strip()) 

                #immediately convert wavelength into angstroms 
                angstrom = 10*wavelength

                #XS is being read as cm^2
                XS = -4*10**21*float(line[1].strip())
                XS+=380
                
                #store them in the premade (and empty) list
                angstrom_list.append([angstrom])
                XS_list.append([XS])

        #plt.twinx() 
        #plt.ylim(0,1*10**-19)
        #form the plot
        plt.plot(angstrom_list, XS_list, color = next(colour), linestyle = '-',label = molecule)


plt.xlim(3000,3400)
plt.grid()
plt.legend(loc = 'upper left')
plt.xlabel('Wavelength (Angstroms)')
plt.ylabel('Flux')
plt.title('Spectrum of ' + location[0] + " compared with ozone cross sections")
plt.show()