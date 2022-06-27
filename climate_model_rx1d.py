# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 17:43:06 2022

@author: Vapson
"""


import os
from netCDF4 import Dataset
os.chdir(r'H:\h\rain\revised_results\nc_revised_coding')
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import basefunc


def rx1d(ref_tif,historical=True,rcp45=True,rcp85=True):
    if historical:
        save_folder=r'H:\h\rain\revised_results\pre_for_fitting\historical'
        pre_path=r'G:\GDDP-NEX-Prec\original\historical'
        file=os.listdir(pre_path)
        for i in range(len(file)):
            if int(file[i][-7:-3])>1970 and int(file[i][-7:-3])<=2000:
                output_path=os.path.join(save_folder,file[i][:-3]+'.tif')
                if os.path.exists( os.path.join(save_folder,output_path)):
                    continue
                else:
                    rootgrp = Dataset(os.path.join(pre_path,file[i])) #open nc data
                    #variables=rootgrp.variables.keys() #see variables
                    data=rootgrp.variables['pr'][:] #read data of our variable
                    array=data.max(0)[::-1,:]
                    
                    basefunc.array2Raster(array,ref_tif,output_path)
                    print('finished:',file[i])
                    del data
            
    if rcp45:
        save_folder=r'H:\h\rain\revised_results\pre_for_fitting\rcp45'
        pre_path=r'G:\GDDP-NEX-Prec\original\rcp45'
        file=os.listdir(pre_path)
        for i in range(len(file)):    
            if int(file[i][-7:-3])>=2030 and int(file[i][-7:-3])<=2100:
                if int(file[i][-7:-3])>=2060 and int(file[i][-7:-3])<2070:
                    continue
                else:
                    output_path=os.path.join(save_folder,file[i][:-3]+'.tif')
                    if os.path.exists( os.path.join(save_folder,output_path)):
                        continue
                    else:                
                        try:
                            rootgrp = Dataset(os.path.join(pre_path,file[i])) 
                            data=rootgrp.variables['pr'][:] 
                            array=data.max(0)[::-1,:]
                            
                            basefunc.array2Raster(array,ref_tif,output_path)
                            print('finished:',file[i])
                            del data
                        except:
                            print('error:',file[i])
    if rcp85:
        save_folder=r'H:\h\rain\revised_results\pre_for_fitting\rcp85'
        pre_path=r'G:\GDDP-NEX-Prec\original\rcp85'
        file=os.listdir(pre_path)
        for i in range(len(file)):    
            if int(file[i][-7:-3])>=2030 and int(file[i][-7:-3])<=2100:  
                if int(file[i][-7:-3])>=2060 and int(file[i][-7:-3])<2070:
                    continue
                else:
                    output_path=os.path.join(save_folder,file[i][:-3]+'.tif')
                    if os.path.exists( os.path.join(save_folder,output_path)):
                        continue
                    else:     
                        try:
                            rootgrp = Dataset(os.path.join(pre_path,file[i])) 
                            data=rootgrp.variables['pr'][:]  
                            array=data.max(0)[::-1,:]
                            
                            basefunc.array2Raster(array,ref_tif,output_path)
                            print('finished:',file[i])
                            del data
                        except:
                            print('error:',file[i])                            
#main                    
ref_tif='ref_tif.tif'
rx1d(ref_tif,historical=False)




