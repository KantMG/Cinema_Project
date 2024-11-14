#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 14:59:12 2024

@author: quentin
"""



def data_preparation_for_plot(df_temp, x_column, y_column, z_column, f_column, g_column, Large_file_memory):

    """
    Goal: Get the pivot of the Count table of the dataframe.
    From a table of dimension x with n indexes to a table of dimension x+1 with n-1 index

    Parameters:
    - df_temp: dataframe which has been created temporary
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - f_column: Function to operate on df_temp[x_column,y_column]
    - g_column: Type of Graphyque for the figure.
    - Large_file_memory: Estimate if the file is too large to be open with panda and use dask instead.

    Returns:
    - Para: List of column in the dataframe (can be different of [x_column,y_column])
    - data_for_plot: Data to plot.
    - x_column: Column in the dataframe (it could have change)
    - y_column: Column in the dataframe (it could have change)
    - z_column: Column in the dataframe (it could have change)
    """

    # Columns in the dataframe which are strings and where the cell can contain multiple values.
    df_col_string = ["genres_split", "directors_split", "writers_split", "category_split"]

    # print("Delete the rows with unknown value and split the column with multiple value per cell.")
    Para, df_temp, x_column, y_column, z_column = delete_rows_unknow_and_split(df_temp, x_column, y_column, z_column, Large_file_memory)

    #Case where y_column is None
    if str(y_column)=='None':

        df_temp = df_temp[[Para[0]]]

        # Get the Count table of the dataframe  
        data_for_plot=df_temp.value_counts(dropna=False).reset_index(name='Count') #dropna=False to count nan value
        
        # sort the data in function of column Para_sorted
        data_for_plot = data_for_plot.sort_values(by=Para[0], ascending=True)

        # Remove rows where any column contains -1.0
        data_for_plot = data_for_plot[data_for_plot[Para[0]] != -1.0]

    #Case where y_column is not None
    elif str(y_column)!='None' and str(z_column)=='None':


        Pivot_table=fd.Pivot_table(df_temp,Para,False, True)
        
        print(Pivot_table)
        
        # Remove rows where any column contains -1.0
        if -1.0 in Pivot_table.index:
            Pivot_table = Pivot_table[Pivot_table.index != -1.0]
        # Remove columns where any row contains -1.0
        if -1.0 in Pivot_table.columns:
            Pivot_table = Pivot_table.drop(columns=[-1.0])
        
        if g_column == "Colormesh":
            first_n_top_amount_col = None
        else:
            first_n_top_amount_col = 5
        if str(f_column)=='None':
            if x_column not in df_col_string:
                data_for_plot = fd.highest_dataframe_sorted_by(Pivot_table, first_n_top_amount_col, Para[0])
            else:
                data_for_plot = Pivot_table.sort_values(by=['Total'], ascending=True)
        
        elif f_column=='Avg':
            # add new column which is th avg value of all the other column times the column name
            data_for_plot = fd.avg_column_value_index(Pivot_table)
            if x_column not in df_col_string:
                # sort the data in function of column Para_sorted
                data_for_plot.sort_index(ascending=True, inplace=True)  
            else:
                data_for_plot.sort_values(ascending=True)
                
    #Case where z_column is not None
    else:
                
        # Remove entries with negative value
        if x_column not in df_col_string:
            df_temp = df_temp[df_temp[x_column] >= 0]
        if y_column not in df_col_string:
            df_temp = df_temp[df_temp[y_column] >= 0]
        if z_column not in df_col_string:
            df_temp = df_temp[df_temp[z_column] >= 0]
        # Calculate average z_column and count for each (x_column, y_column) combination
        data_for_plot = df_temp.groupby([x_column, y_column]).agg(
            avg_z_column=('{}'.format(z_column), 'mean'),
            count=('{}'.format(z_column), 'size')
        ).reset_index()
        avg_col_name = 'avg_' + z_column
        data_for_plot.rename(columns={'avg_z_column': avg_col_name}, inplace=True)
            
    # print(data_for_plot)
    return Para, data_for_plot, x_column, y_column, z_column



def figure_plotly(plotly_fig, ax, x_column, y_column, z_column, f_column, g_column, d_column, Para, data_for_plot):

    """
    Goal: Create the plot inside the figure regarding the inputs.

    Parameters:
    - fig: matplotlib figure.
    - ax: axis of fig.
    - x_column: Column in the dataframe
    - y_column: Column in the dataframe (can be None)
    - z_column: Column in the dataframe (can be None)
    - f_column: Function to operate on df_temp[x_column,y_column]
    - g_column: Type of Graphyque for the figure.
    - d_column: Graphyque dimension for the figure.
    - Para: List of column in the dataframe (can be different of [x_column,y_column])
    - data_for_plot: Data to plot.

    Returns:
    - dropdowns_with_labels: The finalized dropdowns figure. 
    """
    # Convert the DataFrame index to a list
    if x_column not in df_col_string:
        x_values = list(map(int, data_for_plot.index))
    else:
        x_values = data_for_plot.index
    
    if str(f_column)=='None':
        bottom = np.zeros(len(data_for_plot.index))
        # Plot the stacked bar chart
        bars_list = []  # List to hold bar objects for the legend
        for i, (element_col, data_val) in enumerate(data_for_plot.items()):
            if g_column=="Histogram":
                bars = ax.bar(np.arange(len(x_values)), data_val, label=element_col, bottom=bottom, color=colors[i % len(colors)])  # Color assignment
            if g_column=="Curve":
                bars = ax.plot(np.arange(len(x_values)), data_val, label=element_col, linewidth=4., color=colors[i % len(colors)])
            if g_column=="Scatter":
                bars = ax.scatter(np.arange(len(x_values)), data_val, label=element_col, linewidth=4., color=colors[i % len(colors)])
            bars_list.append(bars)  # Store the bars
            bottom += data_val              
        # Create a custom legend using the bars created
        legend_handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors[:len(data_for_plot)]]
        legend_labels = data_for_plot.columns.tolist()  # Get the labels from DataFrame columns
        # Customize the legend to ensure it reflects the colors of the bars
        legend = ax.legend(legend_handles, legend_labels, ncol=2, handletextpad=0.001)
        # legend = ax.legend(ncol=2)
        for text in legend.get_texts():
            text.set_color('white')  # Set the color of the legend text
            text.set_fontsize(15)  # Set the font size of the legend text

    elif str(f_column) == "Avg":
        if g_column=="Histogram":
            ax.bar(np.arange(len(x_values)), data_for_plot)
        if g_column=="Curve":
            ax.plot(np.arange(len(x_values)), data_for_plot, linewidth=4.)
        if g_column=="Scatter":
            ax.scatter(np.arange(len(x_values)), data_for_plot, linewidth=4.)
            
            
            
            
def apply_filter(df, filters):
    
    """
    Goal: 
    - Apply the given filters to the DataFrame.
    
    Parameters:
    - df: DataFrame to filter
    - filters: Dictionary where keys are columns and values are filter conditions
    
    Returns:
    - df: Filtered DataFrame
    """    
    
    print("Apply filter.")
    if not filters:
        return df

    for col, filter_value in filters.items():
        print(col, filter_value)
        
        if filter_value is not None and filter_value != 'All':  
            
            if isinstance(filter_value, bool):
                # Handle boolean filters directly
                df = df[df[col] == filter_value]
                
            elif ">" in str(filter_value):
                # Handle greater than or equal filters (e.g., ">=7.0")
                threshold = float(filter_value.split(">")[1])
                df = df[df[col] > threshold]
            elif "<" in str(filter_value):
                # Handle less than or equal filters (e.g., "<=5.0")
                threshold = float(filter_value.split("<")[1])
                df = df[df[col] < threshold]
            elif ">=" in str(filter_value):
                # Handle greater than or equal filters (e.g., ">=7.0")
                threshold = float(filter_value.split(">=")[1])
                df = df[df[col] >= threshold]
            elif "<=" in str(filter_value):
                # Handle less than or equal filters (e.g., "<=5.0")
                threshold = float(filter_value.split("<=")[1])
                df = df[df[col] <= threshold]
            elif "=" in str(filter_value):
                # Handle equality filters (e.g., "=nm0005690")
                value = filter_value.split("=")[1]
                df = df[df[col] == value]
            elif isinstance(filter_value, str) and filter_value.endswith('*'):
                # Remove the asterisk and apply an exact match filter
                exact_value = filter_value[:-1]
                df = df[df[col] == exact_value]
            else:
                if 'All' in filter_value:
                    return df
                else:
                    # Check if 'value' is a list and apply the filter accordingly
                    if isinstance(filter_value, list):
                        # Use regex pattern to match any of the values in the list
                        pattern = '|'.join(map(re.escape, filter_value))  # Escape special characters to avoid regex issues
                        df = df[df[col].str.contains(pattern, na=False)]
                    else:
                        # Single value case, handle as before
                        df = df[df[col].str.contains(str(filter_value), na=False)]
            print(df[col])
    print()
    return df
    