#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 16:44:52 2024

@author: quentin
"""


"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dask interface for dataframe informations

#=============================================================================
   #=============================================================================
   #============================================================================="""

import dash
from dash import dcc, html, Input, Output, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import dask.dataframe as dd
from collections import OrderedDict
import plotly.express as px
import webbrowser
import numpy as np
import plotly.tools as tls  # For converting Matplotlib to Plotly
import plotly.graph_objects as go

import Function_dataframe as fd
import Function_errors as fe
import Function_visualisation as fv
import web_interface_style as wis
import table_dropdown_style as tds
import figure_dropdown_style as fds
import data_plot_preparation as dpp

"""#=============================================================================
   #=============================================================================
   #============================================================================="""





def dask_interface(Project_path,Large_file_memory):
    
    # List of the required data file.
    List_file=['title.basics.tsv']
    #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    if Large_file_memory==False:
        df = pd.read_csv(Project_path+List_file[0], sep=';', usecols=["tconst", "startYear", "runtimeMinutes", "genres", "isAdult"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    else:
        df = dd.read_csv(
            Project_path+List_file[0],
            sep='\t',
            usecols=["tconst", "startYear", "runtimeMinutes", "genres", "isAdult"],
            encoding='utf-8',
            on_bad_lines='skip',
            quotechar='"',
            dtype={
                'runtimeMinutes': 'object',   # Read as object to handle invalid values
                'startYear': 'object',        # Read as object to handle invalid values
                'isAdult': 'object'           # Read as object to handle invalid values
            }
        )
        df = df.replace('\\N', np.nan)

    list_col_num = ["startYear", "runtimeMinutes"]
    
    # Get column names
    columns = df.columns    
    #Exclude all elements of the dataframe where the column_to_exclude_element correspnds to the Name_element
    column_to_exclude_element="genres"
    Name_element="Short"   
    # Handle NaN values by filling them with an empty string
    df[column_to_exclude_element] = df[column_to_exclude_element].fillna('')
    # Filter out rows where the column contains the specified name element
    df = df[~df[column_to_exclude_element].str.contains(Name_element, na=False)]
    
    df = df.head(100) 


    # Initialize the Dash app with the dark theme (background, table, dropdown, etc)
    app, fixed_widths, dark_dropdown_style, uniform_style = wis.web_interface_style(df)
    
    # Create the table with the appropriate dropdowns for each column
    dropdowns_with_labels, data_table = tds.dropdown_table(df, fixed_widths, dark_dropdown_style, uniform_style, list_col_num)

    # Create the figure with the appropriate dropdowns for each axis
    dropdowns_with_labels_for_fig = fds.dropdown_figure(app, df, dark_dropdown_style, uniform_style, Large_file_memory)



    @app.callback(
        Output('y-dropdown', 'options'),
        Input('x-dropdown', 'value'),
        Input('tabs', 'value')  # Include tab value to conditionally trigger callback
    )
    def update_y_dropdown(selected_x, selected_tab):
        if selected_tab == 'tab-2':  # Only execute if in the Data Visualization tab
            return [{'label': 'None', 'value': 'None'}] + [{'label': col, 'value': col} for col in df.columns if col != selected_x]
        return []  # Return empty if not in the right tab

    # Define the callback to update the Filter input based on the selected value in the y dropdown
    @app.callback(
        Output('Filter-dropdown-container', 'children'),  # Output for the Filter container
        Input('y-dropdown', 'value')  # Input from y dropdown
    )
    def update_filter_input(y_value):
        print(f"Selected y_value: {y_value}")  # Debugging print
    
        if y_value is None or y_value == 'None':
            return html.Div([
                html.Label('Select Filter on y'),  # Label for the input
                html.Div(" Select an y column.", style={"color": "red"})
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and input vertically
        
        if y_value not in list_col_num:  # If a valid column is selected
            # unique_values = sorted(df[y_value].dropna().unique())  # Sort unique values and drop NaNs
            unique_values = sorted(set(val.strip() for sublist in df[y_value].dropna().str.split(',') for val in sublist))
            print("Filter 1 - Unique Values:", unique_values)  # Debugging print
            return html.Div([
                html.Label(f'Select Filter on y'),  # Label for the dropdown
                dcc.Dropdown(
                    id='Filter-dropdown',  # Ensure this ID is correct
                    options=[{'label': val, 'value': val} for val in unique_values],  # Populate with unique values
                    multi=True,  # Enable multiple selection
                    placeholder='Select values',  # Placeholder text
                    style={**dark_dropdown_style, **uniform_style}  # Apply dark theme style
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        else:  # Default behavior for 'None' or 'All'
            print("Filter 2")  # Debugging print
            return html.Div([
                html.Label(f'Select Filter on y'),  # Label for the input
                dcc.Input(
                    id='Filter-dropdown',  # Ensure this ID is correct
                    type='text',
                    placeholder='Condition (e.g., 100-200)',
                    debounce=True,  # Apply changes when pressing Enter or losing focus
                    style={**dark_dropdown_style, **uniform_style}  # Apply dark theme style
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and input vertically


    # Callback to update the figure based on the dropdown selections
    @app.callback(
        Output('graph-output', 'figure'),
        [Input('x-dropdown', 'value'),
         Input('y-dropdown', 'value'),
         Input('Func-dropdown', 'value'),
         # Input('Filter-dropdown', 'value'),
         Input('Graph-dropdown', 'value')],
        Input('tabs', 'value')  # Include tab value to conditionally trigger callback
    )
    def update_graph(x_column, y_column, func_column, graph_type, selected_tab):
        if selected_tab == 'tab-2':  # Only execute if in the Data Visualization tab
            print()
            print("Start with all data")
            filtered_data = df.copy()  # Make sure to work with a copy of the original DataFrame

            # Get the `Filter-dropdown` value only if it exists
            filter_value = None
            triggered = [p['prop_id'] for p in callback_context.triggered]
        
            # Check if the `Filter-dropdown` exists before trying to use its value
            if 'Filter-dropdown.value' in triggered or any('Filter-dropdown-container' in trigger for trigger in triggered):
                filter_value = callback_context.inputs.get('Filter-dropdown.value', None)
            
            print(filter_value)
            # Only apply filtering if y_column is valid
            if y_column is not None and y_column != 'None' and filter_value:
                filtered_data, error_msg = filter_data_by_value(filtered_data, x_column, y_column, filter_value, list_col_num)        
 
            # Create the figure based on filtered data
            fig = fds.create_figure(filtered_data, x_column, y_column, func_column, filter_value, graph_type, Large_file_memory)
            
            return fig
        else:
            return go.Figure()  # Return a blank figure if not in the right tab




    # Create a list of Input objects for each dropdown
    dropdown_inputs = [Input(f'{col}-dropdown', 'value') for col in df.columns]   
    @app.callback(
        Output('data-table', 'data'),
        dropdown_inputs
    )
    
    def update_output(*selected_values):
        # Start with the original DataFrame
        filtered_df = df.copy()
        # Filter the DataFrame based on selections
        for i, selected_value in enumerate(selected_values):
            col_name = df.columns[i]
            filtered_df = filter_data_by_value_array(filtered_df, col_name, selected_value, list_col_num)
        # Return the updated options for all dropdowns and the filtered data for the table
        return filtered_df.to_dict('records')



    # =============================================================================
    # Main
    # =============================================================================
    # Define the layout with Tabs
    app.layout = html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='IMDB Data Table', value='tab-1'),
            dcc.Tab(label='Data Visualization', value='tab-2'),
            dcc.Tab(label='Summary Statistics', value='tab-3')
        ]),
        html.Div(id='tabs-content')  # This Div will hold the content of each tab
    ])


    # Callback to update the content based on the selected tab
    @app.callback(Output('tabs-content', 'children'),
                  [Input('tabs', 'value')])
    def render_content(tab):
        if tab == 'tab-1':
            # Tab 1: IMDB Data Table
            return layout_for_tab1(dropdowns_with_labels, data_table)
        elif tab == 'tab-2':
            # Tab 2: Data Visualization
            return layout_for_tab2(dropdowns_with_labels_for_fig)
        elif tab == 'tab-3':
            # Tab 3: Summary Statistics
            return html.Div([
                html.H3('Summary Statistics'),
                html.Div([
                    html.P(f'Total Rows: {len(df)}'),
                    html.P(f'Number of Unique Genres: {df["genres"].nunique()}'),
                    # Add more statistics as needed
                ])
            ])
    # =============================================================================
    # End Main
    # =============================================================================

    
    app.run_server(debug=True, port=8051)
    
    # Specify the URL you want to open
    url = "http://127.0.0.1:8051/"
    
    # Open the URL in the default web browser
    # webbrowser.open(url)
    
    
    return 0, df




def layout_for_tab1(dropdowns_with_labels, data_table):
    return html.Div([
        html.H1("IMDB DataFrame Interface", style={"color": "#FFD700"}, className="text-light"),
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div(dropdowns_with_labels, style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'})
        ]),
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div(data_table, style={'width': '50%'})
        ])
    ], style={'padding': '20px'})


def layout_for_tab2(dropdowns_with_labels_for_fig):
    return html.Div([
        html.H1("IMDB DataFrame Interface", style={"color": "#FFD700"}, className="text-light"),
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div(dropdowns_with_labels_for_fig, style={'display': 'flex', 'margin-left': '50px', 'justify-content': 'flex-start', 'gap': '5px'})
        ]),
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div([dcc.Graph(id='graph-output', style={'width': '100%', 'height': '600px'})], style={'margin-left': '20px', 'width': '50%'})
        ])
    ], style={'padding': '20px'})






def filter_data_by_value(df, x_column, y_column, filter_value, list_col_num):

    """
    Filters the DataFrame based on the provided x and y columns, and the filter value.
    
    Parameters:
    - df: DataFrame to filter.
    - x_column: Selected x column.
    - y_column: Selected y column.
    - filter_value: The value or range to filter on.
    - list_col_num: List of columns considered as numeric.
    
    Returns:
    - df: Filtered DataFrame.
    - error_msg: Any error message that occurred during filtering (None if no error).
    """    
    
    error_msg = None  # Initialize error message

    if x_column is not None and y_column is not None:
        if y_column in list_col_num:
            print(f"{y_column} is numeric data")
            
            # Ensure the y_column is numeric and drop NaNs
            df[y_column] = pd.to_numeric(df[y_column], errors='coerce')
            df = df.dropna(subset=[y_column])
            
            # Handle numeric filtering
            if filter_value:
                try:
                    if isinstance(filter_value, str):
                        lower, upper = map(int, filter_value.split('-'))
                        if lower > upper:
                            error_msg = f"Invalid range: {lower} is greater than {upper}."
                            print(error_msg)
                        else:
                            df = df[(df[y_column] >= lower) & (df[y_column] <= upper)]
                except ValueError:
                    error_msg = f"Invalid filter format: {filter_value}. Please enter in 'lower-upper' format."
                    print(f"Filter value error: {error_msg}")
        else:
            print(f"{y_column} is string data")

            # Handle string filtering for non-numeric columns
            df[y_column] = df[y_column].astype(str)  # Ensure string type
            if filter_value and isinstance(filter_value, str):
                # Check if the filter value exists in the data
                unique_values = df[y_column].unique()
                if filter_value in unique_values:
                    df = df[df[y_column].str.contains(filter_value, case=False, na=False)]
                else:
                    error_msg = f"Filter value '{filter_value}' not found in column '{y_column}'."
                    print(error_msg)
                        
    
    return df, error_msg



def filter_data_by_value_array(df, y_column, filter_value, list_col_num):

    """
    Filters the DataFrame based on the provided x and y columns, and the filter value.
    
    Parameters:
    - df: DataFrame to filter.
    - y_column: Selected y column.
    - filter_value: The value or range to filter on.
    - list_col_num: List of columns considered as numeric.
    
    Returns:
    - df: Filtered DataFrame.
    - error_msg: Any error message that occurred during filtering (None if no error).
    """    
    
    error_msg = None  # Initialize error message
    print(y_column)
    if y_column is not None:
        if y_column in list_col_num:
            print(f"{y_column} is numeric data")
            
            # Ensure the y_column is numeric and drop NaNs
            df[y_column] = pd.to_numeric(df[y_column], errors='coerce')
            df = df.dropna(subset=[y_column])
            
            # Handle numeric filtering
            if filter_value:
                try:
                    if isinstance(filter_value, str):
                        lower, upper = map(int, filter_value.split('-'))
                        if lower > upper:
                            error_msg = f"Invalid range: {lower} is greater than {upper}."
                            print(error_msg)
                        else:
                            df = df[(df[y_column] >= lower) & (df[y_column] <= upper)]
                except ValueError:
                    error_msg = f"Invalid filter format: {filter_value}. Please enter in 'lower-upper' format."
                    print(f"Filter value error: {error_msg}")
        else:
            
            print(f"{y_column} is string data")

            # Handle string filtering for non-numeric columns
            df[y_column] = df[y_column].astype(str)  # Ensure string type
            if filter_value and isinstance(filter_value, str):
                # Check if the filter value exists in the data
                unique_values = df[y_column].unique()
                if filter_value in unique_values:
                    df = df[df[y_column].str.contains(filter_value, case=False, na=False)]
                elif filter_value == 'All':
                    df = df
                else:
                    error_msg = f"Filter value '{filter_value}' not found in column '{y_column}'."
                    print(error_msg)
                        
    return df