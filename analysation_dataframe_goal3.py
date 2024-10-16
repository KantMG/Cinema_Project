#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:05:41 2024

@author: quentin
"""



"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of specific dataframe analysis

#=============================================================================
   #=============================================================================
   #============================================================================="""

import time

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
import data_infos_system as dis
import open_dataframe as od


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


def movie_making_over_year(Project_path,Large_file_memory, desired_number_of_partitions, Get_file_sys_mem):


    # Start the timer
    start_time = time.time()    

    print("Goal 3: Creates a search by name.")
    print("1- How much is the growth of the movie making.")
    print("2- Which genres are the most popular.")
    print("3- How much evolve the runtimeMinutes of the movies.")
    print("4- Which genres have the shortest runtimeMinutes.")
    print("5- Does the violence in movies increases.")
    print()
    
    look_by_name = True
    if look_by_name :

        List_col = ["nconst", "primaryName", "birthYear", "deathYear"]
        
        List_filter = [None, "William K.L. Dickson*", None, None]

        name_info = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        
        if name_info['nconst'].count() > 1:
            print("The DataFrame has more than one row.")
            return None, None
        else:
            # Code to execute if the DataFrame has zero or one row
            print("The DataFrame has one or zero rows.")
            Name_to_look_for = str(name_info['nconst'].iloc[0])
            print(Name_to_look_for)
            print()
        
    # Name_to_look_for = "nm0000001"

    List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters", "title", "isOriginalTitle"]
    
    List_filter = [None, None, None, None, None, None, ">=5.6", None, Name_to_look_for, None, None, None, True]
    
    # List_col = ["nconst", "title", "isOriginalTitle"]

    # List_filter = [Name_to_look_for, None, True]

    df = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
    
    od.log_performance("Full research", start_time)
    od.plot_performance_logs()
    
    Goal1 = [False, False, False, False, False]

    if Goal1[0] == True:
        print("Answer 1 and 2 of Goal 1")
        print()
        
        Para=["startYear","averageRating"]
        Pivot_table=fd.Pivot_table(df,Para,False, Large_file_memory)
        
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


    # print(df)


    Para, y = None, None
    
    return Para,y