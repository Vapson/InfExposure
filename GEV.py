# -*- coding: utf-8 -*-
"""
Created on Mon May  2 17:07:39 2022

@author: wangx
"""

import numpy as np
from lmoments3 import distr
import collections
from scipy import stats

def smooth(data):
    # calculate mean value of neighbour grid 
    # it would work only if smooth are needed
    ranseq=np.arange(10e-9,(3*10e-8+10e-9),10e-9)
    c=[]
    loc=[]
    scale=[]
    for i in range(data.shape[1]):
        gevfit = distr.gev.lmom_fit(data[:,i]+ranseq)
        c.append(gevfit['c'])
        loc.append(gevfit['loc'])
        scale.append(gevfit['scale'])      
    gevfit=collections.OrderedDict()
    gevfit['c']=np.mean(c)
    gevfit['loc']=np.mean(loc)
    gevfit['scale']=np.mean(scale)
    return gevfit



    
def gev_for_pre(data):
    #Calculate extreme precipitation (RX1D) for a given return period
    rt= np.array( [1.1,2,5,10,20,30,50,100] )
    if data.max()>=1e+10:
        return np.array([-1]*len(rt))
    else:
        if len(data.shape)>1:
            #smooth=True
            gevfit=smooth(data)
            #Put arguments into the distribution function, which can be called directly
            fitted_gev = distr.gev(**gevfit) 
            if data.shape[1]==4:
                grid=0
            elif data.shape[1]==6:
                grid=1
            elif data.shape[1]==9:
                grid=4 
            D,p=stats.kstest(data[:,grid],fitted_gev.cdf)
            if p>0.05:
                
                gevST = fitted_gev.ppf(1.0-1./rt) # ppf: Inverse cumulative distribution function，Returns the value corresponding to the quantile (return period)
                return gevST
            else:
                return np.array([-1]*len(rt))                
        else:
            ranseq=np.arange(10e-9,(3*10e-8+10e-9),10e-9)
            gevfit = distr.gev.lmom_fit(data+ranseq)
            fitted_gev = distr.gev(**gevfit) 
            D,p=stats.kstest(data,fitted_gev.cdf)
            if p>0.05:
                gevST = fitted_gev.ppf(1.0-1./rt)
                return gevST
            else:
                return np.array([-1]*len(rt))




def gev_for_rt(inputs):
    # Calculate the return period for a given precipitation (RX1D)
    # The input array contains two parts of the same size:
    # The first part is the data of the next 30 years which is used for fitting. size: 30 
    # The second part is the precipitation of each return period base on historical data, and the new return period under the future fitting curve would be calculated.  size: 8
    data_fit=np.array(inputs[:30])
    data_convert=inputs[-8:]
    rt= np.array( [1.1,2,5,10,20,30,50,100] )
    if data_fit.max()>=1e+10:
        gevST=np.array([-1]*len(rt))
        RT=np.array([-1]*len(rt))
        return np.concatenate((gevST,RT))
    else:
        if len(data_fit.shape)>1:
            gevfit=smooth(np.array(data_fit))
            fitted_gev = distr.gev(**gevfit) 
            if data_fit.shape[1]==4:
                grid=0
            elif data_fit.shape[1]==6:
                grid=1
            elif data_fit.shape[1]==9:
                grid=4 
            D,p=stats.kstest(data_fit[:,grid],fitted_gev.cdf)
            if p>0.05:
                gevST = fitted_gev.ppf(1.0-1./rt) 
                RT =1/( 1-fitted_gev.cdf(data_convert)) #Return: the return period for the given precipitation(RX1D)
                return np.concatenate((gevST,RT))
            else:
                gevST=np.array([-1]*len(rt))
                RT=np.array([-1]*len(rt))
                return np.concatenate((gevST,RT))     
        else:    
            ranseq=np.arange(10e-9,(3*10e-8+10e-9),10e-9)
            gevfit = distr.gev.lmom_fit(data_fit+ranseq)
            fitted_gev = distr.gev(**gevfit) 
            D,p=stats.kstest(data_fit,fitted_gev.cdf)
            if p>0.05:
                gevST = fitted_gev.ppf(1.0-1./rt) 
            
                RT =1/( 1-fitted_gev.cdf(data_convert))
                RT[np.isinf(RT)]=1
                return np.concatenate((gevST,RT))
            else:
                gevST=np.array([-1]*len(rt))
                RT=np.array([-1]*len(rt))
                return np.concatenate((gevST,RT))


    






















