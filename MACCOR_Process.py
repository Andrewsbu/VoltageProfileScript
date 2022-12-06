#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def main(gui_file,actmass):
    #actmass = input('Active Mass: ')
    data = open_file(gui_file) #Opens file from GUI.py
    calcdata = spec_cap(actmass,data[0,:]) #Converts MACCOR capacity to specific capacity
    adjusted_cap_data = replace_cap(data,calcdata) #Relplaces MACCOR capcicty with calculated specific capacity
    final_data = echem_proc(adjusted_cap_data) #Organizes into (dis)charge voltage and capacity by cycle 
    #vprof = plot_echem(final_data) #Plots data in various ways.
    
    return final_data


#%% ECHEM CALCS
def spec_cap(activemass,mAmph):
    
    spec_cap = mAmph / activemass
    return spec_cap

#%% FILE MANAGEMENT
def open_file(filename):
    rawdata = pd.read_excel(filename, skiprows=1, usecols=['mAmp-hr','Volts','State']) #reads excel as dataframe
    #print(rawdata)
    organizer = np.array((rawdata['mAmp-hr'],rawdata['Volts'],rawdata['State'])) #organizes select columns into numpy array
    #print(organizer[0,:])   
    return organizer


def replace_cap (data, spec_cap):
    data[0,:] = spec_cap
    adjusted_cap_data = data
    return adjusted_cap_data

def echem_proc (spec_cap_data):
    
    #Empty lists that will be filled by for loops
    capcharlst = [] #Charge Capacity
    volcharlst = [] #Charge Voltage
    capdislst = [] #Discharge Capacity
    voldislst = [] #Discharge Voltage
    
    #Temporary lists used to appened to permanent data lists
    captemplst=[]
    voltemplst=[]
    
#Charge Loop:
    for state,i in zip(spec_cap_data[2,:],range(spec_cap_data.shape[1])):
        if state == 'C':
            captemplst.append(spec_cap_data[0][i]) #Capacity column
            voltemplst.append(spec_cap_data[1][i]) #Voltage column
        elif state != 'C':
            if len(captemplst) > 0: #filter non "C" states
                capcharlst.append(captemplst)
                volcharlst.append(voltemplst)
                captemplst=[] #Clear temperoary lists
                voltemplst=[] #
            else:
                pass
#Discharge Loop:
    for state,i in zip(spec_cap_data[2,:],range(spec_cap_data.shape[1])):
        if state == 'D':
            captemplst.append(spec_cap_data[0][i]) #Capacity column
            voltemplst.append(spec_cap_data[1][i]) #Voltage column
        elif state != 'D':
            if len(captemplst) > 0: #filter non "D" states
                capdislst.append(captemplst)
                voldislst.append(voltemplst)
                captemplst=[] #Clear temperoary lists
                voltemplst=[] #
            else:
                pass
                
            
    return [[capcharlst,volcharlst],[capdislst,voldislst]]

#%% PLOTTING
def plot_echem(data): # Data = the processed data from earlier script functions
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(14,5),dpi=100) #Creating the figure parameters
    charge = data[0] # Charge voltage & capacity data
    discharge = data[1] # Disharge voltage & capacity data
    
    #%% Voltage Profile:
    
    #Charge Plot
    for cap,vol in zip(charge[0],charge[1]): #cap = capacity, vol = voltage
        ax1.plot(cap,vol,'r',lw=0.75)
        
    #Discharge Plot
    for cap,vol in zip(discharge[0],discharge[1]):
        ax1.plot(cap,vol,'b',lw=0.75)
        
    ax1.set_xlabel('Specific Capacity (mAh g$^{-1}$)',fontsize=16)
    ax1.set_ylabel('Voltage (V)',fontsize=16)
    ax1.tick_params(axis='both',labelsize=14)
    ax1.margins(x=0,y=0)
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
      
    #%% Capcity vs Cycle Number:
    
    cycnum = len(data[0][0])+1
    endcaplst = []
    caps = data[0][0] #All charge cycle capacities

    for cap in caps:
        endcaplst.append(cap[-1])
        
    ax2.plot(range(1,cycnum),endcaplst,'m.',ms=15,label='Capacity')
    ax2.set_xlabel('Cycle Number',fontsize=16)
    ax2.set_ylabel('Specific Capacity (mAh g$^{-1}$)',fontsize=16)
    ax2.tick_params(axis='both',labelsize=14)
    ax2.margins(x=0,y=0)
    #ax2.set_ylim(min(endcaplst),max(endcaplst)+25) #Add some headroom to the plot
    #ax2.xaxis.set_major_locator(ticker.MultipleLocator(5)) #Too specific for the variety of data this script can plot
    
    #%% Coulombic Efficiency:
    
    #Capacity Data
    charcaps = data[0][0]
    discharcaps= data[1][0]
    
    #List to append
    cou_eff = []
    
    for ccap,dcap in zip(charcaps,discharcaps):
        cou_eff.append((dcap[-1]/ccap[-1])*100) #appending Coulombic Efficiency calaculation
    
    ax3 = ax2.twinx()
    
    ax3.plot(range(1,cycnum),cou_eff,'k.',ms=10,label="Coulomb. Eff.")
    ax3.set_ylabel('Coulombic Efficiency (%)',fontsize=16)
    ax3.tick_params(axis='both',labelsize=14)
    if max(cou_eff) > 100:
        ax3.set_ylim(0,max(cou_eff))
    else:
        ax3.set_ylim(0,100)

