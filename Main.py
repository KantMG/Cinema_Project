#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 19:06:36 2024

@author: quentin
"""


"""
                        THE SEVENTH ART, A STORY OF INFLUENCE
THIS PROJECT ENLIGHT THE EVOLUTION OVER THE YEARS OF THE MOVIE AND SERIE MAKING.
THE ADAPTATION OF THE WAY OF PRODUCTION AS WELL AS OUR WAY OF CONSOMATION ARE ANALYSED.
HOW MUCH THE COUNTRIES ARE INVESTING IN THE FILMS PRODUCTION AND WHICH IS THE LEVEL OF INFLUENCE
OF A COUNTRY OVER THE OTHERS.
"""



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

import pandas as pd

import Function_dataframe as fd
import Documentations_dataframe as dd
import Creation_test_dataframe as ctd
import analysation_dataframe as ad


""" # =============================================================================
    # Get data infos
    # ============================================================================= """

# url                 :   url of the data
# files=None          :   optional list of file, to only get info on specific files
"""             List of the data files  
'title.akas'     'title.basics'       'title.crew'
'title.episode'  'title.principals'   'title.ratings'
'name.basics'   """
#detail_file=None    :   'Yes' or 'No' to get the detail on each file asked

# dd.info_source(source_data,['title.akas', 'title.basics', 'title.crew', 'name.basics'],'Yes')



""" # =============================================================================
    # Create test data set (optional and only to do it one time)
    # ============================================================================= """

# Project_path                :   Path of the current project
# Files=None                  :   List of the files to work on
# Rows_to_keep=None           :   The amount of rows to keep for the new data set
# Large_file_memory=False     :   Option to open with dask.dataframe if source file is too large

# ctd.test_data_creation(Project_path, ['title.akas'], 10**4, True)



""" # =============================================================================
    # Start data analysis
    # ============================================================================= """


# =============================================================================
# Choose to work on the source data set or the test data set 
# =============================================================================

Test_data = True

if Test_data == True:
    Project_path=Project_path+'Test_data/'

# =============================================================================



# =============================================================================
# Amount of movie making by each country over the years
# =============================================================================

ad.movie_making_over_year(Project_path)





