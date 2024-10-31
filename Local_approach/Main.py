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
import time

import Function_dataframe as fd
import Function_visualisation as fv
import Documentations_data_files as ddf
import Creation_test_dataframe as ctd
import analysation_dataframe_goal1 as adg1
import analysation_dataframe_goal2 as adg2
import analysation_dataframe_goal3 as adg3
import interface_creation as ic


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

# ddf.info_source(source_data,['title.akas', 'title.basics', 'title.crew', 'title.ratings', 'title.principals', 'name.basics'],'Yes')



""" # =============================================================================
    # Create test data set (optional and only to do it one time)
    # ============================================================================= """

# Project_path                :   Path of the current project
# Files=None                  :   List of the files to work on
# Rows_to_keep=None           :   The amount of rows to keep for the new data set
# Large_file_memory=False     :   Option to open with dask.dataframe if source file is too large

# ctd.test_data_creation(Project_path, ['title.akas.tsv','title.basics.tsv', 'title.crew.tsv', 'title.episode.tsv', 'title.principals.tsv', 'title.ratings.tsv', 'name.basics.tsv'], 10**4, True)

# ctd.test_data_creation(Project_path, ['title.akas.tsv'], 10**4, True)


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



Large_file_memory = True
Get_file_sys_mem = False
desired_number_of_partitions = 10
# if Test_data == True:
#     Large_file_memory = False
    
def main():
    print("The analysis start from here.")
    print()

    Para, y = adg3.movie_making_over_year(Project_path,Large_file_memory, desired_number_of_partitions, Get_file_sys_mem)
    
    # Para, y = ic.dask_interface(Project_path,Large_file_memory, Get_file_sys_mem)
    
    
    
    return Para, y



if __name__ == "__main__":
    Para, y = main()



