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

from termcolor import colored
import numpy as np
import matplotlib.pyplot as plt
import plotly.tools as tls  # For converting Matplotlib to Plotly
import plotly.graph_objects as go
import plotly.express as px

import Function_dataframe as fd
import Function_errors as fe
import Function_visualisation as fv
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
    - ax: The figure axis. 
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
    - fig: matplotlib figure.
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
    - fig_json_serializable: dash figure.
    - figname: The name of the Figure.
    - xlabel: The xlabel of the axis (can be None).
    - ylabel: The ylabel of the axis (can be None).
    - zlabel: The zlabel of the axis (can be None).
    - x_column: Column in the dataframe
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.

    Returns:
    - fig_json_serializable: dash figure updated.
    """

    fig_json_serializable.update_layout(
        plot_bgcolor='#1e1e1e',  # Darker background for the plot area
        paper_bgcolor='#343a40',  # Dark gray for the paper
        font=dict(color='white'),  # White text color
        title = figname,
        title_font=dict(size=20, color='white')
        )

    if x_column is not None and (d_column =="1D"or d_column =="2D") and g_column != 'Pie':
        fig_json_serializable.update_layout(
            plot_bgcolor='#1e1e1e',  # Darker background for the plot area
            paper_bgcolor='#343a40',  # Dark gray for the paper
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
            paper_bgcolor='#343a40',  # Dark gray for the paper
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
        

"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def get_max_width(col_data, col_name):

    if col_data.empty:
        return 0  # Return 0 or a default width if there are no values
    
    max_length = max(col_data.apply(lambda x: len(str(x))))
    print(max_length,col_name)
    # Set a higher max width for 'title' column
    if col_name == 'title':
        return max(150, min(max_length * 10, 600))  # Minimum 150px, maximum 400px for 'title'
    return max(80, min(max_length * 8, 300))  # Ensure minimum 80px and maximum 300px width for others


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def dropdown_figure(df, id_graph, tab, dark_dropdown_style, uniform_style, Large_file_memory):

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
    graph_type = ["Histogram", "Curve", "Scatter", "Colormesh"]

    # Get the graph dimension
    dim_type = ["1D", "2D", "3D"]
    
    # Get the list of axis and graph function
    axis = ["x", "y", "z", "Func", "Graph", "Dim"]


    # Define a consistent style for both input and dropdown elements
    uniform_style = {
        'width': '160px',  # Set a consistent width
        'height': '40px',  # Set a consistent width
        'borderRadius': '5px',  # Optional: Add rounded corners
    }

    # Create the dropdowns for each column
    dropdowns_with_labels = []
    for axi in axis:
        if axi == 'Dim':
            # Get unique values and sort them
            dropdown_with_label = html.Div([
                html.Label(f'Select graph {axi}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in dim_type],
                    value='1D',  # Set default to "All", meaning no filtering
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        elif axi == 'Graph':
            # Get unique values and sort them
            dropdown_with_label = html.Div([
                html.Label(f'Select a {axi} type'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
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
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in function_on_y],
                    # value='All',  # Set default to "All", meaning no filtering
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        elif axi== 'z':
            dropdown_with_label = html.Div([
                html.Label(f'Select {axi}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in columns],  #[{'label': 'None', 'value': 'None'}] + 
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        elif axi== 'y':
            dropdown_with_label = html.Div([
                html.Label(f'Select {axi}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in columns],  #[{'label': 'None', 'value': 'None'}] + 
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        else:
            dropdown_with_label = html.Div([
                html.Label(f'Select {axi}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in columns],
                    # value=None,
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically

        dropdowns_with_labels.append(dropdown_with_label)

        
    return dropdowns_with_labels


"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def dropdown_figure_filter(df, id_graph, tab, dark_dropdown_style, uniform_style):

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
                    id=f'{col}-fig-dropdown-'+tab,
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
                    id=f'{col}-fig-dropdown-'+tab,
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
   

def dropdown_checkboxes_figure_filter(df, id_graph, tab, dark_dropdown_style, uniform_style):
    
    columns = df.columns
    
    # Calculate widths, ensuring 'title' is handled specifically
    column_widths = {col: get_max_width(df[col], col) for col in columns}
    
    # Create dropdowns with checkboxes using calculated widths
    dropdowns_with_labels_and_checkboxes = []
    for col in columns:
        dtype = df[col].dtype
        dropdown_style = {**dark_dropdown_style, **uniform_style}
        # Define whether to use dropdown or input based on the data type
        if dtype == "float64":
            input_component = dcc.Input(
                id=f'{col}-fig-dropdown-'+tab,
                type='text',
                debounce=True,
                style=dropdown_style
            )
        else:
            # Collect all unique values, ensuring uniqueness
            all_roles = set()
            for value in df[col].dropna().unique():
                roles = [role.strip() for role in str(value).split(',')]
                all_roles.update(roles)
            unique_values = sorted(all_roles)
            
            input_component = dcc.Dropdown(
                id=f'{col}-fig-dropdown-'+tab,
                options=[{'label': val, 'value': val} for val in unique_values],
                style=dropdown_style,
                className='dash-dropdown',
                multi=True
            )
        
        # Add a div that includes the checkbox and the label to the right
        dropdown_with_checkbox = html.Div([
            dcc.Checklist(
                id=f'checkbox-{col}-'+tab,
                options=[{'label': '', 'value': col}],
                value=[],  # Empty by default
                style={'display': 'inline-block', 'verticalAlign': 'middle'}
            ),
            html.Label(f'{col}', style={'marginLeft': '5px', 'marginRight': '10px'}),  # Label on the right of the checkbox
            input_component
        ], style={'display': 'flex', 'alignItems': 'center', 'width': f'{column_widths[col] + 60}px', 'padding': '0 5px'}) # Adjusted width for checkbox
        
        dropdowns_with_labels_and_checkboxes.append(dropdown_with_checkbox)

    return dropdowns_with_labels_and_checkboxes


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def figure_position_checkboxes_dash(idgraph, List_col_tab, dropdowns_with_labels_for_fig, dropdowns_with_labels_for_fig_filter):
    # Generate the checkbox options
    checkbox_options = [{'label': col, 'value': col} for col in List_col_tab]
    
    # Zip the checkbox options and their corresponding dropdowns
    filter_with_checkboxes = zip(checkbox_options, dropdowns_with_labels_for_fig_filter)

    checkboxes = html.Div(
        style={'display': 'flex', 'flex-direction': 'column', 'gap': '10px'},  # Stack vertically
        children=[
            html.Div(
                style={'display': 'flex', 'align-items': 'center', 'gap': '10px'},
                children=[
                    dcc.Checklist(
                        id=f'checkbox-{option["value"]}',  # Unique ID for each checkbox
                        options=[option],  # Use individual options
                        value=[],  # Default to no checked values (or adjust as needed)
                        inline=True,
                    ),
                    dropdown  # Make sure dropdown corresponds to the correct item
                ]
            )
            for option, dropdown in filter_with_checkboxes
        ]
    )

    return html.Div(
        style={'display': 'flex', 'flex-direction': 'column', 'margin-top': '10px'},
        children=[
            # Dropdowns for the main graph filters
            html.Div(
                dropdowns_with_labels_for_fig,
                style={
                    'display': 'flex',
                    'margin-left': '300px',
                    'justify-content': 'flex-start',
                    'gap': '5px',
                    'margin-bottom': '20px'
                }
            ),
            # Graph on the left and checkboxes on the right
            html.Div(
                style={'display': 'flex'}, 
                children=[
                    # Graph on the left
                    html.Div(
                        [dcc.Graph(id=idgraph, style={'width': '100%', 'height': '600px'})], 
                        style={'margin-left': '20px', 'width': '70%'}
                    ),
                    # Checkboxes and dropdowns for filtering on the right
                    html.Div(
                        style={'margin-left': '20px', 'width': '30%'}, 
                        children=[
                            html.H1('Select filters on the dataframe.', style={'margin-bottom': '10px'}),
                            checkboxes  # Insert the dynamically created checkboxes here
                        ]
                    )
                ]
            )
        ]
    )

"""#=============================================================================
   #=============================================================================
   #============================================================================="""



def figure_position_dash(idgraph, dropdowns_with_labels_for_fig, dropdowns_with_labels_for_fig_filter):
    
    return html.Div(
        style={'display': 'flex', 'flex-direction': 'column', 'margin-top': '10px'},  # Use column direction for vertical stacking
        children=[
            # Dropdowns for the graph filters (above the graph)
            html.Div(
                dropdowns_with_labels_for_fig,
                style={
                    'display': 'flex',
                    'margin-left': '300px',
                    'justify-content': 'flex-start',
                    'gap': '5px',
                    'margin-bottom': '20px'  # Add space below the dropdowns
                }
            ),
            # Graph and dropdowns on the right (below the first set of dropdowns)
            html.Div(
                style={'display': 'flex'}, 
                children=[
                    # Graph on the left
                    html.Div(
                        [dcc.Graph(id=idgraph, style={'width': '100%', 'height': '600px'})], 
                        style={'margin-left': '20px', 'width': '70%'}
                    ),
                    # Dropdowns and heading in a vertical column on the right
                    html.Div(
                        style={'margin-left': '20px', 'width': '30%'},  # Container for the heading and dropdowns
                        children=[
                            # Heading above dropdowns
                            html.H1(
                                'Select filters on the dataframe.',
                                style={'margin-bottom': '10px'},  # Add some space below the heading
                                className="text-light"
                            ),
                            # Dropdowns in a vertical column
                            html.Div(
                                dropdowns_with_labels_for_fig_filter,
                                style={
                                    'display': 'flex',
                                    'flex-direction': 'column',  # Arrange dropdowns vertically
                                    'justify-content': 'flex-start',
                                    'gap': '10px',  # Add spacing between dropdowns
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )




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
    



def tab2_initial_id(columns, tab):

    
    # Placeholder dropdowns for tab-2, initially invisible
    return html.Div([
        dcc.Dropdown(id='x-dropdown-tab-2', value=None, style={'display': 'none'}),
        dcc.Dropdown(id='y-dropdown-tab-2', value=None, style={'display': 'none'}),
        dcc.Dropdown(id='z-dropdown-tab-2', value=None, style={'display': 'none'}),
        
        dcc.Dropdown(id='checkbox-startYear-tab-2', style={'display': 'none'}),
        dcc.Dropdown(id='checkbox-runtimeMinutes-tab-2', style={'display': 'none'}),
        dcc.Dropdown(id='checkbox-genres-tab-2', style={'display': 'none'}),
        dcc.Dropdown(id='checkbox-isAdult-tab-2', style={'display': 'none'}),
        # dcc.Dropdown(id='checkbox-directors-tab-2', style={'display': 'none'}),
        # dcc.Dropdown(id='checkbox-writers-tab-2', style={'display': 'none'}),
        dcc.Dropdown(id='checkbox-averageRating-tab-2', style={'display': 'none'}),
        dcc.Dropdown(id='checkbox-numVotes-tab-2', style={'display': 'none'}),

        dcc.Dropdown(id='startYear-fig-dropdown-tab-2', style={'display': 'none'}),
        dcc.Dropdown(id='runtimeMinutes-fig-dropdown-tab-2', style={'display': 'none'}),
        dcc.Dropdown(id='genres-fig-dropdown-tab-2', style={'display': 'none'}),
        dcc.Dropdown(id='isAdult-fig-dropdown-tab-2', style={'display': 'none'}),
        # dcc.Dropdown(id='directors-fig-dropdown-tab-2', style={'display': 'none'}),
        # dcc.Dropdown(id='writers-fig-dropdown-tab-2', style={'display': 'none'}),
        dcc.Dropdown(id='averageRating-fig-dropdown-tab-2', style={'display': 'none'}),
        dcc.Dropdown(id='numVotes-fig-dropdown-tab-2', style={'display': 'none'}),
        
        # Add other dropdowns as placeholders here as needed
    ], style={'display': 'none'})
