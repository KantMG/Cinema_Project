#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:23:15 2024

@author: quentin
"""

"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions for figure dropdown creation.

#=============================================================================
   #=============================================================================
   #============================================================================="""


import dash
from dash import dcc, html, Input, Output, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd

from termcolor import colored


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def get_max_width(col_data, col_name):

    """
    Goal: Calculate the associated dropdown for each table column.

    Parameters:
    - col_data: The dataframe column.
    - col_name: The name of the dataframe column.

    Returns:
    - The dropdown dimension.
    """
    
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
    - id_graph: id of the graphic.
    - dark_dropdown_style: Color style of the dropdown.
    - uniform_style: Color style of the dropdown.
    - Large_file_memory: Estimate if the file is too large to be open with panda.

    Returns:
    - dropdowns_with_labels: The finalized dropdowns figure. 
    """

    # Get column names
    columns = df.columns
    
    # Get the list of y function
    function_on_y = ["Avg", "Avg on the ordinate", "Weight on y"]
    
    # Get the type of graph
    graph_type = ["Histogram", "Curve", "Scatter", "Boxes", "Colormesh"]

    # Get the graph dimension
    dim_type = ["1D", "2D", "3D"]
    
    # Get the list of axis and graph function
    axis = ["x", "y", "z", "Func on y", "Func on z", "Graph", "Dim"]


    # Define a consistent style for both input and dropdown elements
    uniform_style = {
        'width': '160px',  # Set a consistent width
        'height': '40px',  # Set a consistent width
        'borderRadius': '5px',  # Optional: Add rounded corners
        'backgroundColor': '#1e1e1e',
        'color': '#f8f9fa'
    }
    
    dropdown_container_style = {'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}
    
    # Create the dropdowns for each column
    dropdowns_with_labels = []
    for axi in axis:
        if axi == 'Dim':
            # Get unique values and sort them
            dropdown_with_label = html.Div(
                style=dropdown_container_style,
                children=[
                    html.Label(f'Select {axi}'),  # Label for the dropdown
                    dcc.Dropdown(
                        id=f'{axi}-dropdown-'+tab,
                        options=[{'label': val, 'value': val} for val in dim_type],
                        value='1D',  # Set default to "All", meaning no filtering
                        style=uniform_style,
                        className='dash-dropdown',
                        clearable=True
                    )
                ]
            )
        elif axi == 'Graph':
            dropdown_with_label = html.Div(
                style=dropdown_container_style,
                children=[
                    html.Label(f'Select {axi}'),  # Label for the dropdown
                    dcc.Dropdown(
                        id=f'{axi}-dropdown-'+tab,
                        options=[{'label': val, 'value': val} for val in graph_type],
                        value='Histogram',  # Set default to "All", meaning no filtering
                        style=uniform_style,
                        className='dash-dropdown',
                        clearable=True
                    )
                ]
            )
        elif axi == 'Func on z':
            dropdown_with_label = html.Div(
                style=dropdown_container_style,
                children=[
                    html.Label(f'Select {axi}'),  # Label for the dropdown
                    dcc.Dropdown(
                        id=f'{axi}-dropdown-'+tab,
                        options=[{'label': val, 'value': val} for val in function_on_y],
                        value="Avg",
                        style=uniform_style,
                        className='dash-dropdown'
                        # clearable=True
                    )
                ]
            )
        elif axi == 'Func on y':
            dropdown_with_label = html.Div(
                style=dropdown_container_style,
                children=[
                    html.Label(f'Select {axi}'),  # Label for the dropdown
                    dcc.Dropdown(
                        id=f'{axi}-dropdown-'+tab,
                        options=[{'label': val, 'value': val} for val in function_on_y],
                        # value=None,
                        style=uniform_style,
                        className='dash-dropdown',
                        clearable=True
                    )
                ]
            )
        elif axi== 'z':
            dropdown_with_label = html.Div(
                style=dropdown_container_style,
                children=[
                    html.Label(f'Select {axi}'),  # Label for the dropdown
                    dcc.Dropdown(
                        id=f'{axi}-dropdown-'+tab,
                        options=[{'label': val, 'value': val} for val in columns],
                        # value=None,
                        style=uniform_style,
                        className='dash-dropdown',
                        clearable=True
                    )
                ]
            )
        elif axi== 'y':
            dropdown_with_label = html.Div(
                style=dropdown_container_style,
                children=[
                    html.Label(f'Select {axi}'),  # Label for the dropdown
                    dcc.Dropdown(
                        id=f'{axi}-dropdown-'+tab,
                        options=[{'label': val, 'value': val} for val in columns],
                        # value=None,
                        style=uniform_style,
                        className='dash-dropdown',
                        clearable=True
                    )
                ]
            )
        else:
            dropdown_with_label = html.Div(
                style=dropdown_container_style,
                children=[
                    html.Label(f'Select {axi}'),  # Label for the dropdown
                    dcc.Dropdown(
                        id=f'{axi}-dropdown-'+tab,
                        options=[{'label': val, 'value': val} for val in columns],
                        # value=None,
                        style=uniform_style,
                        className='dash-dropdown',
                        clearable=True
                    )
                ]
            )

        dropdowns_with_labels.append(dropdown_with_label)

        
    return dropdowns_with_labels


"""#=============================================================================
   #=============================================================================
   #============================================================================="""

def dropdown_figure_filter(df, id_graph, tab, dark_dropdown_style, uniform_style):

    """
    Goal: Create the dropdown associated to a figure.
    These dropdowns are extra filters and the axis are not necessary shown on the graphic.

    Parameters:
    - df: dataframe.
    - id_graph: id of the graphic.
    - tab: name of the tab where the figure is located.
    - dark_dropdown_style: Color style of the dropdown.
    - uniform_style: Color style of the dropdown.

    Returns:
    - dropdowns_with_labels: The finalized dropdowns figure. 
    """    

    columns = df.columns
    
    # Calculate widths, ensuring 'title' is handled specifically
    column_widths = {col: get_max_width(df[col], col) for col in columns}
    
    # Create dropdowns using calculated widths
    dropdowns_with_labels = []
    for col in columns:
        dtype = df[col].dtype
        # dropdown_style = {**dark_dropdown_style, **uniform_style}  #, 'width': f'{column_widths[col]}px'
        dropdown_style = {'width': f'160px', 'height': '40px', 'boxSizing': 'border-box', 'backgroundColor': '#1e1e1e', 'color': '#f8f9fa'}
        
        dropdown_container_style = {'display': 'flex', 'flex-direction': 'column', 'margin': '2px 0'}  # Vertical alignment and spacing
        
        if dtype == "float64":
            dropdown_with_label = html.Div(
                style=dropdown_container_style,
                children=[
                    html.Label(f'{col}:'),
                    dcc.Input(
                        id=f'fig-dropdown-{col}-'+tab,
                        type='text',
                        debounce=True,
                        style=dropdown_style,  # Adding margin for spacing
                        className='dash-input dynamic-width'
                    )
                ]
            )
        else:
            # Collect all unique values, splitting them by commas and ensuring uniqueness
            all_roles = set()
            for value in df[col].dropna().unique():
                # Split the value by comma and strip any extra spaces
                roles = [role.strip() for role in str(value).split(',')]
                all_roles.update(roles)
            
            # Convert to a sorted list
            unique_values = sorted(all_roles)
            
            dropdown_with_label = html.Div(
                style=dropdown_container_style,
                children=[
                    html.Label(f'{col}:'),
                    dcc.Dropdown(
                        id=f'fig-dropdown-{col}-'+tab,
                        options=[{'label': val, 'value': val} for val in unique_values],
                        style=dropdown_style,
                        className='dash-dropdown',
                        multi=True,
                        clearable=True
                    )
                ]
            )
    
        dropdowns_with_labels.append(dropdown_with_label)

    
    return dropdowns_with_labels


"""#=============================================================================
   #=============================================================================
   #============================================================================="""
   

def dropdown_checkboxes_figure_filter(df, id_graph, tab, dark_dropdown_style, uniform_style):

    """
    Goal: Create the dropdown associated to a figure.
    These dropdowns are extra filters and the axis are not necessary shown on the graphic.
    Furthermore, A checkbox is on located on the left of all Input and dropdown.

    Parameters:
    - df: dataframe.
    - id_graph: id of the graphic.
    - tab: name of the tab where the figure is located.
    - dark_dropdown_style: Color style of the dropdown.
    - uniform_style: Color style of the dropdown.

    Returns:
    - dropdowns_with_labels_and_checkboxes: The finalized dropdowns and checkboxes figure. 
    """   
    
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
                id=f'fig-dropdown-{col}-'+tab,
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
                id=f'fig-dropdown-{col}-'+tab,
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


def button_dropdown_function(text_button, id_button, id_created_func_name, id_created_func, id_submit_button, id_modal, id_output_div, dark_dropdown_style, uniform_style):
    
    dropdown_style = {'width': f'200px', 'height': '40px', 'boxSizing': 'border-box'}
        
    return html.Div([
    dbc.Button(text_button, id=id_button, n_clicks=0, className='button'),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("  Create Function")),
            dbc.ModalBody(
                [
                    dcc.Input(id=id_created_func_name, type="text", style=dropdown_style, className='dash-input dynamic-width', placeholder="Enter function name"),
                    html.Span(":", style={'margin': '0 10px'}),
                    dcc.Input(id=id_created_func, type="text", style=dropdown_style, className='dash-input dynamic-width', placeholder="Enter operation (e.g., A + B)"),
                ]
            ),
            html.Span("", style={'margin': '0 10px'}),
            dbc.ModalFooter(
                dbc.Button("Submit", id=id_submit_button, n_clicks=0, className='button')
            ),
        ],
        id=id_modal,
        is_open=False,  # Initially closed
        className='top-modal',  # Apply the custom class here
        centered=True,
        size="lg",
    ),
    html.Div(id=id_output_div)
    ])


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def button_dropdown_regression(text_button, id_button, id_dropdown, id_order_reg, id_submit_button, id_modal, id_output_div, dark_dropdown_style, uniform_style):

    dropdown_style = {'width': f'200px', 'height': '40px', 'boxSizing': 'border-box'}
        
    return html.Div([
    dbc.Button(text_button, id=id_button, n_clicks=0, className='button'),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("  Create regression")),
            dbc.ModalBody(
                [   
                    dcc.Dropdown(
                        id=id_dropdown,
                        options=["Linear Regression", "Decision Tree", "k-NN", "Polynomial Regression", "Savitzky-Golay Filter"],
                        # value='Decision Tree',
                        clearable=True,
                        style=dropdown_style,
                        className='dash-dropdown'
                    ),
                    html.Span(":", style={'margin': '0 10px'}),
                    dcc.Input(id=id_order_reg, type="number", style=dropdown_style, className='dash-input dynamic-width', placeholder="Enter an order if needed"),
                ]
            ),
            html.Span("", style={'margin': '0 10px'}),
            dbc.ModalFooter(
                dbc.Button("Submit", id=id_submit_button, n_clicks=0, className='button')
            ),
        ],
        id=id_modal,
        is_open=False,  # Initially closed
        className='top-modal',  # Apply the custom class here
        centered=True,
        size="lg",
    ),
    html.Div(id=id_output_div) 
    ])


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def button_dropdown_smoothing(text_button, id_button, id_dropdown, id_order_reg, id_submit_button, id_modal, id_output_div, dark_dropdown_style, uniform_style):

    dropdown_style = {'width': f'200px', 'height': '40px', 'boxSizing': 'border-box'}
        
    return html.Div([
    dbc.Button(text_button, id=id_button, n_clicks=0, className='button'),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("  Select a smoothing function")),
            dbc.ModalBody(
                [   
                    dcc.Dropdown(
                        id=id_dropdown,
                        options=["Savitzky-Golay Filter"],
                        # value='Decision Tree',
                        clearable=True,
                        style=dropdown_style,
                        className='dash-dropdown'
                    ),
                    html.Span(":", style={'margin': '0 10px'}),
                    dcc.Input(id=id_order_reg, type="number", style=dropdown_style, className='dash-input dynamic-width', placeholder="Enter an order if needed"),
                ]
            ),
            html.Span("", style={'margin': '0 10px'}),
            dbc.ModalFooter(
                dbc.Button("Submit", id=id_submit_button, n_clicks=0, className='button')
            ),
        ],
        id=id_modal,
        is_open=False,  # Initially closed
        className='top-modal',  # Apply the custom class here
        centered=True,
        size="lg",
    ),
    html.Div(id=id_output_div) 
    ])
    

"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def figure_position_dash(tab, idgraph, dropdowns_with_labels_for_fig, dropdowns_with_labels_for_fig_filter, button_dropdown_function, button_dropdown_regression, button_dropdown_smoothing):

    """
    Goal: Create the dropdown associated to a figure.
    These dropdowns are extra filters and the axis are not necessary shown on the graphic.
    Furthermore, A checkbox is on located on the left of all Input and dropdown.

    Parameters:
    - id_graph: id of the graphic.
    - dropdowns_with_labels_for_fig: The figue dropdowns.
    - dropdowns_with_labels_for_fig_filter: The figue dropdowns for extra filters (with or without checkbox).

    Returns:
    - The finalized figure with all the dropdowns and checkboxes on dash. 
    """   
    
    return html.Div(
        style={'display': 'flex', 'flex-direction': 'column', 'margin-top': '10px'},  # Use column direction for vertical stacking
        children=[
            # Dropdowns for the graph filters (above the graph)
            html.Div(
                dropdowns_with_labels_for_fig,
                style={
                    'display': 'flex',
                    'margin-left': '200px',
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
                        [dcc.Graph(id=idgraph, style={'width': '100%', 'height': '600px'}),
                         dcc.Store(id='figure-store-'+tab, data={})], 
                        style={'margin-left': '20px', 'width': '70%'}
                    ),
                    # Dropdowns and heading in a vertical column on the right
                    html.Div(
                        style={'margin-left': '20px', 'width': '30%'},  # Container for the heading and dropdowns
                        children=[
                            # Heading above dropdowns
                            html.H2(
                                'Select filters on the dataframe.',
                                style={'margin-bottom': '10px'},  # Add some space below the heading
                                className="text-light"
                            ),
                            # Dropdowns in a vertical column
                            html.Div(
                                dropdowns_with_labels_for_fig_filter,
                                style={
                                    'display': 'flex',
                                    'flexWrap': 'wrap',  # Allow wrapping to new lines
                                    # 'flex-direction': 'column',  # Arrange dropdowns vertically
                                    'justify-content': 'flex-start',
                                    'gap': '10px',  # Add spacing between dropdowns
                                }
                            ),
                            
                            html.Span("", style={'margin': '0 10px'}),
                            
                            html.Div(
                                button_dropdown_function,
                                style={
                                    'display': 'flex',
                                    'justify-content': 'flex-start',
                                    'gap': '10px',  # Add spacing between dropdowns
                                }
                            ),       
                            
                            html.Span("", style={'margin': '0 10px'}),
                            
                            html.Div(
                                button_dropdown_regression,
                                style={
                                    'display': 'flex',
                                    'justify-content': 'flex-start',
                                    'gap': '10px',  # Add spacing between dropdowns
                                }
                            ),  
                            
                            html.Span("", style={'margin': '0 10px'}),
                            
                            html.Div(
                                html.Button("Hide Dropdowns on figure", id='hide-dropdowns-'+tab, n_clicks=0, className='button'),
                                style={
                                    'display': 'flex',
                                    'justify-content': 'flex-start',
                                    'gap': '10px',  # Add spacing between dropdowns
                                }
                            ),  

                            html.Span("", style={'margin': '0 10px'}),
                            
                            html.Div(
                                button_dropdown_smoothing,
                                style={
                                    'display': 'flex',
                                    'justify-content': 'flex-start',
                                    'gap': '10px',  # Add spacing between dropdowns
                                }
                            ),  
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
