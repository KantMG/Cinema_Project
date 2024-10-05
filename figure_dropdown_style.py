#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:23:15 2024

@author: quentin
"""


import dash
from dash import dcc, html, Input, Output, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from collections import OrderedDict
import plotly.express as px
import webbrowser

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import plotly.tools as tls  # For converting Matplotlib to Plotly
import plotly.graph_objects as go

import Function_dataframe as fd
import Function_errors as fe
import Function_visualisation as fv


def histogram_multi(Para,y):

    # Define a list of colors for the bars
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    # Create the Matplotlib figure
    figname = 'Movies over the ' + Para[0]
    fig, ax = plt.subplots(figsize=(8.5, 6))
    ax.set_title(figname)
    
    ax.set_xlabel(Para[0], fontsize=15)
    ax.set_ylabel('Amount of movies', fontsize=15)
    
    bottom = np.zeros(len(y.index))

    # Convert the DataFrame index to a list
    x_values = list(map(int, y.index))
    print(x_values)
    
    # Plot the stacked bar chart
    bars_list = []  # List to hold bar objects for the legend
    for i, (element_col, y_val) in enumerate(y.items()):
        bars = ax.bar(x_values, y_val, label=element_col, bottom=bottom, color=colors[i % len(colors)])  # Color assignment
        bars_list.append(bars)  # Store the bars
        bottom += y_val
    
    
    ax.tick_params(axis='both', labelsize=10)
    ax.grid(True, color='grey', linestyle='--', linewidth=2, alpha=0.5)
    
    # Set x-ticks to the actual index values
    ax.set_xticks(x_values)  # Set the x-ticks to the index of y
    ax.set_xticklabels(x_values, rotation=45, ha='right')  # Set labels and rotate them for better visibility

    
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=10))

    # Create a custom legend using the bars created
    legend_handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors[:len(y)]]
    legend_labels = y.columns.tolist()  # Get the labels from DataFrame columns
    # Customize the legend to ensure it reflects the colors of the bars
    legend = ax.legend(legend_handles, legend_labels, ncol=2, handletextpad=0.001)

    # legend = ax.legend(ncol=2)
    for text in legend.get_texts():
        text.set_color('white')  # Set the color of the legend text
        text.set_fontsize(15)  # Set the font size of the legend text


    plt.tight_layout()
    
    # Now, convert Matplotlib figure to Plotly
    plotly_fig = tls.mpl_to_plotly(fig)  # Convert the Matplotlib figure to Plotly
    
    # Create a Dash compatible Plotly graph figure
    fig_json_serializable = go.Figure(plotly_fig)  # This figure can now be used with dcc.Graph in Dash

    fig_json_serializable.update_layout(
        plot_bgcolor='#1e1e1e',  # Darker background for the plot area
        paper_bgcolor='#343a40',  # Dark gray for the paper
        font=dict(color='white'),  # White text color
        title_font=dict(size=20, color='white'),  # Title styling
        # X-axis and Y-axis styling
        xaxis=dict(
            title=dict(text=Para[0], font=dict(size=18, color='white')),  # X-axis label styling
            tickfont=dict(color='white'),  # X-axis tick color
            showgrid=True,  # Grid styling
            gridcolor='gray'  # Grid color
        ),
        yaxis=dict(
            title=dict(text='Amount of movies', font=dict(size=18, color='white')),  # Y-axis label styling
            tickfont=dict(color='white'),  # Y-axis tick color
            showgrid=True,  # Grid styling
            gridcolor='gray'  # Grid color
        ),
        
        # Legend styling
        legend=dict(
            font=dict(color='white', size=12),  # Legend text color
            bgcolor='#343a40',  # Legend background color
            bordercolor='white',  # Border color of the legend
            borderwidth=1  # Optional: set the width of the border
        )
    )
    plt.show()
    
    return fig_json_serializable


def dropdown_figure(df, dark_dropdown_style, Large_file_memory):


    # Get column names
    columns = df.columns
    
    axis = ['x','y','z']

    # Create the dropdowns for each column
    dropdowns_with_labels = []
    for axi in axis:
        # Get unique values and sort them
        dropdown_with_label = html.Div([
            html.Label(f'Select {axi}'),  # Label for the dropdown
            dcc.Dropdown(
                id=f'{axi}-dropdown',
                options=[{'label': val, 'value': val} for val in columns],
                value='All',  # Set default to "All", meaning no filtering
                style=dark_dropdown_style,  # Apply dark theme style
                className='dash-dropdown'  # Add custom class to target with CSS
            )
        ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        dropdowns_with_labels.append(dropdown_with_label)


    
    print("Answer 1 and 2 of Goal 1")
    print()

    #To count individual elements when multiple elements are stored in a single cell 
    df_exploded, element_counts = fd.explode_dataframe(df, 'genres')
    
    print(df.head(100))
    
    
    Para=["startYear","genres_split"]
    Pivot_table=fd.Pivot_table(df_exploded,Para,False, Large_file_memory)
    
    y = fd.highest_dataframe_sorted_by(Pivot_table, 8, Para[0])

    # =============================================================================
    # Start Plot              
    # =============================================================================  
    fig = histogram_multi(Para,y)
    # =============================================================================
    # ============================================================================= 
        
        
    return dropdowns_with_labels, fig