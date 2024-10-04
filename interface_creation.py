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
from dash import dcc, html, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
import pandas as pd
from collections import OrderedDict
import plotly.express as px
import webbrowser

import Function_dataframe as fd
import Function_errors as fe
import Function_visualisation as fv

"""#=============================================================================
   #=============================================================================
   #============================================================================="""

# Function to calculate maximum width for each column
def calculate_max_width(df):
    max_widths = {}
    for col in df.columns:
        max_length = max(df[col].astype(str).apply(len))  # Longest cell content
        header_length = len(col)  # Length of column header
        max_widths[col] = f"{max(max_length, header_length) * 4}px"  # Adjust multiplier for desired width
    return max_widths

def create_figure(df):
    fig = px.bar(df, x='runtimeMinutes', y='genres', title='genres by runtimeMinutes')
    fig.update_layout(
        plot_bgcolor='#1e1e1e',  # Darker background for the plot area
        paper_bgcolor='#343a40',  # Dark gray for the paper
        font=dict(color='white'),  # White text color
        title_font=dict(size=20, color='white'),  # Title styling
        xaxis=dict(title='runtimeMinutes', color='white'),  # X-axis styling
        yaxis=dict(title='genres', color='white'),  # Y-axis styling
    )
    return fig


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
    
    
    #Exclude all elements of the dataframe where the column_to_exclude_element correspnds to the Name_element
    column_to_exclude_element="genres"
    Name_element="Short"   
    # Handle NaN values by filling them with an empty string
    df[column_to_exclude_element] = df[column_to_exclude_element].fillna('')
    # Filter out rows where the column contains the specified name element
    df = df[~df[column_to_exclude_element].str.contains(Name_element, na=False)]
    
    df = df.head(100)
    
    print(df)
    

    # #To count individual elements when multiple elements are stored in a single cell 
    # df_exploded, element_counts = fd.explode_dataframe(df, 'genres')
    
    # Para=["startYear","genres_split"]
    # Pivot_table=fd.Pivot_table(df_exploded,Para,False, Large_file_memory)
    
    # y = fd.highest_dataframe_sorted_by(Pivot_table, 8, Para[0])
    
    # print(y)


    # Calculate fixed widths for all columns
    fixed_widths = calculate_max_width(df)

    # Initialize the Dash app with the dark theme
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])  # Use the DARKLY theme from Bootstrap

    
    # Get column names
    columns = df.columns

    # Define dark theme styles
    dark_dropdown_style = {
        'backgroundColor': '#1e1e1e',  # Dark background for dropdown
        'color': '#f8f9fa',  # White text color
        'border': '1px solid #555',  # Border for dropdown
        'borderRadius': '5px',
        'width': '160px',
    }

    # CSS to style the dropdown's options menu (this will apply globally)
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Dash Dark Theme</title>
            <style>
                body {
                    background-color: #343a40; /* Ensure dark background */
                    color: white; /* Ensure white text */
                }
                
                /* Dark theme for dropdown options */
                .Select-menu-outer {
                    background-color: #333 !important;  /* Dark background for the options menu */
                    color: white !important;  /* White text for the options */
                }
                
                .Select-option {
                    background-color: #333 !important;  /* Dark background for individual options */
                    color: white !important;  /* White text */
                }
                
                .Select-option.is-focused {
                    background-color: #444 !important;  /* Highlight option on hover */
                    color: white !important;  /* Ensure the text stays white */
                }
                
                .Select-control {
                    background-color: #1e1e1e !important;  /* Dark background for the dropdown control */
                    color: white !important;  /* White text */
                    border: 1px solid #555 !important;  /* Dark border */
                }
                
                /* Ensuring selected text in the dropdown remains white */
                .Select-value-label {
                    color: white !important;
                }
            </style>
        </head>
        <body>
            <div id="react-entry-point">
                {%app_entry%}
            </div>
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

    # Create the dropdowns for each column
    dropdowns_with_labels = []
    for col in columns:
        dropdown_with_label = html.Div([
            html.Label(f'Select {col}'),  # Label for the dropdown
            dcc.Dropdown(
                id=f'{col}-dropdown',
                options=[{'label': val, 'value': val} for val in df[col].unique()],
                value=df[col].iloc[0],  # Default selected value
                style=dark_dropdown_style,  # Apply dark theme style
                className='dash-dropdown'  # Add custom class to target with CSS
            )
        ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        dropdowns_with_labels.append(dropdown_with_label)
    
    
    
    # Create the data_table
    data_table = dash_table.DataTable(
    id='data-table',
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    fixed_rows={'headers': True},
    style_table={'width': str(int(len(columns)*170))+'px'},
    style_cell={
        'backgroundColor': '#1e1e1e',  # Darker background for cells
        'color': '#f8f9fa',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'whiteSpace': 'nowrap',  
        'maxWidth': 0,  # Prevent the last column from stretching
        'textAlign': 'center'  # Center-align text in data cells
    },
    fixed_columns={'headers': True, 'data': 0},
    style_data_conditional=[
         {
             'if': {'column_id': col},
             'width': fixed_widths[col]  # Fixed width for each column
         } for col in df.columns
    ],
    style_header={
        'backgroundColor': '#343a40',  # Dark gray
        'color': 'white',
        'whiteSpace': 'nowrap',  # Ensure headers don't wrap
        'textAlign': 'center'      # Align headers to the left
    },
    style_data={
        'whiteSpace': 'nowrap',   # Ensure data cells don't wrap
        'textAlign': 'center',       # Align data cells to the left
        'backgroundColor': '#1e1e1e',  # Darker background for data cells
    }
    )


    app.layout = html.Div([

        html.H1("IMDB DataFrame Interface", className="text-light"),

        
        # Dropdowns aligned above the columns
        html.Div(dropdowns_with_labels,
                 style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'}),  # Align to the left
        
        # DataTable below the dropdowns
        html.Div(data_table, style={'margin-top': '10px', 'display': 'flex', 'justify-content': 'flex-start'})
    ], style={'padding': '20px'})  # Optional padding for better layout


    
    # app.layout = dbc.Container([
    #     html.H1("IMDB DataFrame Interface", className="text-light"),
        
    #     # Dropdown for filtering
    #     dbc.Row([
    #         dbc.Col(
    #             dropdowns_with_labels
    #         )
    #     ]),
        
        
    #     dbc.Row([
    #         dbc.Col(
    #             data_table,
    #             width={"size": 8, "offset": 7}  # Center the table in the middle of the page
    #         )
    #     ], justify='center'), # Center the row content
        
       
    #     # Graph
    #     dbc.Row([
    #         dbc.Col(
    #             dcc.Graph(id='genres-graph',
    #             figure=create_figure(df),
    #             style={'height': '60vh'}  # Set the height of the graph
    #             ),
    #             width=8  # Adjust width as needed
    #         )
    #     ], justify='center')
    # ])

   
    
    @app.callback(
        Output('data-table', 'data'),
        # Output('genres-graph', 'figure'),
        Input('startYear-dropdown', 'value')
    )
    


    def update_output(selected_cities):
        
        if selected_cities:
            filtered_df = df[df['startYear'].isin(selected_cities)]
        else:
            filtered_df = df
        
        # Ensure the filtered DataFrame is in the correct format
        data_records = filtered_df.to_dict('records')

        # Create DataTable
        table = html.Table(
            # Header
            [html.Tr([html.Th(col) for col in filtered_df.columns])] +
            # Body
            [html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns]) for i in range(len(filtered_df))]
        )
    
        # Create a bar graph
        # fig = px.bar(filtered_df, x='runtimeMinutes', y='genres', title='genres by runtimeMinutes')
        
    
        return create_figure(filtered_df) #data_records, fig

    
    app.run_server(debug=True, port=8051)
    
    # Specify the URL you want to open
    url = "http://127.0.0.1:8051/"
    
    # Open the URL in the default web browser
    webbrowser.open(url)
    
    
    return 0, df
