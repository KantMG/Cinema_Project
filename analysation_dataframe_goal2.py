#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 17:00:43 2024

@author: quentin
"""

"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of specific dataframe analysis

#=============================================================================
   #=============================================================================
   #============================================================================="""


import pandas as pd
import dask.dataframe as dd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as mcolors
import numpy as np
import pylab as pl

import Function_dataframe as fd
import Function_errors as fe
import Function_visualisation as fv


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



# Specify Columns or Data Types: 
# If you dont need all columns or can reduce memory usage by specifying data types, this can reduce the load on memory.

# df = pd.read_csv('large_file.csv', usecols=['col1', 'col2'], dtype={'col1': 'int32', 'col2': 'float32'})

# Use low_memory=True in read_csv: 
# Sometimes large CSVs with mixed types can cause memory issues. 
# You can set low_memory=True (which is the default), allowing pandas to internally process chunks, though it will take longer to infer the data types.

# df = pd.read_csv('large_file.csv', low_memory=True)


# Profile Memory Usage: Use memory profiling to understand where the memory bottleneck occurs.
# You can use the memory_usage() function or the memory-profiler package to identify memory-heavy operations.

# print(df.memory_usage(deep=True))  # Check memory usage of each column


# if __name__ == "__main__":
#     main()  # Calls the main function from file Main
#     print("Continuation in file2.")


"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def movie_making_over_year(Project_path):

    print("Goal 2: Evolution of the global movie making over the year.")
    print("1- How much is the growth of the movie making.")
    print("2- Which genres are the most popular.")
    print("3- How much evolve the runtimeMinutes of the movies.")
    print("4- Which genres have the shortest runtimeMinutes.")
    print("5- Does the violence in movies increases.")
    print()
    
    Goal2 = [True, False, False, False, False]

    # List of the required data file.
    List_file=['title.basics.tsv','title.akas.tsv']
    #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    df = pd.read_csv(Project_path+List_file[0], sep='\t', usecols=["tconst", "startYear", "runtimeMinutes", "genres", "isAdult"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    df2 = dd.read_csv(Project_path+List_file[1], sep='\t', usecols=["titleId", "region", "language", "isOriginalTitle"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    df2 = df2.loc[df2['isOriginalTitle'] == 1]
    df2 = df2.loc[df2['region'] != '\\N']
    
    # #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    # df3 = pd.read_csv(Project_path+List_file[2], sep=';', usecols=["titleId", "region", "language", "isOriginalTitle"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      


    Rows_to_keep=100
    df_cut = df2.head(Rows_to_keep)
    

    print(df2)
    print("ok")
    print(df_cut)
    

    
    return Para,y