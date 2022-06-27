# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 02:29:15 2021

@author: Vapson
"""

from osgeo import gdal
import numpy as np
def getRaster(Path):
    dataset = gdal.Open(Path)
    nXSize = dataset.RasterXSize #lon
    nYSize = dataset.RasterYSize #lat
    data=dataset.ReadAsArray(0,0,nXSize,nYSize)#get data 
    return data

def bandover(data):
    if len(data.shape[:])==2:#lat*lon
        data_array=np.full((data.shape[0],data.shape[1]),np.nan)        
        for m in range(data.shape[0]-1):
            data_array[m,:]=data[data.shape[0]-1-m,:]    
    if len(data.shape[:])==3:#time*lat*lon
        data_array=np.full((data.shape[0],data.shape[1],data.shape[2]),np.nan)        
        for m in range(data.shape[1]-1):
            data_array[:,m,:]=data[:,data.shape[1]-1-m,:]            
    if len(data.shape[:])==4:#model*time*lat*lon
        data_array=np.full((data.shape[0],data.shape[1],data.shape[2],data.shape[3]),np.nan)        
        for m in range(data.shape[2]-1):
            data_array[:,:,m,:]=data[:,:,data.shape[2]-1-m,:]      
    return data_array

def array2Raster(array,ref_tif,output_path,**tif_geotrans):
    #multi-band
    if len(array.shape[:])>2:
        dataset= gdal.Open(ref_tif) 
        if tif_geotrans:
            tif_geotrans=tif_geotrans['tif_geotrans']
        else:
            tif_geotrans = dataset.GetGeoTransform()
        tif_proj = dataset.GetProjection()  
        driver = gdal.GetDriverByName("GTiff")    
        tif_height=array.shape[1]
        tif_width=array.shape[2]
        output = driver.Create(output_path,tif_width, tif_height,array.shape[0],gdal.GDT_Float32) 
        output.SetGeoTransform(tif_geotrans) 
        output.SetProjection(tif_proj)
        for a in range(array.shape[0]):   
            output.GetRasterBand(a+1).WriteArray(array[a,:,:])  
        output = None 
    #single-band    
    else: 
        dataset= gdal.Open(ref_tif) 
        if tif_geotrans:
            tif_geotrans=tif_geotrans['tif_geotrans']
        else:
            tif_geotrans = dataset.GetGeoTransform()
        tif_proj = dataset.GetProjection()
        #print(tif_geotrans['tif_geotrans'])
        driver = gdal.GetDriverByName("GTiff")    
        tif_height=array.shape[0]
        tif_width=array.shape[1]
        output = driver.Create(output_path,tif_width, tif_height,1,gdal.GDT_Float32) 
        output.SetGeoTransform(tif_geotrans)
        output.SetProjection(tif_proj) 
        output.GetRasterBand(1).WriteArray(array)  
        output = None
