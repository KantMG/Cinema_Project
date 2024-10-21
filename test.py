#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 19:12:21 2024

@author: quentin
"""



import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go

import webbrowser

import Function_dataframe as fd
import Function_errors as fe
import Function_visualisation as fv
import web_interface_style as wis
import table_dropdown_style as tds
import figure_dropdown_style as fds
import data_plot_preparation as dpp
import open_dataframe as od


Project_path='/home/quentin/Documents/Work/Data_analytics/Datasets/Cinema_Project/'
Large_file_memory = True
Get_file_sys_mem = False
desired_number_of_partitions = 10
Test_data = True

if Test_data == True:
    Project_path=Project_path+'Test_data/'

List_col = ["nconst", "primaryName", "birthYear", "deathYear"]

List_filter = [None, None, None, None]

df_name = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)


# Initialize the Dash app with suppress_callback_exceptions set to True
app, dark_dropdown_style, uniform_style = wis.web_interface_style()


# app.layout = html.Div([
#     # Tabs Component
#     dcc.Tabs(id='tabs', value='tab-3', children=[
#         dcc.Tab(label='🏠 Home', value='tab-3', className='tab-3d', selected_className='tab-3d-selected'),
#         dcc.Tab(label='📈 Analytics', value='tab-2', className='tab-3d', selected_className='tab-3d-selected'),
#         dcc.Tab(label='Tab 3', value='tab-3', className='tab-3d', selected_className='tab-3d-selected'),
#     ]),

#     # Hidden store to hold df2 data
#     dcc.Store(id='stored-df2', data=None),
    
#     # Content Div for Tabs
#     html.Div(id='tabs-content')
# ])


app.layout = html.Div([
    # Tabs Component
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(id='tabs-1', label='🏠 Home', value='tab-1', 
                 style={
                     'backgroundColor': '#000000',  # Dark black background
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                     'position': 'relative'  # Relative position for pseudo-element
                 },
                 selected_style={
                     'backgroundColor': '#222222',  # Slightly lighter for selected tab
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                 }),
        dcc.Tab(id='tabs-2', label='📈 Analytics', value='tab-2', 
                 style={
                     'backgroundColor': '#000000',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                     'position': 'relative'
                 },
                 selected_style={
                     'backgroundColor': '#222222',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                 }),
        dcc.Tab(id='tabs-3', label='🎥 Movies & Artists', value='tab-3', 
                 style={
                     'backgroundColor': '#000000',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                     'position': 'relative'
                 },
                 selected_style={
                     'backgroundColor': '#222222',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                 }),
    ]),
    
    # Hidden store to hold df1 data
    dcc.Store(id='stored-df1', data=None),
    
    # Hidden store to hold df2 data
    dcc.Store(id='stored-df2', data=None),
        
    # Content Div for Tabs
    html.Div(id='tabs-content')
])

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
            html.H1("IMDB database analysis.", style={"color": "#FFD700"}, className="text-light"),
            tab1_content()
        ])
    elif tab == 'tab-2':
        # Placeholder for Tab 2 content
        return html.Div([
            html.H1("Graphic interface dedicated to the dataframe related to the overall IMDB database.", style={"color": "#FFD700"}, className="text-light"),
            tab2_content(stored_df1)
        ])
    elif tab == 'tab-3':
        # This is the content for Tab 1 - the existing layout we created
        return html.Div([
            html.Div([
                html.H1("Research on an artist or a movie.", style={"color": "#FFD700"}, className="text-light"),
            ]),
            dcc.Input(id='input-value', type='text', placeholder='Enter a value...', style={**dark_dropdown_style, **uniform_style}),
            html.Div(id='dynamic-content')
        ])



# =============================================================================
# =============================================================================
# =============================================================================
# Tab-1
# =============================================================================
# =============================================================================
# =============================================================================

def tab1_content():
    
    Text = f"The IMDB is large ...."
    
    
    return html.Div([
        html.Div([
            html.P(Text),
        ])
        ], style={'padding': '20px'})


# =============================================================================
# =============================================================================
# =============================================================================
# Tab-2
# =============================================================================
# =============================================================================
# =============================================================================

List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters", "title", "isOriginalTitle"]
List_filter = [None, None, None, None, None, None, None, None, None, None, None, None, True]


def tab2_content(stored_df1):

    # Display dropdowns without loading data initially
    df1_placeholder = pd.DataFrame(columns=List_col)           
    dropdowns_with_labels_for_fig_tab2 = fds.dropdown_figure(df1_placeholder, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style, Large_file_memory)
    dropdowns_with_labels_for_fig_filter_tab2 = fds.dropdown_figure_filter(df1_placeholder, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style)
    
    return html.Div([

        html.Div([
            
            fds.figure_position_dash('graph-output-tab-2', dropdowns_with_labels_for_fig_tab2, dropdowns_with_labels_for_fig_filter_tab2)
            
        ], style={'padding': '20px'})
                        
    ], style={'padding': '20px'})


tab = 'tab-2'
# Create a list of Input objects for each dropdown
List_col_fig = ["startYear", "runtimeMinutes", "genres", "directors", "writers", "averageRating", "numVotes", "category"]
dropdown_inputs_fig = [Input(f'{col}-fig-dropdown-'+tab, 'value') for col in List_col_fig]

# =============================================================================
# Callback for df1 in tab-2
# =============================================================================

# Callback to store df1 in dcc.Store
@app.callback(
    Output('stored-df1', 'data'),
    [Input(f'{col}-fig-dropdown-tab-2', 'value') for col in List_col_fig],
    Input('tabs', 'value'),
    prevent_initial_call=True
)
def update_stored_df1(*args):
    
    selected_values = args[:-1]  # Values selected in dropdowns
    tab = args[-1]
    
    if tab == 'tab-2':
        # Identify columns to be loaded based on the user's selection
        selected_columns = [List_col_fig[i] for i, val in enumerate(selected_values) if val]
        # Ensure we are not passing an empty list of columns
        if not selected_columns:
            selected_columns = List_col  # Fallback to all columns if none selected

        List_filter = [None] * len(selected_columns)

        df1 = od.open_dataframe(selected_columns, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        exclude_col = ["tconst", "isAdult", "nconst", "isOriginalTitle"]
        df1 = df1.drop(columns=[col for col in exclude_col if col in df1.columns])
        
        return df1.to_dict('records')
    return dash.no_update


# =============================================================================
# Callback for graph in tab-2
# =============================================================================

@app.callback(
    Output('y-dropdown-tab-2', 'options'),
    Input('x-dropdown-tab-2', 'value'),
    Input('tabs', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df1', 'data')  # Use the correct state data for each tab
)
def update_y_dropdown_tab1(selected_x, selected_tab, stored_df1):
    if selected_tab == 'tab-2':  # Only execute if in the correct tab
        exclude_cols = ["title", "characters"]
        return update_y_dropdown_utility(selected_x, stored_df1, exclude_cols)
    return []  # Return empty if not in the right tab

@app.callback(
    Output('Func-dropdown-tab-2', 'options'),
    Input('y-dropdown-tab-2', 'value'),
    Input('tabs', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df1', 'data')
)
def update_func_dropdown_tab1(selected_y, selected_tab, stored_df1):
    df_col_numeric = ["startYear", "runtimeMinutes", "averageRating", "numVotes"]
    if selected_tab == 'tab-2':
        return update_func_dropdown_utility(selected_y, df_col_numeric)
    return []

@app.callback(
    Output('graph-output-tab-2', 'figure'),
    [Input('x-dropdown-tab-2', 'value'),
     Input('y-dropdown-tab-2', 'value'),
     Input('Func-dropdown-tab-2', 'value'),
     Input('Graph-dropdown-tab-2', 'value'),
     Input('tabs', 'value')] + dropdown_inputs_fig,  # Include tab value to conditionally trigger callback
    State('stored-df1', 'data')
)
def update_graph_tab1(*args):
    x_column, y_column, func_column, graph_type, selected_tab = args[0], args[1], args[2], args[3], args[4]
    selected_values = {col: args[i+5] for i, col in enumerate(List_col_fig)}
    stored_df1 = args[-1]
    
    if selected_tab == 'tab-2' and stored_df1:  # Only execute if in the correct tab
        return update_graph_utility(x_column, y_column, func_column, graph_type, selected_values, stored_df1, Large_file_memory)
    return go.Figure()  # Return a blank figure if not in the right tab



# =============================================================================
# =============================================================================
# =============================================================================
# Tab-3
# =============================================================================
# =============================================================================
# =============================================================================


# Callback to update UI based on input value in Tab 3
@app.callback(
    [Output('dynamic-content', 'children'), Output('stored-df2', 'data')],
    Input('input-value', 'value')
)
def update_ui(input_value):
    if not input_value:  # Return nothing if input is empty or None
        return '', None
    
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

        
        if df2.empty: 
            return html.Div([
                html.Div([
                    html.P(f'The artist '+input_value+' doesnt have referenced movies.'),
                ])
                ], style={'padding': '20px'}), df2.to_dict('records')        
        else:

            # Step 1: Split the strings into individual elements and flatten the list
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
                    
                    fds.figure_position_dash('graph-output-tab-3', dropdowns_with_labels_for_fig, dropdowns_with_labels_for_fig_filter)
                    
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
List_col_tab = ["startYear", "runtimeMinutes", "genres", "directors", "writers", "averageRating", "numVotes", "category", "characters", "title"]
dropdown_inputs_tab = [Input(f'{col}-dropdown', 'value') for col in List_col_tab]

@app.callback(
    Output('table-df2', 'data'),
    dropdown_inputs_tab,
    Input('tabs', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df2', 'data')  # Ensure this is included as State
)
def filter_df2(*args):
    
    selected_tab = args[-2]
    stored_df2 = args[-1]         # The last argument is stored_df2
    selected_values = {col: args[i] for i, col in enumerate(List_col_tab)}

    if selected_tab == 'tab-3':  # Only execute if in the Data Visualization tab
        if stored_df2 is None:  # Check if stored_df2 is None or empty
            return []
        # Convert the stored data back to a DataFrame
        df2 = pd.DataFrame(stored_df2)
        # Create a copy of the DataFrame to avoid modifying the original stored data
        filtered_data_table = df2.copy()
        print("Update table")
        filtered_data_table = od.apply_filter(filtered_data_table, selected_values)
    
        return filtered_data_table.to_dict('records')
    return []  # Return empty if not in the right tab


# =============================================================================
# Callback for graph-df2 in tab-3
# =============================================================================

tab = 'tab-3'
# Create a list of Input objects for each dropdown
List_col_fig = ["startYear", "runtimeMinutes", "genres", "directors", "writers", "averageRating", "numVotes", "category"]
dropdown_inputs_fig = [Input(f'{col}-fig-dropdown-'+tab, 'value') for col in List_col_fig]


@app.callback(
    Output('y-dropdown-tab-3', 'options'),
    Input('x-dropdown-tab-3', 'value'),
    Input('tabs', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df2', 'data')  # Use the correct state data for each tab
)
def update_y_dropdown_tab1(selected_x, selected_tab, stored_df2):
    if selected_tab == 'tab-3':  # Only execute if in the correct tab
        exclude_cols = ["title", "characters"]
        return update_y_dropdown_utility(selected_x, stored_df2, exclude_cols)
    return []  # Return empty if not in the right tab

@app.callback(
    Output('Func-dropdown-tab-3', 'options'),
    Input('y-dropdown-tab-3', 'value'),
    Input('tabs', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df2', 'data')
)
def update_func_dropdown_tab1(selected_y, selected_tab, stored_df2):
    df_col_numeric = ["startYear", "runtimeMinutes", "averageRating", "numVotes"]
    if selected_tab == 'tab-3':
        return update_func_dropdown_utility(selected_y, df_col_numeric)
    return []

@app.callback(
    Output('graph-output-tab-3', 'figure'),
    [Input('x-dropdown-tab-3', 'value'),
     Input('y-dropdown-tab-3', 'value'),
     Input('Func-dropdown-tab-3', 'value'),
     Input('Graph-dropdown-tab-3', 'value'),
     Input('tabs', 'value')] + dropdown_inputs_fig,  # Include tab value to conditionally trigger callback
    State('stored-df2', 'data')
)
def update_graph_tab1(*args):
    x_column, y_column, func_column, graph_type, selected_tab = args[0], args[1], args[2], args[3], args[4]
    selected_values = {col: args[i+5] for i, col in enumerate(List_col_fig)}
    stored_df2 = args[-1]
    
    if selected_tab == 'tab-3':  # Only execute if in the correct tab
        return update_graph_utility(x_column, y_column, func_column, graph_type, selected_values, stored_df2, Large_file_memory)
    return go.Figure()  # Return a blank figure if not in the right tab





# =============================================================================
# Utility Function for Graphs
# =============================================================================

def update_y_dropdown_utility(selected_x, stored_df, exclude_cols):
    """
    Utility function to generate dropdown options for the y-axis based on the selected x-axis column and dataframe.
    """
    if stored_df is None:  # Check if stored_df is None or empty
        return []
    else:
        # Convert the stored data back to a DataFrame
        df = pd.DataFrame(stored_df)
        df_filter = df.drop(columns=exclude_cols)
        return [{'label': col, 'value': col} for col in df_filter.columns if col != selected_x]

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

def update_graph_utility(x_column, y_column, func_column, graph_type, selected_values, stored_df, large_file_memory):
    """
    Utility function to generate a graph based on the provided parameters.
    """
    if stored_df is None:  # Check if stored_df is None or empty
        return go.Figure()  # Return a blank figure
    else:
        # Convert the stored data back to a DataFrame
        df = pd.DataFrame(stored_df)
        # Create a copy of the DataFrame to avoid modifying the original stored data
        filtered_data_graph = df.copy()
        # Apply filters on the dataframe
        filtered_data_graph = od.apply_filter(filtered_data_graph, selected_values)
        # Create the figure based on filtered data
        fig = fds.create_figure(filtered_data_graph, x_column, y_column, func_column, graph_type, large_file_memory)
        return fig

# =============================================================================
# End Utility Function for Graphs
# =============================================================================









if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
    
    # Specify the URL you want to open
    url = "http://127.0.0.1:8052/"
    
    # Open the URL in the default web browser
    webbrowser.open(url)