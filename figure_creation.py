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


def create_figure(df, x_column, y_column, z_column, f_column, g_column, d_column, Large_file_memory):

    """
    Goal: Create a sophisticated figure which adapt to any input variable.

    Parameters:
    - df: dataframe
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - f_column: Function to operate on df_temp[x_column,y_column]
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.
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
    figname, xlabel, ylabel, zlabel = label_fig(x_column, y_column, z_column, f_column, g_column, d_column)

    if x_column is not None: 
        print("Extract from data base the required column and prepare them for the figure.")
        Para, data_for_plot, x_column, y_column, z_column = dpp.data_preparation_for_plot(df , x_column, y_column, z_column, f_column, g_column, Large_file_memory)
        print("The data ready to be ploted is")
        print(data_for_plot)
        print()
        # Add the core of the figure
        fig_json_serializable = figure_plotly(fig_json_serializable, x_column, y_column, z_column, f_column, g_column, d_column, data_for_plot)

    # Update the figure layout
    fig_update_layout(fig_json_serializable,figname,xlabel,ylabel,zlabel,x_column,g_column,d_column)       
    
    plt.close()
    # =============================================================================
    print(colored("=============================================================================", "green"))
    return fig_json_serializable


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def label_fig(x_column, y_column, z_column, f_column, g_column, d_column):

    """
    Goal: Create the figure labels.

    Parameters:
    - x_column: Column in the dataframe (can be None).
    - y_column: Column in the dataframe (can be None).
    - z_column: Column in the dataframe (can be None).
    - f_column: Function to operate on df_temp[x_column,y_column].
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.

    Returns:
    - figname: The name of the Figure.
    - xlabel: The xlabel of the axis (can be None).
    - ylabel: The ylabel of the axis (can be None).
    - zlabel: The zlabel of the axis (can be None).
    """
    
    if x_column is not None: 
        figname = 'Movies over the ' + x_column
        xlabel = x_column
        
        if d_column == "1D":
            if str(f_column)=='None':
                ylabel = 'Number of movies'
            elif str(f_column)=='Avg':
                ylabel = 'Average '+y_column+' of the movies'
            zlabel = "None"
        
        elif d_column == "2D":
            if g_column == 'Colormesh':
                ylabel = y_column
            else:
                ylabel = "None"
            zlabel = "None"

        else:
            ylabel = y_column
            zlabel = "None"

    else: 
        figname = 'No data selected'
        xlabel, ylabel, zlabel = "None","None","None"
        
    return figname, xlabel, ylabel, zlabel


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def figure_plotly(plotly_fig, x_column, y_column, z_column, f_column, g_column, d_column, data_for_plot):

    """
    Goal: Create the plot inside the figure regarding the inputs.

    Parameters:
    - plotly_fig: Dash figure.
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - f_column: Function to operate on df_temp[x_column,y_column]
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.
    - data_for_plot: Data to plot.

    Returns:
    - plotly_fig: The core figure.
    """
    
    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]
    
    # Define a list of colors for the bars
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    legend = "None"
    
    x_values = data_for_plot[x_column].unique()
    # Check if all elements are either int or float
    is_numeric = all(isinstance(x, (int, float)) for x in x_values)
    if is_numeric:
        x_values = np.array(x_values)
        fig_x_value = x_values-min(x_values)
    else:
        fig_x_value = list(np.arange(len(x_values)))
    
    if str(y_column)!='None':
        y_values = data_for_plot[y_column].unique()
        # Check if all elements are either int or float
        is_numeric = all(isinstance(y, (int, float)) for y in y_values)
        if is_numeric:
            y_values = np.array(y_values)
            fig_y_value = y_values-min(y_values)
        else:
            fig_y_value = list(np.arange(len(y_values))) 
    else:
        y_values, fig_y_value = None, None

    if d_column=="1D": 
        if str(y_column)=='None':
            if g_column=="Histogram":
                plotly_fig = px.bar(
                    data_for_plot, 
                    x=x_column, 
                    y='count'
                    )
            if g_column=="Curve":
                plotly_fig = px.line(
                    data_for_plot, 
                    x=x_column, 
                    y='count'
                    ) #, color=y_column, symbol="country"
            if g_column=="Scatter":
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_column,
                    y='count',
                    # log_x=True,
                    size_max=60
                    )
        elif str(y_column)!='None' and str(z_column)=='None':
            if g_column=="Histogram":
                plotly_fig = px.bar(
                    data_for_plot, 
                    x=x_column, 
                    y='count',
                    color=y_column
                    )
            if g_column=="Curve":
                plotly_fig = px.line(
                    data_for_plot, 
                    x=x_column, 
                    y='count',
                    color=y_column
                    ) #symbol="country"
            if g_column=="Scatter":
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_column,
                    y='count',
                    color=y_column,
                    # log_x=True,
                    size_max=60
                    )
        else:
            y_values = data_for_plot[y_column].unique()
            if g_column=="Histogram":
               plotly_fig = px.bar(
                   data_for_plot, 
                   x=x_column, 
                   y='count',
                   color=y_column
                   )
            if g_column=="Curve":
                plotly_fig = go.Figure()
                # Add traces for each unique group
                for key in data_for_plot[y_column].unique():
                    group = data_for_plot[data_for_plot[y_column] == key]
                    plotly_fig.add_trace(go.Scatter(
                        x=group[x_column],
                        y=group['count'],
                        mode='lines',
                        name=key,
                        line=dict(width=group['avg_'+z_column].mean())  # Set line width based on avg thickness
                    ))
            if g_column=="Scatter":
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_column,
                    y='count',
                    size='avg_'+z_column,
                    color=y_column,
                    # hover_name=y_column,
                    # log_x=True,
                    size_max=60
                )

    if g_column=="Pie": #d_column=="2D" and 
            x_values,fig_x_value,y_values,fig_y_value=None,None,None,None
            plotly_fig = px.pie(
                data_for_plot, 
                values="count", 
                names=x_column
                )

    if d_column=="2D" and g_column=="Colormesh":        
        plotly_fig = px.density_heatmap(
            data_for_plot, 
            x=x_column, 
            y=y_column, 
            nbinsx=100, nbinsy=100, 
            color_continuous_scale="Viridis")

                    
    if d_column == "3D" and g_column == "Histogram":
        
        # Pivoting the DataFrame to create a grid for surface plot
        pivoted_data = data_for_plot.pivot(index=y_column, columns=x_column, values='count')
        # Fill NaN values with zeros or an appropriate value for the surface
        pivoted_data = pivoted_data.fillna(0)
        # Now, create the surface plot

        plotly_fig = go.Figure(
            data=[go.Surface(z=pivoted_data.values, x=pivoted_data.columns, y=pivoted_data.index)])

        x_values=pivoted_data.columns  # Explicitly set tick positions
        fig_x_value=[str(val) for val in x_values]  # Cust
        y_values=pivoted_data.index  # Explicitly set tick positions
        fig_y_value=[str(val) for val in y_values]  # Cust

    return plotly_fig       


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

    fig_json_serializable.update_layout(
        plot_bgcolor='#1e1e1e',  # Darker background for the plot area
        paper_bgcolor='#101820',  # Dark gray for the paper
        font=dict(color='white'),  # White text color
        title = figname,
        title_font=dict(size=20, color='white')
        )

    if x_column is not None and (d_column =="1D"or d_column =="2D") and g_column != 'Pie':
        fig_json_serializable.update_layout(
            plot_bgcolor='#1e1e1e',  # Darker background for the plot area
            paper_bgcolor='#101820',  # Dark gray for the paper
            font=dict(color='white'),  # White text color
            title = figname,
            title_font=dict(size=20, color='white'),  # Title styling
            xaxis=dict(
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
                categoryorder='category ascending',  # Ensures categorical x-values are treated correctly
            )
        )
    elif x_column is not None and d_column =="3D":
        fig_json_serializable.update_layout(
            plot_bgcolor='#1e1e1e',  # Darker background for the plot area
            paper_bgcolor='#101820',  # Dark gray for the paper
            font=dict(color='white'),  # White text color
            title = figname,
            title_font=dict(size=20, color='white'),  # Title styling
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

    if d_column == "3D":
        name = 'default'
        # Default parameters which are used when `layout.scene.camera` is not provided
        camera = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.25, y=1.25, z=1.25)
        )
        
        fig_json_serializable.update_layout(scene_camera=camera) #, title=name
        