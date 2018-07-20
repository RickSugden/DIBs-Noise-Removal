import statistics as stats
import matplotlib.pyplot as plt
from astropy.io import fits, ascii
import numpy as np 
import os
import sys
print (sys.argv)

#manual setting of where the data should start and stop, it will also adjus the window
USEFUL_DATA_STARTS = 3050
USEFUL_DATA_STOPS = 3400

#the abundances are listed in Dobson Units in the order O3, NO2, SO2
#this will be used to adjust the data with a vertical stretch 
abundances = [260,0.04,90,20,30]
#we determine the max value in the list so that we can fit each as a % of the highest abundance
max_ab = max(abundances)

#the fit counter will be used to keep track of which fit file we are on (for baryocentric correction)
fit_count = 0
#the other counter is part of the mechanism to account for relative abundances
counter = 0

#define a colour generator so its not a bunch of red chaos
def colourGenerator():
    yield 'purple'
    yield 'green'
    yield 'yellow'
    yield 'orange'
    yield 'teal'
    yield 'grey'
    yield 'cyan'
    yield 'black'
    yield 'magenta'

colour = colourGenerator()

#make a list of files out of the directory (folder) where you're keeping them
list_of_files = (os.listdir('/home/pystudent/Desktop/Summer18_Research/MPI_FITS_files'))

#move the handling cursor to the same folder so we can look at them
os.chdir('/home/pystudent/Desktop/Summer18_Research/MPI_FITS_files') 


#run a for loop that will go through all the files in the desired folder
for file_number in range(len(list_of_files)):

    #set the name to the name of the current file from the list
    file_name = list_of_files[file_number]
    file_type = file_name.split('.')

    
    #as we run through the folder the first time, this picks out all FITS files
    if (file_type [-1] == 'fits') :

        #the leading segment of the file name contains where in the sky the measurements were taken
        location = file_name.split("_")

        #open the desired FITS file in a list and then make it as a single object (hdu)
        hdulist = fits.open(file_name)
        hdu = hdulist[0]
        data = hdu.data
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

        #each for loop runs along the x value array until it finds your specified/desired start/stop points
        #it then saves that position as a numeric index in the array
        for position in range(len(array)):
            value = array[position]
            if value > USEFUL_DATA_STOPS:
                stop_position = position
                break

        for position in range(len(array)):
            value = array[position]
            if value > USEFUL_DATA_STARTS:
                start_position = position
                break

        #these lines manually truncate the x array and the data array to the new found start/stop
        array = array[start_position:stop_position]
        data = data[start_position:stop_position]

        #define the speed of light (does not need to be too precise)
        c = 2.99*10**8

        #these are manual inputs of where the Na (sodium) lines appear without cloud or baryocentric correction
        #this is so that each can be corrected based on its own error
        
        lambda_observed = [3302.38,3302.16,3302.46]
        #based on where the sodium lines are we can deduce how fast the cloud is moving
        #then make a correction factor based on that and have the fit counter move to the next one so we get the different original peak locations
        cloud_velocity = c*(lambda_observed[fit_count] - 3302.8)/3302.8
        cloud_correction = (1-cloud_velocity/c)
        fit_count +=1

        #this makes a correction factor based on an embedded baryocentric correction value from header
        baryocentric_correction = (1+hdu.header ["HIERARCH ESO QC VRAD BARYCOR"]/c)
        
        #CALCULATING THE AVERAGE OF THE HDU DATA WITHIN THE FRAME
        spectrum_average = max(data) #alternatively: stats.median
        
        #you can plot it with the correction factors applied to the X VALUE (its a horizontal shift)
        #
        plt.plot(array*cloud_correction*baryocentric_correction, data/spectrum_average, label = location[0])

for file_number in range(len(list_of_files)):

    #set the name to the name of the current file from the list
    file_name = list_of_files[file_number]
    file_type = file_name.split('.')
    if file_type[-1] == 'txt':

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

                #XS is being read as cm^2 then scaled to fit the spectrum data
                XS = float(line[1].strip())
                
                #store them in the premade (and empty) list
                angstrom_list.append(angstrom)
                XS_list.append(XS)


            #this loop will run through all the x values for the cross section data. 
            #once it finds the point at which you declared at the top that it's useful, it sets a new start point
            for position in range(len(angstrom_list)):
                    value = angstrom_list[position]
                    
                    if value > USEFUL_DATA_STARTS:
                        start_position = position
                        break

            #this does the same but for the end position
            for position in range(len(angstrom_list)):
                    value = angstrom_list[position]
                   
                    if value > USEFUL_DATA_STOPS:
                        stop_position = position
                        break

            #get the lists to start and stop where they are told to 
            angstrom_list = angstrom_list[start_position: stop_position]
            XS_list = XS_list[start_position:stop_position]

            xs_max = max(XS_list)

            for i in range(len(XS_list)):

                XS_list[i] = (XS_list[i])/-xs_max *(abundances[counter]/max_ab) +0.9
            counter += 1

        plt.plot(angstrom_list, XS_list, color = next(colour), linestyle = '-',label = molecule)

    else:
        pass

plt.grid()
plt.legend()
plt.xlabel('Wavelength (Angstroms)')
plt.ylabel('Flux')
plt.title('Spectrum of ' + location[0] + " compared with various cross sections")
plt.xlim(USEFUL_DATA_STARTS,USEFUL_DATA_STOPS)
plt.show()
plt.close()
plt.clf()
