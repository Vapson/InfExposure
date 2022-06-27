# -*- coding: utf-8 -*-
"""
Created on Fri May  6 16:04:45 2022

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
    new_rt=inputs[-8:]
    y=-1.0
    if assets_type==1:
        if income==1 or income==2: #low/lower middle
            y=(new_rt[1]-2.0)/2.0 #median: x.index[1]                               
        elif income==3: #upper middle
            y=(new_rt[2]-5.0)/5.0 #median: x.index[2]  
        elif  income==4: #high
            y=(new_rt[3]-10.0)/10.0 #median: x.index[3]  
        else:
            y=-1.0   
    elif assets_type==2:
        if income==1 or income==2:
            y=-1.0
        elif income==3:
            y=(new_rt[1]-2.0)/2.0 #median: x.index[1]             
        elif income==4:    
            y=(new_rt[2]-5.0)/5.0 #median: x.index[2]             
        else:
            y=-1.0
    elif assets_type==3:
        if income==1 or income==2:
            y=(new_rt[3]-10.0)/10.0 #median: x.index[1]  
        elif income==3:
            y=(new_rt[4]-20.0)/20.0 #median: x.index[1]             
        elif income==4:    
            y=(new_rt[5]-30.0)/30.0 #median: x.index[2]             
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
    new_rt=inputs[-8:]
    y=-1.0
    if assets_type==1:
        if income==1 or income==2: #low/lower middle
            y=(new_rt[2]-5)/5 #median: x.index[1]                               
        elif income==3: #upper middle
            y=(new_rt[3]-10)/10 #median: x.index[2]  
        elif  income==4: #high
            y=(new_rt[4]-20)/20 #median: x.index[3]  
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


'''main'''
#single asset type
name='railway'
types=['motorway','trunk','primary','secondary','tertiary','railway']#
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
            new_rt=basefunc.getRaster('H:\\h\\rain\\revised_results\\results_for_gev\\newRT_under_'+scen+'_'+time+'_mme.tif')
            
            array=np.concatenate((income,assets_type,new_rt),axis=0)
            rt_change=np.apply_along_axis(f_strong,0,array)
            rt_change=rt_change.reshape(1,720,1440)
               
            length=basefunc.getRaster('H:\\h\\rain\\revised_results\\GISdata\\RoadandRailway\\global_'+name+'_720vs1440.tif')
            length=length.reshape(1,720,1440)
            out=np.concatenate((length,rt_change),axis=0)
            
            ref_tif='ref_tif.tif'
            output_path='H:\\h\\rain\\revised_results\\results_for_rt_change\\'+name+'_under_'+scen+'_'+time+'_mme.tif'
            basefunc.array2Raster(out,ref_tif,output_path)
      
