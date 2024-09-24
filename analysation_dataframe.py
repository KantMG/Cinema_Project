#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 18:46:14 2024

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






"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def movie_making_over_year(Project_path):
    """
    Make the analysis of the project by achieving the goals decribed below.
    Goals: 
    -1 PROJECT ENLIGHT THE EVOLUTION OVER THE YEARS OF THE MOVIE AND SERIE MAKING.
    -2 THE ADAPTATION OF THE WAY OF PRODUCTION AS WELL AS OUR WAY OF CONSOMATION ARE ANALYSED.
    -3 HOW MUCH THE COUNTRIES ARE INVESTING IN THE FILMS PRODUCTION.
    -4 WHICH IS THE LEVEL OF INFLUENCE OF A COUNTRY OVER THE OTHERS.

    Parameters:
    - Project_path: Directory where the data is located

    Returns:
    - The entire analysis described above.
    """

    
    print("Goal 1: Evolution of the global movie making over the year.")
    print("1- How much is the growth of the movie making.")
    print("2- Which genres are the most popular.")
    print("3- How much evolve the runtimeMinutes of the movies.")
    print("4- Which genres have the shortest runtimeMinutes.")
    print("5- Does the violence in movies increases.")
    print()
    
    Goal1 = [True, False, True, True, False]

    # List of the required data file.
    List_file=['title.basics.tsv']
    #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    df = pd.read_csv(Project_path+List_file[0], sep=';', usecols=["tconst", "startYear", "runtimeMinutes", "genres", "isAdult"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    
    
    if Goal1[0] == True or Goal1[1] == True :
        print("Answer 1 and 2 of Goal 1")
        print()
        

        column_to_exclude_element="genres"
        Name_element="Short"        
        df = df[~df[column_to_exclude_element].str.contains(Name_element)]
        
        #To count individual elements when multiple elements are stored in a single cell 
        df_exploded, element_counts = fd.explode_dataframe(df, 'genres')
        
        Para=["startYear","genres_split"]
        Pivot_table=fd.Pivot_table(df_exploded,Para,False)
        
        y = fd.highest_dataframe_sorted_by(Pivot_table, 8, Para[0])
    
        # =============================================================================
        # Start Plot              
        # =============================================================================  
        fv.histogram_multi(Para,y)
        # =============================================================================
        # ============================================================================= 
    
    
    if Goal1[2] == True :
        print("Answer 3 of Goal 1")
        print()
        
        Para=["startYear","runtimeMinutes"]
        Pivot_table=fd.Pivot_table(df,Para,True)
        
        # add new column which is th avg value of all the other column times the column name
        y = fd.avg_column_value_index(Pivot_table)
        
        # remove from the dataframe the index which cannot be eval
        y = y[y.index.to_series().apply(lambda x: isinstance(fe.myeval(x), int))]
        
        # sort the data in function of column Para_sorted
        y.sort_index(ascending=True, inplace=True)
        
        # =============================================================================
        # Start Plot              
        # =============================================================================  
        fv.curve_multi(Para,y)
        # =============================================================================
        # ============================================================================= 


    if Goal1[3] == True :
        print("Answer 4 of Goal 1")
        print()
        
        # #To count individual elements when multiple elements are stored in a single cell 
        df_exploded, element_counts = fd.explode_dataframe(df, 'genres')
        
        Para=["genres_split","runtimeMinutes"]
        Pivot_table=fd.Pivot_table(df_exploded,Para,True)
        
        # add new column which is th avg value of all the other column times the column name
        y = fd.avg_column_value_index(Pivot_table)
        
        # sort the data in function of column Para_sorted
        y = y.sort_values(ascending=False)[:9]
        
        # =============================================================================
        # Start Plot              
        # =============================================================================  
        fv.histogram(Para,y,'Avg_minute')
        # =============================================================================
        # ============================================================================= 


    if Goal1[4] == True :
        print("Answer 5 of Goal 1")
        print()
            
        Para=["startYear","isAdult"]
        Pivot_table=fd.Pivot_table(df,Para,False)
        Pivot_table  = Pivot_table.drop(['Total'], axis=1)
    
        # sort the data in function of the index value
        Pivot_table.sort_index(ascending=True, inplace=True)       
        
        # =============================================================================
        # Start Plot              
        # =============================================================================  
        fv.histogram_multi(Para,Pivot_table)
        # =============================================================================
        # ============================================================================= 



    # # print(df[['genres']].value_counts())
    
    
    # df_short = df.loc[df['genres'].str.contains("Short", na=False)]
    # df_Documentary = df.loc[df['genres'].str.contains("Documentary", na=False)]
    # print(df_short)
    # print(df_Documentary)
    
    



    
    return None