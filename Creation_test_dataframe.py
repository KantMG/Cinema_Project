#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 16:37:35 2024

@author: quentin
"""


import pandas as pd
import dask.dataframe as dd

"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Creation of data set from the original source data. 
    A small amount of the source data set is taken in order to have light file.
    The goal of this section is to build the analysis more easily by managging low memory files.

#=============================================================================
   #=============================================================================
   #============================================================================="""


# Project_path                :   Path of the current project
# Files=None                  :   List of the files to work on
# Rows_to_keep=None           :   The amount of rows to keep for the new data set
# Large_file_memory=False     :   Option to open with dask.dataframe if source file is too large


def test_data_creation(Project_path, Files=None, Rows_to_keep=None, Large_file_memory=False):
    
    
    for data in Files:
        #Create class 'pandas.core.frame.DataFrame'
        if Large_file_memory==False:
            df = pd.read_csv(Project_path+data+'.tsv',sep='\t')
        else:
            df = dd.read_csv(Project_path+data+'.tsv',sep='\t')
        print(df)
        print()
        
        # Keep only the first "Rows_to_keep" rows
        df_cut = df.head(Rows_to_keep)
        print(df_cut)
        print()   
        
        # Save the new data set into the Test_data directory
        df_cut.to_csv(Project_path+'Test_data/'+data+'.tsv', index=False, sep=';', encoding='utf-8', quotechar='"')
