#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 23:18:23 2024

@author: quentin
"""


"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions for visualisation of the dataframe.

#=============================================================================
   #=============================================================================
   #============================================================================="""


import dash
from dash import dcc, html, Input, Output, dash_table, callback, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import linear_model as lm, tree, neighbors
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from scipy import signal

from termcolor import colored

import matplotlib.pyplot as plt
import plotly.tools as tls  # For converting Matplotlib to Plotly
import plotly.graph_objects as go
import plotly.express as px

import Function_dataframe as fd
import Function_errors as fe
import data_plot_preparation as dpp


cmaps = [('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])]


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def create_figure(df, x_column, y_column, z_column, yf_column, zf_column, g_column, d_column, r_column, o_column, Large_file_memory):

    """
    Goal: Create a sophisticated figure which adapt to any input variable.

    Parameters:
    - df: dataframe
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - yf_column: Function to operate on y_column with the rest of the dataframe
    - zf_column: Function to operate on z_column with the rest of the dataframe
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.
    - r_column: Type of regression for the data.
    - o_column: Order of the regression for the data.
    - Large_file_memory: Estimate if the file is too large to be open with panda

    Returns:
    - fig_json_serializable: The finalized plotly figure. 
    """

    # =============================================================================
    print(colored("========================= Start figure creation =========================", "green"))
    # =============================================================================      
    # Create a Dash compatible Plotly graph figure
    fig_json_serializable = go.Figure()  # This figure can now be used with dcc.Graph in Dash

    # Create the label of the figure
    figname, xlabel, ylabel, zlabel = label_fig(x_column, y_column, z_column, yf_column, zf_column, g_column, d_column, True)  
    
    if x_column is not None: 
        print("Extract from data base the required column and prepare them for the figure.")
        Para, data_for_plot, x_column, y_column, z_column = dpp.data_preparation_for_plot(df , x_column, y_column, z_column, yf_column, zf_column, g_column, Large_file_memory)
        print("The data ready to be ploted is")
        print(data_for_plot)
        print()
        # Add the core of the figure
        fig_json_serializable, xlabel, ylabel, zlabel = figure_plotly(fig_json_serializable, x_column, y_column, z_column, yf_column, zf_column, g_column, d_column, r_column, o_column, data_for_plot, xlabel, ylabel, zlabel)
    
    # Update the figure layout
    fig_update_layout(fig_json_serializable,figname,xlabel,ylabel,zlabel,x_column,g_column,d_column)       
    
    plt.close()
    # =============================================================================
    print(colored("=============================================================================", "green"))
    if x_column is None: 
        return fig_json_serializable, None
    return fig_json_serializable, data_for_plot.to_dict(orient='records')


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def label_fig(x_column, y_column, z_column, yf_column, zf_column, g_column, d_column, init):

    """
    Goal: Create the figure labels.

    Parameters:
    - x_column: Column in the dataframe (can be None).
    - y_column: Column in the dataframe (can be None).
    - z_column: Column in the dataframe (can be None).
    - yf_column: Function to operate on y_column with the rest of the dataframe
    - zf_column: Function to operate on z_column with the rest of the dataframe
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.

    Returns:
    - figname: The name of the Figure.
    - xlabel: The xlabel of the axis (can be None).
    - ylabel: The ylabel of the axis (can be None).
    - zlabel: The zlabel of the axis (can be None).
    """

    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres", "directors", "writers", "category"]
    
    if init == False:
        if x_column is not None: 
            figname = 'Movies over the ' + x_column
    
            if x_column == 'count':
                xlabel = 'Number of movies'
            elif 'avg_' in x_column:
                xlabel = 'Average '+x_column[3:]+' of the movies'
            else:
                xlabel = x_column
            
            if y_column == 'count':
                ylabel = 'Number of movies'
            elif 'avg_' in y_column:
                ylabel = 'Average '+y_column[3:]+' of the movies'              
            else:
                ylabel = y_column
            
            if z_column is not None:
                if z_column == 'count':
                    zlabel = 'Number of movies'
                elif 'avg_' in z_column:
                    zlabel = 'Average '+z_column[3:]+' of the movies'
                else:
                    zlabel = z_column
                    
                if zf_column == 'Weight on y':
                    ylabel = 'Average '+y_column[3:]+' of the movies'
                    
            else:
                zlabel = None


            if d_column == "2D":
                if g_column == 'Colormesh':
                    ylabel = y_column
                else:
                    ylabel = "None"
                zlabel = "None"
    
    
        else: 
            figname = 'No data selected'
            xlabel, ylabel, zlabel = "None","None","None"
    
    else:
        figname = 'No data selected'
        xlabel, ylabel, zlabel = "None","None","None"        
    
    if x_column in df_col_string:
        xlabel_temp = xlabel
        xlabel = ylabel
        ylabel = xlabel_temp
    
    return figname, xlabel, ylabel, zlabel


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def figure_plotly(plotly_fig, x_column, y_column, z_column, yf_column, zf_column, g_column, d_column, r_column, o_column, data_for_plot, xlabel, ylabel, zlabel):

    """
    Goal: Create the plot inside the figure regarding the inputs.

    Parameters:
    - plotly_fig: Dash figure.
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - yf_column: Function to operate on y_column with the rest of the dataframe
    - zf_column: Function to operate on z_column with the rest of the dataframe
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.
    - r_column: Type of regression for the data.
    - o_column: Order of the regression for the data.
    - data_for_plot: Data to plot.

    Returns:
    - plotly_fig: The core figure.
    """
    
    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]
    
    # Define a list of colors for the bars
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    legend = "None"
    

    x_axis = x_column
    y_axis = 'count'
    z_axis = None
    if str(y_column)!='None':
        z_axis = y_column
    if x_column in df_col_string:
        x_axis = 'count'
        y_axis = x_column

    if yf_column == "Avg":
        z_axis = 'avg_' + y_column

    if yf_column == "Avg on the ordinate":
        x_axis = x_column
        y_axis = 'avg_' + y_column
        z_axis = 'count'
        if x_column in df_col_string:
            x_axis = 'avg_' + y_column
            y_axis = x_column
            z_axis = 'count'
    
    if z_column is not None and zf_column == "Avg":
        t_axis = 'avg_' + z_column
    

    print("x_axis=", x_axis)
    print("y_axis=", y_axis)
    if str(y_column)!='None':
        print("z_axis=", z_axis)
    if str(z_column)!='None' and zf_column == "Avg":
        print("t_axis=", t_axis)


    # Rename the label of the figure
    figname, xlabel, ylabel, zlabel = label_fig(x_axis, y_axis, z_axis, yf_column, zf_column, g_column, d_column, False)  

    if d_column=="1D": 
        
        if str(y_column)=='None':
            
            if g_column=="Histogram":
                plotly_fig = px.bar(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis
                    )
            if g_column=="Curve":
                plotly_fig = px.line(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis
                    ) #, color=y_column, symbol="country"
            if g_column=="Scatter":
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_axis,
                    y=y_axis,
                    # log_x=True,
                    size_max=60
                    )
        
        #Case where y_column is None and z_column is None
        elif str(y_column)!='None' and str(z_column)=='None':

            if x_column in df_col_string:
                # Grouping y_column values
                n = 12  # Number of top categories to keep
                data_for_plot = group_small_values(data_for_plot, x_column, 'count', n)

            if y_column in df_col_string:
                # Grouping y_column values
                n = 7  # Number of top categories to keep
                data_for_plot = group_small_values(data_for_plot, y_column, 'count', n)

            if "Histogram" in g_column:
                plotly_fig = px.bar(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis,
                    color=z_axis if "Movie" not in g_column else None,
                    animation_frame=z_axis if "Movie" in g_column else None
                    )
            if "Curve" in g_column:
                plotly_fig = px.line(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis,
                    color=z_axis if "Movie" not in g_column else None,
                    animation_frame=z_axis if "Movie" in g_column else None,
                    line_group=g_column if "Movie" in g_column else None
                    ) #symbol="country"
            if "Scatter" in g_column:
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_axis,
                    y=y_axis,
                    size_max=60,
                    # log_x=True,
                    color=z_axis if "Movie" not in g_column else None,
                    animation_frame=z_axis if "Movie" in g_column else None
                    )  
            if "Boxes" in g_column:
                if x_column in df_col_string:
                    x_axis = y_column
                    xlabel = y_column
                else:
                    y_axis = y_column
                    ylabel = y_column
                plotly_fig = px.box(
                    data_for_plot, 
                    x=x_axis, 
                    y=y_axis,
                    points=False)

        #Case where z_column is not None
        else:
            
            if y_column in df_col_string:
                # Grouping y_column values
                n = 7  # Number of top categories to keep
                data_for_plot = group_small_values(data_for_plot, y_column, 'count', n)

            if z_column in df_col_string:
                # Grouping y_column values
                n = 7  # Number of top categories to keep
                data_for_plot = group_y_values(data_for_plot, z_column, n)
                        
            # y_values = data_for_plot[y_column].unique()
            if g_column=="Histogram" and zf_column == "Avg":
               plotly_fig = px.bar(
                   data_for_plot, 
                   x=x_axis, 
                   y=y_axis,
                   color=z_axis if "Movie" not in g_column else None,
                   animation_frame=z_axis if "Movie" in g_column else None
                   )
            elif g_column=="Curve" and zf_column == "Avg":
                plotly_fig = go.Figure()
                # Add traces for each unique group
                for key in data_for_plot[y_column].unique():
                    group = data_for_plot[data_for_plot[y_column] == key]
                    plotly_fig.add_trace(go.Scatter(
                        x=group[x_column],
                        y=group['count'],
                        mode='lines',
                        name=key,
                        line=dict(width=group['avg_'+z_column].mean())  # Set line width based on avg thickness
                    ))
            elif g_column=="Scatter" and zf_column == "Avg":
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_axis,
                    y=y_axis,
                    size=t_axis,
                    size_max=60,
                    color=z_axis if "Movie" not in g_column else None,
                    animation_frame=z_axis if "Movie" in g_column else None
                )

            elif g_column=="Histogram" and zf_column == "Weight on y":
                plotly_fig = px.bar(
                    data_for_plot,
                    x=x_axis,
                    y=z_axis,
                    title='Weighted Average'+y_column+'Over the'+x_axis,
                    error_y='standard_error'
                )
            elif g_column=="Curve" and zf_column == "Weight on y":
                plotly_fig = px.line(
                    data_for_plot,
                    x=x_axis,
                    y=z_axis,
                    title='Weighted Average'+y_column+'Over the'+x_axis,
                    error_y='standard_error'
                )
            elif g_column=="Scatter" and zf_column == "Weight on y":
                plotly_fig = px.scatter(
                    data_for_plot,
                    x=x_axis,
                    y=z_axis,
                    title='Weighted Average'+y_column+'Over the'+x_axis,
                    error_y='standard_error'
                )



    if g_column=="Pie": #d_column=="2D" and 

            if x_column in df_col_string:
                # Grouping y_column values
                n = 7  # Number of top categories to keep
                data_for_plot = group_small_values(data_for_plot, x_column, 'count', n)

            # x_values,fig_x_value,y_values,fig_y_value=None,None,None,None
            plotly_fig = px.pie(
                data_for_plot, 
                values="count", 
                names=x_column
                )

    if d_column=="2D" and g_column=="Colormesh":     
        
        px_fig = px.density_heatmap(
            data_for_plot, 
            x=x_column, 
            y=y_column, 
            # nbinsx=100, nbinsy=100, 
            z='count',
            color_continuous_scale="Viridis")

        # Get the z data from the px figure
        z_data = px_fig.data[0].z  # Access the z values (the counts)
        x_values = px_fig.data[0].x  # Access the x values (start years)
        y_values = px_fig.data[0].y  # Access the y values (runtime minutes)
        
        # Create a Go Figure and add the Heatmap trace
        plotly_fig = go.Figure()
        
        # Add Heatmap trace
        plotly_fig.add_trace(go.Heatmap(
            x=x_values,
            y=y_values,
            z=z_data,
            colorscale='Viridis'
        ))

                    
    if d_column == "3D" and g_column == "Histogram":
        
        # Pivoting the DataFrame to create a grid for surface plot
        pivoted_data = data_for_plot.pivot(index=y_column, columns=x_column, values='count')
        # Fill NaN values with zeros or an appropriate value for the surface
        pivoted_data = pivoted_data.fillna(0)
        # Now, create the surface plot

        plotly_fig = go.Figure(
            data=[go.Surface(z=pivoted_data.values, x=pivoted_data.columns, y=pivoted_data.index)])

    return plotly_fig, xlabel, ylabel, zlabel  


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def figure_add_trace(fig_json_serializable, data_for_plot, x_column, y_column, z_column, yfunc_column, zfunc_column, graph_type, dim_type, reg_type, reg_order):

    """
    Goal: Add a trace inside the figure regarding the inputs.

    Parameters:
    - fig_json_serializable: Dash figure.
    - data_for_plot: Dataframe which has been use to create the figure that is re-opened in this function.
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - yf_column: Function to operate on y_column with the rest of the dataframe
    - zf_column: Function to operate on z_column with the rest of the dataframe
    - graph_type: Type of Graphyque for the figure.
    - dim_type: Graphyque dimension for the figure.
    - reg_type: Type of regression for the data.
    - reg_order: Order of the regression for the data.

    Returns:
    - fig_json_serializable: Dash figure updated with the trace.
    - data_for_plot: Dataframe updated with the trace.
    """
    
    
    plotly_fig = go.Figure(fig_json_serializable)
    
    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]
    
    # Define a list of colors for the bars
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'] 
    
    x_axis = x_column
    y_axis = 'count'
    if x_column in df_col_string:
        x_axis = 'count'
        y_axis = x_column    
    
    print(x_axis,y_axis)    

    # Creating a DataFrame
    data_for_plot = pd.DataFrame(data_for_plot)
    
    # Resetting the index to have a clean index
    data_for_plot.reset_index(drop=True, inplace=True)

    
    if reg_type != "Savitzky-Golay Filter":

        Dict_regression_models = {'Linear Regression': lm.LinearRegression,
                  'Decision Tree': tree.DecisionTreeRegressor,
                  'k-NN': neighbors.KNeighborsRegressor,
                  'Polynomial Regression': lambda: make_pipeline(PolynomialFeatures(degree=reg_order), lm.LinearRegression())  # Use a lambda to return a new instance
                  }        

        # Instantiate the model
        model = Dict_regression_models[reg_type]()
        
        print("model=",model)
        
        X_reg = data_for_plot[[x_axis]]
        y_reg = data_for_plot[y_axis]
        
        print(X_reg)
        print(y_reg)
        # Fit the model
        model.fit(X_reg, y_reg)
        
        round_coef = 2
        # Get coefficients
        if reg_type == 'Linear Regression':
            # Output coefficients for Linear Regression
            print("Coefficients:", model.coef_)
            # rounded_coefs = [round(coef, round_coef) for coef in model.coef_]
            equation = format_coefs(model.coef_, reg_type)
        elif reg_type == 'Polynomial Regression':
            # Output coefficients for Polynomial Regression
            linear_model = model.named_steps['linearregression']
            # rounded_coefs = [round(coef, round_coef) for coef in linear_model.coef_]
            print("Coefficients:", linear_model.coef_)
            equation = format_coefs(linear_model.coef_, reg_type)
        
        
        # Make predictions (optional)
        predictions = model.predict(X_reg)
        
        # You can also view the predictions alongside the original DataFrame if desired
        data_for_plot['predicted_count'] = predictions   


        # Plotly figure with the original data and the regression line
        plotly_fig.add_trace(go.Scatter(
            x=data_for_plot[x_axis],
            y=data_for_plot['predicted_count'],
            mode='lines',
            name=reg_type if reg_type in ['Decision Tree','k-NN'] else equation,
            line=dict(color='red', width=2)  # Customizing line color and width
        ))
    
    else:
        
        window_lenght = len(data_for_plot[x_axis])//5
        print("window_lenght=",window_lenght)
        
        plotly_fig.add_trace(go.Scatter(
            x=data_for_plot[x_axis],
            y=signal.savgol_filter(data_for_plot[y_axis],
                                   window_lenght, # window size used for filtering
                                   reg_order), # order of fitted polynomial
            mode='lines',
            name=reg_type,
            line=dict(color='red', width=2)  # Customizing line color and width
        ))

        
    fig_json_serializable = plotly_fig.to_dict()
        
    plt.close()
    # =============================================================================
    print(colored("=============================================================================", "green"))
    
    return fig_json_serializable, data_for_plot.to_dict(orient='records') 


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def format_coefs(coefs, reg_type, x_variable='x'):
    round_coef = 2
    if reg_type == 'Linear Regression':
        # For linear regression, the equation is in the form: y = m*x + b
        equation = r"y = " + " + ".join([f"{coef:.{round_coef}f}*{x_variable}^{i}" if i > 0 
                                           else f"{coef:.{round_coef}f}" 
                                           for i, coef in enumerate(coefs)])
    elif reg_type == 'Polynomial Regression':
        # For polynomial regression, the equation is constructed similarly
        equation = r"y = " + " + ".join([f"{coef:.{round_coef}f}*{x_variable}^{i}" for i, coef in enumerate(coefs)])
    else:
        equation = "Unsupported regression type"
    return equation


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


# Function to group small values
def group_small_values(data, col, count_column, n):
    
    print(n)
    print(col)
    print(count_column)
    
    # # Get the top n values based on count
    # top_n = data.nlargest(n, count_column)[col].unique()
    
    # Group by genres and sum the counts
    grouped_data = data.groupby(col)[count_column].sum().reset_index()
    
    # Get the top n genres based on summed counts
    top_n_genres = grouped_data.nlargest(n, count_column)
    print(top_n_genres)
    
    # Extract the genres
    top_n = top_n_genres[col].unique()
    print(top_n)
    
    # Replace values not in top_n with "Other"
    data[col] = data[col].where(data[col].isin(top_n), 'Other')
    
    return data

"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def fig_update_layout(fig_json_serializable,figname,xlabel,ylabel,zlabel,x_column,g_column,d_column):

    """
    Goal: Update the layout of the dash figure.

    Parameters:
    - fig_json_serializable: Dash figure.
    - figname: The name of the Figure.
    - xlabel: The xlabel of the axis (can be None).
    - ylabel: The ylabel of the axis (can be None).
    - zlabel: The zlabel of the axis (can be None).
    - x_column: Column in the dataframe
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.

    Returns:
    - fig_json_serializable: Dash figure updated.
    """

    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]

    fig_json_serializable.update_layout(
        plot_bgcolor='#1e1e1e',  # Darker background for the plot area
        paper_bgcolor='#101820',  # Dark gray for the paper
        font=dict(color='white'),  # White text color
        # title = figname,
        # title_font=dict(size=20, color='white')
        )

    if x_column is not None and (d_column =="1D"or d_column =="2D") and g_column != 'Pie':
        fig_json_serializable.update_layout(
            plot_bgcolor='#1e1e1e',  # Darker background for the plot area
            paper_bgcolor='#101820',  # Dark gray for the paper
            font=dict(color='white'),  # White text color
            # title = figname,
            # title_font=dict(size=20, color='white'),  # Title styling
            xaxis=dict(
                # range=[0, 2000] if g_column == 'Histogram Movie' else None,
                title=dict(text=xlabel, font=dict(size=20, color='white')),  # X-axis label styling
                tickfont=dict(color='white', size=18),  # X-axis tick color
                tickangle=0,  # Rotate the x-axis labels for better readability
                showgrid=True,  # Grid styling
                gridcolor='gray',  # Grid color
                categoryorder='category ascending',  # Ensures categorical x-values are treated correctly
            ),
            yaxis=dict(
                title=dict(text=ylabel, font=dict(size=20, color='white')),  # Y-axis label styling
                tickfont=dict(color='white', size=18),  # Y-axis tick color
                tickangle=0,  # Rotate the x-axis labels for better readability
                showgrid=True,  # Grid styling
                gridcolor='gray',  # Grid color
                categoryorder='total ascending' if x_column in df_col_string else 'category ascending',  # Ensures categorical x-values are treated correctly
                
            )
            
        )
    elif x_column is not None and d_column =="3D":
        fig_json_serializable.update_layout(
            plot_bgcolor='#1e1e1e',  # Darker background for the plot area
            paper_bgcolor='#101820',  # Dark gray for the paper
            font=dict(color='white'),  # White text color
            # title = figname,
            # title_font=dict(size=20, color='white'),  # Title styling
            scene=dict(
                    xaxis=dict(
                        title=dict(text=xlabel, font=dict(size=18, color='white')),  # X-axis label styling
                        tickmode='array',
                        tickfont=dict(color='white', size=14),  # X-axis tick color
                        tickangle=0,  # Rotate the x-axis labels for better readability
                        showgrid=True,  # Grid styling
                        gridcolor='gray',  # Grid color
                        categoryorder='category ascending',  # Ensures categorical x-values are treated correctly
                    ),
                    yaxis=dict(
                        title=dict(text=ylabel, font=dict(size=18, color='white')),  # Y-axis label styling
                        tickmode='array',
                        tickfont=dict(color='white', size=14),  # Y-axis tick color
                        tickangle=0,  # Rotate the x-axis labels for better readability
                        showgrid=True,  # Grid styling
                        gridcolor='gray',  # Grid color
                        categoryorder='category ascending',  # Ensures categorical x-values are treated correctly
                    ),
                    zaxis=dict(
                        title=dict(text='Count', font=dict(size=18, color='white')),
                        tickmode='array',
                        tickfont=dict(color='white', size=14)  # Z-axis tick color
                    )
            )
        )
        
    if g_column == 'Colormesh':    

        # Update 3D scene options
        fig_json_serializable.update_scenes(
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode="manual"
        )
        
        # Add dropdowns
        button_layer_1_height = 1.08
        
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["colorscale", "Viridis"],
                        label="Viridis",
                        method="restyle"
                    ),
                    dict(
                        args=["colorscale", "Cividis"],
                        label="Cividis",
                        method="restyle"
                    ),
                    dict(
                        args=["colorscale", "Blues"],
                        label="Blues",
                        method="restyle"
                    ),
                    dict(
                        args=["colorscale", "Greens"],
                        label="Greens",
                        method="restyle"
                    ),
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=button_layer_1_height,
                yanchor="top"
            ),
            dict(
                buttons=list([
                    dict(
                        args=["reversescale", False],
                        label="False",
                        method="restyle"
                    ),
                    dict(
                        args=["reversescale", True],
                        label="True",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.37,
                xanchor="left",
                y=button_layer_1_height,
                yanchor="top"
            ),
            dict(
                buttons=list([
                    dict(
                        args=[{"contours.showlines": False, "type": "contour"}],
                        label="Hide lines",
                        method="restyle"
                    ),
                    dict(
                        args=[{"contours.showlines": True, "type": "contour"}],
                        label="Show lines",
                        method="restyle"
                    ),
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.58,
                xanchor="left",
                y=button_layer_1_height,
                yanchor="top"
            ),
        ]
    
        fig_json_serializable.update_layout(
        updatemenus=updatemenus
        )
        
        
    if g_column == 'Histogram Movie':
        fig_json_serializable.update_layout(
        margin=dict(l=150, r=20, t=20, b=20)
        )
        


    if d_column == "3D":
        name = 'default'
        # Default parameters which are used when `layout.scene.camera` is not provided
        camera = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.25, y=1.25, z=1.25)
        )
        
        fig_json_serializable.update_layout(scene_camera=camera) #, title=name
        
