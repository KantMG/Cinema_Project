#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 16:14:13 2024

@author: quentin
"""


import dash
from dash import dcc, html, Input, Output, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from collections import OrderedDict
import plotly.express as px
import webbrowser

import open_dataframe as od

def dropdown_artist(dark_dropdown_style, uniform_style, Project_path, Large_file_memory, Get_file_sys_mem):

    List_col = ["nconst", "primaryName", "birthYear", "deathYear"]
    
    List_filter = [None, None, None, None]

    df = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
    columns = df.columns
    
    dropdown_style = {**dark_dropdown_style, **uniform_style}
    # Create dropdowns using calculated widths
    dropdown_with_label = html.Div([
        dcc.Input(
            id=f'primaryName-dropdown',
            type='text',
            debounce=True,
            style=dropdown_style
        )
    ], style={'display': 'inline-block', 'padding': '0 5px'})
    
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
    
    return dropdown_with_label, data_table, df