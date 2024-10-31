#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 16:22:46 2024

@author: quentin
"""



"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions on the dataframe

#=============================================================================
   #=============================================================================
   #============================================================================="""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import Levenshtein

import Function_errors as fe

"""#=============================================================================
   #=============================================================================
   #============================================================================="""


    
def df_empty(columns, dtypes, index=None):
    """
    Goal: 
    - Create an empty dataframe.

    Parameters:
    - columns: List of column to create in the dataframe.
    - dtypes: List of type which corresponding to the columns list.

    Returns:
    - Dataframe which has been created.
    """
    assert len(columns)==len(dtypes)
    
    df = pd.DataFrame(index=index)
    
    for c,d in zip(columns, dtypes):
        df[c] = pd.Series(dtype=d)
        
    return df


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def explode_dataframe(df, Para):
    """
    Goal: 
    - Count individual elements when multiple elements are stored in a single cell
    - Explode the Dataframe where cells with muliple elements are counted multiple time.

    Parameters:
    - df: Dataframe
    - Para: List of column in the df for which the table should explode the cells with multiple elements.

    Returns:
    - Dataframe which have been explode and the new counts of each elements.
    
    Warning:
    - Can create very large array if many cells contain many elements.
    """
    
    df_temp = df.copy()
    
    # Step 1: Split the elements into lists of elements
    df_temp[Para+'_split'] = df_temp[Para].str.split(',')
    
    # Step 2: Explode the list of elements into individual rows
    df_temp = df_temp.explode(Para+'_split')
        
    # Step 3: Replace empty cells with 'Unknown' 
    df_temp[Para+'_split'] = df_temp[Para+'_split'].replace('', 'Unknown')
    
    # Step 3: Count the occurrences of each element
    element_counts = df_temp[Para+'_split'].str.strip().value_counts()
    
    # Display the result
    print("Dataframe have been explode base on parameter "+Para)
    print("The new counts of each elements is:")
    print(element_counts)
    print()
    
    return df_temp, element_counts


"""#=============================================================================
   #=============================================================================
   #============================================================================="""



def reverse_explode_dataframe(df_exploded, Para):
    """
    Goal: 
    - Revert the exploded data

    Parameters:
    - df_exploded: Dataframe
    - Para: List of column in the df for which the table should explode the cells with multiple elements.

    Returns:
    - Dataframe which have been explode and the new counts of each elements.
    
    Warning:
    - 
    """

    # Now let's revert back to the original DataFrame
    # Step 4: Group by the original ID and aggregate back to the original format
    df_reverted = df_exploded.groupby('tconst')[Para + '_split'].agg(lambda x: ', '.join(x.str.strip())).reset_index()
    
    # Rename the aggregated column back to the original name
    df_reverted.rename(columns={Para + '_split': Para}, inplace=True)
    
    # Display the reverted DataFrame
    print("Reverted DataFrame to original:")
    print(df_reverted)
    
    return df_reverted


"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def Pivot_table(csvFile,Para,remove_unknown_colmun, Large_file_memory=False):
    """
    Goal: Get the pivot of the Count table of the dataframe.
    From a table of dimension x with n indexes to a table of dimension x+1 with n-1 index

    Parameters:
    - csvFile: dataframe
    - Para: List of column in the dataframe
    - remove_unknown_value: Bolean (True or False)
    - Large_file_memory: Estimate if the file is too large to be open with panda and use dask instead.

    Returns:
    - Dataframe which have been pivoted.
    """
    
    df = csvFile[Para]
        
    # Get the Count table of the dataframe  
    y=df.value_counts(dropna=False).reset_index(name='Count') #dropna=False to count nan value    
    
    # Pivot the Count table 
    pivot_table = y.pivot(index=Para[0], 
                          columns=Para[1] if len(Para) == 2 else (Para[1], Para[2]), 
                          values='Count').fillna(0)
    
    # # Remove unknown column name if remove_unknown_colmun==True
    # if remove_unknown_colmun==True and Large_file_memory==False:
    #     pivot_table  = pivot_table.drop(['\\N'], axis=1)
    # elif remove_unknown_colmun==True and Large_file_memory==True:
    #     pivot_table = pivot_table.dropna()
    
    #Add last column for the sum of each rows named Total
    s = sum ( [pivot_table[i] for i in  pivot_table.columns])
    pivot_table2 = pivot_table.assign(Total=s).sort_values(by=['Total'], ascending=False)

    print("Dataframe of parameters "+' and '.join([str(i) for i in Para])+" have been pivoted.")
    print(pivot_table2)
    print()
    
    return pivot_table2


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def highest_dataframe_sorted_by(Pivot_table, first_n_top_amount_col, Para_sorted):
    """
    Goal: From a table take only the first first_n_top_amount_col largest sum columns.
    : Pivot_table where only the first first_n_top_amount_col have been which have been sorted and .

    Parameters:
    - Pivot_table: dataframe which have been pivoted.
    - first_n_top_amount_col: integer which represents the number of columns to keep.
    - Para_sorted: columns name which will be use to sort the table.

    Returns:
    - Table y: New table which contains the highest sum columns 
    and a column named 'Other' which is the sum of all the other columns
    """    
        
    # # remove from the dataframe the index which cannot be eval
    # y = Pivot_table[Pivot_table.index.to_series().apply(lambda x: isinstance(fe.myeval(x), int))] 
    y = Pivot_table
    
    # sort the data in function of column Para_sorted
    y = y.sort_values(by=[Para_sorted], ascending=True)     
    
    # Calculate the sum of each column
    column_sums = y.sum()
    
    # Sort columns by their sum in descending order
    if first_n_top_amount_col != None:
        top_columns = column_sums.nlargest(first_n_top_amount_col).index
    else:
        top_columns = column_sums.index
    
    # Create the new DataFrame 
    rest_columns = column_sums.index.difference(top_columns)
    s = sum ( [y[rest_columns][i] for i in  y[rest_columns].columns])
    y = y[top_columns].assign(Other=s)
        
    # Divide all the dataframe by the first column
    y_divided = y.div(y.iloc[:, 0], axis=0)*100
       
    # Remove the column Total and nan if needed from y and y_divided
    y_divided = y_divided.drop('Total', axis=1)
    y  = y.drop('Total', axis=1)
    
    print("Table created with only the first "+str(first_n_top_amount_col)+" columns+1 of the initial table.")
    print()
    return y

"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def avg_column_value_index(Pivot_table):
    """
    Goal: Creates in the table a new column which is th avg value of all the other column times the 
    column name.

    Parameters:
    - Pivot_table: dataframe which have been pivoted.

    Returns:
    - Table y: new avg_col column of the dataframe 
    """        
    
    #Get the sum of each rows, where each column element is multiplied by the column's name
    # s = sum([Pivot_table[i] * int(i) for i in Pivot_table.columns if isinstance(i, str) and i.isdigit()])
    # s = Pivot_table.apply(lambda row: sum([row[i] * float(i) for i in Pivot_table.columns if isinstance(i, float)]), axis=1)
    s = Pivot_table.apply(lambda row: sum([row[i] * int(i) for i in Pivot_table.columns[:-1]]), axis=1)
    
    print(s)
    
    #Add avg_col as the last column of the dataframe and sort the dataframe
    pivot_table2 = Pivot_table.assign(avg_col=s).sort_values(by=['avg_col'], ascending=False)
    
    print(pivot_table2)
    
    #Correct the avg_col by dividing the values with the total value
    pivot_table2['avg_col']=pivot_table2['avg_col']/pivot_table2['Total']
    
    return pivot_table2['avg_col']   


"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def name_check(df,Job,Name):
    """
    Goal: Get the list of names which represent the same person
    to overpass the bad names writing by the user.

    Parameters:
    - df: dataframe
    - Job: Profession of the name
    - Name: Name of the person

    Returns:
    - List of the names which have fulfill the test.
    """
        
    df_sec=list(df[Job])
    max_distance=2   
    accepted_name=[]
    for i in range(len(df_sec)):
        sim_name=are_names_close_with_inversion(Name, df_sec[i], max_distance)
        if sim_name==True and df_sec[i] not in accepted_name:
            accepted_name.append(df_sec[i])
                
    return accepted_name

# =============================================================================
# =============================================================================

def are_names_close_with_inversion(name1, name2, max_distance):
    """
    Goal: Check if two names are close enough, considering potential inversion of first and last names.

    Parameters:
    - name1: First name
    - name2: Second name
    - max_distance: Maximum allowed distance for the names to be considered close

    Returns:
    - True if the Levenshtein distance between the names (and their inversions) is less than 
    or equal to max_distance, else False
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

"""#=============================================================================
   #=============================================================================
   #============================================================================="""