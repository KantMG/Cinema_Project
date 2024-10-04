#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 16:56:51 2024

@author: quentin
"""


import panel as pn
import pandas as pd
import plotly.express as px

# Enable Panel's widgets and dashboard features
pn.extension('plotly')

# Sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Age': [24, 30, 22, 29, 34],
    'Occupation': ['Engineer', 'Doctor', 'Artist', 'Lawyer', 'Scientist'],
    'Salary': [70000, 120000, 50000, 110000, 90000]
}
df = pd.DataFrame(data)

# Create interactive widgets
column_select = pn.widgets.Select(name='Select Column', options=['Age', 'Salary'], value='Age')

# Function to create a dynamic bar chart
@pn.depends(column_select)
def create_bar_chart(column):
    fig = px.bar(df, x='Name', y=column, color='Occupation', title=f"Bar Chart of {column}")
    return fig

# Table to show the DataFrame
data_table = pn.widgets.DataFrame(df, name="Data Table", width=500, height=300)

# Sidebar with dropdown
sidebar = pn.Column("## Controls", column_select)

# Main content (bar chart and data table)
main_content = pn.Column(
    pn.pane.Markdown("## Interactive Bar Chart"), 
    pn.panel(create_bar_chart, height=400),
    pn.pane.Markdown("## Data Table"),
    data_table
)

# Create the layout using Template
dashboard = pn.template.MaterialTemplate(
    title="Interactive Dashboard with Panel",
    sidebar=[sidebar],
    main=[main_content],
)

# Serve the dashboard
dashboard.servable()