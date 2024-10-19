#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:23:15 2024

@author: quentin
"""

"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions for visualisation of the dataframe

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
# matplotlib.use('Agg')  # Use the Agg backend (no GUI)
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


def create_figure(df, x_column, y_column, z_column, g_column, Large_file_memory):

    """
    Goal: Create a sophisticated figure which adapt to any input variable.

    Parameters:
    - df: dataframe
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Function to operate on df_temp[x_column,y_column]
    - g_column: Type of Graphyque for the figure.
    - Large_file_memory: Estimate if the file is too large to be open with panda

    Returns:
    - fig_json_serializable: The finalized plotly figure. 
    """
    
    if x_column is not None: 
        print("Extract from data base the required column and prepare them for the figure.")
        Para, y = dpp.data_preparation_for_plot(df , x_column, y_column, z_column, Large_file_memory)
    
    # =============================================================================
    print("Start figure creation")
    # =============================================================================

    # Create the Matplotlib figure
    
    fig, ax = plt.subplots(figsize=(11.5, 7))
    
    # Create the label of the figure
    ax, xlabel, ylabel = label_fig(ax, x_column, y_column, z_column)
    x_values, legend = [], []
    
    if x_column is not None: 
        # Add the core of the figure
        fig, ax, x_values, legend = figure_core(fig, ax, x_column, y_column, z_column, g_column, Para, y)  
    
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=10))

    plt.tight_layout()
    
    # Now, convert Matplotlib figure to Plotly
    plotly_fig = tls.mpl_to_plotly(fig)  # Convert the Matplotlib figure to Plotly
    
    # Create a Dash compatible Plotly graph figure
    fig_json_serializable = go.Figure(plotly_fig)  # This figure can now be used with dcc.Graph in Dash

    fig_json_serializable.update_layout(
        plot_bgcolor='#1e1e1e',  # Darker background for the plot area
        paper_bgcolor='#343a40',  # Dark gray for the paper
        font=dict(color='white'),  # White text color
        title_font=dict(size=20, color='white'),  # Title styling
        # X-axis and Y-axis styling
        xaxis=dict(
            tickvals=np.arange(len(x_values)),  # Set the tick positions
            ticktext=x_values,  # Set the tick labels to the genre names
            title=dict(text=xlabel, font=dict(size=20, color='white')),  # X-axis label styling
            tickfont=dict(color='white', size=18),  # X-axis tick color
            tickangle=0,  # Rotate the x-axis labels for better readability
            showgrid=True,  # Grid styling
            gridcolor='gray',  # Grid color
            categoryorder='category ascending'  # Ensures categorical x-values are treated correctly
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(size=20, color='white')),  # Y-axis label styling
            tickfont=dict(color='white', size=18),  # Y-axis tick color
            showgrid=True,  # Grid styling
            gridcolor='gray',  # Grid color
            categoryorder='category ascending'  # Ensures categorical x-values are treated correctly
        ),
        # Legend styling
        legend=dict(
            font=dict(color='white', size=12),  # Legend text color
            bgcolor='#343a40',  # Legend background color
            bordercolor='white',  # Border color of the legend
            borderwidth=1  # Optional: set the width of the border
        )
    )
    plt.close()
    # =============================================================================
    print("=============================================================================")
    return fig_json_serializable


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def label_fig(ax, x_column, y_column, z_column):

    """
    Goal: Create the figure labels.

    Parameters:
    - ax: axis of fig.
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Function to operate on df_temp[x_column,y_column]

    Returns:
    - ax: The figure axis. 
    - xlabel: The xlabel of the axis
    - ylabel: The ylabel of the axis
    """
    
    if x_column is not None: 
        figname = 'Movies over the ' + x_column
        ax.set_title(figname)
        xlabel = x_column
        if str(z_column)=='None':
            ylabel = 'Number of movies'
        elif str(z_column)=='Avg':
            ylabel = 'Average '+y_column+' of the movies'
        else:
            ylabel = "None"

    else: 
        ax.set_title('No data selected')
        xlabel, ylabel = "None","None"
        
    ax.set_xlabel(xlabel, fontsize=15)
    ax.set_ylabel(ylabel, fontsize=15)
    
    return ax, xlabel, ylabel


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def figure_core(fig, ax, x_column, y_column, z_column, g_column, Para, y):

    """
    Goal: Create the plot inside the figure regarding the inputs.

    Parameters:
    - fig: matplotlib figure.
    - ax: axis of fig.
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Function to operate on df_temp[x_column,y_column]
    - g_column: Type of Graphyque for the figure.
    - Para: List of column in the dataframe (can be different of [x_column,y_column])
    - y: Data to plot.

    Returns:
    - dropdowns_with_labels: The finalized dropdowns figure. 
    """
    
    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres", "directors", "writers", "category"]
    
    # Define a list of colors for the bars
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    legend = "None"
    
    if str(y_column)=='None':
                
        # Convert the DataFrame index to a list
        if x_column not in df_col_string:
            x_values = list(map(int, y[Para[0]]))
        else:
            x_values = list(y[Para[0]])
        
        
        if g_column=="Histogram":
            ax.bar(np.arange(len(x_values)), y["Count"])
        if g_column=="Curve":
            ax.plot(np.arange(len(x_values)), y["Count"], linewidth=4.)

            
    else:
        
        # Convert the DataFrame index to a list
        if x_column not in df_col_string:
            x_values = list(map(int, y.index))
        else:
            x_values = y.index
        
        if str(z_column)=='None':
            
            bottom = np.zeros(len(y.index))

            # Plot the stacked bar chart
            bars_list = []  # List to hold bar objects for the legend
            for i, (element_col, y_val) in enumerate(y.items()):
                if g_column=="Histogram":
                    bars = ax.bar(np.arange(len(x_values)), y_val, label=element_col, bottom=bottom, color=colors[i % len(colors)])  # Color assignment
                if g_column=="Curve":
                    bars = ax.plot(np.arange(len(x_values)), y_val, label=element_col, linewidth=4., color=colors[i % len(colors)])
                bars_list.append(bars)  # Store the bars
                bottom += y_val              
                

            # Create a custom legend using the bars created
            legend_handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors[:len(y)]]
            legend_labels = y.columns.tolist()  # Get the labels from DataFrame columns
            # Customize the legend to ensure it reflects the colors of the bars
            legend = ax.legend(legend_handles, legend_labels, ncol=2, handletextpad=0.001)
        
            # legend = ax.legend(ncol=2)
            for text in legend.get_texts():
                text.set_color('white')  # Set the color of the legend text
                text.set_fontsize(15)  # Set the font size of the legend text
    
        elif str(z_column) == "Avg":
                        
            if g_column=="Histogram":
                ax.bar(np.arange(len(x_values)), y)
            if g_column=="Curve":
                ax.plot(np.arange(len(x_values)), y, linewidth=4.)
            
    print(np.arange(len(x_values)))
    print(x_values)
    
    # Set x-ticks to the actual index values
    ax.set_xticks(np.arange(len(x_values)))  # Set the x-ticks to the index of y
    ax.set_xticklabels(x_values, rotation=45, ha='right')  # Set labels and rotate them for better visibility
            
    ax.tick_params(axis='both', labelsize=10)
    ax.grid(True, color='grey', linestyle='--', linewidth=2, alpha=0.5)  
            
    return fig, ax, x_values, legend


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def get_max_width(col_data, col_name):
    max_length = max(col_data.apply(lambda x: len(str(x))))
    print(max_length,col_name)
    # Set a higher max width for 'title' column
    if col_name == 'title':
        return max(150, min(max_length * 10, 600))  # Minimum 150px, maximum 400px for 'title'
    return max(80, min(max_length * 8, 300))  # Ensure minimum 80px and maximum 300px width for others


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def dropdown_figure(df, id_graph, dark_dropdown_style, uniform_style, Large_file_memory):

    """
    Goal: Create the dropdown associated to a figure.

    Parameters:
    - df: dataframe.
    - dark_dropdown_style: Color style of the dropdown.
    - Large_file_memory: Estimate if the file is too large to be open with panda.

    Returns:
    - dropdowns_with_labels: The finalized dropdowns figure. 
    """

    # Get column names
    columns = df.columns
    
    # Get the list of y function
    function_on_y = ["Avg"]
    
    # Get the type of graph
    graph_type = ["Histogram", "Curve"]
    
    # Get the list of axis and graph function
    axis = ["x", "y", "Func", "Graph"]

    # Define a consistent style for both input and dropdown elements
    uniform_style = {
        'width': '160px',  # Set a consistent width
        'height': '40px',  # Set a consistent width
        'borderRadius': '5px',  # Optional: Add rounded corners
    }

    # Create the dropdowns for each column
    dropdowns_with_labels = []
    for axi in axis:
        if axi == 'Graph':
            # Get unique values and sort them
            dropdown_with_label = html.Div([
                html.Label(f'Select a {axi} type'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown',
                    options=[{'label': val, 'value': val} for val in graph_type],
                    value='Histogram',  # Set default to "All", meaning no filtering
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        elif axi == 'Func':
            # Get unique values and sort them
            dropdown_with_label = html.Div([
                html.Label(f'Select {axi} on y'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown',
                    options=[{'label': val, 'value': val} for val in function_on_y],
                    value='All',  # Set default to "All", meaning no filtering
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        elif axi== 'y':
            dropdown_with_label = html.Div([
                html.Label(f'Select {axi}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown',
                    options=[{'label': val, 'value': val} for val in columns],  #[{'label': 'None', 'value': 'None'}] + 
                    # value='All',  # Set default to "All", meaning no filtering
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        else:
            dropdown_with_label = html.Div([
                html.Label(f'Select {axi}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown',
                    options=[{'label': val, 'value': val} for val in columns],
                    # value='All',  # Set default to "All", meaning no filtering
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically

        dropdowns_with_labels.append(dropdown_with_label)

        
    return dropdowns_with_labels


"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def dropdown_figure_filter(df, id_graph, dark_dropdown_style, uniform_style):

    columns = df.columns
    

    # Calculate widths, ensuring 'title' is handled specifically
    column_widths = {col: get_max_width(df[col], col) for col in columns}
    
    # Create dropdowns using calculated widths
    dropdowns_with_labels = []
    for col in columns:
        dtype = df[col].dtype
        dropdown_style = {**dark_dropdown_style, **uniform_style, 'width': f'{column_widths[col]}px'}

        if dtype == "float64":
            dropdown_with_label = html.Div([
                html.Label(f'{col}'),
                dcc.Input(
                    id=f'{col}-fig-dropdown',
                    type='text',
                    debounce=True,
                    style=dropdown_style
                )
            ], style={'display': 'inline-block', 'width': f'{column_widths[col]}px', 'padding': '0 5px'})
        else:
            # Collect all unique values, splitting them by commas and ensuring uniqueness
            all_roles = set()
            for value in df[col].dropna().unique():
                # Split the value by comma and strip any extra spaces
                roles = [role.strip() for role in str(value).split(',')]
                all_roles.update(roles)
            
            # Convert to a sorted list
            unique_values = sorted(all_roles)
            
            # unique_values = sorted(df[col].unique())
            dropdown_with_label = html.Div([
                html.Label(f'{col}'),
                dcc.Dropdown(
                    id=f'{col}-fig-dropdown',
                    options=[{'label': val, 'value': val} for val in unique_values], #[{'label': 'All', 'value': 'All'}] + 
                    # value='All',
                    style=dropdown_style,
                    className='dash-dropdown',
                    multi=True
                )
            ], style={'display': 'inline-block', 'width': f'{column_widths[col]}px', 'padding': '0 5px'})
    
        dropdowns_with_labels.append(dropdown_with_label)

    
    return dropdowns_with_labels


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def get_dropdown_options(filtered_data, y_column):
    print("""Generate dropdown options based on the type of y_column.""")
    # Convert column to numeric, forcing errors to NaN
    filtered_data[y_column] = pd.to_numeric(filtered_data[y_column], errors='coerce')
    filtered_data = filtered_data.dropna(subset=[y_column]).copy()

    # Generate options based on the type of y_column
    if y_column in list_col_num:
        # Generate numeric ranges
        min_val, max_val = int(filtered_data[y_column].min()), int(filtered_data[y_column].max())
        ranges = [f"{i}-{i + 10}" for i in range(min_val, max_val, 10)]  # Adjust range size as needed
        return ranges
    else:
        # For string columns like genres, return unique string values
        filtered_data[y_column] = filtered_data[y_column].astype(str)  # Ensure column is string type
        unique_values = filtered_data[y_column].dropna().unique().tolist()
        return unique_values
    
