# -*- coding: utf-8 -*-
"""
Created on Fri May  6 16:04:45 2022

@author: Vapson
"""

import os
coding_home = r'H:\h\rain\revised_results\nc_revised_coding' # Please change the coding work folder at your own computer
os.chdir(coding_home)
import basefunc
import numpy as np

data_home = r'H:\h\rain\revised_results' # Please change the data folder at your own computer
os.chdir(data_home)

def f_normal(inputs):
    """
    According to lower design standards assumption (see supplementary Table S1)
    
                motorway et.al return period/year, tertiary, railways design return period/year
    high income：10, 5, 30
    upper middle income：5, 2 ,20
    low middle/low income：2, 0, 10
    
    inputs[0]: income group index. 1: low income group, 2: lower middle income group, 3: upper middle income group, 4: high income group
    inputs[1]: assets_type
    inputs[2:]: new return period in the future. 0: 1.1years, 1: 2years, 2: 5years, 3: 10years, 4: 20years, 5: 30years, 6: 50years, 7: 100years 
    
    output: the proportion of new return period to the historical design return period
    """
    income=inputs[0]
    assets_type=inputs[1]
    new_rt=inputs[-8:]
    y=-1.0
    if assets_type==1:
        if income==1 or income==2: 
            y=(new_rt[1]-2.0)/2.0                           
        elif income==3: 
            y=(new_rt[2]-5.0)/5.0 
        elif  income==4: 
            y=(new_rt[3]-10.0)/10.0  
        else:
            y=-1.0   
    elif assets_type==2:
        if income==1 or income==2:
            y=-1.0
        elif income==3:
            y=(new_rt[1]-2.0)/2.0             
        elif income==4:    
            y=(new_rt[2]-5.0)/5.0              
        else:
            y=-1.0
    elif assets_type==3:
        if income==1 or income==2:
            y=(new_rt[3]-10.0)/10.0  
        elif income==3:
            y=(new_rt[4]-20.0)/20.0            
        elif income==4:    
            y=(new_rt[5]-30.0)/30.0             
        else:
            y=-1.0        
    return  y

def f_strong(inputs):
    """
    According to higher design standards assumption (see supplementary Table S1)
    
                return period/years: motorway et.al, tertiary, railways
    high income：20, 10, 50
    upper middle income：10, 5, 30
    low middle/low income：5, 0, 20
    
    inputs[0]: income group index. 1: low income group, 2: lower middle income group, 3: upper middle income group, 4: high income group
    inputs[1]: assets_type
    inputs[2:]: new return period in the future. 0: 1.1years, 1: 2years, 2: 5years, 3: 10years, 4: 20years, 5: 30years, 6: 50years, 7: 100years 
    
    output: the proportion of new return period to the historical design return period
    """
    income=inputs[0]
    assets_type=inputs[1]
    new_rt=inputs[-8:]
    y=-1.0
    if assets_type==1:
        if income==1 or income==2: 
            y=(new_rt[2]-5)/5                            
        elif income==3: 
            y=(new_rt[3]-10)/10  
        elif  income==4: 
            y=(new_rt[4]-20)/20 
        else:
            y=-1.0    
    elif assets_type==2:
        if income==1 or income==2:
            y=-1.0
        elif income==3:
            y=(new_rt[2]-5)/5          
        elif income==4:    
            y=(new_rt[3]-10)/10 
        else:
            y=-1.0
    elif assets_type==3:
        if income==1 or income==2:
            y=(new_rt[4]-20)/20 
        elif income==3:
            y=(new_rt[5]-30)/30      
        elif income==4:    
            y=(new_rt[6]-50)/50          
        else:
            y=-1.0       
    return  y


# main
types=['motorway','trunk','primary','secondary','tertiary','railway']
for name in types:
    scens=['rcp45','rcp85']
    times=['20302059','20702099']
    for scen in scens:
        for time in times:
            if name=='motorway' or name=='trunk' or name=='primary' or name=='secondary':
                assets_type=1.0
            if name=='tertiary':
                assets_type=2.0
            if name=='railway':
                assets_type=3.0
              
            assets_type=np.full((1,720,1440),assets_type)
            income=basefunc.getRaster('income_group.tif')
            income=income.reshape(1,720,1440)
            new_rt=basefunc.getRaster('./results_for_gev/newRT_under_'+scen+'_'+time+'_mme.tif')
            
            array=np.concatenate((income,assets_type,new_rt),axis=0)
            rt_change=np.apply_along_axis(f_strong,0,array)
            rt_change=rt_change.reshape(1,720,1440)
               
            length=basefunc.getRaster('./GISdata/RoadandRailway/global_'+name+'_720vs1440.tif')
            length=length.reshape(1,720,1440)
            out=np.concatenate((length,rt_change),axis=0)
            
            ref_tif='./ref_tif.tif'
            output_path='./results_for_rt_change/'+name+'_under_'+scen+'_'+time+'_mme.tif'
            basefunc.array2Raster(out,ref_tif,output_path)
      
