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
from collections import OrderedDict
import plotly.express as px
import webbrowser

import Function_dataframe as fd
import Function_errors as fe
import Function_visualisation as fv
import web_interface_style as wis
import table_dropdown_style as tds
import figure_dropdown_style as fds


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
    app, fixed_widths, dark_dropdown_style = wis.web_interface_style(df)
    
    # Create the table with the appropriate dropdowns for each column
    dropdowns_with_labels, data_table = tds.dropdown_table(df, fixed_widths, dark_dropdown_style)

    # Create the figure with the appropriate dropdowns for each axis
    dropdowns_with_labels_for_fig = fds.dropdown_figure(df, dark_dropdown_style, Large_file_memory)


    
    app.layout = html.Div([
    
        # Title with custom style
        html.H1("IMDB DataFrame Interface", style={"color": "#FFD700"}, className="text-light"),
    
        # First row of dropdowns
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div(dropdowns_with_labels, style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'}),
            html.Div(dropdowns_with_labels_for_fig, style={'display': 'flex', 'margin-left': '150px', 'justify-content': 'flex-start', 'gap': '5px'})
        ]),  # Closing the html.Div for the dropdown row
    
        # Second row: Data table on the left, Plotly graph on the right
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div(data_table, style={'width': '50%'}),  # Data table takes 50% of the space
            html.Div([
                dcc.Graph(id='graph-output', style={'width': '100%', 'height': '600px'})  #, figure=fig Plotly figure
            ], style={'margin-left': '20px', 'width': '50%'})  # Adjusting width and margin for spacing
        ])
    ], style={'padding': '20px'})


    # Callback to update y-dropdown options based on x-dropdown selection
    @app.callback(
        Output('y-dropdown', 'options'),
        Input('x-dropdown', 'value')
    )
    def update_y_dropdown(selected_x):
        # Exclude the selected x from the options in the y dropdown
        return [{'label': 'None', 'value': 'None'}] + [{'label': col, 'value': col} for col in columns if col != selected_x]


    # Callback to update the figure based on the dropdown selections
    @app.callback(
        Output('graph-output', 'figure'),
        [Input('x-dropdown', 'value'),
         Input('y-dropdown', 'value'),
         Input('Func-dropdown', 'value'),
         Input('Graph-dropdown', 'value')]
    )
    def update_graph(x_column, y_column, z_column, g_column):
        
        # # If no valid selection is made, return an empty figure
        # if x_column is None or z_column is None:
        #     return fds.create_empty_figure('No data selected', x_column, y_column, z_column, g_column)

        fig = fds.create_figure(df, x_column, y_column, z_column, g_column, Large_file_memory)
        
        return fig





    # Create a list of Input objects for each dropdown
    dropdown_inputs = [Input(f'{col}-dropdown', 'value') for col in df.columns]
    
    @app.callback(
        [Output(f'{col}-dropdown', 'options') for col in df.columns] + [Output('data-table', 'data')],
        dropdown_inputs
    )
    def update_output(*selected_values):
        # Start with the original DataFrame
        filtered_df = df.copy()
    
        # Filter the DataFrame based on selections
        for i, selected_value in enumerate(selected_values):
            if selected_value != 'All':  # Skip filtering if 'All' is selected
                col_name = df.columns[i]
                filtered_df = filtered_df[filtered_df[col_name] == selected_value]
    
        # Create updated options for each dropdown based on the filtered DataFrame
        updated_options = []
        for col in df.columns:
            # Get unique values in the filtered DataFrame for the current column
            unique_values = sorted(filtered_df[col].unique())
            # Prepare options, adding 'All' as the first option
            options = [{'label': 'All', 'value': 'All'}] + [{'label': val, 'value': val} for val in unique_values]
            updated_options.append(options)
    
        # Return the updated options for all dropdowns and the filtered data for the table
        return updated_options + [filtered_df.to_dict('records')]




    
    app.run_server(debug=True, port=8051)
    
    # Specify the URL you want to open
    url = "http://127.0.0.1:8051/"
    
    # Open the URL in the default web browser
    # webbrowser.open(url)
    
    
    return 0, df
