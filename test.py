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

print(df1)


# Initialize the Dash app with suppress_callback_exceptions set to True
app, dark_dropdown_style, uniform_style = wis.web_interface_style()

app.layout = html.Div([
    # Tabs Component
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Tab 1', value='tab-1'),
        dcc.Tab(label='Tab 2', value='tab-2'),
        dcc.Tab(label='Tab 3', value='tab-3'),
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
        ])
    elif tab == 'tab-3':
        # Placeholder for Tab 3 content
        return html.Div([
            html.H3('Tab 3 Content'),
            html.P('This is a placeholder for Tab 3. You can add any content you like here.')
        ])

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
        # Create dropdown options based on df2
        # dropdown_options = [
        #     {'label': row['directors'], 'value': row['directors']} for index, row in df2.iterrows()
        # ]

        nconst_value = df1[df1['primaryName'] == input_value]['nconst'].iloc[0]
        
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
            # Create the table with the appropriate dropdowns for each column
            dropdowns_with_labels, data_table = tds.dropdown_table(df2, 'table-df2', dark_dropdown_style, uniform_style)
    
            return html.Div([
                html.Div(style={'display': 'flex', 'margin-top': '10px', 'flex-wrap': 'wrap'}, children=[
                    html.Div(dropdowns_with_labels, style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'})
                ]),
                html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
                    html.Div(data_table, style={'width': '100%'})  # Adjusted to take full width
                ])
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


# Create a list of Input objects for each dropdown
List_col = ["startYear", "runtimeMinutes", "genres", "directors", "writers", "averageRating", "numVotes", "category", "characters", "title"]
dropdown_inputs = [Input(f'{col}-dropdown', 'value') for col in List_col]


@app.callback(
    Output('table-df2', 'data'),
    dropdown_inputs,
    State('stored-df2', 'data')  # Ensure this is included as State
)
def filter_df2(*args):
    
    stored_df2 = args[-1]         # The last argument is stored_df2
    selected_values = {col: args[i] for i, col in enumerate(List_col)}
    

    print(selected_values)
    
    if stored_df2 is None:  # Check if stored_df2 is None or empty
        return []
    
    # Convert the stored data back to a DataFrame
    df2 = pd.DataFrame(stored_df2)
    print(df2)
    
    df2 = od.apply_filter(df2, selected_values)
    print(df2)

    return df2.to_dict('records')



if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
    
    # Specify the URL you want to open
    url = "http://127.0.0.1:8052/"
    
    # Open the URL in the default web browser
    # webbrowser.open(url)