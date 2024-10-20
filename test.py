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

df1 = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)




# Initialize the Dash app with suppress_callback_exceptions set to True
app, dark_dropdown_style, uniform_style = wis.web_interface_style()


# app.layout = html.Div([
#     # Tabs Component
#     dcc.Tabs(id='tabs-example', value='tab-1', children=[
#         dcc.Tab(label='🏠 Home', value='tab-1', className='tab-3d', selected_className='tab-3d-selected'),
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
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
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
        dcc.Tab(id='tabs-3', label='Tab 3', value='tab-3', 
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

    # Hidden store to hold df2 data
    dcc.Store(id='stored-df2', data=None),
    
    # Content Div for Tabs
    html.Div(id='tabs-content')
])

# Callback to manage tab content
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-example', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        # This is the content for Tab 1 - the existing layout we created
        return html.Div([
            html.Div([
                html.P(f'This interface is dedicated to the research on specific artist.'),
            ]),
            dcc.Input(id='input-value', type='text', placeholder='Enter a value...', style={**dark_dropdown_style, **uniform_style}),
            html.Div(id='dynamic-content')
        ])
    elif tab == 'tab-2':
        # Placeholder for Tab 2 content
        return html.Div([
            html.H3('Tab 2 Content'),
            html.P('This is a placeholder for Tab 2. You can add any content you like here.')
            # tab2_content()
        ])
    elif tab == 'tab-3':
        # Placeholder for Tab 3 content
        return html.Div([
            html.H3('Tab 3 Content'),
            html.P('This is a placeholder for Tab 3. You can add any content you like here.')
        ])


# =============================================================================
# =============================================================================
# =============================================================================
# Tab-1
# =============================================================================
# =============================================================================
# =============================================================================

# Callback to update UI based on input value in Tab 1
@app.callback(
    [Output('dynamic-content', 'children'), Output('stored-df2', 'data')],
    Input('input-value', 'value')
)
def update_ui(input_value):
    if not input_value:  # Return nothing if input is empty or None
        return '', None
    
    # Check if the input value exists in the 'nconst' column of df1
    if input_value in df1['primaryName'].values:

        nconst_value = df1[df1['primaryName'] == input_value]['nconst'].iloc[0]
        birthYear_value = int(df1[df1['primaryName'] == input_value]['birthYear'].iloc[0])
        deathYear_value = int(df1[df1['primaryName'] == input_value]['deathYear'].iloc[0])
        
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
            dropdowns_with_labels, data_table = tds.dropdown_table(df2, 'table-df2', dark_dropdown_style, uniform_style)
            
            exclude_col = ["title", "characters"]
            df2_filter = df2.drop(columns=exclude_col)            
            dropdowns_with_labels_for_fig = fds.dropdown_figure(df2_filter, 'graph-df2', dark_dropdown_style, uniform_style, Large_file_memory)
                        
            dropdowns_with_labels_for_fig_filter = fds.dropdown_figure_filter(df2_filter, 'graph-df2', dark_dropdown_style, uniform_style)
            
            return html.Div([
                html.P(f'The artist '+input_value+' is born in '+str(birthYear_value)+' and died in '+str(deathYear_value)+' during its career as '+', '.join(primaryProfession)+' he participated to the creation of the following productions.'),
                html.Div(style={'display': 'flex', 'margin-top': '10px', 'flex-wrap': 'wrap'}, children=[
                    html.Div(dropdowns_with_labels, style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'})
                ]),
                html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
                    html.Div(data_table, style={'width': '100%'})  # Adjusted to take full width
                ]),

                html.Div([
                    html.H1("Graphic interface dedicated to the dataframe related to the artist "+input_value+".", style={"color": "#FFD700"}, className="text-light"),
                    
                    fds.figure_position_dash('graph-output', dropdowns_with_labels_for_fig, dropdowns_with_labels_for_fig_filter)
                    
                ], style={'padding': '20px'})
                                
            ], style={'padding': '20px'}), df2.to_dict('records')
        
    
    # If the input does not correspond to any primaryName, filter df1
    filtered_df = df1[df1['primaryName'].str.contains(input_value, case=False, na=False)]

    # Default case: show table based on df1    
    # Calculate widths, ensuring 'title' is handled specifically
    column_widths = {col: tds.get_max_width(df1[col], col) for col in df1.columns}
    return dash_table.DataTable(
        id='table-df1',
        data=filtered_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df1.columns],
        fixed_rows={'headers': True},
        style_table={
            'minWidth': str(int(len(df1.columns) * 170)) + 'px',  # Minimum width calculation
            'overflowX': 'auto',  # Allow horizontal scrolling
            'paddingLeft': '2px',  # Add padding to prevent it from being cut off
            'paddingRight': '20px',
            'marginLeft': '8px'  # Ensure some margin on the left side
        },
        style_cell={
            'backgroundColor': '#1e1e1e',
            'color': '#f8f9fa',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'whiteSpace': 'nowrap',
            'textAlign': 'center',
            'height': '40px',
            'lineHeight': '40px'
        },
        fixed_columns={'headers': True, 'data': 0},
        style_data_conditional=[
            {
                'if': {'column_id': col},
                'width': f'{column_widths[col]}px'
            } for col in df1.columns
        ],
        style_header={
            'backgroundColor': '#343a40',
            'color': 'white',
            'whiteSpace': 'nowrap',
            'textAlign': 'center',
            'height': '40px'
        },
        style_data={
            'whiteSpace': 'nowrap',
            'textAlign': 'center',
            'backgroundColor': '#1e1e1e',
        }
    ), None




# =============================================================================
# Callback for table-df2 in tab-1
# =============================================================================

# Create a list of Input objects for each dropdown
List_col_tab = ["startYear", "runtimeMinutes", "genres", "directors", "writers", "averageRating", "numVotes", "category", "characters", "title"]
dropdown_inputs_tab = [Input(f'{col}-dropdown', 'value') for col in List_col_tab]

@app.callback(
    Output('table-df2', 'data'),
    dropdown_inputs_tab,
    Input('tabs-example', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df2', 'data')  # Ensure this is included as State
)
def filter_df2(*args):
    
    selected_tab = args[-2]
    stored_df2 = args[-1]         # The last argument is stored_df2
    selected_values = {col: args[i] for i, col in enumerate(List_col_tab)}

    if selected_tab == 'tab-1':  # Only execute if in the Data Visualization tab
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
# =============================================================================


# =============================================================================
# Callback for graph in tab-1
# =============================================================================

# Create a list of Input objects for each dropdown
List_col_fig = ["startYear", "runtimeMinutes", "genres", "directors", "writers", "averageRating", "numVotes", "category"]
dropdown_inputs_fig = [Input(f'{col}-fig-dropdown', 'value') for col in List_col_fig]

@app.callback(
    Output('y-dropdown', 'options'),
    Input('x-dropdown', 'value'),
    Input('tabs-example', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df2', 'data')
)
def update_y_dropdown(selected_x, selected_tab, stored_df2):
    if selected_tab == 'tab-1':  # Only execute if in the Data Visualization tab
        if stored_df2 is None:  # Check if stored_df2 is None or empty
            return []
        else:
            # Convert the stored data back to a DataFrame
            df2 = pd.DataFrame(stored_df2)
            exclude_col = ["title", "characters"]
            df2_filter = df2.drop(columns=exclude_col)
            return [{'label': col, 'value': col} for col in df2_filter.columns if col != selected_x]  #[{'label': 'None', 'value': 'None'}] + 
    return []  # Return empty if not in the right tab


@app.callback(
    Output('Func-dropdown', 'options'),
    Input('y-dropdown', 'value'),
    Input('tabs-example', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df2', 'data')
)
def update_func_dropdown(selected_y, selected_tab, stored_df2):

    # Columns in the dataframe which are numerics.
    df_col_numeric = ["startYear", "runtimeMinutes", "averageRating", "numVotes"]

    # Get the list of y function
    function_on_y = ["Avg"]

    if selected_tab == 'tab-1':  # Only execute if in the Data Visualization tab
        if selected_y not in df_col_numeric:  # Check if stored_df2 is None or empty
            return []
        else:
            return [{'label': col, 'value': col} for col in function_on_y]
    return []  # Return empty if not in the right tab


# Callback to update the figure based on the dropdown selections
@app.callback(
    Output('graph-output', 'figure'),
    [Input('x-dropdown', 'value'),
     Input('y-dropdown', 'value'),
     Input('Func-dropdown', 'value'),
     Input('Graph-dropdown', 'value'),
     Input('tabs-example', 'value')] + dropdown_inputs_fig,  # Include tab value to conditionally trigger callback
    State('stored-df2', 'data')
)
def update_graph(*args):
    
    x_column, y_column, func_column, graph_type, selected_tab = args[0], args[1], args[2], args[3], args[4]
    selected_values = {col: args[i+5] for i, col in enumerate(List_col_fig)}
    stored_df2 = args[-1]
    
    if selected_tab == 'tab-1':  # Only execute if in the Data Visualization tab
        if stored_df2 is None:  # Check if stored_df2 is None or empty
            return []
        else:
            # Convert the stored data back to a DataFrame
            df2 = pd.DataFrame(stored_df2)
            # Create a copy of the DataFrame to avoid modifying the original stored data
            filtered_data_graph = df2.copy()
            # Apply filters on the dataframe df2
            print("Update graph")
            filtered_data_graph = od.apply_filter(filtered_data_graph, selected_values)
            # Create the figure based on filtered data
            fig = fds.create_figure(filtered_data_graph, x_column, y_column, func_column, graph_type, Large_file_memory)
        return fig
    else:
        return go.Figure()  # Return a blank figure if not in the right tab

# =============================================================================
# =============================================================================

# =============================================================================
# =============================================================================
# =============================================================================
# Tab-2
# =============================================================================
# =============================================================================
# =============================================================================


# def tab2_content():

#     nconst_value = 'nm0005690'
    
#     # Display the found nconst value (for debugging purposes)
#     print(f"Matched nconst: {nconst_value}")
                    
#     List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters", "title", "isOriginalTitle"]
    
#     List_filter = [None, None, None, None, None, None, None, None, nconst_value, None, None, None, True]
    
#     df3 = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
#     exclude_col = ["tconst", "isAdult", "nconst", "isOriginalTitle"]
#     df3 = df3.drop(columns=exclude_col)

#     # Step 1: Split the strings into individual elements and flatten the list
#     all_elements = df3['category'].str.split(',').explode().str.strip()
#     primaryProfession = all_elements.value_counts()
#     primaryProfession = primaryProfession[primaryProfession > 1].index.tolist()


#     exclude_col = ["title", "characters"]
#     df3_filter = df3.drop(columns=exclude_col)            
#     dropdowns_with_labels_for_fig_tab2 = fds.dropdown_figure(df3_filter, 'graph-df3', dark_dropdown_style, uniform_style, Large_file_memory)
                
#     dropdowns_with_labels_for_fig_filter_tab2 = fds.dropdown_figure_filter(df3_filter, 'graph-df3', dark_dropdown_style, uniform_style)
    
#     print(dropdowns_with_labels_for_fig_filter_tab2)
    
#     return html.Div([

#         html.Div([
            
#             fds.figure_position_dash('graph-df3', dropdowns_with_labels_for_fig_tab2, dropdowns_with_labels_for_fig_filter_tab2)
            
#         ], style={'padding': '20px'})
                        
#     ], style={'padding': '20px'}), df3.to_dict('records')
        
    






if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
    
    # Specify the URL you want to open
    url = "http://127.0.0.1:8052/"
    
    # Open the URL in the default web browser
    # webbrowser.open(url)