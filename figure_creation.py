#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 23:18:23 2024

@author: quentin
"""


"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions for visualisation of the dataframe.

#=============================================================================
   #=============================================================================
   #============================================================================="""


import dash
from dash import dcc, html, Input, Output, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import linear_model as lm, tree, neighbors
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from scipy import signal

from termcolor import colored

import matplotlib.pyplot as plt
import plotly.tools as tls  # For converting Matplotlib to Plotly
import plotly.graph_objects as go
import plotly.express as px

import Function_dataframe as fd
import Function_errors as fe
import data_plot_preparation as dpp


cmaps = [('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])]


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def create_figure(df, x_column, y_column, z_column, yf_column, zf_column, g_column, d_column, smt_dropdown_value, smt_order_value, sub_bot_smt_value, Large_file_memory):

    """
    Goal: Create a sophisticated figure which adapt to any input variable.

    Parameters:
    - df: dataframe
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - yf_column: Function to operate on y_column with the rest of the dataframe
    - zf_column: Function to operate on z_column with the rest of the dataframe
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.
    - sub_bot_smt_value: Button to apply the smoothing.
    - smt_dropdown_value: Type of smoothing for the data.
    - smt_dropdown_value: Order of the smoothing for the data.
    - Large_file_memory: Estimate if the file is too large to be open with panda

    Returns:
    - fig_json_serializable: The finalized plotly figure. 
    """

    # =============================================================================
    print(colored("========================= Start figure creation =========================", "green"))
    # =============================================================================      
    # Create a Dash compatible Plotly graph figure
    fig_json_serializable = go.Figure()  # This figure can now be used with dcc.Graph in Dash

    # Create the label of the figure
    figname, xlabel, ylabel, zlabel = label_fig(x_column, y_column, z_column, yf_column, zf_column, g_column, d_column, True)  
    
    if x_column is not None: 
        print("Extract from data base the required column and prepare them for the figure.")
        Para, data_for_plot, x_column, y_column, z_column = dpp.data_preparation_for_plot(df , x_column, y_column, z_column, yf_column, zf_column, g_column, Large_file_memory)
        print("The data ready to be ploted is:")
        print(data_for_plot)
        print()
        # Add the core of the figure
        print("############## Core figure creation ##############")
        fig_json_serializable, data_for_plot, xlabel, ylabel, zlabel = figure_plotly(fig_json_serializable, x_column, y_column, z_column, yf_column, zf_column, g_column, d_column, smt_dropdown_value, smt_order_value, sub_bot_smt_value, data_for_plot, xlabel, ylabel, zlabel)
    
    # Update the figure layout
    print("############## Update figure layout ##############")
    fig_update_layout(fig_json_serializable,figname,xlabel,ylabel,zlabel,x_column,g_column,d_column)       
    
    plt.close()
    # =============================================================================
    print(colored("=============================================================================", "green"))
    if x_column is None: 
        return fig_json_serializable, None
    return fig_json_serializable, data_for_plot.to_dict(orient='records')


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def label_fig(x_column, y_column, z_column, yf_column, zf_column, g_column, d_column, init):

    """
    Goal: Create the figure labels.

    Parameters:
    - x_column: Column in the dataframe (can be None).
    - y_column: Column in the dataframe (can be None).
    - z_column: Column in the dataframe (can be None).
    - yf_column: Function to operate on y_column with the rest of the dataframe
    - zf_column: Function to operate on z_column with the rest of the dataframe
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.

    Returns:
    - figname: The name of the Figure.
    - xlabel: The xlabel of the axis (can be None).
    - ylabel: The ylabel of the axis (can be None).
    - zlabel: The zlabel of the axis (can be None).
    """

    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres", "directors", "writers", "category"]
    
    if init == False:
        if x_column is not None: 
            figname = 'Movies over the ' + x_column
    
            if x_column == 'count':
                xlabel = 'Number of movies'
            elif 'avg_' in x_column:
                xlabel = 'Average '+x_column[4:]+' of the movies'
            else:
                xlabel = x_column
            
            if y_column == 'count':
                ylabel = 'Number of movies'
            elif 'avg_' in y_column:
                ylabel = 'Average '+y_column[4:]+' of the movies'              
            else:
                ylabel = y_column
            
            if z_column is not None:
                if z_column == 'count':
                    zlabel = 'Number of movies'
                elif 'avg_' in z_column:
                    zlabel = 'Average '+z_column[4:]+' of the movies'
                else:
                    zlabel = z_column
                    
                if zf_column == 'Weight on y':
                    ylabel = 'Average '+z_column[4:]+' of the movies'
                    
            else:
                zlabel = None


            if d_column == "2D":
                if g_column == 'Colormesh':
                    ylabel = y_column
                else:
                    ylabel = "None"
                zlabel = "None"
    
    
        else: 
            figname = 'No data selected'
            xlabel, ylabel, zlabel = "None","None","None"
    
    else:
        figname = 'No data selected'
        xlabel, ylabel, zlabel = "None","None","None"        
    
    if x_column in df_col_string:
        xlabel_temp = xlabel
        xlabel = ylabel
        ylabel = xlabel_temp
    
    return figname, xlabel, ylabel, zlabel


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def figure_plotly(plotly_fig, x_column, y_column, z_column, yf_column, zf_column, g_column, d_column, smt_dropdown_value, smt_order_value, sub_bot_smt_value, data_for_plot, xlabel, ylabel, zlabel):

    """
    Goal: Create the plot inside the figure regarding the inputs.

    Parameters:
    - plotly_fig: Dash figure.
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - yf_column: Function to operate on y_column with the rest of the dataframe
    - zf_column: Function to operate on z_column with the rest of the dataframe
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.
    - sub_bot_smt_value: Button to apply the smoothing.
    - smt_dropdown_value: Type of smoothing for the data.
    - smt_dropdown_value: Order of the smoothing for the data.
    - data_for_plot: Data to plot.

    Returns:
    - plotly_fig: The core figure.
    """
    
    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]
    
    # Define a list of colors for the bars
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    legend = "None"
    
    x_axis = x_column
    y_axis = 'count'
    z_axis = None
    if str(y_column)!='None':
        z_axis = y_column
    if x_column in df_col_string:
        x_axis = 'count'
        y_axis = x_column

    if yf_column == "Avg":
        z_axis = 'avg_' + y_column

    if yf_column == "Avg on the ordinate":
        x_axis = x_column
        y_axis = 'avg_' + y_column
        z_axis = 'count'
        if x_column in df_col_string:
            x_axis = 'avg_' + y_column
            y_axis = x_column
            z_axis = 'count'
    
    if z_column is not None and zf_column == "Avg":
        t_axis = 'avg_' + z_column
    if z_column is not None and zf_column == "Avg on the ordinate":
        y_axis = 'avg_' + z_column
        t_axis = 'count'
    if z_column is not None and zf_column == "Weight on y":
        y_axis = 'sum_' + z_column
        t_axis = 'standard_error'         

    print("x_axis=", x_axis)
    print("y_axis=", y_axis)
    if str(y_column)!='None':
        print("z_axis=", z_axis)
    if str(z_column)!='None':
        print("t_axis=", t_axis)


    # Rename the label of the figure
    figname, xlabel, ylabel, zlabel = label_fig(x_axis, y_axis, z_axis, yf_column, zf_column, g_column, d_column, False)  

    if d_column=="1D": 
        
        if str(y_column)=='None':
            
            data_for_plot = smoothing_data(sub_bot_smt_value, smt_dropdown_value, smt_order_value, data_for_plot, x_axis, y_axis, z_axis)
                            
            if g_column=="Histogram":
                plotly_fig = px.bar(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis
                    )
            if g_column=="Curve":
                plotly_fig = px.line(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis
                    ) #, color=y_column, symbol="country"
            if g_column=="Scatter":
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_axis,
                    y=y_axis,
                    # log_x=True,
                    size_max=60
                    )
        
        #Case where y_column is None and z_column is None
        elif str(y_column)!='None' and str(z_column)=='None':           

            if x_column in df_col_string:
                # Grouping y_column values
                n = 12  # Number of top categories to keep
                data_for_plot = group_small_values(data_for_plot, y_axis, x_axis, n)

            if y_column in df_col_string:
                # Grouping y_column values
                n = 7  # Number of top categories to keep
                data_for_plot = group_small_values(data_for_plot, z_axis, y_axis, n, x_axis)

            data_for_plot = smoothing_data(sub_bot_smt_value, smt_dropdown_value, smt_order_value, data_for_plot, x_axis, y_axis, z_axis)

            if "Histogram" in g_column:
                plotly_fig = px.bar(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis,
                    color=z_axis if "Movie" not in g_column else None,
                    animation_frame=z_axis if "Movie" in g_column else None
                    )
            if "Curve" in g_column:
                plotly_fig = px.line(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis,
                    color=z_axis if "Movie" not in g_column else None,
                    animation_frame=z_axis if "Movie" in g_column else None,
                    line_group=g_column if "Movie" in g_column else None
                    ) #symbol="country"
            if "Scatter" in g_column:
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_axis,
                    y=y_axis,
                    size_max=60,
                    # log_x=True,
                    color=z_axis if "Movie" not in g_column else None,
                    animation_frame=z_axis if "Movie" in g_column else None
                    )  
            if "Boxes" in g_column:
                if x_column in df_col_string:
                    x_axis = y_column
                    xlabel = y_column
                else:
                    y_axis = y_column
                    ylabel = y_column
                plotly_fig = px.box(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis,
                    points=False)

        #Case where z_column is not None
        else:
                        
            if y_column in df_col_string:
                # Grouping y_column values
                n = 7  # Number of top categories to keep
                if zf_column == "Avg":
                    data_for_plot = group_small_values(data_for_plot, z_axis, y_axis, n, x_axis)
                elif zf_column == "Avg on the ordinate":
                    data_for_plot = group_small_values(data_for_plot, z_axis, t_axis, n, x_axis)
                elif zf_column == "Weight on y":
                    data_for_plot = group_small_values(data_for_plot, z_axis, y_axis, n, x_axis)

            data_for_plot = smoothing_data(sub_bot_smt_value, smt_dropdown_value, smt_order_value, data_for_plot, x_axis, y_axis, z_axis)
                        
            # y_values = data_for_plot[y_column].unique()
            if g_column=="Histogram" and (zf_column == "Avg" or zf_column == "Avg on the ordinate"):
               plotly_fig = px.bar(
                   data_for_plot, 
                   x=x_axis, 
                   y=y_axis,
                   color=z_axis if "Movie" not in g_column else None,
                   animation_frame=z_axis if "Movie" in g_column else None
                   )
            elif g_column=="Curve" and (zf_column == "Avg"):
                plotly_fig = go.Figure()
                # Add traces for each unique group
                for key in data_for_plot[z_axis].unique():
                    group = data_for_plot[data_for_plot[z_axis] == key]
                    plotly_fig.add_trace(go.Scatter(
                        x=group[x_axis],
                        y=group[y_axis],
                        mode='lines',
                        name=key,
                        line=dict(width=group[t_axis].mean())  # Set line width based on avg thickness
                    ))
            elif g_column=="Curve" and (zf_column == "Avg on the ordinate"):
                plotly_fig = px.line(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis,
                    color=z_axis if "Movie" not in g_column else None,
                    animation_frame=z_axis if "Movie" in g_column else None,
                    line_group=g_column if "Movie" in g_column else None
                    )
            elif g_column=="Scatter" and (zf_column == "Avg" or zf_column == "Avg on the ordinate"):
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_axis,
                    y=y_axis,
                    size=t_axis if zf_column == "Avg" else None,
                    size_max=60,
                    color=z_axis if "Movie" not in g_column else None,
                    animation_frame=z_axis if "Movie" in g_column else None
                )

            elif g_column=="Histogram" and zf_column == "Weight on y":
                plotly_fig = px.bar(
                    data_for_plot,
                    x=x_axis,
                    y=z_axis,
                    # title='Weighted Average'+y_column+'Over the'+x_axis,
                    error_y='standard_error'
                )
            elif g_column=="Curve" and zf_column == "Weight on y":
                plotly_fig = px.line(
                    data_for_plot,
                    x=x_axis,
                    y=z_axis,
                    # title='Weighted Average'+y_column+'Over the'+x_axis,
                    error_y='standard_error'
                )
            elif g_column=="Scatter" and zf_column == "Weight on y":
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_axis,
                    y=z_axis,
                    # title='Weighted Average'+y_column+'Over the'+x_axis,
                    error_y='standard_error'
                )



    if g_column=="Pie": #d_column=="2D" and 

            if x_column in df_col_string:
                # Grouping y_column values
                n = 7  # Number of top categories to keep
                data_for_plot = group_small_values(data_for_plot, x_column, 'count', n)

            # x_values,fig_x_value,y_values,fig_y_value=None,None,None,None
            plotly_fig = px.pie(
                data_for_plot, 
                values="count", 
                names=x_column
                )

    if d_column=="2D" and g_column=="Colormesh":     
        
        px_fig = px.density_heatmap(
            data_for_plot, 
            x=x_column, 
            y=y_column, 
            # nbinsx=100, nbinsy=100, 
            z='count',
            color_continuous_scale="Viridis")

        # Get the z data from the px figure
        z_data = px_fig.data[0].z  # Access the z values (the counts)
        x_values = px_fig.data[0].x  # Access the x values (start years)
        y_values = px_fig.data[0].y  # Access the y values (runtime minutes)
        
        # Create a Go Figure and add the Heatmap trace
        plotly_fig = go.Figure()
        
        # Add Heatmap trace
        plotly_fig.add_trace(go.Heatmap(
            x=x_values,
            y=y_values,
            z=z_data,
            colorscale='Viridis'
        ))

                    
    if d_column == "3D" and g_column == "Histogram":
        
        # Pivoting the DataFrame to create a grid for surface plot
        pivoted_data = data_for_plot.pivot(index=y_column, columns=x_column, values='count')
        # Fill NaN values with zeros or an appropriate value for the surface
        pivoted_data = pivoted_data.fillna(0)
        # Now, create the surface plot

        plotly_fig = go.Figure(
            data=[go.Surface(z=pivoted_data.values, x=pivoted_data.columns, y=pivoted_data.index)])

    return plotly_fig, data_for_plot, xlabel, ylabel, zlabel  


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def smoothing_data(sub_bot_smt_value, smt_dropdown_value, smt_order_value, data_for_plot, x_axis, y_axis, z_axis):

    """
    Goal: Apply a filter on the data.

    Parameters:
    - sub_bot_smt_value: Button to apply the smoothing.
    - smt_dropdown_value: Type of smoothing for the data.
    - smt_dropdown_value: Order of the smoothing for the data.
    - data_for_plot: Dataframe which will be filtered.
    - x_axis: Column in the dataframe.
    - y_axis: Column in the dataframe.
    - z_axis: Column in the dataframe.

    Returns:
    - data_for_plot: Dataframe updated.
    """

    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]
    
    if sub_bot_smt_value % 2 == 1:
        
        print("############## Smoothing #################")
        
        data_for_plot['original_index'] = data_for_plot.index
        
        if z_axis is None or z_axis not in df_col_string:
            window_lenght = len(data_for_plot[x_axis])//5
            data_for_plot[y_axis] = signal.savgol_filter(data_for_plot[y_axis],
                                   window_lenght, # window size used for filtering
                                   smt_order_value)
            print("window_length=",window_length)
            print("Data updated by the smoothing")
            print(data_for_plot)

        else:
            # Function to apply savgol_filter
            def apply_savgol_filter(group):
                # Calculate window length based on the size of the group
                window_length = len(group)//5
                
                # Ensure that window_length is odd and less than or equal to the total group length
                if window_length < 3:  # Savitzky-Golay filter needs at least a size of 3
                    return group  # Skip filtering for groups too small
                
                if window_length % 2 == 0:
                    window_length -= 1  # Make sure window_length is odd
                
                print("window_length=",window_length)
                print("Amount of data", len(group[y_axis]))
                print()
                
                # Apply the savgol_filter
                filtered_values = signal.savgol_filter(group[y_axis], window_length, smt_order_value)
    
                # Replace the original 'count' with the filtered values
                group[y_axis] = filtered_values
                                
                return group
            
            # Apply the filter to each genre
            data_for_plot_filtered = data_for_plot.groupby(z_axis, as_index=False, group_keys=False).apply(apply_savgol_filter)
                        
            # Sort the DataFrame by the original index
            data_for_plot_filtered.sort_values(by='original_index', inplace=True)
                        
            # Drop the 'original_index' column if you no longer need it
            data_for_plot_filtered.drop(columns='original_index', inplace=True)
                
            data_for_plot = data_for_plot_filtered
        
            
            print("Data updated by the smoothing")
            print(data_for_plot)
            
    return data_for_plot
            

"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def figure_add_trace(fig_json_serializable, data_for_plot, x_column, y_column, z_column, yf_column, zf_column, graph_type, dim_type, reg_type, reg_order):

    """
    Goal: Add a trace inside the figure regarding the inputs.

    Parameters:
    - fig_json_serializable: Dash figure.
    - data_for_plot: Dataframe which has been use to create the figure that is re-opened in this function.
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - yf_column: Function to operate on y_column with the rest of the dataframe
    - zf_column: Function to operate on z_column with the rest of the dataframe
    - graph_type: Type of Graphyque for the figure.
    - dim_type: Graphyque dimension for the figure.
    - reg_type: Type of regression for the data.
    - reg_order: Order of the regression for the data.

    Returns:
    - fig_json_serializable: Dash figure updated with the trace.
    - data_for_plot: Dataframe updated with the trace.
    """
    
    
    plotly_fig = go.Figure(fig_json_serializable)
    
    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]
    
    # Define a list of colors for the bars
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'] 
    
    x_axis = x_column
    y_axis = 'count'
    z_axis = None
    t_axis = None
    if str(y_column)!='None':
        z_axis = y_column
    if x_column in df_col_string:
        x_axis = 'count'
        y_axis = x_column

    if yf_column == "Avg":
        z_axis = 'avg_' + y_column

    if yf_column == "Avg on the ordinate":
        x_axis = x_column
        y_axis = 'avg_' + y_column
        z_axis = 'count'
        if x_column in df_col_string:
            x_axis = 'avg_' + y_column
            y_axis = x_column
            z_axis = 'count'
    
    if z_column is not None and zf_column == "Avg":
        t_axis = 'avg_' + z_column
    if z_column is not None and zf_column == "Avg on the ordinate":
        y_axis = 'avg_' + z_column
        t_axis = 'count'
    if z_column is not None and zf_column == "Weight on y":
        y_axis = 'sum_' + z_column
        t_axis = 'standard_error'        

    print("x_axis=", x_axis)
    print("y_axis=", y_axis)
    print("z_axis=", z_axis)
    print("t_axis=", t_axis)

    # Creating a DataFrame
    data_for_plot = pd.DataFrame(data_for_plot)
    
    # Resetting the index to have a clean index
    data_for_plot.reset_index(drop=True, inplace=True)
    
    # Calculate the offset
    offset = data_for_plot[x_axis].values.min()
    
    # Adjust x values by subtracting the minimum value
    x_offset = data_for_plot[x_axis].values - offset
    x = x_offset.reshape(-1, 1)
    y = data_for_plot[y_axis].values.reshape(-1, 1)

    
    # x, y = data_for_plot[x_axis].values.reshape(-1, 1), data_for_plot[y_axis].values.reshape(-1, 1)
    if z_column is not None and zf_column == "Weight on y":
        y = data_for_plot[z_axis].values.reshape(-1, 1)
        weights = data_for_plot[t_axis].values.reshape(-1, 1).flatten()
    
    # Split the data
    if t_axis is not None:
        if t_axis == 'standard_error':
            x_train, x_test, y_train, y_test, weights_train, weights_test = train_test_split(x, y, weights, test_size=0.2, random_state=0)
    else:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    Dict_regression_models = {
        'Linear Regression': lm.LinearRegression,
        'Decision Tree': tree.DecisionTreeRegressor,
        'k-NN': neighbors.KNeighborsRegressor,
        'Polynomial Regression': lambda: make_pipeline(PolynomialFeatures(degree=reg_order), lm.LinearRegression())  # Use a lambda to return a new instance
        }        

    # Instantiate the model
    model = Dict_regression_models[reg_type]()
    
    # Fit the model
    if t_axis == 'standard_error':
        model.fit(x_train, y_train, linearregression__sample_weight=weights_train)
    else:
        model.fit(x_train, y_train)
    
    # Make predictions
    y_pred = model.predict(x_test)    
    
    if reg_type == 'Polynomial Regression':
        # # Get the coefficients and intercept
        # # Note: Here we access the named steps in the pipeline.
        poly = model.named_steps['polynomialfeatures']  # Get the PolynomialFeatures step
        linear_reg = model.named_steps['linearregression']  # Get the LinearRegression step
        
        coefficients = linear_reg.coef_
        intercept = linear_reg.intercept_    
    
        # Display the polynomial equation
        round_coef = 8
        polynomial_equation = f"y = {round(intercept[0], round_coef)}"
        for i in range(1, len(coefficients[0])):
            polynomial_equation += f" + {round(coefficients[0][i], round_coef)} * x^{i}"
        
        print(polynomial_equation)

    # Mean Squared Error (MSE)
    # Average of the squares of the differences between predicted values (y_pred) and actual values (y_test).
    mse = mean_squared_error(y_test, y_pred)
    # R-squared (R²)
    # Proportion of variance in the dependent variable that can be explained by the independent variables in the model.
    r2 = r2_score(y_test, y_pred)
    
    print(f'Mean Squared Error: {mse}')
    print(f'R^2 Score: {r2}')
    
    # Make predictions (optional)
    predictions = model.predict(x)
    
    # You can also view the predictions alongside the original DataFrame if desired
    data_for_plot['predicted_count'] = predictions   

    # Plotly figure with the original data and the regression line
    plotly_fig.add_trace(go.Scatter(
        x=data_for_plot[x_axis],
        y=data_for_plot['predicted_count'],
        mode='lines',
        name=reg_type if reg_type in ['Linear Regression', 'Decision Tree','k-NN'] else "Poly deg "+str(reg_order),#polynomial_equation,
        line=dict(dash='dash', width=2)  # Customizing line color and width
    ))
    
        
    fig_json_serializable = plotly_fig.to_dict()
        
    plt.close()
    # =============================================================================
    print(colored("=============================================================================", "green"))
    
    return fig_json_serializable, data_for_plot.to_dict(orient='records') 

"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def group_small_values(data, col, count_column, n, col_ref=None):
    
    """
    Goal: Group the values which are the less present in the dataframe other the same name "Other".

    Parameters:
    - data: Dataframe.
    - col: Column in the dataframe that must be grouped.
    - count_column: Column in the dataframe (usally count) which will give the total amount of the Other.
    - n: Integer that will define which value of col are counted in the "Other" value. All values of col which are not in the n first count.
    - col_ref: Column in the dataframe that will be use as a reference to regroup the values of col.

    Returns:
    - The updated Dataframe.
    """
    
    # Group by col value and sum the count_column
    grouped_data = data.groupby(col)[count_column].sum().reset_index()
    
    # Get the top n col value based on summed of count_column
    top_n_genres = grouped_data.nlargest(n, count_column)
    
    # Extract the col value
    top_n = top_n_genres[col].unique()
    
    # Replace values not in top_n with "Other"
    data[col] = data[col].where(data[col].isin(top_n), 'Other')
    
    result = aggregate_value(data, col, count_column, col_ref)
    
    return result


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def aggregate_value(data, col_to_aggregate, count_col, col_ref=None):

    """
    Goal: Aggregate the value of the dataframe.

    Parameters:
    - data: Dataframe.
    - col_to_aggregate: Column in the dataframe that must be grouped.
    - count_col: Column in the dataframe (usally count) which will give the total amount of the Other.
    - col_ref: Column in the dataframe that will be use as a reference to regroup the values of col.

    Returns:
    - The updated Dataframe.
    """

    # Identify columns to aggregate based on exclusions
    columns_to_aggregate = data.columns.tolist()
    
    if col_ref is not None:
        columns_to_aggregate.remove(col_ref)
    columns_to_aggregate.remove(col_to_aggregate)
    columns_to_aggregate.remove(count_col)

    # Create aggregation dictionary for other columns
    aggregation_dict = {}
    for col in columns_to_aggregate:
        # Assign the average calculation for each column
        aggregation_dict[col] = (col, lambda x: (x * data.loc[x.index, count_col]).sum() / data.loc[x.index, count_col].sum())

    # Perform aggregation
    if col_ref is not None:
        temp_data = data.groupby([col_ref, col_to_aggregate], as_index=False).agg(
            count=(count_col, 'sum'),
            **aggregation_dict
        )
    else:
        temp_data = data.groupby([col_to_aggregate], as_index=False).agg(
            count=(count_col, 'sum'),
            **aggregation_dict
        )
  
    # Now we want to merge the aggregated data back with the unaggregated data without the grouped rows
    if col_ref is not None:
        # Keep other unique entries in the original data
        other_data = data[~data[col_to_aggregate].isin(temp_data[col_to_aggregate])]

        # Concatenate the aggregated and the other data
        final_data = pd.concat([temp_data, other_data], ignore_index=True).sort_values(by=[col_ref, col_to_aggregate])
    else:
        # Keep other unique entries in the original data
        other_data = data[~data[col_to_aggregate].isin(temp_data[col_to_aggregate])]

        # Concatenate the aggregated and the other data
        final_data = pd.concat([temp_data, other_data], ignore_index=True).sort_values(by=[col_to_aggregate])

    return final_data.reset_index(drop=True)


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def fig_update_layout(fig_json_serializable,figname,xlabel,ylabel,zlabel,x_column,g_column,d_column):

    """
    Goal: Update the layout of the dash figure.

    Parameters:
    - fig_json_serializable: Dash figure.
    - figname: The name of the Figure.
    - xlabel: The xlabel of the axis (can be None).
    - ylabel: The ylabel of the axis (can be None).
    - zlabel: The zlabel of the axis (can be None).
    - x_column: Column in the dataframe
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.

    Returns:
    - fig_json_serializable: Dash figure updated.
    """

    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]

    fig_json_serializable.update_layout(
        plot_bgcolor='#1e1e1e',  # Darker background for the plot area
        paper_bgcolor='#101820',  # Dark gray for the paper
        font=dict(color='white'),  # White text color
        # title = figname,
        # title_font=dict(size=20, color='white')
        )

    if x_column is not None and (d_column =="1D"or d_column =="2D") and g_column != 'Pie':
        fig_json_serializable.update_layout(
            plot_bgcolor='#1e1e1e',  # Darker background for the plot area
            paper_bgcolor='#101820',  # Dark gray for the paper
            font=dict(color='white'),  # White text color
            # title = figname,
            # title_font=dict(size=20, color='white'),  # Title styling
            xaxis=dict(
                # range=[0, 2000] if g_column == 'Histogram Movie' else None,
                title=dict(text=xlabel, font=dict(size=20, color='white')),  # X-axis label styling
                tickfont=dict(color='white', size=18),  # X-axis tick color
                tickangle=0,  # Rotate the x-axis labels for better readability
                showgrid=True,  # Grid styling
                gridcolor='gray',  # Grid color
                categoryorder='category ascending',  # Ensures categorical x-values are treated correctly
            ),
            yaxis=dict(
                title=dict(text=ylabel, font=dict(size=20, color='white')),  # Y-axis label styling
                tickfont=dict(color='white', size=18),  # Y-axis tick color
                tickangle=0,  # Rotate the x-axis labels for better readability
                showgrid=True,  # Grid styling
                gridcolor='gray',  # Grid color
                categoryorder='total ascending' if x_column in df_col_string else 'category ascending',  # Ensures categorical x-values are treated correctly
                
            )
            
        )
    elif x_column is not None and d_column =="3D":
        fig_json_serializable.update_layout(
            plot_bgcolor='#1e1e1e',  # Darker background for the plot area
            paper_bgcolor='#101820',  # Dark gray for the paper
            font=dict(color='white'),  # White text color
            # title = figname,
            # title_font=dict(size=20, color='white'),  # Title styling
            scene=dict(
                    xaxis=dict(
                        title=dict(text=xlabel, font=dict(size=18, color='white')),  # X-axis label styling
                        tickmode='array',
                        tickfont=dict(color='white', size=14),  # X-axis tick color
                        tickangle=0,  # Rotate the x-axis labels for better readability
                        showgrid=True,  # Grid styling
                        gridcolor='gray',  # Grid color
                        categoryorder='category ascending',  # Ensures categorical x-values are treated correctly
                    ),
                    yaxis=dict(
                        title=dict(text=ylabel, font=dict(size=18, color='white')),  # Y-axis label styling
                        tickmode='array',
                        tickfont=dict(color='white', size=14),  # Y-axis tick color
                        tickangle=0,  # Rotate the x-axis labels for better readability
                        showgrid=True,  # Grid styling
                        gridcolor='gray',  # Grid color
                        categoryorder='category ascending',  # Ensures categorical x-values are treated correctly
                    ),
                    zaxis=dict(
                        title=dict(text='Count', font=dict(size=18, color='white')),
                        tickmode='array',
                        tickfont=dict(color='white', size=14)  # Z-axis tick color
                    )
            )
        )
        
    if g_column == 'Colormesh':    

        # Update 3D scene options
        fig_json_serializable.update_scenes(
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode="manual"
        )
        
        # Add dropdowns
        button_layer_1_height = 1.08
        
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["colorscale", "Viridis"],
                        label="Viridis",
                        method="restyle"
                    ),
                    dict(
                        args=["colorscale", "Cividis"],
                        label="Cividis",
                        method="restyle"
                    ),
                    dict(
                        args=["colorscale", "Blues"],
                        label="Blues",
                        method="restyle"
                    ),
                    dict(
                        args=["colorscale", "Greens"],
                        label="Greens",
                        method="restyle"
                    ),
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=button_layer_1_height,
                yanchor="top"
            ),
            dict(
                buttons=list([
                    dict(
                        args=["reversescale", False],
                        label="False",
                        method="restyle"
                    ),
                    dict(
                        args=["reversescale", True],
                        label="True",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.37,
                xanchor="left",
                y=button_layer_1_height,
                yanchor="top"
            ),
            dict(
                buttons=list([
                    dict(
                        args=[{"contours.showlines": False, "type": "contour"}],
                        label="Hide lines",
                        method="restyle"
                    ),
                    dict(
                        args=[{"contours.showlines": True, "type": "contour"}],
                        label="Show lines",
                        method="restyle"
                    ),
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.58,
                xanchor="left",
                y=button_layer_1_height,
                yanchor="top"
            ),
        ]
    
        fig_json_serializable.update_layout(
        updatemenus=updatemenus
        )
        
        
    if g_column == 'Histogram Movie':
        fig_json_serializable.update_layout(
        margin=dict(l=150, r=20, t=20, b=20)
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
        
