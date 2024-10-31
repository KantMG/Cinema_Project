#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 19:12:21 2024

@author: quentin
"""

"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Main.

#=============================================================================
   #=============================================================================
   #============================================================================="""


import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import dask.dataframe as dd
import plotly.graph_objects as go
import numpy as np
from termcolor import colored

import time
import webbrowser
import shutil
import os

import Function_dataframe as fd
import Function_errors as fe
import web_interface_style as wis
import table_dropdown_style as tds
import figure_creation as fc
import figure_dropdown_style as fds
import data_plot_preparation as dpp
import open_dataframe as od
import Dash_callback_ids as dci


"""#=============================================================================
   #=============================================================================
   #============================================================================="""

# Source for data set : 
source_data = 'https://developer.imdb.com/non-commercial-datasets/'

# Save the project on github with: !bash ./save_project_on_git.sh
GitHub_adress= 'https://github.com/KantMG/Cinema_Project'

# Save the project on the laptop:
Project_path='/home/quentin/Documents/Work/Data_analytics/Datasets/Cinema_Project/'


start_time = time.time()

# Define the path to the folder you want to remove
folder_path = '/home/quentin/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/temp_df1.parquet'
# Check if the folder exists
if os.path.exists(folder_path):
    # Remove the folder and all its contents
    shutil.rmtree(folder_path)
    print(f"Successfully removed the folder: {folder_path}")
else:
    print(f"The folder {folder_path} does not exist.")


Large_file_memory = True
Get_file_sys_mem = False
desired_number_of_partitions = 10
Test_data = True
if Test_data == True:
    Project_path=Project_path+'Test_data/'


df_col_numeric = ["startYear", "runtimeMinutes", "averageRating", "numVotes"]
df_col_string = ["genres", "directors", "writers", "nconst", "category", "characters", "title"]


List_col_tab2 = ["startYear", "runtimeMinutes", "genres", "isAdult", "averageRating", "numVotes"]
List_dtype_tab2 = [float, float, str, float, float, float]
List_filter_tab2 = [None for i in List_col_tab2]
df_col_numeric_tab2 = ["startYear", "runtimeMinutes", "averageRating", "numVotes"]
df_col_string_tab2 = ["genres"]


List_dim = ["1D", "2D", "3D"]
List_graph_type = ["Histogram", "Curve", "Scatter", "Colormesh", "Pie"]


# Initialize the Dash app with suppress_callback_exceptions set to True
app, dark_dropdown_style, uniform_style = wis.web_interface_style()

# Callback to manage tab content
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'),
    State('stored-df1', 'data')
)
def render_content(tab, stored_df1):
    if tab == 'tab-1':
        # Placeholder for Tab 3 content
        return html.Div([
            html.H1("THE SEVENTH ART, A STORY OF INFLUENCE", style={"color": "#FFD700"}, className="text-light"),
            tab1_content()
        ])
    elif tab == 'tab-2':
        # Placeholder for Tab 2 content
        return html.Div([
            html.H1("Graphic interface dedicated to the dataframe related to the overall IMDB database.", style={"color": "#FFD700"}, className="text-light"),
            tab2_content()
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Div([
                html.H1("Research on an artist or a movie.", style={"color": "#FFD700"}, className="text-light"),
            ]),
            dcc.Input(id='input-value', type='text', placeholder='Enter a value...', style={**dark_dropdown_style, **uniform_style}),
            html.Div(id='dynamic-content')
        ])


"""
# =============================================================================
# =============================================================================
# =============================================================================
# Tab-1
# =============================================================================
# =============================================================================
# =============================================================================
"""

def tab1_content():
    print()
    print("Time computation=", time.time()-start_time)
    print("=====================  Tab1_content  =========================")
    # Source for data set : 
    source_data = 'https://developer.imdb.com/non-commercial-datasets/'
    
    # Save the project on github with: !bash ./save_project_on_git.sh
    GitHub_adress= 'https://github.com/KantMG/Cinema_Project'
    
    Text1 = f"THIS PROJECT ENLIGHT THE EVOLUTION OVER THE YEARS OF THE MOVIE AND SERIE MAKING."
    Text2 = f"THE ADAPTATION OF THE WAY OF PRODUCTION AS WELL AS OUR WAY OF CONSOMATION ARE ANALYSED."
    Text3 = f"HOW MUCH THE COUNTRIES ARE INVESTING IN THE FILMS PRODUCTION AND WHICH IS THE LEVEL OF INFLUENCE OF A COUNTRY OVER THE OTHERS."
    
    Text4 = f"The IMDb Non-Commercial Datasets has been used to perform this study, the open source can be find here: "+source_data
    Text5 = f"It corresponds to a multiple variety of tab-separated-values (TSV) formatted files in the UTF-8 character set. "
    Text6 = f"The "

    # Print all ids
    component_ids = dci.get_component_ids(app.layout)
    print("Component IDs:", component_ids)
    print("==================== End Tab1_content ========================")    
    return html.Div([
        html.Div([
            html.P(Text1),
            html.P(Text2),
            html.P(Text3),
        ]),
        html.Div([
            html.P(Text4),
            html.P(Text5),
            html.P(Text6),
        ]),        
        ], style={'padding': '20px'})


"""
# =============================================================================
# =============================================================================
# =============================================================================
# Tab-2
# =============================================================================
# =============================================================================
# =============================================================================
"""

def tab2_content():
    print()
    print("Time computation=", time.time()-start_time)
    print("=====================  Tab2_content  =========================")
    # Display dropdowns without loading data initially
    df1_placeholder = fd.df_empty(List_col_tab2, dtypes=List_dtype_tab2)    
    dropdowns_with_labels_for_fig_tab2 = fds.dropdown_figure(df1_placeholder, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style, Large_file_memory)
    dropdowns_with_labels_for_fig_filter_tab2 = fds.dropdown_checkboxes_figure_filter(df1_placeholder, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style)

    # Print all ids
    component_ids = dci.get_component_ids(app.layout)
    print("Component IDs:", component_ids)
    print("==================== End Tab2_content ========================")
    return html.Div([
        html.Div([
            fds.figure_position_dash('graph-output-tab-2',
                                     dropdowns_with_labels_for_fig_tab2,
                                     dropdowns_with_labels_for_fig_filter_tab2)
            
        ], style={'padding': '20px'})
    ], style={'padding': '20px'})
    

# =============================================================================
# Callback for df1 in tab-2
# =============================================================================

@app.callback(
    Output('stored-df1', 'data'),
    [Input('tabs', 'value')] +  # Use the tab selection for context
    [Input('x-dropdown-tab-2', 'value'),  # x-axis dropdown
     Input('y-dropdown-tab-2', 'value'),  # y-axis dropdown
     Input('z-dropdown-tab-2', 'value')] +  # z-axis dropdown
    [Input(f'checkbox-{col}-tab-2', 'value') for col in List_col_tab2] +  # Each checkbox's value
    [Input(f'{col}-fig-dropdown-tab-2', 'value') for col in List_col_tab2]  # Rest of dropdowns
)
def update_stored_df1(selected_tab, x_dropdown_value, y_dropdown_value, z_dropdown_value, *args):
    print()
    print(colored("------------ callback update_stored_df1 ------------", "red"))
    
    ctx = dash.callback_context
    # Print out which component triggered the callback for debugging
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Triggered component:", triggered_id)
    print()
    
    # Collect values from checkboxes
    checkbox_values = list(args[0:len(List_col_tab2)])  # Get the values for checkboxes
    
    # Collect values from the filter  input
    filter_values = list(args[len(List_col_tab2):-1])  # Get the values for checkboxes   
            
    # Print debug information
    print("Active Tab=", selected_tab)
    print("Time computation=", time.time()-start_time)
    print("X Dropdown Value:", x_dropdown_value)
    print("Y Dropdown Value:", y_dropdown_value)
    print("Z Dropdown Value:", z_dropdown_value)
    print("Checkbox Values:", checkbox_values)
    print("Filter Value:", filter_values)

    if selected_tab == 'tab-2':
        if x_dropdown_value is None:
            print("X Dropdown Value is None, returning no update.")
            return dash.no_update  
        
        selected_columns = []
        selected_filter = []
        
        # Add x_dropdown_value if it's not already in checkbox_values
        if x_dropdown_value not in checkbox_values and x_dropdown_value not in selected_columns:
            selected_columns.append(x_dropdown_value)
            # Append None for the filter associated with x_dropdown_value
            selected_filter.append(None)
        
        # Add y_dropdown_value if it's not already in checkbox_values and not already added
        if y_dropdown_value not in checkbox_values and y_dropdown_value not in selected_columns:
            selected_columns.append(y_dropdown_value)
            # Append None for the filter associated with y_dropdown_value
            selected_filter.append(None)

        # Add z_dropdown_value if it's not already in checkbox_values and not already added
        if z_dropdown_value not in checkbox_values and z_dropdown_value not in selected_columns:
            selected_columns.append(z_dropdown_value)
            # Append None for the filter associated with y_dropdown_value
            selected_filter.append(None)
        
        # Add values from checkbox_values that are not empty or duplicates
        for index, value in enumerate(checkbox_values):
            if value and value[0] not in selected_columns:  # Take the first value assuming it's a list with one item
                selected_columns.append(value[0])
                selected_filter.append(filter_values[index])
            
            if value and value[0] == x_dropdown_value :
                selected_filter[0] = filter_values[index]
            if value and value[0] == y_dropdown_value :
                selected_filter[1] = filter_values[index]
            if value and value[0] == z_dropdown_value :
                selected_filter[0] = filter_values[index]
                
        print("Selected Columns:", selected_columns)  # Debugging output for selected columns
        print("Selected Filter:", selected_filter)
        
        # Call your open_dataframe function to get the data
        df1 = od.open_dataframe(selected_columns, selected_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        # Check if the folder exists
        if os.path.exists(folder_path):
            # Remove the folder and all its contents
            shutil.rmtree(folder_path)
            print(f"Successfully removed the folder: {folder_path}")
        else:
            print(f"The folder does not exist: {folder_path}")
        df1.to_parquet('temp_df1.parquet')  # Store the DataFrame
        return "Data loaded and saved."

    return dash.no_update


# =============================================================================
# Callback for graph in tab-2
# =============================================================================

@app.callback(
    Output('y-dropdown-tab-2', 'options'),
    [Input('x-dropdown-tab-2', 'value'),
    Input('tabs', 'value')]
)
def update_y_dropdown_tab2(selected_x, selected_tab):
    print()
    print(colored("------------ callback update_y_dropdown_tab2 ------------", "red"))
    print("Active Tab=", selected_tab)
    print("Time computation=", time.time()-start_time)
    ctx = dash.callback_context
    # Print out which component triggered the callback for debugging
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Triggered component:", triggered_id)
    print()
    if selected_tab == 'tab-2':
        if selected_x is None:
            print("X Dropdown Value is None, returning an empty list [].")
            return []
        print(f"Selected X: {selected_x}")  # Additional debugging
        exclude_cols=[]
        return update_y_dropdown_utility(selected_x, List_col_tab2, exclude_cols)
    return dash.no_update

@app.callback(
    Output('z-dropdown-tab-2', 'options'),
    [Input('x-dropdown-tab-2', 'value'),
     Input('y-dropdown-tab-2', 'value'),
    Input('tabs', 'value')]
)
def update_z_dropdown_tab2(selected_x, selected_y, selected_tab):
    print()
    print(colored("------------ callback update_z_dropdown_tab2 ------------", "red"))
    print("Active Tab=", selected_tab)
    print("Time computation=", time.time()-start_time)
    ctx = dash.callback_context
    # Print out which component triggered the callback for debugging
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Triggered component:", triggered_id)
    print()
    if selected_tab == 'tab-2':
        if selected_y is None:
            print("Y Dropdown Value is None, returning an empty list [].")
            return []
        print(f"Selected y: {selected_y}")  # Additional debugging
        exclude_cols=[]
        return update_z_dropdown_utility(selected_x, selected_y, List_col_tab2, exclude_cols)
    return dash.no_update

@app.callback(
    Output('Func-dropdown-tab-2', 'options'),
    Input('y-dropdown-tab-2', 'value'),
    Input('tabs', 'value')  # Include tab value to conditionally trigger callback
)
def update_func_dropdown_tab2(selected_y, selected_tab):
    print()
    print(colored("------------ callback update_func_dropdown_tab2 ------------", "red"))
    print("Active Tab=", selected_tab)
    print("Time computation=", time.time()-start_time)
    if selected_tab == 'tab-2':
        if selected_y is None:
            print("Y Dropdown Value is None, returning an empty list [].")
            return []  # Return an empty options list if the DF is not ready
        # Proceed to get options based on selected_x and stored_df1...
        print(f"Selected Y: {selected_y}")  # Additional debugging
        return update_func_dropdown_utility(selected_y, df_col_numeric_tab2)
    return dash.no_update

@app.callback(
    Output('Dim-dropdown-tab-2', 'options'),
    Input('y-dropdown-tab-2', 'value'),
    Input('tabs', 'value')  # Include tab value to conditionally trigger callback
)
def update_dim_dropdown_tab2(selected_y, selected_tab):
    print()
    print(colored("-------- callback update_dim_dropdown_tab2 --------", "red"))
    print("Active Tab=", selected_tab)
    print("Time computation=", time.time()-start_time)
    if selected_tab == 'tab-2':
        if selected_y is None:
            return [{'label': "1D", 'value': "1D"}, {'label': "2D", 'value': "2D"}]  # Return an empty options list if the DF is not ready
        return [{'label': col, 'value': col} for col in List_dim]
    return dash.no_update

@app.callback(
    [Output('Graph-dropdown-tab-2', 'options'),
    Output('Graph-dropdown-tab-2', 'value')],
    Input('Dim-dropdown-tab-2', 'value'),
    Input('tabs', 'value')  # Include tab value to conditionally trigger callback
)
def update_graph_dropdown_tab2(selected_dim, selected_tab):
    print()
    print(colored("------------ callback update_dim_dropdown_tab2 ------------", "red"))
    print("Active Tab=", selected_tab)
    print("Time computation=", time.time()-start_time)
    if selected_tab == 'tab-2':
        if selected_dim == "1D":
            return [{'label': col, 'value': col} for col in List_graph_type if col not in ("Colormesh", "Pie")], 'Histogram'  # Return an empty options list if the DF is not ready
        if selected_dim == "2D":
            return [{'label': col, 'value': col} for col in List_graph_type if col not in ("Histogram", "Curve", "Scatter")], None
        if selected_dim == "3D":
            return [{'label': col, 'value': col} for col in List_graph_type], None
    return dash.no_update, dash.no_update


@app.callback(
    [Output(f'{col}-fig-dropdown-tab-2', 'options') for col in df_col_string_tab2],  # Rest of dropdowns
    [Input(f'checkbox-{col}-tab-2', 'value') for col in df_col_string_tab2] +
    [Input('tabs', 'value')],
    Input('stored-df1', 'data')
)
def update_filter_dropdown_tab2(*args):
    print()
    print(colored("------------ callback update_filter_dropdown_tab2 ------------", "red"))
    selected_boxes = list(args[:-2])
    selected_tab = args[-2]
    stored_df1 = args[-1]
    print("Active Tab=", selected_tab)
    print("Time computation=", time.time()-start_time)
    ctx = dash.callback_context
    # Print out which component triggered the callback for debugging
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Triggered component:", triggered_id)
    print()
    if selected_tab == 'tab-2':
        if all(not sublist for sublist in selected_boxes):
            print("No filters selected.")
            return [[] for col in df_col_string_tab2] # Return an empty options list if the DF is not ready
        print(f"Selected filter: {selected_boxes}")  # Additional debugging
        stored_df1 = dd.read_parquet('temp_df1.parquet')
        return update_filter_dropdown_utility(selected_boxes, stored_df1)
    return [[] for col in df_col_string_tab2]  # If not in the right tab


@app.callback(
    Output('graph-output-tab-2', 'figure'),
    [Input('tabs', 'value'),
     Input('x-dropdown-tab-2', 'value'),
     Input('y-dropdown-tab-2', 'value'),
     Input('z-dropdown-tab-2', 'value'),
     Input('Func-dropdown-tab-2', 'value'),
     Input('Graph-dropdown-tab-2', 'value'),
     Input('Dim-dropdown-tab-2', 'value')],  # Rest of dropdowns
    Input('stored-df1', 'data')
)
def update_graph_tab2(selected_tab, x_dropdown_value, y_dropdown_value, z_dropdown_value, func_dropdown_value, graph_dropdown_value, dim_dropdown_value, stored_df1):
    print()
    print(colored("------------ callback update_graph_tab2 ------------", "red"))
    # Load the Dask DataFrame from Parquet
    print("Active Tab=", selected_tab)
    print("Time computation=", time.time()-start_time)

    # Check if we're in the correct tab and there is data available
    if selected_tab == 'tab-2':
        print(graph_dropdown_value)
        if graph_dropdown_value is None:
            return dash.no_update
        if stored_df1 is None:
            print("Stored DF1 is not ready yet.")
        else:
            stored_df1 = dd.read_parquet('temp_df1.parquet')

    print("x_dropdown_value, y_dropdown_value, z_dropdown_value, func_dropdown_value, graph_dropdown_value, dim_dropdown_value=",x_dropdown_value, y_dropdown_value, z_dropdown_value, func_dropdown_value, graph_dropdown_value, dim_dropdown_value)
    print("stored_df1=", stored_df1)
    return update_graph_utility(x_dropdown_value, y_dropdown_value, z_dropdown_value, func_dropdown_value, graph_dropdown_value, dim_dropdown_value, stored_df1, Large_file_memory)
  
    
"""
# =============================================================================
# =============================================================================
# =============================================================================
# Tab-3
# =============================================================================
# =============================================================================
# =============================================================================
"""

# Callback to update UI based on input value in Tab 3
@app.callback(
    [Output('dynamic-content', 'children'), Output('stored-df2', 'data')],
    Input('input-value', 'value')
)
def update_ui(input_value):
    if not input_value:  # Return nothing if input is empty or None
        return '', None
    print()
    print(colored("------------ callback update_ui ------------", "red"))

    List_col = ["nconst", "primaryName", "birthYear", "deathYear"]

    List_filter = [None, None, None, None]

    df_name = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        
    # Check if the input value exists in the 'nconst' column of df_name
    if input_value in df_name['primaryName'].values:

        nconst_value = df_name[df_name['primaryName'] == input_value]['nconst'].iloc[0]
        birthYear_value = int(df_name[df_name['primaryName'] == input_value]['birthYear'].iloc[0])
        deathYear_value = int(df_name[df_name['primaryName'] == input_value]['deathYear'].iloc[0])
        
        # Display the found nconst value (for debugging purposes)
        print(f"Matched nconst: {nconst_value}")
                        
        List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters", "title", "isOriginalTitle"]
        
        List_filter = [None, None, None, None, None, None, None, None, nconst_value, None, None, None, True]
        
        df2 = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        exclude_col = ["tconst", "isAdult", "nconst", "isOriginalTitle"]
        df2 = df2.drop(columns=exclude_col)
        
        df2 = df2.compute()
        
        if len(df2.index) == 0: 
            return html.Div([
                html.Div([
                    html.P(f'The artist '+input_value+' doesnt have referenced movies.'),
                ])
                ], style={'padding': '20px'}), df2.to_dict('records')        
        else:
                        
            # Split the strings into individual elements and flatten the list
            all_elements = df2['category'].str.split(',').explode().str.strip()
            primaryProfession = all_elements.value_counts()
            primaryProfession = primaryProfession[primaryProfession > 1].index.tolist()

            # Create the table with the appropriate dropdowns for each column
            dropdowns_with_labels, data_table_df2 = tds.dropdown_table(df2, 'table-df2', dark_dropdown_style, uniform_style, True)
            
            exclude_col = ["title", "characters"]
            df2_filter = df2.drop(columns=exclude_col)            
            dropdowns_with_labels_for_fig = fds.dropdown_figure(df2_filter, 'graph-df2', 'tab-3', dark_dropdown_style, uniform_style, Large_file_memory)
            dropdowns_with_labels_for_fig_filter = fds.dropdown_figure_filter(df2_filter, 'graph-df2', 'tab-3', dark_dropdown_style, uniform_style)
            
            return html.Div([
                html.P(f'The artist '+input_value+' is born in '+str(birthYear_value)+' and died in '+str(deathYear_value)+' during its career as '+', '.join(primaryProfession)+' he participated to the creation of the following productions.'),
                html.Div(style={'display': 'flex', 'margin-top': '10px', 'flex-wrap': 'wrap'}, children=[
                    html.Div(dropdowns_with_labels, style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'})
                ]),
                html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
                    html.Div(data_table_df2, style={'width': '100%'})  # Adjusted to take full width
                ]),

                html.Div([
                    html.H1("Graphic interface dedicated to the dataframe related to the artist "+input_value+".", style={"color": "#FFD700"}, className="text-light"),
                    
                    fds.figure_position_dash('graph-output-tab-3', 
                                             dropdowns_with_labels_for_fig, 
                                             dropdowns_with_labels_for_fig_filter)
                    
                ], style={'padding': '20px'})
                                
            ], style={'padding': '20px'}), df2.to_dict('records')
        
    
    # If the input does not correspond to any primaryName, filter df_name
    filtered_df = df_name[df_name['primaryName'].str.contains(input_value, case=False, na=False)]
    dropdowns_with_labels_df_name, data_table_df_name = tds.dropdown_table(filtered_df, 'table-df_name', dark_dropdown_style, uniform_style, False)
    return data_table_df_name, None



# =============================================================================
# Callback for table-df2 in tab-3
# =============================================================================

# Create a list of Input objects for each dropdown
List_col_tab3 = ["startYear", "runtimeMinutes", "genres", "directors", "writers", "averageRating", "numVotes", "category", "characters", "title"]
dropdown_inputs_tab3 = [Input(f'{col}-dropdown', 'value') for col in List_col_tab3]

@app.callback(
    Output('table-df2', 'data'),
    dropdown_inputs_tab3,
    Input('tabs', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df2', 'data')  # Ensure this is included as State
)
def update_stored_df2(*args):
    print()
    print(colored("------------ callback update_stored_df2 ------------", "red")) 
    selected_tab = args[-2]
    stored_df2 = args[-1]         # The last argument is stored_df2
    selected_values = {col: args[i] for i, col in enumerate(List_col_tab3)}
    
    if selected_tab == 'tab-3':  # Only execute if in the Data Visualization tab
        if stored_df2 is None:  # Check if stored_df2 is None or empty
            return []
        # Convert the stored data back to a DataFrame
        df2 = pd.DataFrame(stored_df2)
        # Create a copy of the DataFrame to avoid modifying the original stored data
        filtered_data_table = df2.copy()
        print("Update table")
        print(filtered_data_table)
        filtered_data_table = od.apply_filter(filtered_data_table, selected_values)
        
        return filtered_data_table.to_dict('records')
    return []  # Return empty if not in the right tab


# =============================================================================
# Callback for graph-df2 in tab-3
# =============================================================================

tab = 'tab-3'
# Create a list of Input objects for each dropdown
List_col_fig_tab3 = ["startYear", "runtimeMinutes", "genres", "directors", "writers", "averageRating", "numVotes", "category"]
dropdown_inputs_fig_tab3 = [Input(f'{col}-fig-dropdown-'+tab, 'value') for col in List_col_fig_tab3]


@app.callback(
    Output('y-dropdown-tab-3', 'options'),
    Input('x-dropdown-tab-3', 'value'),
    Input('tabs', 'value')  # Include tab value to conditionally trigger callback
)
def update_y_dropdown_tab3(selected_x, selected_tab):
    print()
    print(colored("------------ callback update_y_dropdown_tab3 ------------", "red")) 
    if selected_tab == 'tab-3':  # Only execute if in the correct tab
        exclude_cols = ["title", "characters"]
        return update_y_dropdown_utility(selected_x, List_col_fig_tab3, exclude_cols)
    return []  # Return empty if not in the right tab

@app.callback(
    Output('Func-dropdown-tab-3', 'options'),
    Input('y-dropdown-tab-3', 'value'),
    Input('tabs', 'value')  # Include tab value to conditionally trigger callback
)
def update_func_dropdown_tab3(selected_y, selected_tab):
    print()
    print(colored("------------ callback update_func_dropdown_tab3 ------------", "red")) 
    if selected_tab == 'tab-3':
        return update_func_dropdown_utility(selected_y, df_col_numeric)
    return []

@app.callback(
    Output('graph-output-tab-3', 'figure'),
    [Input('tabs', 'value'),
     Input('x-dropdown-tab-3', 'value'),
     Input('y-dropdown-tab-3', 'value'),
     Input('z-dropdown-tab-3', 'value'),
     Input('Func-dropdown-tab-3', 'value'),
     Input('Graph-dropdown-tab-3', 'value'),
     Input('Dim-dropdown-tab-3', 'value')] +  # Rest of dropdowns
    dropdown_inputs_fig_tab3,
    State('stored-df2', 'data')
)
def update_graph_tab2(selected_tab, x_dropdown_value, y_dropdown_value, z_dropdown_value, func_dropdown_value, graph_dropdown_value, dim_dropdown_value, *args):
    print()
    print(colored("------------ callback update_graph_tab3 ------------", "red")) 
    # selected_values = {col: args[i+5] for i, col in enumerate(List_col_fig_tab3)}
    stored_df2 = args[-1]
    
    # Convert the stored data back to a DataFrame
    df2 = pd.DataFrame(stored_df2)
    # Create a copy of the DataFrame to avoid modifying the original stored data
    filtered_data_table = df2.copy()
        
    print("Active Tab:", selected_tab)
    print(filtered_data_table)
    if selected_tab == 'tab-3' and stored_df2 is not None:  # Only execute if in the correct tab
            print(x_dropdown_value, y_dropdown_value, z_dropdown_value, func_dropdown_value, graph_dropdown_value, dim_dropdown_value)
            return update_graph_utility(x_dropdown_value, y_dropdown_value, z_dropdown_value, func_dropdown_value, graph_dropdown_value, dim_dropdown_value, filtered_data_table, False)
    return go.Figure()  # Return a blank figure if not in the right tab



# =============================================================================
# Utility Function for Graphs
# =============================================================================

def update_y_dropdown_utility(selected_x, List_cols, exclude_cols):
    """
    Utility function to generate dropdown options for the y-axis based on the selected x-axis column and dataframe.
    """
    return [{'label': col, 'value': col} for col in List_cols if col != selected_x]

def update_z_dropdown_utility(selected_x, selected_y, List_cols, exclude_cols):
    """
    Utility function to generate dropdown options for the z-axis based on the selected x-axis and y-axis column and dataframe.
    """
    return [{'label': col, 'value': col} for col in List_cols if col not in (selected_x, selected_y)]
 
def update_func_dropdown_utility(selected_y, df_col_numeric):
    """
    Utility function to generate dropdown options for the function based on the selected y-axis column.
    """
    # Get the list of y functions
    function_on_y = ["Avg"]
    
    if selected_y not in df_col_numeric:  # Check if y column is not numeric
        return []
    else:
        return [{'label': col, 'value': col} for col in function_on_y]

def update_filter_dropdown_utility(selected_boxes, df):
    """
    Utility function to generate dropdown options for the function based on the selected y-axis column.
    """
    
    dropdowns = []    
    
    for col in selected_boxes:
        if col == []:
            dropdowns.append([])
        else:
            col = col[0]
            dopdown_values = []
            # Collect all unique values, splitting them by commas and ensuring uniqueness
            all_roles = set()
            for value in df[col].dropna().unique():
                # Split the value by comma and strip any extra spaces
                roles = [role.strip() for role in str(value).split(',')]
                all_roles.update(roles)
            
            # Convert to a sorted list
            unique_values = sorted(all_roles)
                
            dropdowns.append(unique_values)
        
    return dropdowns 

def update_graph_utility(x_column, y_column, z_column, func_column, graph_type, dim_type, stored_df, large_file_memory):
    """
    Utility function to generate a graph based on the provided parameters.
    """
    if stored_df is None:  # Check if stored_df is None or empty
        filtered_data_graph = None
    else:
        # Convert the stored data back to a DataFrame
        # print(stored_df)
        # df = pd.DataFrame(stored_df)
        df = stored_df
        # Create a copy of the DataFrame to avoid modifying the original stored data
        filtered_data_graph = df.copy()
        # print(filtered_data_graph)
        # print(selected_values)
        # Apply filters on the dataframe
        # filtered_data_graph = od.apply_filter(filtered_data_graph, selected_values)
        # Create the figure based on filtered data
    fig = fc.create_figure(filtered_data_graph, x_column, y_column, z_column, func_column, graph_type, dim_type, large_file_memory)
    return fig

# =============================================================================
# End Utility Function for Graphs
# =============================================================================



if __name__ == '__main__':
    app.run_server(debug=True, port=8054)

    # Specify the URL you want to open
    url = "http://127.0.0.1:8054/"
    
    # Open the URL in the default web browser
    # webbrowser.open(url)