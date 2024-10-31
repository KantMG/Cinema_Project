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

def movie_making_over_year(Project_path,Large_file_memory, desired_number_of_partitions, Get_file_sys_mem):

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
    List_file=['title.basics.tsv','title.crew.tsv']

    #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    if Large_file_memory==False:
        # List to store DataFrames
        df_list = []

        # Path to your CSV files (adjust as needed)
        csv_files_path = Project_path+"*.csv"  # This selects all CSV files in the directory
        common_column = 'tconst'  # Replace with the actual common variable (e.g., 'ID', 'Date')

        
        # Use glob to find all the CSV files
        for file in List_file:
            if file =='title.basics.tsv':
                usecol=["tconst", "startYear", "runtimeMinutes", "genres", "isAdult"]
            if file =='title.crew.tsv':
                usecol=["tconst", "directors", "writers"]
            print(usecol)
            df = pd.read_csv(Project_path+file, sep=';', usecols=usecol, encoding='utf-8', on_bad_lines='skip', quotechar='"')
            df_list.append(df)  # Append the DataFrame to the list
        
        # Merge all DataFrames on the common variable
        df1 = pd.concat(df_list, axis=0, join='outer', ignore_index=True).drop_duplicates(subset=common_column)
        
        
        print(df1)
        
        tsv_file_path = 'name.basics.tsv'
        # usecol = ["nconst", "primaryName", "birthYear", "deathYear", "primaryProfession"]
        usecol = ["nconst", "primaryName", "birthYear", "deathYear", "primaryProfession"]
        name_df = pd.read_csv(Project_path+tsv_file_path, sep=';', usecols=usecol, encoding='utf-8', on_bad_lines='skip', quotechar='"')
        print(name_df.head())

        # Create a dictionary to map nconst to primaryName
        id_to_name = dict(zip(name_df['nconst'], name_df['primaryName']))


        # Define a function to replace IDs with names
        def replace_ids_with_names(id_list):
            if pd.isna(id_list):
                return id_list
            ids = id_list.split(',')
            names = [id_to_name.get(i, i) for i in ids]  # Replace ID with name or leave ID if not found
            return ','.join(names)
        
        # Apply the function to both 'directors' and 'writers' columns
        df1['directors'] = df1['directors'].apply(replace_ids_with_names)
        df1['writers'] = df1['writers'].apply(replace_ids_with_names)
        
        # Check the result
        print(df1[["tconst", "startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers"]].head())



        # # Define which column in df1 contains the ID values (as part of cell content)
        # id_column_in_df1 = 'directors'  # Replace with the actual column name in df1 that contains the IDs

        # # Define the key (ID column) in df2
        # id_column_in_df2 = 'nconst'  # Replace with the column name that represents the ID in df2
        
        # # Example of cells in df1[id_column_in_df1] containing an ID from df2[id_column_in_df2]
        # # Extract the ID values from df1. Assume ID is embedded directly or part of the string, and you need to extract it.
        # # For simplicity, this example assumes the entire cell is just the ID. Adjust extraction if necessary.
        # df1['extracted_id'] = df1[id_column_in_df1]  # If IDs are directly in this column
        
        # # If the IDs are embedded in text, use this as an example of extracting them (adjust the regex or method as needed)
        # # df1['extracted_id'] = df1[id_column_in_df1].str.extract('(\d+)')  # Example regex to extract digits
        
        # # Merge df1 with df2 based on the extracted ID
        # merged_df = pd.merge(df1, df2, left_on='extracted_id', right_on=id_column_in_df2, how='left')
        
        # # Now, merged_df contains the original columns from df1, plus the corresponding data from df2
        
        # # Optionally, drop the extracted ID column if you no longer need it
        # merged_df.drop('extracted_id', axis=1, inplace=True)

        
        # merged_df = pd.merge(merged_df, tsv_df, on=common_column, how='left')



    # If you look for the name
    
    




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

    
    # Para = ["nconst", "primaryName", "birthYear", "deathYear", "primaryProfession", "knownForTitles"]
    # y = df
    
    
    
    
    # print(merged_df)


    # #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    # df = pd.read_csv(Project_path+List_file[0], sep='\t', usecols=["tconst", "originalTitle", "startYear", "runtimeMinutes", "genres", "isAdult"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    # #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    # df2 = dd.read_csv(Project_path+List_file[1], sep='\t', usecols=["titleId", "isOriginalTitle"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    # df2 = df2.loc[df2['isOriginalTitle'] == 1]
    
    # df3 = dd.read_csv(Project_path+List_file[2], sep='\t', usecols=["tconst", "directors"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    


    Para, y = None, None
    
    return Para,y