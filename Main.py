#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 19:06:36 2024

@author: quentin
"""



import pandas as pd

import Function_dataframe as fd
import Documentations_dataframe as dd
import Creation_test_dataframe as ctd


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


# Source for data set : 
source_data = 'https://developer.imdb.com/non-commercial-datasets/'

# Save the project on github with: !bash ./save_project_on_git.sh
GitHub_adress= 'https://github.com/KantMG/Cinema_Project'

# Save the project on the laptop:
Project_path='/home/quentin/Documents/Work/Data_analytics/Datasets/Cinema_Project/'


"""#=============================================================================
   #=============================================================================
   #============================================================================="""
 

# =============================================================================
# Get data infos
# =============================================================================

# All infos on the data set :  info_source( url of the data  , optional list of file  , detail_file )


# url                 :   url of the data
# files=None          :   optional list of file, to only get info on specific files
"""             List of the data files  
'title.akas'     'title.basics'       'title.crew'
'title.episode'  'title.principals'   'title.ratings'
'name.basics'   """
#detail_file=None    :   'Yes' or 'No' to get the detail on each file asked
dd.info_source(source_data,['title.akas','title.basics','title.crew','title.episode','title.principals','title.ratings','name.basics'],'No')



# =============================================================================
# Create data test (optional and only to do it one time)
# =============================================================================

# Project_path                :   Path of the current project
# Files=None                  :   List of the files to work on
# Rows_to_keep=None           :   The amount of rows to keep for the new data set
# Large_file_memory=False     :   Option to open with dask.dataframe if source file is too large

# ctd.test_data_creation(Project_path, ['title.akas'], 10**4, True)



# =============================================================================
# Start data analysis
# =============================================================================


# File_name='title.crew.tsv'

# #Create class 'pandas.core.frame.DataFrame'
# csvFile = pd.read_csv(Project_path+File_name,sep='\t')
# print(csvFile)
# print()





# title.crew.tsv.gz is an array of dimension 3
# tconst
# directors
# writers

# [10392848 rows x 3 columns]



# name.basics.tsv.gz is an array of dimension 6
# nconst
# primaryName
# birthYear
# deathYear
# primaryProfession
# knownForTitles

# [13769111 rows x 6 columns]
