#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 19:06:36 2024

@author: quentin
"""



import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as mcolors
import numpy as np
import pylab as pl

import Function_dataframe as fd

params = {'axes.labelsize': 28,

          'font.size': 22,

          'legend.fontsize': 22,

          'axes.titlesize': 20,

          'xtick.labelsize': 20,

          'ytick.labelsize': 20,

          'text.usetex': False,

          'figure.figsize': (16,11),

          'axes.unicode_minus': True}

pl.rcParams.update(params)
plt.rcParams["font.family"] = "serif"

"""#=============================================================================
   #=============================================================================
   #============================================================================="""


# Source for data set : https://developer.imdb.com/non-commercial-datasets/




File_path='/home/quentin/Documents/Work/Data_analytics/Datasets/Cinema_Project/'
File_name='name.basics.tsv'

#Create class 'pandas.core.frame.DataFrame'
csvFile = pd.read_csv(File_path+File_name,sep='\t')
print(csvFile)
print()

for col in csvFile.columns:    print(col)
print('')

"""#=============================================================================
   #=============================================================================
   #============================================================================="""
 

# [13769111 rows x 6 columns]

# nconst
# primaryName
# birthYear
# deathYear
# primaryProfession
# knownForTitles
