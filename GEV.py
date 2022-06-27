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
    ranseq=np.arange(10e-9,(3*10e-8+10e-9),10e-9)#为每个数据添加一个随机项
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
    rt= np.array( [1.1,2,5,10,20,30,50,100] )
    if data.max()>=1e+10:
        return np.array([-1]*len(rt))
    else:
        if len(data.shape)>1:
            #smooth=True
            gevfit=smooth(data)
            fitted_gev = distr.gev(**gevfit) #将参数带入分布函数，可直接调用
            if data.shape[1]==4:
                grid=0
            elif data.shape[1]==6:
                grid=1
            elif data.shape[1]==9:
                grid=4 
            D,p=stats.kstest(data[:,grid],fitted_gev.cdf)
            if p>0.05:
                gevST = fitted_gev.ppf(1.0-1./rt) # ppf: Inverse cumulative distribution function，返回分位数（重现期）对应的值
                return gevST
            else:
                return np.array([-1]*len(rt))                
        else:
            ranseq=np.arange(10e-9,(3*10e-8+10e-9),10e-9)#为每个数据添加一个随机项
            gevfit = distr.gev.lmom_fit(data+ranseq)#范围拟合参数 c, loc, scale
            fitted_gev = distr.gev(**gevfit) #将参数带入分布函数，可直接调用
            D,p=stats.kstest(data,fitted_gev.cdf)
            if p>0.05:
                gevST = fitted_gev.ppf(1.0-1./rt) # ppf: Inverse cumulative distribution function，返回分位数（重现期）对应的值
                return gevST
            else:
                return np.array([-1]*len(rt))




def gev_for_rt(inputs):
    #组合的数组包含相同大小的两部分：
    #第一部分为未来30年数据并用于拟合。 size: 30
    #第二部分为历史各重现期的降水，计算在未来的拟合曲线下新的重现期  size: 8
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
            fitted_gev = distr.gev(**gevfit) #将参数带入分布函数，可直接调用
            if data_fit.shape[1]==4:
                grid=0
            elif data_fit.shape[1]==6:
                grid=1
            elif data_fit.shape[1]==9:
                grid=4 
            D,p=stats.kstest(data_fit[:,grid],fitted_gev.cdf)
            if p>0.05:
                gevST = fitted_gev.ppf(1.0-1./rt) # ppf: Inverse cumulative distribution function，返回分位数（重现期）对应的值
                RT =1/( 1-fitted_gev.cdf(data_convert))#返回该降雨量下的重现期
                return np.concatenate((gevST,RT))
            else:
                gevST=np.array([-1]*len(rt))
                RT=np.array([-1]*len(rt))
                return np.concatenate((gevST,RT))     
        else:    
            ranseq=np.arange(10e-9,(3*10e-8+10e-9),10e-9)#为每个数据添加一个随机项
            gevfit = distr.gev.lmom_fit(data_fit+ranseq)#范围拟合参数 c, loc, scale
            fitted_gev = distr.gev(**gevfit) #将参数带入分布函数，可直接调用
            D,p=stats.kstest(data_fit,fitted_gev.cdf)
            if p>0.05:
                gevST = fitted_gev.ppf(1.0-1./rt) # ppf: Inverse cumulative distribution function，返回分位数（重现期）对应的值
            
                RT =1/( 1-fitted_gev.cdf(data_convert))#返回该降雨量下的重现期
                RT[np.isinf(RT)]=1
                return np.concatenate((gevST,RT))
            else:
                gevST=np.array([-1]*len(rt))
                RT=np.array([-1]*len(rt))
                return np.concatenate((gevST,RT))


    






















