# -*- coding: utf-8 -*-
"""
Created on Sat May  7 19:39:56 2022

@author: wangx
"""


import numpy as np
import basefunc

def f_normal(inputs):
    """
                motorway et.al return period/year、tertiary return period/year
    high income：10、5
    upper middle income：5、2
    low middle/low income：2、0
    """
    #new_rt[]👉 0: 1.1years、1: 2years、2: 5years、3: 10years、4: 20years、5: 30years、6: 50years 7: 100years 
    income=inputs[0]
    assets_type=inputs[1]
    new_pre=inputs[-16:-8]
    his_pre=inputs[-8:]
    y=-1.0
    if assets_type==1:
        if income==1 or income==2: #low/lower middle
            y=new_pre[1]/his_pre[1] #median: x.index[1]                               
        elif income==3: #upper middle
            y=new_pre[2]/his_pre[2]#median: x.index[2]  
        elif  income==4: #high
            y=new_pre[3]/his_pre[3] #median: x.index[3]  
        else:
            y=-1.0   
    elif assets_type==2:
        if income==1 or income==2:
            y=-1.0
        elif income==3:
            y=new_pre[1]/his_pre[1] #median: x.index[1]             
        elif income==4:    
            y=new_pre[2]/his_pre[2] #median: x.index[2]             
        else:
            y=-1.0
    elif assets_type==3:
        if income==1 or income==2:
            y=new_pre[3]/his_pre[3] #median: x.index[1]  
        elif income==3:
            y=new_pre[4]/his_pre[4] #median: x.index[1]             
        elif income==4:    
            y=new_pre[5]/his_pre[5] #median: x.index[2]             
        else:
            y=-1.0        
    return  y

def f_strong(inputs):
    """
                return period/years: motorway et.al 、tertiary、railways
    high income：20、10、50
    upper middle income：10、5、30
    low middle/low income：5、0、20
    """
    #new_rt[]👉 0: 1.1years、1: 2years、2: 5years、3: 10years、4: 20years、5: 30years、6: 50years 7: 100years 
    income=inputs[0]
    assets_type=inputs[1]
    new_pre=inputs[-16:-8]
    his_pre=inputs[-8:]
    y=-1.0
    if assets_type==1:
        if income==1 or income==2: #low/lower middle
            y=new_pre[2]/his_pre[2] #median: x.index[1]                               
        elif income==3: #upper middle
            y=new_pre[3]/his_pre[3] #median: x.index[2]  
        elif  income==4: #high
            y=new_pre[4]/his_pre[4] #median: x.index[3]  
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


'''main'''
#single asset type
name='railway'
types=['motorway','trunk','primary','secondary','tertiary','railway']
his_pre=basefunc.getRaster('H:\\h\\rain\\revised_results\\results_for_gev\\historical_mme.tif')
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
            new_pre=basefunc.getRaster('H:\\h\\rain\\revised_results\\results_for_gev\\'+scen+'pre'+time+'_mme.tif')
             
            array=np.concatenate((income,assets_type,new_pre,his_pre),axis=0)
            amf=np.apply_along_axis(f_normal,0,array)
            
            ref_tif='ref_tif.tif'
            output_path='H:\\h\\rain\\revised_results\\results_for_amf\\f_normal\\'+name+'_under_'+scen+'_'+time+'_mme.tif'
            basefunc.array2Raster(amf,ref_tif,output_path)

    
#mean results of all types 
types=['motorway','trunk','primary','secondary','tertiary','railway']
scens=['rcp45','rcp85']
times=['20302059','20702099']
for scen in scens:
    for time in times:
        data=np.full((6,720,1440),np.nan)
        i=0
        for name in types:
            data[i,:,:]=basefunc.getRaster('H:\\h\\rain\\revised_results\\results_for_amf\\f_normal\\'+name+'_under_'+scen+'_'+time+'_mme.tif')
            i=i+1
        data[data==-1]=np.nan
        data[data<0]=np.nan #filter the parts that did not pass ks test
        amf_mean=np.nanmean(data,axis=0)
        
        ref_tif='ref_tif.tif'
        output_path='H:\\h\\rain\\revised_results\\results_for_amf\\f_normal\\amf_under_'+scen+'_'+time+'_mme.tif'
        basefunc.array2Raster(amf_mean,ref_tif,output_path)




