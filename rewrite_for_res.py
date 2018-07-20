import numpy as np 
import matplotlib.pyplot as plt 
import scipy.integrate 
import os

####################################
#READ THE FILE AND MAKE A LIST
XS_list = []
angstrom_list = []

# open the file and give it a "pointer" called f
# this pointer can be used to reference a location in the file but it's not actually the information stored in the file
# it is like a cursor (pointing at a line) the first line is where it starts
with open(os.path.join('/home/pystudent/Desktop/Summer18_Research/MPI-Mainz_xsections/NO2_edit.txt'), "r") as f:
    
    #extract the element (the first line in the file)
    molecule = f.readline()
    #print (molecule)

    #extract the wavenumber range
    wavenumber_range = f.readline()
    #print (wavenumber_range)


    for line in f:

        #remove the new line markers and split up the WN and XS into a list called line that contains two strings
        line = line.replace('\n', '')
        line = line.split('   ')
        
        #separate the list called line into two variables

        #wave number is being read as cm^-1
        wave_length = float(line[0].strip()) 

        #immediately convert wave number into angstroms 
        angstrom = wave_length
        #XS is being read as cm^2
        XS = float(line[1].strip())
        
        #store them in the premade (and empty) list
        angstrom_list.append(angstrom)
        XS_list.append(XS)


import scipy.interpolate
'''
file_name = 'spline_data.csv'
#this function returns a list of strings
data = parseTextFile(file_name)
data = np.array(data).astype(np.float64)
print(data)
x,y = data.T
'''

plt.plot(angstrom_list,XS_list, marker = None)
#plt.show()
plt.clf()
plt.close()

spline = scipy.interpolate.CubicSpline(angstrom_list,XS_list)
x_spline = np.linspace(300,340,20000)
y_spline = spline(x_spline)

plt.plot(x_spline, y_spline)
#plt.show()
plt.clf()
plt.close()

############################################

#REWRITE THE NEW FILE
new_file_name = 'NO2_rewrite.txt'
wl = 300.000
with open(new_file_name,'w') as f:

    for i in range(20000):

        
        str_line = str('{:.3f}'.format(round(wl,3)))+ '\t' +str(round(float(spline(wl)),27))
        f.write( str_line+ '\n')

        wl+=0.002
        
