#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:05:42 2024

@author: quentin
"""


import dash
from dash import dcc, html, Input, Output, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from collections import OrderedDict
import plotly.express as px
import webbrowser

# # Function to calculate maximum width for each column
# def calculate_max_width(df):
#     max_widths = {}
#     for col in df.columns:
#         max_length = max(df[col].astype(str).apply(len))  # Longest cell content
#         header_length = len(col)  # Length of column header
#         max_widths[col] = f"{max(max_length, header_length) * 4}px"  # Adjust multiplier for desired width
#     return max_widths


def web_interface_style():

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

    # app.index_string = '''
    # <!DOCTYPE html>
    # <html>
    #     <head>
    #         <title>Dash Dark Theme</title>
    #         <style>
    #             body {
    #                 background-color: #343a40; /* Ensure dark background */
    #                 color: white; /* Ensure white text */
    #             }
    #         </style>
    #     </head>
    #     <body>
    #         <div id="react-entry-point">
    #             {%app_entry%}
    #         </div>
    #         <footer>
    #             {%config%}
    #             {%scripts%}
    #             {%renderer%}
    #         </footer>
    #     </body>
    # </html>
    # '''


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
    
    return app, dark_dropdown_style, uniform_style
    