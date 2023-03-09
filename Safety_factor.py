# -*- coding: utf-8 -*-
"""
Created on Sat May  7 19:39:56 2022

@author: Vapson
"""


import numpy as np
import basefunc

def f_normal(inputs):
    """
    According to lower design standards assumption (see supplementary Table S1)
    
                design return period/years: motorway et.al, tertiary, railways
    high income：10, 5, 30
    upper middle income：5, 2 ,20
    low middle/low income：2, 0, 10
    
    inputs[0]: income group index. 1: low income group, 2: lower middle income group, 3: upper middle income group, 4: high income group
    inputs[1]: assets_type. 1: Motorway/Trunk/Primary/Secondary,  2: Tertiary, 3: Railway
    inputs[2:]: new return period in the future. 0: 1.1years, 1: 2years, 2: 5years, 3: 10years, 4: 20years, 5: 30years, 6: 50years, 7: 100years 
    
    output: the proportion of new return period to the historical design return period
    """
    income=inputs[0]
    assets_type=inputs[1]
    new_pre=inputs[-16:-8]
    his_pre=inputs[-8:]
    y=-1.0
    if assets_type==1:
        if income==1 or income==2: 
            y=new_pre[1]/his_pre[1]                                
        elif income==3: #upper middle
            y=new_pre[2]/his_pre[2]
        elif  income==4: 
            y=new_pre[3]/his_pre[3]  
        else:
            y=-1.0   
    elif assets_type==2:
        if income==1 or income==2:
            y=-1.0
        elif income==3:
            y=new_pre[1]/his_pre[1]             
        elif income==4:    
            y=new_pre[2]/his_pre[2]             
        else:
            y=-1.0
    elif assets_type==3:
        if income==1 or income==2:
            y=new_pre[3]/his_pre[3] 
        elif income==3:
            y=new_pre[4]/his_pre[4]              
        elif income==4:    
            y=new_pre[5]/his_pre[5]             
        else:
            y=-1.0        
    return  y

def f_strong(inputs):
    """
    According to higher design standards assumption (see supplementary Table S1)
    
                design return period/years: motorway et.al, tertiary, railways
    high income：20, 10, 50
    upper middle income：10, 5, 30
    low middle/low income：5, 0, 20
    
    inputs[0]: income group index. 1: low income group, 2: lower middle income group, 3: upper middle income group, 4: high income group
    inputs[1]: assets_type. 1: Motorway/Trunk/Primary/Secondary,  2: Tertiary, 3: Railway
    inputs[2:]: new return period in the future. 0: 1.1years, 1: 2years, 2: 5years, 3: 10years, 4: 20years, 5: 30years, 6: 50years, 7: 100years 
    
    output: the proportion of new return period to the historical design return period   
    """
    income=inputs[0]
    assets_type=inputs[1]
    new_pre=inputs[-16:-8]
    his_pre=inputs[-8:]
    y=-1.0
    if assets_type==1:
        if income==1 or income==2: 
            y=new_pre[2]/his_pre[2]                               
        elif income==3: 
            y=new_pre[3]/his_pre[3] 
        elif  income==4: 
            y=new_pre[4]/his_pre[4] 
        else:
            y=-1.0    
    elif assets_type==2:
        if income==1 or income==2:
            y=-1.0
        elif income==3:
            y=new_pre[2]/his_pre[2]       
        elif income==4:    
            y=new_pre[3]/his_pre[3]
        else:
            y=-1.0
    elif assets_type==3:
        if income==1 or income==2:
            y=new_pre[4]/his_pre[4]
        elif income==3:
            y=new_pre[5]/his_pre[5]     
        elif income==4:    
            y=new_pre[6]/his_pre[6]     
        else:
            y=-1.0       
    return  y


# main
types=['motorway','trunk','primary','secondary','tertiary','railway']
his_pre=basefunc.getRaster('./results_for_gev/historical_mme.tif')
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
            new_pre=basefunc.getRaster('./results_for_gev/'+scen+'pre'+time+'_mme.tif')
             
            array=np.concatenate((income,assets_type,new_pre,his_pre),axis=0)
            amf=np.apply_along_axis(f_normal,0,array)
            
            ref_tif='./ref_tif.tif'
            output_path='./results_for_amf/f_normal/'+name+'_under_'+scen+'_'+time+'_mme.tif'
            basefunc.array2Raster(amf,ref_tif,output_path)

    
# mean results of all types 
types=['motorway','trunk','primary','secondary','tertiary','railway']
scens=['rcp45','rcp85']
times=['20302059','20702099']
for scen in scens:
    for time in times:
        data=np.full((6,720,1440),np.nan)
        i=0
        for name in types:
            data[i,:,:]=basefunc.getRaster('./results_for_amf/f_normal/'+name+'_under_'+scen+'_'+time+'_mme.tif')
            i=i+1
        data[data==-1]=np.nan
        data[data<0]=np.nan  # filter the parts that did not pass ks test
        amf_mean=np.nanmean(data,axis=0)
        
        ref_tif='./ref_tif.tif'
        output_path='./results_for_amf/f_normal/amf_under_'+scen+'_'+time+'_mme.tif'
        basefunc.array2Raster(amf_mean,ref_tif,output_path)




