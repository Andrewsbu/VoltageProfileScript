import pandas as pd
import numpy as np

actmass = 10

def main():
    open_file('C:/Users/Andrew/Box/Andrew and Patrick B.-Python Project -Cycling Data Analysis/Project Scripts/VoltageProfileScript/AN258-68-5E_100cycles.073 [SAMPLE DATA].xlsx')
    #user_inputs()
    
    
def user_inputs(): #More inputs to be added later
    askfile = open_file(input('Enter file name [User directory]:\n'))
    #theocap = input('Enter Theoretical Capacity:\n')
    #actmass = input('Enter Active Mass:\n')
    return askfile
    

def open_file(filename):
    rawdata = pd.read_excel(filename, skiprows=1, usecols=['mAmp-hr','Volts','State']) #reads excel as dataframe
    
    organizer = np.array((rawdata['mAmp-hr'],rawdata['Volts'],rawdata['State'])) #organizes select columns into numpy array
    print(organizer[0,:])   
    
'''
Next Steps:
    - Calculate specific capacity from mAmp-h column and user input active mass (we'll just use a constant variable for now)
    - Charge/Discharge Diacriminator function
    
'''
main()