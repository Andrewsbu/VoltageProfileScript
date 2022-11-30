import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
import sys
actmass = 10
#%% GENERAL USER FUNTIONS
#if platform.node() == 'DESKTOP-L2QEF9I': #andrew AERTC PC
  #  scan_file_folder_path = 'C:/Users/Andrew/Box/Andrew and Patrick B.-Python Project -Cycling Data Analysis/Project Scripts/VoltageProfileScript/AN258-68-5E_100cycles.073 [SAMPLE DATA].xlsx'
#elif platform.node() == 'LAPTOP-GPVHLAR6':
 #   scan_file_folder_path = 'C:/Users/Andrew/Box/Andrew and Patrick B.-Python Project -Cycling Data Analysis/Project Scripts/VoltageProfileScript/AN258-68-5E_100cycles.073 [SAMPLE DATA].xlsx'
#elif platform.node() == 'DESKTOP-VATSK7K':
    #scan_file_folder_path = 'C:/Users/Patrick B/Box/Andrew and Patrick B.-Python Project -Cycling Data Analysis/Project Scripts/VoltageProfileScript/AN258-68-5E_100cycles.073 [SAMPLE DATA].xlsx'

#else:
    #sys.exit('Not a whitelisted file path. Add a filepath for this computer.')

def main():
    data = open_file(r"C:\Users\Patrick B\Desktop\MACCOR Data\Complete Data\PB273-14-1.2.089.xls")
    #print('Exported Data = \n', data)
    calcdata = spec_cap(actmass,data[0,:])
    #print('Specific Capcity = \n' ,calcdata)
    adjusted_cap_data = replace_cap(data,calcdata)
    #print('Adjusted Capacity Data = \n',adjusted_cap_data)
    #print('Index 1:',adjusted_cap_data[0][0],'\n Index 2:',adjusted_cap_data[1][0])
    #print(adjusted_cap_data.shape)
    stated = create_state_array(adjusted_cap_data)
    print(stated)
    cap,vol = create_state_array2(adjusted_cap_data)
    #print(len(cap))
    for caplst,vollst in zip(cap[:10],vol[:10]):
        ncap = caplst
        nvol = vollst
        for capindx,volindx in zip(ncap,nvol):
            #print(capindx,volindx)         
            plt.plot(capindx,volindx,'r')
    plt.show()
    
    return
   
    
    
    #    plt.plot(cap[cyc],vol[cyc])
    return 
    
    
def user_inputs(file): #More inputs to be added later
    rawdata = open(file)
    #theocap = input('Enter Theoretical Capacity:\n')
    #actmass = input('Enter Active Mass:\n')
    return rawdata
    
#%% FILE MANAGEMENT
def open_file(filename):
    rawdata = pd.read_excel(filename, skiprows=1, usecols=['Cyc#','mAmp-hr','Volts','State']) #reads excel as dataframe
    #print(rawdata)
    organizer = np.array((rawdata['mAmp-hr'],rawdata['Volts'],rawdata['State'],rawdata['Cyc#'])) #organizes select columns into numpy array
    #print(organizer[0,:])   
    return organizer


def replace_cap (data, spec_cap):
    data[0,:] = spec_cap
    adjusted_cap_data = data
    return adjusted_cap_data

def create_state_array (spec_cap_data):
    charge_data = pd.DataFrame(columns = ['mAmp-hr/g','Volts','State','Cyc#'])
    discharge_data = pd.DataFrame(columns = ['mAmp-hr/g','Volts','State','Cyc#'])
    # print(spec_cap_data.shape)
    converted_data = pd.DataFrame(spec_cap_data.T,index=range(spec_cap_data.shape[1]),columns = ['mAmp-hr/g','Volts','State','Cyc#'])
   

    for state,i in zip(converted_data.State,range(spec_cap_data.shape[1])):
        if state == 'C':
            #charge_data.append({'mAmp-hr/g':spec_cap_data[0][i]},ignore_index=True)
            #charge_data.append({'Volts':spec_cap_data[1][i]},ignore_index=True)
            #charge_data.append({'cycle #':spec_cap_data[3][i]},ignore_index=True)
            charge_data['mAmp-hr/g'] = [spec_cap_data[0][i]]
            charge_data['Volts'] = [spec_cap_data[1][i]]
            charge_data['State'] = [spec_cap_data[1,:]]
            charge_data['Cyc#'] = [spec_cap_data[3,:]]
            #pd.concat((charge_data,converted_data[i,]))

        elif state == 'D':
            #discharge_data.append({'mAmp-hr/g':spec_cap_data[0][i]},ignore_index=True)
            #discharge_data.append({'Volts':spec_cap_data[1][i]},ignore_index=True)
            #discharge_data.append({'cycle #':spec_cap_data[3][i]},ignore_index=True)
            discharge_data['mAmp-hr/g'] = [spec_cap_data[0][i]]
            discharge_data['Volts'] = [spec_cap_data[1][i]]
            discharge_data['State'] = [spec_cap_data[1,:]]
            discharge_data['Cyc#'] = [spec_cap_data[3,:]]
            #pd.concat((discharge_data,converted_data[i,]))
        else:
            pass

    return (charge_data, discharge_data)

def create_state_array2 (spec_cap_data):
    
    capcharlst = []
    volcharlst = []
    captemplst=[]
    voltemplst=[]
    
    for state,i in zip(spec_cap_data[2,:],range(spec_cap_data.shape[1])):
        if state == 'C':
            captemplst.append(spec_cap_data[0][i]) #Capacity
            voltemplst.append(spec_cap_data[1][i]) #Voltage
        elif state != 'C':
            if len(captemplst) > 0: #filter out empty lists
                capcharlst.append(captemplst)
                volcharlst.append(voltemplst)
                captemplst=[]
                voltemplst=[]
            else:
                pass
                
            
    return capcharlst,volcharlst

#def sep_by_cycle(charge_dataframe,discharge_dataframe):
    
 #   for i in charge_dataframe.Volts

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

