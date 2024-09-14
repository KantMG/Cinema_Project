#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 16:22:46 2024

@author: quentin
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import Levenshtein



"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions on the dataframe

#=============================================================================
   #=============================================================================
   #============================================================================="""




"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def Pivot_table(csvFile,Para):
    
    df = csvFile[Para]
    #Count 
    y=df.value_counts(dropna=False).reset_index(name='Count') #dropna=False to count nan value
    pivot_table = y.pivot(index=Para[0], columns=Para[1], values='Count').fillna(0)
    
    #Add last column for the sum of the row named Total
    s = sum ( [pivot_table[i] for i in  pivot_table.columns])
    pivot_table2 = pivot_table.assign(Total=s).sort_values(by=['Total'], ascending=False)
    print(pivot_table2)
    print()
    return pivot_table2


"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def are_names_close_with_inversion(name1, name2, max_distance):
    """
    Check if two names are close enough, considering potential inversion of first and last names.

    Parameters:
    - name1: First name
    - name2: Second name
    - max_distance: Maximum allowed distance for the names to be considered close

    Returns:
    - True if the Levenshtein distance between the names (and their inversions) is less than or equal to max_distance, else False
    """
    
    def split_name(name):
        parts = name.split()
        if len(parts) == 2:
            return parts[0], parts[1]
        return parts[0], ""  # Handle cases with just a single name part
    
    try:
        name1, name2=name1.lower(), name2.lower()
        first1, last1 = split_name(name1)
        first2, last2 = split_name(name2)
    
        # Compare as is
        direct_comparison = (Levenshtein.distance(first1, first2) <= max_distance and
                             Levenshtein.distance(last1, last2) <= max_distance)
    
        # Compare with inversion
        inversion_comparison = (Levenshtein.distance(first1, last2) <= max_distance and
                                Levenshtein.distance(last1, first2) <= max_distance)
    
        return direct_comparison or inversion_comparison
    
    except AttributeError:
        return 'None'

# =============================================================================
# =============================================================================

def name_check(df,Job,Name):
    
    print(Name)
    
    df_sec=list(df[Job])
    max_distance=2   
    accepted_name=[]
    for i in range(len(df_sec)):
        sim_name=are_names_close_with_inversion(Name, df_sec[i], max_distance)
        if sim_name==True and df_sec[i] not in accepted_name:
            accepted_name.append(df_sec[i])
                
    return accepted_name

"""#=============================================================================
   #=============================================================================
   #============================================================================="""