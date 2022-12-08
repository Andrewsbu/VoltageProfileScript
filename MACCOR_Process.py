#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def main(gui_file,actmass):
    data = open_file(gui_file) #Opens file from GUI.py
    calcdata = spec_cap(actmass,data[0,:]) #Converts MACCOR capacity to specific capacity (mAh/g)
    adjusted_cap_data = replace_cap(data,calcdata) #Relplaces MACCOR capcicty with calculated specific capacity
    final_data = echem_proc(adjusted_cap_data) #Organizes into (dis)charge voltage and capacity by cycle 
    
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

# Color gradients help discern direction of charge and discharge in the voltage profile
def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

blue ='#0000FF'
cyan ='#00FFFF'
red = '#FA0000'
magenta = '#FF00FF'


def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]

#%% Figure Parameters

def plot_echem(data): # Data = the processed data from earlier script functions
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(14,5),dpi=100) #Creating the figure parameters
    charge = data[0] # Charge voltage & capacity data
    char_color = get_color_gradient(red, magenta, len(charge[0]))
    discharge = data[1] # Disharge voltage & capacity data
    dis_color = get_color_gradient(blue, cyan, len(discharge[0]))
    
#%% Voltage Profile:
    
    #Charge Plot
    for cap,vol,cc in zip(charge[0],charge[1],char_color): #cap = capacity, vol = voltage
        ax1.plot(cap,vol,color=cc,lw=0.75)
        
    #Discharge Plot
    for cap,vol,dc in zip(discharge[0],discharge[1],dis_color):
        ax1.plot(cap,vol,color=dc,lw=0.75)
        
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
    #ax2.xaxis.set_major_locator(ticker.MultipleLocator(5)) #Other specifc parameters
    
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
    
    fig.legend(loc=3, bbox_to_anchor=(0,0), bbox_transform=ax2.transAxes)
