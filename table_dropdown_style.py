#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:13:48 2024

@author: quentin
"""

import dash
from dash import dcc, html, Input, Output, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from collections import OrderedDict
import plotly.express as px
import webbrowser


def dropdown_table(df, fixed_widths, dark_dropdown_style, uniform_style, list_col_num):

    # Get column names
    columns = df.columns

    # Create the dropdowns for each column
    dropdowns_with_labels = []
    for col in columns:
        # Get unique values and sort them
        unique_values = sorted(df[col].unique())  # Sort unique values
        if col in list_col_num:
            dropdown_with_label = html.Div([
                html.Label(f'Select {col}'),  # Label for the dropdown
                dcc.Input(
                    id=f'{col}-dropdown',
                    type='text',
                    placeholder='Condition (e.g., 100-200)',
                    debounce=True,  # Apply changes when pressing Enter or losing focus
                    style={**dark_dropdown_style, **uniform_style} # Apply dark theme style
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        else:
            dropdown_with_label = html.Div([
                html.Label(f'Select {col}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{col}-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': val, 'value': val} for val in unique_values],
                    value='All',  # Set default to "All", meaning no filtering
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
    
    return dropdowns_with_labels, data_table