import statistics as stats
import matplotlib.pyplot as plt
from astropy.io import fits, ascii
import numpy as np 
import os
import sys
print (sys.argv)

#manual setting of where the data should start and stop, it will also adjus the window
USEFUL_DATA_STARTS = 3000
USEFUL_DATA_STOPS = 3400

#the abundances are listed in Dobson Units in the order NO2, SO2
#this will be used to adjust the data with a vertical stretch 
abundances = [9,0.4,2,3]
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
    #yield 'yellow'
    yield 'orange'
    yield 'teal'
    yield 'grey'
    yield 'cyan'
    yield 'black'
    yield 'magenta'

colour = colourGenerator()

#make a list of files out of the directory (folder) where you're keeping them
list_of_files = (os.listdir('/home/pystudent/Desktop/Summer18_Research/text_spectra'))

#move the handling cursor to the same folder so we can look at them
os.chdir('/home/pystudent/Desktop/Summer18_Research/text_spectra') 


#run a for loop that will go through all the files in the desired folder
for file_number in range(len(list_of_files)):

    #set the name to the name of the current file from the list
    file_name = list_of_files[file_number]
    file_type = file_name.split('_')

    
    #as we run through the folder the first time, this picks out all FITS files
    if (file_type [0] == 'HD148937') :

        name_split = file_name.split("_")
        location = name_split[0]

        angstrom_list = []
        flux_list = []
        

        # open the file and give it a "pointer" called f
        # this pointer can be used to reference a location in the file but it's not actually the information stored in the file
        # it is like a cursor (pointing at a line) the first line is where it starts
        with open(os.path.join(file_name), "r") as f:
                    
            for line in f:

                #remove the new line markers and split up the wavelength and flux into a list called line that contains two strings
                line = line.replace('\n', '')
                line = line.strip()
                line = line.split('   ')
                
                #separate the list called line into two variables
                
                #wavelength is being read in angstroms
                angstrom = float(line[0].strip())

                #flux is being read without units or in energy per area
                flux = float(line[1].strip())
                
                #store them in the premade (and empty) list
                angstrom_list.append(angstrom)
                flux_list.append(flux)


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
        flux_list = flux_list[start_position:stop_position]

        #form the plot
        plt.plot(angstrom_list, flux_list, color = next(colour), linestyle = '-',label = location)


    if  file_type[0] != 'HD148937':
        print(file_name)
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

                XS_list[i] = (XS_list[i])/-xs_max*(abundances[counter]/max_ab)+1
            counter += 1

        plt.plot(angstrom_list, XS_list, color = next(colour), linestyle = '-',label = molecule)

    else:
        pass

plt.grid()
plt.legend()
plt.xlabel('Wavelength (Angstroms)')
plt.ylabel('Flux')
#plt.title('Spectrum of ' + location[0] + " compared with various cross sections")
plt.xlim(USEFUL_DATA_STARTS,USEFUL_DATA_STOPS)
plt.show()
plt.close()
plt.clf()
