#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:05:42 2024

@author: quentin
"""

"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions for Dash app creation.

#=============================================================================
   #=============================================================================
   #============================================================================="""


import dash
from dash import dcc, html, Input, Output, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import webbrowser


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def web_interface_style():

    """
    Goal: Create the Dash app and define the style and theme.

    Parameters:
    - None

    Returns:
    - app: The Dash app.
    - dark_dropdown_style: Color style of the dropdown.
    - uniform_style: Color style of the dropdown.    
    """        

    # Initialize the Dash app with the dark theme
    app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])  # Use the DARKLY theme from Bootstrap

    # Define dark theme styles
    dark_dropdown_style = {
        'backgroundColor': '#1e1e1e',  # Dark background for dropdown
        'color': '#f8f9fa',  # White text color
        'border': '1px solid #555',  # Border for dropdown
        'borderRadius': '5px',
        'width': '160px',
    }

    # Define a consistent style for both input and dropdown elements
    uniform_style = {
        'width': '160px',  # Set a consistent width
        'height': '40px',  # Set a consistent width
        'borderRadius': '5px',  # Optional: Add rounded corners
    }

    # CSS to style the dropdown's options menu (this will apply globally)
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Dash Dark Theme</title>
            <link rel="stylesheet" href="/assets/style.css">  <!-- Add this line -->
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


    #Creation of the app layout
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
        html.Div(id='tabs-content'),
    
        # fds.tab2_initial_id(List_col_tab2, 'tab-2')
    
    ])

    return app, dark_dropdown_style, uniform_style
    