import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
import sys
actmass = 10
#%% GENERAL USER FUNTIONS
if platform.node() == 'DESKTOP-L2QEF9I': #andrew AERTC PC
    scan_file_folder_path = 'C:\Users\Patrick B\Box\Andrew and Patrick B.-Python Project -Cycling Data Analysis\Project Scripts\'
else:
    sys.exit('Not a whitelisted file path. Add a filepath for this computer.')

def main():
    data = open_file(scan_file_folder_path)
    print('Exported Data = \n', data)
    calcdata = spec_cap(actmass,data[0,:])
    print('Specific Capcity = \n' ,calcdata)
    adjusted_cap_data = replace_cap(data,calcdata)
    print('Adjusted Capacity Data = \n',adjusted_cap_data)
    print('Index 1:',adjusted_cap_data[0][0],'\n Index 2:',adjusted_cap_data[1][0])
    #print(adjusted_cap_data.shape)
    #stated = create_state_array(adjusted_cap_data)
    #print(stated)
    stated2 = create_state_array2(adjusted_cap_data)
    print(stated2)
    print(len(stated2))
    print(range(len(stated2)))
          
    #for cyc in range(len(stated2)):
    #    plt.plot(stated2[cyc][0],stated2[cyc][1])
    return 
    
    
def user_inputs(): #More inputs to be added later
    askfile = open_file(input('Enter file name [User directory]:\n'))
    #theocap = input('Enter Theoretical Capacity:\n')
    #actmass = input('Enter Active Mass:\n')
    return askfile
    
#%% FILE MANAGEMENT
def open_file(filename):
    rawdata = pd.read_excel(filename, skiprows=1, usecols=['mAmp-hr','Volts','State']) #reads excel as dataframe
    print(rawdata)
    organizer = np.array((rawdata['mAmp-hr'],rawdata['Volts'],rawdata['State'])) #organizes select columns into numpy array
    #print(organizer[0,:])   
    return organizer


def replace_cap (data, spec_cap):
    data[0,:] = spec_cap
    adjusted_cap_data = data
    return adjusted_cap_data

def create_state_array (spec_cap_data):
    count = 0
    charge_data = pd.DataFrame()
    discharge_data = pd.DataFrame()
    while count != spec_cap_data.shape[1]:
        for state,i in zip(spec_cap_data[2,:],range(spec_cap_data.shape[1])):
            if state == 'C':
                charge_data['mAmp-hr/g'] = [spec_cap_data[0][i]]
                charge_data['Volts'] = [spec_cap_data[1][i]]
                #charge_data['State'] = [spec_cap_data[1,:]]

            elif state == 'D':
                discharge_data['mAmp-hr/g'] = [spec_cap_data[0][i]]
                discharge_data['Volts'] = [spec_cap_data[1][i]]
                #discharge_data['State'] = [spec_cap_data[1,:]]

            else:
                pass
        count = count + 1
    return (charge_data, discharge_data)

def create_state_array2 (spec_cap_data):
    size = spec_cap_data.shape[1]
    c_cyclst = []
    d_cyclst = []
    c_data = np.zeros((2,size))
    d_data = np.zeros((2,size))
    for state,i in zip(spec_cap_data[2,:],range(spec_cap_data.shape[1])):
        if state == 'C':
            c_data[0][i] = spec_cap_data[0][i] #Capacity
            c_data[1][i] = spec_cap_data[1][i] #Volts
            c_cyclst.append(c_data[0][i],c_data[1][i])
            
        elif state == 'D':
            d_data[0][i] = spec_cap_data[0][i] #Capacity
            d_data[1][i] = spec_cap_data[1][i] #Volts
            
        else:
            pass
    return c_cyclst
    
#%% ECHEM CALCS
def spec_cap(activemass,mAmph):
    
    spec_cap = mAmph / activemass
    return spec_cap
    #print(spec_cap) 
    
    
#%% PLOTTING

def plot_vprof(proc_data):
    c_data = proc_data[0]
    d_data = proc_data[1]
    print(proc_data[1])
    #Extracting Charge capacity and voltage
    c_caparray = pd.DataFrame.to_numpy(c_data[0])
    c_voltarray = np.array(c_data['Volts'])
    #extracting dicharge capacity and voltage
    d_caparray = np.array(d_data['mAmp-hr/g'])
    d_voltarray = np.array(d_data['Volts'])
    print(c_caparray)

'''
Next Steps:
    - Calculate specific capacity from mAmp-h column and user input active mass (we'll just use a constant variable for now) = DONE
    - Charge/Discharge Diacriminator function = DONE
    - Create a function to plot charge and discharge data
'''
main()




