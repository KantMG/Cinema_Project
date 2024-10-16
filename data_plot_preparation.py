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


import dash
from dash import dcc, html, Input, Output, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from collections import OrderedDict
import plotly.express as px
import webbrowser

import matplotlib
matplotlib.use('Agg')  # Use the Agg backend (no GUI)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import plotly.tools as tls  # For converting Matplotlib to Plotly
import plotly.graph_objects as go

import Function_dataframe as fd
import Function_errors as fe
import Function_visualisation as fv
import data_plot_preparation as dpp


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def data_preparation_for_plot(df_temp, x_column, y_column, z_column, f_column, Large_file_memory):

    """
    Goal: Get the pivot of the Count table of the dataframe.
    From a table of dimension x with n indexes to a table of dimension x+1 with n-1 index

    Parameters:
    - df_temp: dataframe which has been created temporary
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Function to operate on df_temp[x_column,y_column]
    - Large_file_memory: Estimate if the file is too large to be open with panda and use dask instead.

    Returns:
    - Para: List of column in the dataframe (can be different of [x_column,y_column])
    - y: Data to plot.
    """

    print("Delete the rows with unknown value and split the column with multiple value per cell.")
    Para, df_temp = delete_rows_unknow_and_split(df_temp, x_column, y_column)
    
    print(Para)
    print(df_temp)
    
    #Case where y_column is None
    if str(y_column)=='None':
        
        df_temp = df_temp[[Para[0]]]
                
        # Get the Count table of the dataframe  
        y=df_temp.value_counts(dropna=False).reset_index(name='Count') #dropna=False to count nan value
        
        # sort the data in function of column Para_sorted
        y = y.sort_values(by=Para[0], ascending=True)
        

    #Case where y_column is not None
    else:

        Pivot_table=fd.Pivot_table(df_temp,Para,False, Large_file_memory)

        if str(z_column)=='None':
            print("1")
            if x_column!='genres':
                print("2")
                y = fd.highest_dataframe_sorted_by(Pivot_table, 8, Para[0])
            else:
                print("3")
                y = Pivot_table.sort_values(by=['Total'], ascending=True)
            print("4")


            
        elif z_column=='Avg':
            
            # add new column which is th avg value of all the other column times the column name
            y = fd.avg_column_value_index(Pivot_table)
            
            print("2", y)
            
            if x_column!='genres':
                
                # remove from the dataframe the index which cannot be eval
                y = y[y.index.to_series().apply(lambda x: isinstance(fe.myeval(x), int))]
                
                print("3", y)
                
                # sort the data in function of column Para_sorted
                y.sort_index(ascending=True, inplace=True)  
                
            else:
                
                y.sort_values(ascending=True)
                
    print(y)
    return Para, y


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def delete_rows_unknow(df_temp, x_column, y_column):

    """
    Goal: Delete the rows in a dataframe which correspond to '\\N'.

    Parameters:
    - df_temp: dataframe which has been created temporary.
    - x_column: Column in the dataframe.
    - y_column: Column in the dataframe (can be None).

    Returns:
    - Para: List of column in the dataframe (can be different of [x_column,y_column]).
    - df_temp: dataframe which has been created temporary.
    """
        
    #Case where y_column is None
    if str(y_column)=='None':    

        df_temp = df_temp[[x_column]]
        Para=[x_column]

        # Filter out rows where 'Value' is '\\N'
        df_temp.replace('\\N', np.nan, inplace=True)
        df_temp.dropna(inplace=True)         
    
    else:
                
        df_temp = df_temp[[x_column, y_column]]
        Para=[x_column, y_column]
        
        # Filter out rows where 'Value' is '\\N'
        df_temp.replace('\\N', np.nan, inplace=True)
        df_temp.dropna(inplace=True)
        
    return Para, df_temp


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def delete_rows_unknow_and_split(df_temp, x_column, y_column):

    """
    Goal: Delete the rows in a dataframe which correspond to '\\N'.

    Parameters:
    - df_temp: dataframe which has been created temporary.
    - x_column: Column in the dataframe.
    - y_column: Column in the dataframe (can be None).

    Returns:
    - Para: List of column in the dataframe (can be different of [x_column,y_column]).
    - df_temp: dataframe which has been created temporary.
    """
    
    
    #Case where y_column is None
    if str(y_column)=='None':    

        df_temp = df_temp[[x_column]]
        Para=[x_column]

        # Filter out rows where 'Value' is '\\N'
        df_temp.replace('\\N', np.nan, inplace=True)
        df_temp.dropna(inplace=True)

        # # remove from the dataframe the index which cannot be eval
        # df_temp = df_temp[df_temp.index.to_series().apply(lambda x: isinstance(fe.myeval(x), int))] 
        
        # # Filter out rows where 'Value' is '\\N'
        # df_temp = df_temp[df_temp != '\\N']      
        
    
    else:

        df_temp = df_temp[[x_column, y_column]]
        Para=[x_column, y_column]
        
        # Filter out rows where 'Value' is '\\N'
        df_temp.replace('\\N', np.nan, inplace=True)
        df_temp.dropna(inplace=True)
        
    
    
    if x_column=='genres':
        #To count individual elements when multiple elements are stored in a single cell 
        df_temp, element_counts = fd.explode_dataframe(df_temp, x_column)
        Para=[x_column+"_split",y_column]

    
    if y_column=='genres':
        #To count individual elements when multiple elements are stored in a single cell 
        df_temp, element_counts = fd.explode_dataframe(df_temp, y_column)
        Para=[x_column,y_column+"_split"]    

    
    return Para, df_temp
