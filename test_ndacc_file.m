%mkdir makes a directory with a starting place of the current directory
%mkdir ('text_files');

%opens the file by name, declares it's for writing
%if it doesn't exist it will write/create one
fileID = fopen('data.txt','w');

%this WRITES in the form (directory_object, text)
fprintf(fileID,'hi\n wiley was here'); %why doesn't \n do anything?

%close the file
fclose(fileID);

%creates a .m file
matfileID = edit('ndacc.m');

%set the directory of the data going in
data_in = 'C:\Users\rickj\Documents\UWO_Summer_18\HDF_conversion_samples';

%set the directory of the data going out
path_out = 'C:\Users\rickj\Documents\UWO_Summer_18\HDF_conversion_trials';

%call the function
%save_ndacc_hdf_TEMP(data_in,path_out)



