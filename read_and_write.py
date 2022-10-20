import pandas as pd
import numpy as np

actmass = 10
#%% GENERAL USER FUNTIONS
def main():
    data = open_file('C:/Users/Patrick B/Box/Andrew and Patrick B.-Python Project -Cycling Data Analysis/Project Scripts/VoltageProfileScript/AN258-68-5E_100cycles.073 [SAMPLE DATA].xlsx')
    print('Exported Data =', data)
    print('')
    calcdata = spec_cap(actmass,data[0,:])
    print('Specific Capcity =',calcdata)
    print('')
    adjusted_cap_data = replace_cap(data,calcdata)
    print('Adjusted Capacity Data =',adjusted_cap_data)
    
    #user_inputs()
    
    
def user_inputs(): #More inputs to be added later
    askfile = open_file(input('Enter file name [User directory]:\n'))
    #theocap = input('Enter Theoretical Capacity:\n')
    #actmass = input('Enter Active Mass:\n')
    return askfile
    
#%% FILE MANAGEMENT
def open_file(filename):
    rawdata = pd.read_excel(filename, skiprows=1, usecols=['mAmp-hr','Volts','State']) #reads excel as dataframe
    
    organizer = np.array((rawdata['mAmp-hr'],rawdata['Volts'],rawdata['State'])) #organizes select columns into numpy array
    #print(organizer[0,:])   
    return organizer


def replace_cap (data, spec_cap):
    data[0,:] = spec_cap
    adjusted_cap_data = data
    return adjusted_cap_data
#%% ECHEM CALCS
def spec_cap(activemass,mAmph):
    
    spec_cap = mAmph / activemass
    return spec_cap
    #print(spec_cap) 
    
'''
Next Steps:
    - Calculate specific capacity from mAmp-h column and user input active mass (we'll just use a constant variable for now)
    - Charge/Discharge Diacriminator function
    
'''
main()

