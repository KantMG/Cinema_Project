#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 17:09:05 2024

@author: quentin
"""


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

import time

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
import name_dropdown_style as nds
import data_plot_preparation as dpp
import open_dataframe as od

"""#=============================================================================
   #=============================================================================
   #============================================================================="""





def dask_interface(Project_path, Large_file_memory, Get_file_sys_mem):
    
    # # List of the required data file.
    # List_file=['title.basics.tsv']
    # #Create class 'pandas.core.frame.DataFrame' with only the necessary columns
    # if Large_file_memory==False:
    #     df = pd.read_csv(Project_path+List_file[0], sep=';', usecols=["tconst", "startYear", "runtimeMinutes", "genres", "isAdult"], encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    # else:
    #     df = dd.read_csv(
    #         Project_path+List_file[0],
    #         sep='\t',
    #         usecols=["tconst", "startYear", "runtimeMinutes", "genres", "isAdult"],
    #         encoding='utf-8',
    #         on_bad_lines='skip',
    #         quotechar='"',
    #         dtype={
    #             'runtimeMinutes': 'object',   # Read as object to handle invalid values
    #             'startYear': 'object',        # Read as object to handle invalid values
    #             'isAdult': 'object'           # Read as object to handle invalid values
    #         }
    #     )
    #     df = df.replace('\\N', np.nan)

    # list_col_num = ["startYear", "runtimeMinutes"]
    
    # # Get column names
    # columns = df.columns    
    # #Exclude all elements of the dataframe where the column_to_exclude_element correspnds to the Name_element
    # column_to_exclude_element="genres"
    # Name_element="Short"   
    # # Handle NaN values by filling them with an empty string
    # df[column_to_exclude_element] = df[column_to_exclude_element].fillna('')
    # # Filter out rows where the column contains the specified name element
    # df = df[~df[column_to_exclude_element].str.contains(Name_element, na=False)]
   
    # df = df.head(100) 
    # print(df)




    # Start the timer
    start_time = time.time()    
    
    # look_by_name = True
    # if look_by_name :

    #     List_col = ["nconst", "primaryName", "birthYear", "deathYear"]
        
    #     List_filter = [None, "William K.L. Dickson*", None, None]

    #     name_info = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        
    #     if name_info['nconst'].count() > 1:
    #         print("The DataFrame has more than one row.")
    #         return None, None
    #     else:
    #         # Code to execute if the DataFrame has zero or one row
    #         print("The DataFrame has one or zero rows.")
    #         Name_to_look_for = str(name_info['nconst'].iloc[0])
    #         print(Name_to_look_for)
    #         print()


    # Initialize the Dash app with the dark theme (background, table, dropdown, etc)
    app, dark_dropdown_style, uniform_style = wis.web_interface_style()

    dropdowns_artist_with_labels, info_artist, name_df = nds.dropdown_artist(dark_dropdown_style, uniform_style, Project_path, Large_file_memory, Get_file_sys_mem)

    List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters", "title", "isOriginalTitle"]
    
    List_filter = [None, None, None, None, None, None, None, None, str(name_df['nconst'].iloc[0]), None, None, None, True]
    
    df = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
    exclude_col = ["tconst", "isAdult", "nconst", "isOriginalTitle"]
    df = df.drop(columns=exclude_col)
    
    od.log_performance("Full research", start_time)
    od.plot_performance_logs()

    # Create the table with the appropriate dropdowns for each column
    dropdowns_with_labels, data_table = tds.dropdown_table(df, dark_dropdown_style, uniform_style)

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
        
        # if y_value not in list_col_num:  # If a valid column is selected
        dtype = df[y_value].dtype
        if dtype != "float64":
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
                filtered_data, error_msg = filter_data_by_value(filtered_data, x_column, y_column, filter_value)        
 
            # Create the figure based on filtered data
            fig = fds.create_figure(filtered_data, x_column, y_column, func_column, filter_value, graph_type, Large_file_memory)
            
            return fig
        else:
            return go.Figure()  # Return a blank figure if not in the right tab



    # Create a list of Input objects for each dropdown
    dropdown_input_name = Input(f'primaryName-dropdown', 'value')
    @app.callback(
        Output('nameinfo', 'data'),
        dropdown_input_name
    )
    
    def update_nameinfo(selected_values):
        # Start with the original DataFrame
        filtered_df = df.copy()
        # Filter the DataFrame based on selections
        filtered_df = filter_data_by_value_name(filtered_df, selected_value, Project_path, Large_file_memory, Get_file_sys_mem)
        # Return the updated options for all dropdowns and the filtered data for the table
        return filtered_df.to_dict('records')


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
            filtered_df = filter_data_by_value_array(filtered_df, col_name, selected_value)
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
            return layout_for_tab3(df)
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
        html.Div([
            html.P(f'This interface is dedicated to the research on specific artist.'),
        ]),
        html.Div(style={'display': 'flex', 'margin-top': '10px', 'flex-wrap': 'wrap'}, children=[
            html.Div(dropdowns_artist_with_labels, style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'})
        ]),
        html.Div(style={'display': 'flex', 'margin-top': '10px', 'flex-wrap': 'wrap'}, children=[
            html.Div(dropdowns_with_labels, style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'})
        ]),
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div(data_table, style={'width': '100%'})  # Adjusted to take full width
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


def layout_for_tab3(df):
    return html.Div([
        html.H1("IMDB DataFrame Interface", style={"color": "#FFD700"}, className="text-light"),
        html.Div([
                html.H3('Summary Statistics'),
                html.Div([
                    html.P(f'Total Rows: {len(df)}'),
                    html.P(f'Number of Unique Genres: {df["genres"].nunique()}'),
                    # Add more statistics as needed
                ])
            ])
    ], style={'padding': '20px'})





def filter_data_by_value(df, x_column, y_column, filter_value):

    """
    Filters the DataFrame based on the provided x and y columns, and the filter value.
    
    Parameters:
    - df: DataFrame to filter.
    - x_column: Selected x column.
    - y_column: Selected y column.
    - filter_value: The value or range to filter on.
    
    Returns:
    - df: Filtered DataFrame.
    - error_msg: Any error message that occurred during filtering (None if no error).
    """    
    
    error_msg = None  # Initialize error message

    if x_column is not None and y_column is not None:
        # if y_column in list_col_num:
        dtype = df[y_column].dtype
        if dtype != "float64":
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



def filter_data_by_value_array(df, y_column, filter_value):

    """
    Filters the DataFrame based on the provided x and y columns, and the filter value.
    
    Parameters:
    - df: DataFrame to filter.
    - y_column: Selected y column.
    - filter_value: The value or range to filter on.
    
    Returns:
    - df: Filtered DataFrame.
    - error_msg: Any error message that occurred during filtering (None if no error).
    """    
    
    error_msg = None  # Initialize error message
    print(y_column)
    if y_column is not None:
        # if y_column in list_col_num:
        dtype = df[y_column].dtype
        if dtype == "float64":
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

def filter_data_by_value_name(filtered_df, selected_value, Project_path, Large_file_memory, Get_file_sys_mem):
    
    """
    Filters the DataFrame based on the provided x and y columns, and the filter value.
    
    Parameters:
    - df: DataFrame to filter.
    - y_column: Selected y column.
    - filter_value: The value or range to filter on.
    
    Returns:
    - df: Filtered DataFrame.
    - error_msg: Any error message that occurred during filtering (None if no error).
    """    
    
    error_msg = None  # Initialize error message


    List_col = ["nconst", "primaryName", "birthYear", "deathYear"]
    
    List_filter = [None, selected_value, None, None]

    name_info = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
    
    if name_info['nconst'].count() > 1:
        print("The DataFrame has more than one row.")
        return None, None
    else:
        # Code to execute if the DataFrame has zero or one row
        print("The DataFrame has one or zero rows.")
        Name_to_look_for = str(name_info['nconst'].iloc[0])
        print(Name_to_look_for)
        print()
                        
    return name_info




####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
#                           The initial one
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################


"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dask interface for dataframe informations

#=============================================================================
   #=============================================================================
   #============================================================================="""

import time

import dash
from dash import dcc, html, Input, Output, State, dash_table, callback, callback_context
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
import open_dataframe as od

"""#=============================================================================
   #=============================================================================
   #============================================================================="""





def dask_interface(Project_path, Large_file_memory, Get_file_sys_mem):
    

    # Start the timer
    start_time = time.time()    
    
    # look_by_name = True
    # if look_by_name :

    #     List_col = ["nconst", "primaryName", "birthYear", "deathYear"]
        
    #     List_filter = [None, "William K.L. Dickson*", None, None]

    #     name_info = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        
    #     if name_info['nconst'].count() > 1:
    #         print("The DataFrame has more than one row.")
    #         return None, None
    #     else:
    #         # Code to execute if the DataFrame has zero or one row
    #         print("The DataFrame has one or zero rows.")
    #         Name_to_look_for = str(name_info['nconst'].iloc[0])
    #         print(Name_to_look_for)
    #         print()
        

    # List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters", "title", "isOriginalTitle"]
    
    # List_filter = [None, None, None, None, None, None, None, None, Name_to_look_for, None, None, None, True]
    
    # df = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
    # exclude_col = ["tconst", "isAdult", "nconst", "isOriginalTitle"]
    # df = df.drop(columns=exclude_col)
    
    # od.log_performance("Full research", start_time)
    # od.plot_performance_logs()


    # Initialize the Dash app with the dark theme (background, table, dropdown, etc)
    app, dark_dropdown_style, uniform_style = wis.web_interface_style()

    # Create a DataFrame variable to hold the filtered data
    df = pd.DataFrame()
    Name_to_look_for = None  # Initialize variable to hold name input
    
    # =============================================================================
    # Main
    # =============================================================================
    # Define the layout with Tabs
    app.layout = html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='IMDB Data Table', value='tab-1')
            # dcc.Tab(label='Data Visualization', value='tab-2'),
            # dcc.Tab(label='Summary Statistics', value='tab-3')
        ]),
        html.Div(id='tabs-content'),  # This Div will hold the content of each tab
        dcc.Input(id='name-input', type='text', placeholder='Enter primary name (e.g., William K.L. Dickson*)'),
        html.Button('Submit', id='name-submit', n_clicks=0),
        html.Div(id='name-output')
    ])

    # # Callback to update the content based on the selected tab
    # @app.callback(Output('tabs-content', 'children'),
    #               [Input('tabs', 'value'),
    #                Input('name-input', 'value')])

    # Combined callback to process the name input and update the tab content
    @app.callback(
        [Output('name-output', 'children'),
         Output('tabs-content', 'children')],
        [Input('name-submit', 'n_clicks'),
         Input('tabs', 'value')],
        State('name-input', 'value')
    )
    
    def update_name_and_tab_content(n_clicks, tab, name_input):
        global df, Name_to_look_for  # Use global to modify the outer scope variables
        
        if tab == 'tab-1':  # Logic for Tab 1
            if n_clicks > 0 and name_input:
                # Assuming od.open_data_name() works as intended
                List_col = ["nconst", "primaryName", "birthYear", "deathYear"]
                List_filter = [None, name_input, None, None]  # Filter by primaryName
                
                name_info = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
                
                if name_info['nconst'].count() > 1:
                    Name_to_look_for = None  # Reset if more than one name found
                    df = None  # Reset the DataFrame
                    return "The DataFrame has more than one row. Please refine your search.", layout_for_tab1(None, dark_dropdown_style, uniform_style, Name_to_look_for)
                elif name_info['nconst'].count() == 0:
                    Name_to_look_for = None  # Reset if no names found
                    df = None  # Reset the DataFrame
                    return "No results found.", layout_for_tab1(None, dark_dropdown_style, uniform_style, Name_to_look_for)
                else:
                    Name_to_look_for = str(name_info['nconst'].iloc[0])
                    df = name_info  # Set the DataFrame to the filtered result
                    return f"Name found: {Name_to_look_for}", layout_for_tab1(df, dark_dropdown_style, uniform_style, Name_to_look_for)

            return "Enter a name and click Submit.", layout_for_tab1(df, dark_dropdown_style, uniform_style, Name_to_look_for)
        
        # # For other tabs
        # if tab == 'tab-2':
        #     return "Data visualization content goes here.", layout_for_tab2(dropdowns_with_labels_for_fig)
        # elif tab == 'tab-3':
        #     return "Summary statistics content goes here.", layout_for_tab3(df)
    

    def layout_for_tab1(df, dark_style, uniform_style, name_found):
        if df is not None and name_found is not None:  # Only display the table if a valid name is found
            # Create the table with the appropriate dropdowns for each column
            dropdowns_with_labels, data_table = tds.dropdown_table(df, dark_style, uniform_style)

            return html.Div([
                html.H4(f"Results for: {name_found}"),
                data_table
            ])
        else:
            return html.Div([
                html.H4("Please enter a name to search."),
            ])    
    
    # def render_content(tab):
    #     if tab == 'tab-1':
    #         # Tab 1: IMDB Data Table
    #         return layout_for_tab1(df, dropdowns_with_labels, data_table, Name_to_look_for)
    #     elif tab == 'tab-2':
    #         # Tab 2: Data Visualization
    #         return layout_for_tab2(app, df, dark_dropdown_style, uniform_style, Large_file_memory, dropdowns_with_labels_for_fig)
    #         # return layout_for_tab2(dropdowns_with_labels_for_fig)
    #     elif tab == 'tab-3':
    #         # Tab 3: Summary Statistics
    #         return layout_for_tab3(df)
    # =============================================================================
    # End Main
    # =============================================================================



    # @app.callback(
    #     Output('y-dropdown', 'options'),
    #     Input('x-dropdown', 'value'),
    #     Input('tabs', 'value')  # Include tab value to conditionally trigger callback
    # )
    # def update_y_dropdown(selected_x, selected_tab):
    #     if selected_tab == 'tab-2':  # Only execute if in the Data Visualization tab
    #         return [{'label': 'None', 'value': 'None'}] + [{'label': col, 'value': col} for col in df.columns if col != selected_x]
    #     return []  # Return empty if not in the right tab

    # # Define the callback to update the Filter input based on the selected value in the y dropdown
    # @app.callback(
    #     Output('Filter-dropdown-container', 'children'),  # Output for the Filter container
    #     Input('y-dropdown', 'value')  # Input from y dropdown
    # )
    # def update_filter_input(y_value):
    #     print(f"Selected y_value: {y_value}")  # Debugging print
    
    #     if y_value is None or y_value == 'None':
    #         return html.Div([
    #             html.Label('Select Filter on y'),  # Label for the input
    #             html.Div(" Select an y column.", style={"color": "red"})
    #         ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and input vertically
        
    #     # if y_value not in list_col_num:  # If a valid column is selected
    #     dtype = df[y_value].dtype
    #     if dtype != "float64":
    #         # unique_values = sorted(df[y_value].dropna().unique())  # Sort unique values and drop NaNs
    #         unique_values = sorted(set(val.strip() for sublist in df[y_value].dropna().str.split(',') for val in sublist))
    #         print("Filter 1 - Unique Values:", unique_values)  # Debugging print
    #         return html.Div([
    #             html.Label(f'Select Filter on y'),  # Label for the dropdown
    #             dcc.Dropdown(
    #                 id='Filter-dropdown',  # Ensure this ID is correct
    #                 options=[{'label': val, 'value': val} for val in unique_values],  # Populate with unique values
    #                 multi=True,  # Enable multiple selection
    #                 placeholder='Select values',  # Placeholder text
    #                 style={**dark_dropdown_style, **uniform_style}  # Apply dark theme style
    #             )
    #         ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
    #     else:  # Default behavior for 'None' or 'All'
    #         print("Filter 2")  # Debugging print
    #         return html.Div([
    #             html.Label(f'Select Filter on y'),  # Label for the input
    #             dcc.Input(
    #                 id='Filter-dropdown',  # Ensure this ID is correct
    #                 type='text',
    #                 placeholder='Condition (e.g., 100-200)',
    #                 debounce=True,  # Apply changes when pressing Enter or losing focus
    #                 style={**dark_dropdown_style, **uniform_style}  # Apply dark theme style
    #             )
    #         ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and input vertically


    # # Callback to update the figure based on the dropdown selections
    # @app.callback(
    #     Output('graph-output', 'figure'),
    #     [Input('x-dropdown', 'value'),
    #      Input('y-dropdown', 'value'),
    #      Input('Func-dropdown', 'value'),
    #      # Input('Filter-dropdown', 'value'),
    #      Input('Graph-dropdown', 'value')],
    #     Input('tabs', 'value')  # Include tab value to conditionally trigger callback
    # )
    # def update_graph(x_column, y_column, func_column, graph_type, selected_tab):
    #     if selected_tab == 'tab-2':  # Only execute if in the Data Visualization tab
    #         print()
    #         print("Start with all data")
    #         filtered_data = df.copy()  # Make sure to work with a copy of the original DataFrame

    #         # Get the `Filter-dropdown` value only if it exists
    #         filter_value = None
    #         triggered = [p['prop_id'] for p in callback_context.triggered]
        
    #         # Check if the `Filter-dropdown` exists before trying to use its value
    #         if 'Filter-dropdown.value' in triggered or any('Filter-dropdown-container' in trigger for trigger in triggered):
    #             filter_value = callback_context.inputs.get('Filter-dropdown.value', None)
            
    #         print(filter_value)
    #         # Only apply filtering if y_column is valid
    #         if y_column is not None and y_column != 'None' and filter_value:
    #             filtered_data, error_msg = filter_data_by_value(filtered_data, x_column, y_column, filter_value)        
 
    #         # Create the figure based on filtered data
    #         fig = fds.create_figure(filtered_data, x_column, y_column, func_column, filter_value, graph_type, Large_file_memory)
            
    #         return fig
    #     else:
    #         return go.Figure()  # Return a blank figure if not in the right tab




    # # Create a list of Input objects for each dropdown
    # dropdown_inputs = [Input(f'{col}-dropdown', 'value') for col in df.columns]   
    # @app.callback(
    #     Output('data-table', 'data'),
    #     dropdown_inputs
    # )
    
    # def update_output(*selected_values):
    #     # Start with the original DataFrame
    #     filtered_df = df.copy()
    #     # Filter the DataFrame based on selections
    #     for i, selected_value in enumerate(selected_values):
    #         col_name = df.columns[i]
    #         filtered_df = filter_data_by_value_array(filtered_df, col_name, selected_value)
    #     # Return the updated options for all dropdowns and the filtered data for the table
    #     return filtered_df.to_dict('records')




    # # Callback to process the name input and filter DataFrame
    # @app.callback(
    #     Output('name-output', 'children'),
    #     Output('tabs-content', 'children'),
    #     Input('name-submit', 'n_clicks'),
    #     Input('name-input', 'value')
    # )
    # def update_name(n_clicks, name_input):
    #     nonlocal Name_to_look_for, df  # Use nonlocal to modify the outer scope variables
        
    #     if n_clicks > 0 and name_input:
    #         # Assuming od.open_data_name() works as intended
    #         List_col = ["nconst", "primaryName", "birthYear", "deathYear"]
    #         List_filter = [None, name_input, None, None]  # Filter by primaryName
            
    #         name_info = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
            
    #         if name_info['nconst'].count() > 1:
    #             Name_to_look_for = None  # Reset if more than one name found
    #             df = None  # Reset the DataFrame
    #             return "The DataFrame has more than one row. Please refine your search.", layout_for_tab1(df, dark_dropdown_style, uniform_style, Name_to_look_for)
    #         elif name_info['nconst'].count() == 0:
    #             Name_to_look_for = None  # Reset if no names found
    #             df = None  # Reset the DataFrame
    #             return "No results found.", layout_for_tab1(df, dark_dropdown_style, uniform_style, Name_to_look_for)
    #         else:
    #             Name_to_look_for = str(name_info['nconst'].iloc[0])
    #             df = name_info  # Set the DataFrame to the filtered result
    #             return f"Name found: {Name_to_look_for}", layout_for_tab1(df, dark_dropdown_style, uniform_style, Name_to_look_for)

    #     return "Enter a name and click Submit.", layout_for_tab1(df, dark_dropdown_style, uniform_style, Name_to_look_for)




    
    app.run_server(debug=True, port=8051)
    
    # Specify the URL you want to open
    url = "http://127.0.0.1:8051/"
    
    # Open the URL in the default web browser
    webbrowser.open(url)
    
    
    return 0, df


# def layout_for_tab1(dropdowns_with_labels, data_table):
#     return html.Div([
#         html.Div([
#             html.P(f'This interface is dedicated to the research on specific artist.'),
#         ]),

#         # Input field for primaryName
#         html.Div([
#             dcc.Input(id='name-input', type='text', placeholder='Enter primary name (e.g., William K.L. Dickson*)'),
#             html.Button('Submit', id='name-submit', n_clicks=0),
#             html.Div(id='name-output'),
#         ]),

#         html.Div(style={'display': 'flex', 'margin-top': '10px', 'flex-wrap': 'wrap'}, children=[
#             html.Div(dropdowns_with_labels, style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'})
#         ]),
#         html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
#             html.Div(data_table, style={'width': '100%'})  # Adjusted to take full width
#         ])
#     ], style={'padding': '20px'})


# def layout_for_tab1(df, dark_style, uniform_style, name_found):
#     if df is not None and name_found is not None:  # Only display the table if a valid name is found
        
#         # Create the table with the appropriate dropdowns for each column
#         dropdowns_with_labels, data_table = tds.dropdown_table(df, dark_dropdown_style, uniform_style)

#         return html.Div([
#             html.H4(f"Results for: {name_found}"),
#             # Assuming a Dash DataTable is being used here
#             dash.dash_table.DataTable(
#                 data=df.to_dict('records'),
#                 columns=[{"name": col, "id": col} for col in df.columns],
#                 style_table={'overflowX': 'auto'},
#                 style_cell={'textAlign': 'left'},
#             )
#         ])
#     else:
#         return html.Div([
#             html.H4("Please enter a name to search."),
#         ])


def layout_for_tab2(app, df, dark_dropdown_style, uniform_style, Large_file_memory, dropdowns_with_labels_for_fig):

    # Create the figure with the appropriate dropdowns for each axis
    dropdowns_with_labels_for_fig = fds.dropdown_figure(app, df, dark_dropdown_style, uniform_style, Large_file_memory)


    return html.Div([
        html.H1("IMDB DataFrame Interface", style={"color": "#FFD700"}, className="text-light"),
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div(dropdowns_with_labels_for_fig, style={'display': 'flex', 'margin-left': '50px', 'justify-content': 'flex-start', 'gap': '5px'})
        ]),
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div([dcc.Graph(id='graph-output', style={'width': '100%', 'height': '600px'})], style={'margin-left': '20px', 'width': '50%'})
        ])
    ], style={'padding': '20px'})


def layout_for_tab3(df):
    return html.Div([
        html.H1("IMDB DataFrame Interface", style={"color": "#FFD700"}, className="text-light"),
        html.Div([
                html.H3('Summary Statistics'),
                html.Div([
                    html.P(f'Total Rows: {len(df)}'),
                    html.P(f'Number of Unique Genres: {df["genres"].nunique()}'),
                    # Add more statistics as needed
                ])
            ])
    ], style={'padding': '20px'})





def filter_data_by_value(df, x_column, y_column, filter_value):

    """
    Filters the DataFrame based on the provided x and y columns, and the filter value.
    
    Parameters:
    - df: DataFrame to filter.
    - x_column: Selected x column.
    - y_column: Selected y column.
    - filter_value: The value or range to filter on.
    
    Returns:
    - df: Filtered DataFrame.
    - error_msg: Any error message that occurred during filtering (None if no error).
    """    
    
    error_msg = None  # Initialize error message

    if x_column is not None and y_column is not None:
        # if y_column in list_col_num:
        dtype = df[y_column].dtype
        if dtype != "float64":
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



def filter_data_by_value_array(df, y_column, filter_value):

    """
    Filters the DataFrame based on the provided x and y columns, and the filter value.
    
    Parameters:
    - df: DataFrame to filter.
    - y_column: Selected y column.
    - filter_value: The value or range to filter on.
    
    Returns:
    - df: Filtered DataFrame.
    - error_msg: Any error message that occurred during filtering (None if no error).
    """    
    
    error_msg = None  # Initialize error message
    print(y_column)
    if y_column is not None:
        # if y_column in list_col_num:
        dtype = df[y_column].dtype
        if dtype == "float64":
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



