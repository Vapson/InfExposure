# -*- coding: utf-8 -*-
"""
Created on Mon May  2 17:55:47 2022

@author: Vapson
"""

import os
os.chdir(r'H:\h\rain\revised_results\nc_revised_coding')

import numpy as np
from concurrent.futures import ProcessPoolExecutor
import basefunc
import GEV
import datetime


'''read_data'''

def read_data(folder,time_low,time_up):
    climate_data_path=os.path.join('H:\\h\\rain\\revised_results\\pre_for_fitting',folder)
    model=os.listdir(climate_data_path)
    model.remove('GFDL-CM3')
    '''
    model.remove('bcc-csm1-1')
    model.remove('BNU-ESM')
    model.remove('CESM1-BGC')
    model.remove('NorESM1-M')
    model.remove('CCSM4')
    model.remove('GFDL-ESM2G')
    model.remove('inmcm4')
    '''
    for i in range(len(model)):
        path=os.path.join(climate_data_path, model[i])
        all_files=os.listdir(path)
        all_files.sort()
        
        # filt files for specific years
        files=[]
        for f in range(len(all_files)):
            if int(all_files[f][-8:-4])>=time_low and int(all_files[f][-8:-4])<=time_up:
                files.append(all_files[f])      
                
        # concatenate files for 30 years        
        for j in range(len(files)):
            data=basefunc.getRaster(os.path.join(path, files[j]))
            data=data.reshape(1,data.shape[0],data.shape[1])
            if j==0:
                climate_model_data=data
            else:
                climate_model_data=np.concatenate((climate_model_data,data),axis=0)  
                
        # concatenate files for 20 models        
        climate_model_data=climate_model_data.reshape(1,climate_model_data.shape[0],climate_model_data.shape[1],climate_model_data.shape[2])       
        if i==0:              
            climate_data=climate_model_data
        else:
            climate_data=np.concatenate((climate_data,climate_model_data),axis=0)    
        del climate_model_data
        del data
    return climate_data,model


'''with smoorh'''

def neighbour(z,stack):
    #z: input data
    #stack: push start coordinate on stack, like stack = [(3,2)]
    neighbours = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
    mask = np.zeros_like(z[0,:], dtype = bool)  
    x, y = stack.pop()
    mask[x, y] = True
    for dx, dy in neighbours:
        nx, ny = x + dx, y + dy
        if (0 <= nx < z.shape[1] and 0 <= ny < z.shape[2] 
            and not mask[nx, ny]):
            mask[nx, ny] = True
    return z[:,mask]

def smooth_input_data(z):
    new_data=[]
    stack=[]
    for i in range(720):#z.shape[1]
        for j in range(1440):#z.shape[2]
            stack.append([(i,j)])
    new_data=[neighbour(z,i) for i in stack]
            #new_data.append(neighbour(z,stack))
        #print(i)
    return new_data


smooth=False
#smooth=True

'''01 calculate pre for historical values corresponding return periods'''

climate_data,model=read_data('historical',1971,2000)
climate_data=np.sort(climate_data,axis=1)
mme_median=np.median(climate_data,axis=0)#*60*60*24 #convert to "mm"
#del climate_data
    
def multi_process(prim):
    with ProcessPoolExecutor() as pool:
        results = pool.map(GEV.gev_for_pre, prim)
        out = list(results)
    return out

#for MME
# without smooth
if smooth==False:
    inputs=list(mme_median.reshape(30,-1).T)
# with smooth
if smooth==True:
    inputs=smooth_input_data(mme_median)

r=[]
for z in range(104):
    print(datetime.datetime.now())
    r.extend( multi_process( inputs[ z*10000:min( z*10000+10000,len(inputs) ) ]) )
    print(datetime.datetime.now())

rs=np.array(r).T.reshape(8,720,1440)

ref_tif='ref_tif.tif'
output_path=r'H:\h\rain\revised_results\results_for_gev\historical_mme.tif'
basefunc.array2Raster(rs,ref_tif,output_path)

#multi-models
for i in range((len(model))):
    if smooth==False:
        inputs=list(climate_data[i,:,:,:].reshape(30,-1).T)
    # with smooth
    if smooth==True:
        inputs=smooth_input_data(climate_data[i,:,:,:])
    
    r=[]
    for z in range(104):
        print(datetime.datetime.now())
        r.extend( multi_process( inputs[ z*10000:min( z*10000+10000,len(inputs) ) ]) )
        print(datetime.datetime.now())
    
    rs=np.array(r).T.reshape(8,720,1440)
    
    ref_tif='ref_tif.tif'
    output_path='H:\\h\\rain\\revised_results\\results_for_gev\\historical_'+model[i]+'.tif'
    basefunc.array2Raster(rs,ref_tif,output_path)


'''02 calculate pre for future values corresponding return periods'''

'''multi-model mdian project'''
def multi_process(prim):
    with ProcessPoolExecutor() as pool:
        results = pool.map(GEV.gev_for_rt, prim)
        out = list(results)
    return out

def future(scen,time_low,time_up):
    climate_data,model=read_data(scen,time_low,time_up)
    climate_data=np.sort(climate_data,axis=1)
    mme_median=np.median(climate_data,axis=0)#*60*60*24 #convert to "mm"
    del climate_data
    
    historical_mme=basefunc.getRaster(r'H:\h\rain\revised_results\results_for_gev\historical_mme.tif')
    #historical_mme=basefunc.getRaster(r'H:\h\rain\rain\result_30yr\water_capacity\median_change\historical_median_pre.tif')[:,::-1,:]
    # without smooth
    if smooth==False:
        inputs=np.concatenate((mme_median,historical_mme),axis=0)
        inputs=list(inputs.reshape(38,-1).T)       
    # with smooth
    if smooth==True:
        inputs=smooth_input_data(mme_median)
        inputs=[list(inputs[i]) for i in range(len(inputs))]   
        historical_mme=list(historical_mme.reshape(8,-1).T)
        yy=[inputs[i].extend(historical_mme[i]) for i in range(len(inputs))] #yy has no use. "extend" could change the inputs         
    
    r=[]
    for z in range(104):
        print(datetime.datetime.now())
        r.extend( multi_process( inputs[ z*10000:min( z*10000+10000,len(inputs) ) ]) )
        print(datetime.datetime.now())
    
    return r
    

#main
for i in ['rcp45','rcp85']:
    scen=i
    time_low=2030
    time_up=2059
    r=future(scen,2030,2059)
    r=np.array(r).T.reshape(16,720,1440)

    future_pre=r[:8,:,:]
    future_rt=r[-8:,:,:]

    ref_tif='ref_tif.tif'
    outname=scen+'pre'+str(time_low)+str(time_up)+'_mme.tif'
    output_path='H:\\h\\rain\\revised_results\\results_for_gev\\'+outname
    basefunc.array2Raster(future_pre,ref_tif,output_path)

    outname='newRT_under_'+scen+'_'+str(time_low)+str(time_up)+'_mme.tif'
    output_path='H:\\h\\rain\\revised_results\\results_for_gev\\'+outname
    basefunc.array2Raster(future_rt,ref_tif,output_path)
    
    time_low=2070
    time_up=2099
    r=future(scen,time_low,time_up)
    r=np.array(r).T.reshape(16,720,1440)

    future_pre=r[:8,:,:]
    future_rt=r[-8:,:,:]

    ref_tif='ref_tif.tif'
    outname=scen+'pre'+str(time_low)+str(time_up)+'_mme.tif'
    output_path='H:\\h\\rain\\revised_results\\results_for_gev\\'+outname
    basefunc.array2Raster(future_pre,ref_tif,output_path)

    outname='newRT_under_'+scen+'_'+str(time_low)+str(time_up)+'_mme.tif'
    output_path='H:\\h\\rain\\revised_results\\results_for_gev\\'+outname
    basefunc.array2Raster(future_rt,ref_tif,output_path)


'''multi models'''    
def future(scen,time_low,time_up):
    climate_data,model=read_data(scen,time_low,time_up)
    climate_data=np.sort(climate_data,axis=1)
    for i in range((len(model))):
        historical_mme=basefunc.getRaster('H:\\h\\rain\\revised_results\\results_for_gev\\historical_'+model[i]+'.tif')
        #historical_mme=basefunc.getRaster(r'H:\h\rain\rain\result_30yr\water_capacity\median_change\historical_median_pre.tif')[:,::-1,:]
        # without smooth
        if smooth==False:
            inputs=np.concatenate((climate_data[i,:,:,:],historical_mme),axis=0)
            inputs=list(inputs.reshape(38,-1).T)       
        # with smooth
        if smooth==True:
            inputs=smooth_input_data(climate_data[i,:,:,:])
            inputs=[list(inputs[i]) for i in range(len(inputs))]   
            historical_mme=list(historical_mme.reshape(8,-1).T)
            yy=[inputs[j].extend(historical_mme[j]) for j in range(len(inputs))] #yy has no use. "extend" could change the inputs         
        
        r=[]
        for z in range(104):
            print(datetime.datetime.now())
            r.extend( multi_process( inputs[ z*10000:min( z*10000+10000,len(inputs) ) ]) )
            print(datetime.datetime.now())
            
        r=np.array(r).T.reshape(16,720,1440)

        future_pre=r[:8,:,:]
        future_rt=r[-8:,:,:]
    
        ref_tif='ref_tif.tif'
        outname=scen+'pre'+str(time_low)+str(time_up)+'_'+model[i]+'.tif'
        output_path='H:\\h\\rain\\revised_results\\results_for_gev\\'+outname
        basefunc.array2Raster(future_pre,ref_tif,output_path)
    
        outname='newRT_under_'+scen+'_'+str(time_low)+str(time_up)+'_'+model[i]+'.tif'
        output_path='H:\\h\\rain\\revised_results\\results_for_gev\\'+outname
        basefunc.array2Raster(future_rt,ref_tif,output_path)
            
    

#main
for i in ['rcp45','rcp85']:
    scen=i
    time_low=2030
    time_up=2059
    future(scen,2030,2059)

    time_low=2070
    time_up=2099
    future(scen,time_low,time_up)
 
