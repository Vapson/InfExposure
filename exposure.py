# -*- coding: utf-8 -*-
"""
Created on Fri May  6 18:52:58 2022

@author: wangx
"""

import numpy as np
import basefunc

'''01 absolute exposure'''
def absolute_exposure(data):
    data[0,:,:][data[1,:,:]>-0.25]=0
    data[0,:,:][data[1,:,:]==-1]=0
    return data[0,:,:]

#by assets type
types=['motorway','trunk','primary','secondary','tertiary','railway']#
scens=['rcp45','rcp85']
times=['20302059','20702099']
for name in types:
    for scen in scens:
        for time in times:
            data=basefunc.getRaster('F:\\h\\rain\\revised_results\\results_for_rt_change\\f_strong\\'+name+'_under_'+scen+'_'+time+'_mme.tif')
            a_exposure = absolute_exposure(data)
            
            ref_tif='ref_tif.tif'
            output_path='F:\\h\\rain\\revised_results\\results_for_exposure\\f_strong\\'+name+'_AE_under_'+scen+'_'+time+'_mme.tif'
            basefunc.array2Raster(a_exposure,ref_tif,output_path)        

#all types
types=['motorway','trunk','primary','secondary','tertiary','railway']
for scen in scens:
    for time in times:
        a_exposure=np.full((720,1440),0.0)
        for name in types:  
            data=basefunc.getRaster('F:\\h\\rain\\revised_results\\results_for_rt_change\\f_normal\\'+name+'_under_'+scen+'_'+time+'_mme.tif')
            a_exposure = absolute_exposure(data) + a_exposure
        
        ref_tif='ref_tif.tif'
        output_path='F:\\h\\rain\\revised_results\\results_for_exposure\\f_normal\\AE_under_'+scen+'_'+time+'_mme.tif'
        basefunc.array2Raster(a_exposure,ref_tif,output_path)     



'''02 relative exposure'''
def relative_exposure(exposed_length,length):
    exposure=np.sum(exposed_length,axis=0)
    total_length=np.sum(length,axis=0)
    return exposure/total_length


#by types
types=['motorway','trunk','primary','secondary','tertiary','railway']#
scens=['rcp45','rcp85']
times=['20302059','20702099']
for name in types:
    for scen in scens:
        for time in times:
            exposed_length=basefunc.getRaster('F:\\h\\rain\\revised_results\\results_for_exposure\\f_strong\\'+name+'_AE_under_'+scen+'_'+time+'_mme.tif')
            length=basefunc.getRaster('F:\\h\\rain\\revised_results\\GISdata\\RoadandRailway\\global_'+name+'_720vs1440.tif')
                
            r_exposure = exposed_length/length
            
            ref_tif='ref_tif.tif'
            output_path='H:\\h\\rain\\revised_results\\results_for_exposure\\f_strong\\'+name+'_RE_under_'+scen+'_'+time+'_mme.tif'
            basefunc.array2Raster(r_exposure,ref_tif,output_path)        
    


#all types
types=['motorway','trunk','primary','secondary','tertiary','railway']#
scens=['rcp45','rcp85']
times=['20302059','20702099']
for scen in scens:
    for time in times:
        if 'exposed_length' in vars():
            del exposed_length
        if 'length' in vars():
            del length            
        for name in types:  
            a_exposure=basefunc.getRaster('H:\\h\\rain\\revised_results\\results_for_exposure\\f_strong\\'+name+'_AE_under_'+scen+'_'+time+'_mme.tif')
            leng=basefunc.getRaster('H:\\h\\rain\\revised_results\\results_for_rt_change\\f_strong\\'+name+'_under_'+scen+'_'+time+'_mme.tif')[0,:,:]
            rt_change=basefunc.getRaster('H:\\h\\rain\\revised_results\\results_for_rt_change\\f_strong\\'+name+'_under_'+scen+'_'+time+'_mme.tif')[1,:,:]
            leng[rt_change==-1]=0
            
            a_exposure=a_exposure.reshape(1,720,1440)
            leng=leng.reshape(1,720,1440)
            try:
                exposed_length=np.concatenate((exposed_length,a_exposure),axis=0)
                length=np.concatenate((length,leng),axis=0)
            except:
                exposed_length=a_exposure
                length=leng
        
        r_exposure = relative_exposure(exposed_length,length)
        
        ref_tif='ref_tif.tif'
        output_path='H:\\h\\rain\\revised_results\\results_for_exposure\\f_strong\\RE_under_'+scen+'_'+time+'_mme.tif'
        basefunc.array2Raster(r_exposure,ref_tif,output_path)        











