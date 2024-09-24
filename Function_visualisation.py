#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:23:04 2024

@author: quentin
"""


"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions for visualisation of the dataframe

#=============================================================================
   #=============================================================================
   #============================================================================="""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as mcolors
import numpy as np
import pylab as pl

import Function_errors as fe

"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def histogram(Para, y, yaxis):
    """
    Parameters:
    - Para: List of column in the dataframe
    - y: dataframe which must be an array with only one index per row.

    Returns:
    - An histogram where each bar contains several elements.
    """
       
       
    figname='Movies over the '+Para[0]
    fig, ax = plt.subplots(figsize=(22,12))
    ax.set_title(figname)
    
    ax.set_xlabel(Para[0], fontsize=35)
    ax.set_ylabel(yaxis, fontsize=35)
    
    p = ax.bar(y.index, y) # , color=mcolors.CSS4_COLORS[colors[i]]
   
    ax.tick_params(axis='both', labelsize=20)
        
    ax.legend(ncol=2)
    plt.tight_layout()
    
    plt.show()

"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def histogram_multi(Para,y):
    """
    Parameters:
    - Para: List of column in the dataframe
    - y: dataframe which must be an array with only one index per row.

    Returns:
    - An histogram where each bar contains several elements.
    """

       
    figname='Movies over the '+Para[0]
    fig, ax = plt.subplots(figsize=(22,12))
    ax.set_title(figname)
    
    ax.set_xlabel(Para[0], fontsize=35)
    ax.set_ylabel('Amount of movies', fontsize=35)
    
    bottom = np.zeros(len(y.index))
    i=0
    for element_col, y in y.items():
        p = ax.bar(y.index, y, label=element_col, bottom=bottom) # , color=mcolors.CSS4_COLORS[colors[i]]
        bottom += y
        i+=1
    
    
    ax.tick_params(axis='both', labelsize=20)
    ax.grid(True, color='grey', linestyle='--', linewidth=2, alpha=0.5)
    
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=10))
    
    ax.legend(ncol=2)
    plt.tight_layout()
    
    plt.show()


"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def curve_multi(Para,y):
    """
    Parameters:
    - Para: List of column in the dataframe
    - y: dataframe which must be an array with only one index per row.

    Returns:
    - A curve.
    """
    
       
    figname='Movies over the '+Para[0]
    fig, ax = plt.subplots(figsize=(22,12))
    ax.set_title(figname)
    
    ax.set_xlabel(Para[0], fontsize=35)
    ax.set_ylabel('Average movie '+Para[1], fontsize=35)
    
    p = ax.plot(y.index, y, linewidth=4.)    
    
    ax.tick_params(axis='both', labelsize=20)
    ax.grid(True, color='grey', linestyle='--', linewidth=2, alpha=0.5)
    
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=10))
    
    ax.legend(ncol=2)
    plt.tight_layout()
    
    plt.show()
