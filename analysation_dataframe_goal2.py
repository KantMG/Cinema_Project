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



"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def movie_making_over_year(Project_path,Large_file_memory):

    print("Goal 2: Creates an interface which from a selected artist name will return informations.")
    print("1- How much is the growth of the movie making.")
    print("2- Which genres are the most popular.")
    print("3- How much evolve the runtimeMinutes of the movies.")
    print("4- Which genres have the shortest runtimeMinutes.")
    print("5- Does the violence in movies increases.")
    print()
    
    Goal2 = [True, False, False, False, False]

    # List of the required data file.
    List_file=['name.basics.tsv','title.basics.tsv','title.akas.tsv','title.crew.tsv']

    #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    if Large_file_memory==False:
        df = pd.read_csv(Project_path+List_file[0], sep=';', usecols=["tconst", "startYear", "runtimeMinutes", "genres", "isAdult"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    else:
        df = dd.read_csv(
            Project_path+List_file[0],
            sep='\t',
            usecols=["nconst", "primaryName", "birthYear", "deathYear", "primaryProfession", "knownForTitles"],
            encoding='utf-8',
            on_bad_lines='skip',
            quotechar='"',
            dtype={
                'runtimeMinutes': 'object',   # Read as object to handle invalid values
                'startYear': 'object',        # Read as object to handle invalid values
                'isAdult': 'object'           # Read as object to handle invalid values
            }
        )
        df = df.replace('\\N', np.nan)

    
    Para = ["nconst", "primaryName", "birthYear", "deathYear", "primaryProfession", "knownForTitles"]
    y = df
    
    
    
    
    print(df)


    # #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    # df = pd.read_csv(Project_path+List_file[0], sep='\t', usecols=["tconst", "originalTitle", "startYear", "runtimeMinutes", "genres", "isAdult"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    # #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    # df2 = dd.read_csv(Project_path+List_file[1], sep='\t', usecols=["titleId", "isOriginalTitle"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    # df2 = df2.loc[df2['isOriginalTitle'] == 1]
    
    # df3 = dd.read_csv(Project_path+List_file[2], sep='\t', usecols=["tconst", "directors"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    


    
    return Para,y