import matplotlib.pyplot as plt 
import os

def colourGenerator():
    yield 'blue'
    yield 'red'
    yield 'green'
    yield 'yellow'
    yield 'orange'
    yield 'teal'

colour = colourGenerator()

list_of_files = (os.listdir('/home/pystudent/Desktop/Summer18_Research/MPI-Mainz_xsections'))
os.chdir('/home/pystudent/Desktop/Summer18_Research/MPI-Mainz_xsections') 


for file_number in range(len(list_of_files)):

    file_name = list_of_files[file_number]

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
            XS = float(line[1].strip())
            
            #store them in the premade (and empty) list
            angstrom_list.append([angstrom])
            XS_list.append([XS])


    #convert the wave_number_list into an Angstrom list


    #form the plot
    plt.plot(angstrom_list, XS_list, color = next(colour), linestyle = '-',label = molecule)

    
#set up labels and communication
plt.title('Absorption Crossections')
plt.xlabel("Wavelength(Angstroms)")
plt.ylabel("XS(cm^2)")
plt.grid()
plt.legend()
#this is an optional line where if you were to zoom in on the huggins band it reveals them plt.yscale('log')

#display and close
plt.show()
plt.close()
plt.clf()