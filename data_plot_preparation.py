#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 17:50:57 2024

@author: quentin
"""


"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions for dataframe preparation before plot

#=============================================================================
   #=============================================================================
   #============================================================================="""


import Function_dataframe as fd


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def data_preparation_for_plot(df_temp, x_column, y_column, z_column, f_column, g_column, Large_file_memory):

    """
    Goal: Get the pivot of the Count table of the dataframe.
    From a table of dimension x with n indexes to a table of dimension x+1 with n-1 index

    Parameters:
    - df_temp: dataframe which has been created temporary
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - f_column: Function to operate on df_temp[x_column,y_column]
    - g_column: Type of Graphyque for the figure.
    - Large_file_memory: Estimate if the file is too large to be open with panda and use dask instead.

    Returns:
    - Para: List of column in the dataframe (can be different of [x_column,y_column])
    - data_for_plot: Data to plot.
    - x_column: Column in the dataframe (it could have change)
    - y_column: Column in the dataframe (it could have change)
    - z_column: Column in the dataframe (it could have change)
    """

    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]

    # print("Delete the rows with unknown value and split the column with multiple value per cell.")
    Para, df_temp, x_column, y_column, z_column = delete_rows_unknow_and_split(df_temp, x_column, y_column, z_column, Large_file_memory)

    if x_column not in df_col_string:
        df_temp = df_temp[df_temp[x_column] >= 0]
    if str(y_column)!='None':
        if y_column not in df_col_string:
            df_temp = df_temp[df_temp[y_column] >= 0]   
    if str(z_column)!='None':
        if z_column not in df_col_string:
            df_temp = df_temp[df_temp[z_column] >= 0]        

    #Case where y_column is None
    if str(y_column)=='None':
        # Get the Count table of the dataframe  
        data_for_plot=df_temp.value_counts(dropna=False).reset_index(name='count') #dropna=False to count nan value
        # sort the data in function of column Para_sorted
        data_for_plot = data_for_plot.sort_values(by=Para[0], ascending=True)
        
    #Case where y_column is not None and z_column is None
    elif str(y_column)!='None' and str(z_column)=='None':
        # Calculate average z_column and count for each (x_column, y_column) combination
        data_for_plot = df_temp.groupby([x_column, y_column]).size().reset_index(name='count')
                
    #Case where z_column is not None
    else:
        # Calculate average z_column and count for each (x_column, y_column) combination
        data_for_plot = df_temp.groupby([x_column, y_column]).agg(
            avg_z_column=('{}'.format(z_column), 'mean'),
            count=('{}'.format(z_column), 'size')
        ).reset_index()
        avg_col_name = 'avg_' + z_column
        data_for_plot.rename(columns={'avg_z_column': avg_col_name}, inplace=True)
            
    return Para, data_for_plot, x_column, y_column, z_column


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def delete_rows_unknow_and_split(df_temp, x_column, y_column, z_column, Large_file_memory):

    """
    Goal: Delete the rows in a dataframe which correspond to '\\N'.

    Parameters:
    - df_temp: dataframe which has been created temporary.
    - x_column: Column in the dataframe.
    - y_column: Column in the dataframe (can be None).
    - z_column: Column in the dataframe (can be None).
    - Large_file_memory: Estimate if the file is too large to be open with panda and use dask instead.
    
    Returns:
    - Para: List of column in the dataframe (can be different of [x_column,y_column]).
    - df_temp: dataframe which has been created temporary.
    - x_column: Column in the dataframe (it could have change)
    - y_column: Column in the dataframe (it could have change)
    - z_column: Column in the dataframe (it could have change)
    """
    
    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres", "directors", "writers", "category"]

    # Columns in the dataframe which are numerics.
    df_col_numeric = ["startYear", "runtimeMinutes", "averageRating", "numVotes"]

    if str(x_column) in df_col_numeric:
        df_temp[x_column] = df_temp[x_column].replace('', '0').fillna('0').astype(int)
    if str(y_column) in df_col_numeric:
        df_temp[y_column] = df_temp[y_column].replace('', '0').fillna('0').astype(int)
    if str(z_column) in df_col_numeric:
        df_temp[z_column] = df_temp[z_column].replace('', '0').fillna('0').astype(int)
        
    if str(x_column) in df_col_string:
        df_temp[x_column] = df_temp[x_column].replace('', 'Unknown').astype(str)
    if str(y_column) in df_col_string:
        df_temp[y_column] = df_temp[y_column].replace('', 'Unknown').astype(str)
    if str(z_column) in df_col_string:
        df_temp[z_column] = df_temp[z_column].replace('', 'Unknown').astype(str)        
        
    if Large_file_memory==True:
        #Convert the Dask DataFrame to a Pandas DataFrame
        df_temp = df_temp.compute()
    
    if x_column in df_col_string:
        #To count individual elements when multiple elements are stored in a single cell 
        df_temp, element_counts = fd.explode_dataframe(df_temp, x_column)
        x_column = x_column+'_split'

    if y_column in df_col_string:
        #To count individual elements when multiple elements are stored in a single cell 
        df_temp, element_counts = fd.explode_dataframe(df_temp, y_column)
        y_column = y_column+'_split'

    if z_column in df_col_string:
        #To count individual elements when multiple elements are stored in a single cell 
        df_temp, element_counts = fd.explode_dataframe(df_temp, z_column)
        z_column = z_column+'_split'

    #Case where y_column is None
    if str(y_column)=='None':    
        df_temp = df_temp[[x_column]]
        Para=[x_column]
    elif str(y_column)!='None' and str(z_column)=='None':
        df_temp = df_temp[[x_column, y_column]]
        Para=[x_column, y_column]
    else:
        df_temp = df_temp[[x_column, y_column, z_column]]
        Para=[x_column, y_column, z_column]        

    return Para, df_temp, x_column, y_column, z_column


"""#=============================================================================
   #=============================================================================
   #============================================================================="""
