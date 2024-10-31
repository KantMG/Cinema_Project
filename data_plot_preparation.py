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
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import plotly.tools as tls  # For converting Matplotlib to Plotly
import plotly.graph_objects as go
import plotly.express as px

import Function_dataframe as fd
import Function_errors as fe
import Function_visualisation as fv
import data_plot_preparation as dpp


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
    df_col_string = ["genres", "directors", "writers", "category"]

    # print("Delete the rows with unknown value and split the column with multiple value per cell.")
    Para, df_temp, x_column, y_column, z_column = delete_rows_unknow_and_split(df_temp, x_column, y_column, z_column, Large_file_memory)

    #Case where y_column is None
    if str(y_column)=='None':

        df_temp = df_temp[[Para[0]]]

        # Get the Count table of the dataframe  
        data_for_plot=df_temp.value_counts(dropna=False).reset_index(name='Count') #dropna=False to count nan value
        
        # sort the data in function of column Para_sorted
        data_for_plot = data_for_plot.sort_values(by=Para[0], ascending=True)

        # Remove rows where any column contains -1.0
        data_for_plot = data_for_plot[data_for_plot[Para[0]] != -1.0]
        

    #Case where y_column is not None
    elif str(y_column)!='None' and str(z_column)=='None':

        Pivot_table=fd.Pivot_table(df_temp,Para,False, True)
        
        print(Pivot_table)
        
        # Remove rows where any column contains -1.0
        if -1.0 in Pivot_table.index:
            Pivot_table = Pivot_table[Pivot_table.index != -1.0]
        # Remove columns where any row contains -1.0
        if -1.0 in Pivot_table.columns:
            Pivot_table = Pivot_table.drop(columns=[-1.0])
        
        if g_column == "Colormesh":
            first_n_top_amount_col = None
        else:
            first_n_top_amount_col = 5
        if str(f_column)=='None':
            if x_column not in df_col_string:
                data_for_plot = fd.highest_dataframe_sorted_by(Pivot_table, first_n_top_amount_col, Para[0])
            else:
                data_for_plot = Pivot_table.sort_values(by=['Total'], ascending=True)
        
        elif f_column=='Avg':
            # add new column which is th avg value of all the other column times the column name
            data_for_plot = fd.avg_column_value_index(Pivot_table)
            if x_column not in df_col_string:
                # sort the data in function of column Para_sorted
                data_for_plot.sort_index(ascending=True, inplace=True)  
            else:
                data_for_plot.sort_values(ascending=True)
                
    #Case where z_column is not None
    else:
        Pivot_table=fd.Pivot_table(df_temp,Para,False, True)
        # Remove rows where any column contains -1.0
        if -1.0 in Pivot_table.index:
            Pivot_table = Pivot_table[Pivot_table.index != -1.0]
        # Remove columns where any row contains -1.0
        if -1.0 in Pivot_table.columns:
            Pivot_table = Pivot_table.drop(columns=[-1.0])

        # # add new column which is th avg value of all the other column times the column name
        # data_for_plot = fd.avg_column_value_index(Pivot_table)
        # if x_column not in df_col_string:
        #     # sort the data in function of column Para_sorted
        #     data_for_plot.sort_index(ascending=True, inplace=True)  
        # else:
        #     data_for_plot.sort_values(ascending=True)
            

        first_n_top_amount_col = 5
        if str(f_column)=='None':
            if x_column not in df_col_string:
                data_for_plot = fd.highest_dataframe_sorted_by(Pivot_table, first_n_top_amount_col, Para[0])
            else:
                data_for_plot = Pivot_table.sort_values(by=['Total'], ascending=True)


            
    # print(data_for_plot)
    return Para, data_for_plot, x_column


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def replace_rows_unknow(df_temp):

    """
    Goal: Delete the rows in a dataframe which correspond to '\\N'.

    Parameters:
    - df_temp: dataframe which has been created temporary.

    Returns:
    - df_temp: dataframe which has been created temporary.
    """
        
    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres", "directors", "writers", "category"]

    # Columns in the dataframe which are numerics.
    df_col_numeric = ["startYear", "runtimeMinutes", "averageRating", "numVotes"]
    
    for col in df_temp.columns:
        if str(col) in df_col_numeric:
            df_temp[col] = df_temp[col].replace('', '0').fillna('0').astype(int)
        if str(col) in df_col_string:
            df_temp[col] = df_temp[col].replace('', 'Unknown').astype(str)

    return df_temp



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

    Returns:
    - Para: List of column in the dataframe (can be different of [x_column,y_column]).
    - df_temp: dataframe which has been created temporary.
    - x_column: Column in the dataframe (it could have change)
    - y_column: Column in the dataframe (it could have change)
    - z_column: Column in the dataframe (it could have change)
    """
    print(x_column, y_column, z_column)
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

def figure_plotly(fig, ax, x_column, y_column, z_column, f_column, g_column, d_column, Para, data_for_plot):

    """
    Goal: Create the plot inside the figure regarding the inputs.

    Parameters:
    - fig: matplotlib figure.
    - ax: axis of fig.
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - f_column: Function to operate on df_temp[x_column,y_column]
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.
    - Para: List of column in the dataframe (can be different of [x_column,y_column])
    - data_for_plot: Data to plot.

    Returns:
    - dropdowns_with_labels: The finalized dropdowns figure. 
    """
    
    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]
    
    # Define a list of colors for the bars
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    legend = "None"
    
    
    fig_y_value, y_values = None, None

    if d_column=="1D": 
        
        if str(y_column)=='None':
            
            # Convert the DataFrame index to a list
            if x_column not in df_col_string:
                x_values = list(map(int, data_for_plot[Para[0]]))
            else:
                x_values = list(data_for_plot[Para[0]])
            
            if g_column=="Histogram":
                bars = ax.bar(np.arange(len(x_values)), data_for_plot["Count"])
                # Add rounded corners with a specified radius
                # draw_rounded_bars(ax, np.arange(len(x_values)), data_for_plot["Count"])
            if g_column=="Curve":
                ax.plot(np.arange(len(x_values)), data_for_plot["Count"], linewidth=4.)
            if g_column=="Scatter":
                ax.scatter(np.arange(len(x_values)), data_for_plot["Count"], linewidth=4.)
        else:
            
            # Convert the DataFrame index to a list
            if x_column not in df_col_string:
                x_values = list(map(int, data_for_plot.index))
            else:
                x_values = data_for_plot.index
            
            if str(f_column)=='None':
                bottom = np.zeros(len(data_for_plot.index))
                # Plot the stacked bar chart
                bars_list = []  # List to hold bar objects for the legend
                for i, (element_col, data_val) in enumerate(data_for_plot.items()):
                    if g_column=="Histogram":
                        bars = ax.bar(np.arange(len(x_values)), data_val, label=element_col, bottom=bottom, color=colors[i % len(colors)])  # Color assignment
                    if g_column=="Curve":
                        bars = ax.plot(np.arange(len(x_values)), data_val, label=element_col, linewidth=4., color=colors[i % len(colors)])
                    if g_column=="Scatter":
                        bars = ax.scatter(np.arange(len(x_values)), data_val, label=element_col, linewidth=4., color=colors[i % len(colors)])
                    bars_list.append(bars)  # Store the bars
                    bottom += data_val              
                # Create a custom legend using the bars created
                legend_handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors[:len(data_for_plot)]]
                legend_labels = data_for_plot.columns.tolist()  # Get the labels from DataFrame columns
                # Customize the legend to ensure it reflects the colors of the bars
                legend = ax.legend(legend_handles, legend_labels, ncol=2, handletextpad=0.001)
                # legend = ax.legend(ncol=2)
                for text in legend.get_texts():
                    text.set_color('white')  # Set the color of the legend text
                    text.set_fontsize(15)  # Set the font size of the legend text
        
            elif str(f_column) == "Avg":
                if g_column=="Histogram":
                    ax.bar(np.arange(len(x_values)), data_for_plot)
                if g_column=="Curve":
                    ax.plot(np.arange(len(x_values)), data_for_plot, linewidth=4.)
                if g_column=="Scatter":
                    ax.scatter(np.arange(len(x_values)), data_for_plot, linewidth=4.)
            
        # Check if all elements are either int or float
        is_numeric = all(isinstance(x, (int, float)) for x in x_values)
        if is_numeric:
            x_values = np.array(x_values)
            fig_x_value = x_values-min(x_values)
        else:
            fig_x_value = list(np.arange(len(x_values)))
                    
        # Now, convert Matplotlib figure to Plotly
        plotly_fig = tls.mpl_to_plotly(fig)  # Convert the Matplotlib figure to Plotly  
    
    elif y_column is not None and (d_column == "2D" or d_column == "3D"):
        
        if x_column in df_col_string or y_column in df_col_string:
            print("Errors")
        else:

            # Remove rows where any column contains "Other"
            if "Other" in data_for_plot.index:
                data_for_plot = data_for_plot[data_for_plot.index != "Other"]
            # Remove columns where any row contains "Other"
            if "Other" in data_for_plot.columns:
                data_for_plot = data_for_plot.drop(columns=["Other"])
            
            # Sort the columns in ascending order based on column labels
            sorted_columns = sorted(data_for_plot.columns)
            # Reindex the DataFrame to reflect the new sorted column order
            data_for_plot = data_for_plot.reindex(columns=sorted_columns)

            x_values = list(data_for_plot.index)
            y_values = list(data_for_plot.columns)  
                        
            if d_column == "2D":
                data_for_plot = data_for_plot.T  # Transposed the DataFrame
                data_for_plot = data_for_plot.values  # This will give you just the data without indices and column names
                vmin, vmax = data_for_plot.min(), data_for_plot.max() # Find vmin and vmax from the values only
                
            # Check if all elements are either int or float
            is_numeric = all(isinstance(x, (int, float)) for x in x_values)
            if is_numeric:
                x_values = np.array(x_values)
                fig_x_value = x_values-min(x_values)
                y_values = np.array(y_values)
                fig_y_value = y_values-min(y_values) 
            else:
                fig_x_value = list(np.arrange(len(x_values)))
                fig_y_value = list(np.arrange(len(y_values)))
            
            if d_column == "2D":
                
                plotly_fig = go.Heatmap(
                    z=data_for_plot,
                    x=fig_x_value,
                    y=fig_y_value,
                    colorscale='Jet',
                    zmin=vmin,
                    zmax=vmax,
                    coloraxis="coloraxis"  # Assign to coloraxis for layout reference
                )   
            
            if d_column == "3D" and g_column == "Histogram":
                                
                z = data_for_plot.iloc[:, 1:].values
                plotly_fig = go.Surface(z=z, showscale=False)

    elif y_column is None and d_column == "2D" :    
        if g_column=="Pie":
            x_values,fig_x_value,y_values,fig_y_value=None,None,None,None
            plotly_fig = px.pie(data_for_plot, values="Count", names=x_column)
        
    if g_column!="Pie":
        # Determine the interval for x-axis
        num_ticks = 7
        if len(x_values) > num_ticks:
            interval = max(1, len(x_values) // num_ticks)  # Calculate the interval for x-ticks
            # Set x-ticks to every 'interval'-th x value's index
            fig_x_value = fig_x_value[::interval]
            x_values = x_values[::interval]
            
        if d_column == "2D" or d_column == "3D":
            # Determine the interval for y-axis
            num_ticks = 7
            if len(y_values) > num_ticks:
                interval = max(1, len(y_values) // num_ticks)  # Calculate the interval for x-ticks
                # Set x-ticks to every 'interval'-th x value's index
                fig_y_value = fig_y_value[::interval]
                y_values = y_values[::interval]    

        
    return plotly_fig, fig_x_value, x_values, fig_y_value, y_values, legend        
        


def fig_update_layout(fig_json_serializable,figname,xlabel,x_values,fig_x_value,ylabel,y_values,fig_y_value,zlabel,legend,g_column,d_column):
    
    
    if g_column != 'Pie':
    
        fig_json_serializable.update_layout(
            plot_bgcolor='#1e1e1e',  # Darker background for the plot area
            paper_bgcolor='#343a40',  # Dark gray for the paper
            font=dict(color='white'),  # White text color
            title = figname,
            title_font=dict(size=20, color='white'),  # Title styling
            # X-axis and Y-axis styling
            xaxis=dict(
                tickvals=fig_x_value,  # Set the tick positions
                ticktext=x_values,  # Set the tick labels to the genre names
                title=dict(text=xlabel, font=dict(size=20, color='white')),  # X-axis label styling
                tickfont=dict(color='white', size=18),  # X-axis tick color
                tickangle=0,  # Rotate the x-axis labels for better readability
                showgrid=True,  # Grid styling
                gridcolor='gray',  # Grid color
                categoryorder='category ascending',  # Ensures categorical x-values are treated correctly
                nticks=10
            ),
            yaxis=dict(
                tickvals=fig_y_value,  # Set the tick positions
                ticktext=y_values,  # Set the tick labels to the genre names
                title=dict(text=ylabel, font=dict(size=20, color='white')),  # Y-axis label styling
                tickfont=dict(color='white', size=18),  # Y-axis tick color
                showgrid=True,  # Grid styling
                gridcolor='gray',  # Grid color
                categoryorder='category ascending'  # Ensures categorical x-values are treated correctly
                # dtick=10
            ),
            coloraxis=dict(
                colorbar=dict(
                title=zlabel,  # Set the color bar label here
                title_font=dict(color='white', size=18),  # Customize title font
                tickfont=dict(color='white', size=14),  # Customize tick font
                bgcolor='#343a40',  # Optional: background color for the colorbar
                bordercolor='white',  # Optional: border color for the colorbar
                borderwidth=1,  # Optional: border width for the colorbar
            )),
            # Legend styling
            legend=dict(
                font=dict(color='white', size=12),  # Legend text color
                bgcolor='#343a40',  # Legend background color
                bordercolor='white',  # Border color of the legend
                borderwidth=1  # Optional: set the width of the border
            ),
            scene=dict(
                    # xaxis_title=xlabel,  # Change x-axis label to 'startyear'
                    # yaxis_title=ylabel,           # You can set y-axis title if needed
                    # zaxis_title=zlabel,   # Set z-axis title if needed
                    xaxis=dict(
                        tickvals=fig_x_value,  # Generate tick positions based on the number of years
                        ticktext=x_values,  # Set tick labels to the year values
                        title=dict(text=xlabel, font=dict(size=20, color='white')),  # X-axis label styling
                        tickfont=dict(color='white', size=18),  # X-axis tick color
                        tickangle=0,  # Rotate the x-axis labels for better readability
                        showgrid=True,  # Grid styling
                        gridcolor='gray',  # Grid color
                        categoryorder='category ascending',  # Ensures categorical x-values are treated correctly
                    ),
                    yaxis=dict(
                        tickvals=fig_y_value,  # Adjust y-axis ticks based on runtimeMinutes indices, if needed
                        ticktext=y_values,  # Use the index for runtimeMinutes as tick labels
                        title=dict(text=xlabel, font=dict(size=20, color='white')),  # X-axis label styling
                        tickfont=dict(color='white', size=18),  # X-axis tick color
                        tickangle=0,  # Rotate the x-axis labels for better readability
                        showgrid=True,  # Grid styling
                        gridcolor='gray',  # Grid color
                        categoryorder='category ascending',  # Ensures categorical x-values are treated correctly
                    )
            )
        )
    else:
        fig_json_serializable.update_layout(
            plot_bgcolor='#1e1e1e',  # Darker background for the plot area
            paper_bgcolor='#343a40',  # Dark gray for the paper
            font=dict(color='white'),  # White text color
            title = figname,
            title_font=dict(size=20, color='white')
            )

    if d_column == "3D":
        name = 'default'
        # Default parameters which are used when `layout.scene.camera` is not provided
        camera = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.25, y=1.25, z=1.25)
        )
        
        fig_json_serializable.update_layout(scene_camera=camera) #, title=name

