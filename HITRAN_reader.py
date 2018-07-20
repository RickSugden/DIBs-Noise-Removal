import matplotlib.pyplot as plt 
import os
import numpy as np

def colourGenerator():
    yield 'blue'
    yield 'red'
    yield 'green'
    yield 'yellow'
    yield 'orange'
    yield 'purple'
    yield 'brown'
    yield 'black'
    yield 'teal'
    yield 'pink'

colour = colourGenerator()


list_of_files = (os.listdir('/home/pystudent/Desktop/Summer18_Research/HITRAN_xsections'))
os.chdir('/home/pystudent/Desktop/Summer18_Research/HITRAN_xsections') 

for file_number in range(len(list_of_files)):

    file_name = list_of_files[file_number]

    XS_list = []
    angstrom_list = []

    # open the file and give it a "pointer" called f
    # this pointer can be used to reference a location in the file but it's not actually the information stored in the file
    # it is like a cursor (pointing at a line) the first line is where it starts
    with open(os.path.join(file_name), "r") as f:
        
        #extract the element (the first line in the file)
        molecule = f.readline()
        #print (molecule)

        #extract the wavenumber range
        wavenumber_range = f.readline()
        #print (wavenumber_range)

        # skip the headers
        next(f)
        next(f)

        for line in f:

            #remove the new line markers and split up the WN and XS into a list called line that contains two strings
            line = line.replace('\n', '')
            line = line.split('   ')
            
            #separate the list called line into two variables

            #wave number is being read as cm^-1
            wave_number = float(line[0].strip()) 

            #immediately convert wave number into angstroms 
            angstrom = (1/wave_number)*10**8
        
            #XS is being read as cm^2
            XS = float(line[1].strip())
            
            #store them in the premade (and empty) list
            angstrom_list.append(angstrom)
            XS_list.append(XS)


    #convert the wave_number_list into an Angstrom list


    #form the plot
    plt.plot(angstrom_list, XS_list, color = next(colour), linestyle = '-', label = file_name)


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

diff_list=[]

for line in range((len(angstrom_list)-1)):
    # if angstrom_list[line+1] == None:
    #    break

    diff_list.append(angstrom_list[line+1]-angstrom_list[line])
diff_list = 1/diff_list
end = len(diff_list)
x = np.linspace(0,end,end)

plt.plot(x,diff_list,color = 'r')
plt.show()

