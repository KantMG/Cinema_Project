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


def dropdown_table(df, dark_dropdown_style, uniform_style):
    columns = df.columns
    
    def get_max_width(col_data, col_name):
        max_length = max(col_data.apply(lambda x: len(str(x))))
        print(max_length,col_name)
        # Set a higher max width for 'title' column
        if col_name == 'title':
            return max(150, min(max_length * 10, 600))  # Minimum 150px, maximum 400px for 'title'
        return max(80, min(max_length * 8, 300))  # Ensure minimum 80px and maximum 300px width for others
    
    # Calculate widths, ensuring 'title' is handled specifically
    column_widths = {col: get_max_width(df[col], col) for col in columns}
    
    # Create dropdowns using calculated widths
    dropdowns_with_labels = []
    for col in columns:
        dtype = df[col].dtype
        dropdown_style = {**dark_dropdown_style, **uniform_style, 'width': f'{column_widths[col]}px'}

        if dtype == "float64":
            dropdown_with_label = html.Div([
                dcc.Input(
                    id=f'{col}-dropdown',
                    type='text',
                    debounce=True,
                    style=dropdown_style
                )
            ], style={'display': 'inline-block', 'width': f'{column_widths[col]}px', 'padding': '0 5px'})
        else:
            unique_values = sorted(df[col].unique())
            dropdown_with_label = html.Div([
                dcc.Dropdown(
                    id=f'{col}-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': val, 'value': val} for val in unique_values],
                    value='All',
                    style=dropdown_style,
                    className='dash-dropdown'
                )
            ], style={'display': 'inline-block', 'width': f'{column_widths[col]}px', 'padding': '0 5px'})
    
        dropdowns_with_labels.append(dropdown_with_label)
    
    # Ensure the DataTable columns use the same calculated widths
    data_table = dash_table.DataTable(
        id='data-table',
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in columns],
        fixed_rows={'headers': True},
        style_table={
            'minWidth': str(int(len(columns) * 170)) + 'px',  # Minimum width calculation
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
            } for col in columns
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
    )
    
    return dropdowns_with_labels, data_table