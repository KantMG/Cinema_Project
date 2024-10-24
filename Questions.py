

I have a code which create with dash 3 tabs

tab 2 content

def tab2_content():
    print()
    print("=====================  Tab2_content  =========================")
    # Display dropdowns without loading data initially
    df1_placeholder = fd.df_empty(List_col_tab2, dtypes=List_dtype_tab2)    
    dropdowns_with_labels_for_fig_tab2 = fds.dropdown_figure(df1_placeholder, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style, Large_file_memory)
    dropdowns_with_labels_for_fig_filter_tab2 = fds.dropdown_figure_filter(df1_placeholder, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style)
    print("==================== End Tab2_content ========================")
    return html.Div([

        html.Div([
            fds.figure_position_checkboxes_dash('graph-output-tab-2',
                                     List_col_tab2,
                                     dropdowns_with_labels_for_fig_tab2,
                                     dropdowns_with_labels_for_fig_filter_tab2)
            
        ], style={'padding': '20px'})
                        
    ], style={'padding': '20px'})


I have many callback for tab2


# =============================================================================
# Callback for df1 in tab-2
# =============================================================================

@app.callback(
    Output('stored-df1', 'data'),
    [Input(f'checkbox-{col}', 'value') for col in List_col_tab2] +  # Each checkbox's value
    [Input('x-dropdown-tab-2', 'value'),  # x-axis dropdown
     Input('y-dropdown-tab-2', 'value')] +  # y-axis dropdown
    [Input(f'{col}-fig-dropdown-tab-2', 'value') for col in List_col_fig_tab2],  # Rest of dropdowns
    Input('tabs', 'value'),
    prevent_initial_call=True
)
def update_stored_df1(*args):
    print()
    print("------------ callback update_stored_df1 ------------")
    ctx = dash.callback_context
    if not ctx.triggered:  # If nothing has triggered the update, do nothing
        return dash.no_update

    # Get the current active tab
    tab = args[-1]  # Get the current active tab
    
    # Collect values from checkboxes
    checkbox_values = list(args[:len(List_col_tab2)])  # Get the values for checkboxes
    
    # Get x and y dropdown values
    x_dropdown_value = args[len(List_col_tab2)]  # x-dropdown value
    y_dropdown_value = args[len(List_col_tab2) + 1]  # y-dropdown value
        
    checkbox_values = list([[x_dropdown_value], [y_dropdown_value]]) + checkbox_values

    # Print debug information
    
    print("Active Tab:", tab)
    print("Checkbox Values:", checkbox_values)
    print("X Dropdown Value:", x_dropdown_value)
    print("Y Dropdown Value:", y_dropdown_value)

    if tab == 'tab-2':

        selected_columns = [
            value[0] for value in checkbox_values if value  # Check if the inner list is not empty
        ]  # This will include the first element of inner lists that are not empty
        
        # Manually append None if it exists in the inner lists
        # (since it’s treated as a separate case)
        if [None] in checkbox_values:
            selected_columns.append(None)
                
        # Optional: Check if any values are specifically None and handle those as well
        selected_columns = [
            col for col in selected_columns 
            if col is not None and col != ''
        ]

        if x_dropdown_value is None:
            print("X Dropdown Value is None, returning no update.")
            return dash.no_update    

        print("Selected Columns:", selected_columns)  # Debugging output for selected columns


        # Call your open_dataframe function to get the data
        df1 = od.open_dataframe(selected_columns, List_filter_tab2, Project_path, Large_file_memory, Get_file_sys_mem)

        return df1.to_dict('records')  # Convert DataFrame to a dictionary format for storing

    return dash.no_update


# =============================================================================
# Callback for graph in tab-2
# =============================================================================

@app.callback(
    Output('y-dropdown-tab-2', 'options'),
    Input('x-dropdown-tab-2', 'value'),
    Input('tabs', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df1', 'data')  # Use the correct state data for each tab
)
def update_y_dropdown_tab1(selected_x, selected_tab, stored_df1):
    print()
    print("---------- callback update_y_dropdown_tab1 ----------")
    print(selected_x, selected_tab)
    if selected_tab == 'tab-2':
        if stored_df1 is None:
            print("Stored DF1 is not ready yet.")
            return []  # Return an empty options list if the DF is not ready
        # Proceed to get options based on selected_x and stored_df1...

        print(f"Selected X: {selected_x}")  # Additional debugging
        # Logic to generate y options...
    return []  # If not in the right tab


@app.callback(
    Output('Func-dropdown-tab-2', 'options'),
    Input('y-dropdown-tab-2', 'value'),
    Input('tabs', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df1', 'data')
)
def update_func_dropdown_tab1(selected_y, selected_tab, stored_df1):
    print()
    print("-------- callback update_func_dropdown_tab1 --------")
    df_col_numeric = ["startYear", "runtimeMinutes", "averageRating", "numVotes"]
    if selected_tab == 'tab-2':
        return update_func_dropdown_utility(selected_y, df_col_numeric)
    return []

@app.callback(
    Output('graph-output-tab-2', 'figure'),
    [Input('x-dropdown-tab-2', 'value'),
     Input('y-dropdown-tab-2', 'value'),
     Input('Func-dropdown-tab-2', 'value'),
     Input('Graph-dropdown-tab-2', 'value'),
     Input('tabs', 'value')] + 
    [Input(f'checkbox-{col}', 'value') for col in List_col_fig_tab2],  # Dynamic checkbox inputs
    State('stored-df1', 'data')
)
def update_graph_tab2(*args):
    print()
    print("------------ callback update_graph_tab2 ------------")
    # Extract the necessary inputs from the arguments
    x_column, y_column, func_column, graph_type, selected_tab = args[:5]
    stored_df1 = args[-1]
    
    # Collecting selected values from checkboxes
    selected_values = [item for sublist in [args[i + 5] for i, value in enumerate(List_col_fig_tab2) if args[i + 5]] for item in sublist]
    # Check if we're in the correct tab and there is data available
    if selected_tab == 'tab-2':
        print(selected_values)
        if stored_df1 is None:
            print("Stored DF1 is not ready yet.")
            
    # Check if we're in the correct tab and there is data available
    if selected_tab == 'tab-2' and stored_df1:
        print(x_column, y_column, func_column, graph_type, stored_df1)
        return update_graph_utility(x_column, y_column, func_column, graph_type, selected_values, stored_df1, Large_file_memory)
    
    return go.Figure()  # Return a blank figure if not in the right tab



thanks to prevent_initial_call=True the callback update_stored_df1 should execute first and he did it.
however when it goes to the function

def open_dataframe(requested_columns, requested_filters, Project_path, Large_file_memory, Get_file_sys_mem):
    """
    Goal: 
    - Read and rename the DataFrame.
    
    Parameters:
    - requested_columns: List of columns to extract from the DataFrame located in several file.
    - requested_filters: List of filter to apply on each column.
    - Project_path: Path of the tsv file.
    - Large_file_memory: Estimate if the file is too large to be open with panda and use dask instead.
    - Get_file_sys_mem: Estimate the memory consuming by the files.
    
    Returns:
    - df: DataFrame
    """
    
    print("      ----- open_dataframe -----")
    start_time = time.time()  
        
    # Define the mapping of files to their columns and their types
    file_columns_mapping_dtype = file_columns_dtype()
    file_columns_mapping = {k: v for k, v in file_columns_mapping_dtype.items() if k != 'name.basics.tsv'}
    
    # Create a dictionary to map each requested column to its filter
    column_filter_mapping = dict(zip(requested_columns, requested_filters))
    
    # Determine which files need to be opened
    files_to_open = []
    columns_in_files = {}
    
    # Iterate through each file and check if it has any of the requested columns
    for file, info in file_columns_mapping.items():
        columns = info["columns"]
        types = info["types"]
        
        # Find the intersection of requested columns and columns in the current file
        common_columns = set(requested_columns).intersection(columns)
        if common_columns:  # Only consider files that have at least one requested column
            files_to_open.append(file)

            # Handle renaming if it's the 'title.akas.tsv' file
            if file == 'title.akas.tsv' and "titleId" in common_columns:
                common_columns.discard("titleId")  # Remove 'titleId'
                common_columns.add("tconst")  # Add 'tconst' instead

            # Track the columns that should be used from this file, always including 'tconst' if present
            if "tconst" in columns or (file == 'title.akas.tsv' and "titleId" in columns):
                common_columns.add("tconst")

            columns_in_files[file] = {
                "columns": common_columns,
                "types": {("tconst" if col == "titleId" else col): types[col] for col in common_columns if col in types},
                "filters": {("tconst" if col == "titleId" else col): column_filter_mapping[col] for col in common_columns if col in column_filter_mapping},
                "rename": info.get("rename", {})
            }
    
    # Identify common columns between files to be opened
    if len(files_to_open) > 1:
        # Find common columns among all files using set intersection
        common_columns_all_files = set.intersection(*(columns_in_files[file]["columns"] for file in files_to_open))
    else:
        common_columns_all_files = set(columns_in_files[files_to_open[0]]["columns"])
    
    # Ensure 'tconst' is added as a common column if at least two files are being opened and 'tconst' exists in those files
    tconst_in_files = all("tconst" in file_columns_mapping[file]["columns"] for file in files_to_open)
    if len(files_to_open) > 1 and tconst_in_files:
        common_columns_all_files.add("tconst")
    
    print("Files to open:", files_to_open)
    print("Common columns across all selected files:", common_columns_all_files)
    
    print("Columns, filters, and types in each selected file:")
    for file, info in columns_in_files.items():
        print(f"{file}:")
        print("  Columns:", info["columns"])
        print("  Filters:", info["filters"])
        print("  Types:", info["types"])

    

    # Create DataFrames based on the files, columns, and filters
    dataframes = []
    for file, info in columns_in_files.items():
        # Define the columns to read from the file
        usecols = list(info["columns"])
        # Ensure 'titleId' is used instead of 'tconst' in the akas file
        if 'tconst' in usecols and file == 'title.akas.tsv':
            usecols.remove('tconst')
            usecols.append('titleId')

        # Create a dictionary to define the dtypes for the DataFrame
        dtype_mapping = {col: info["types"][col] for col in usecols if col in info["types"]}       
        
        print("Will read tsv")
        
        # Read the file into a DataFrame
        filepath = f"{Project_path}/{file}"
        # Log the time taken for each file reading
        file_start_time = time.time()
        df = read_and_rename(
            filepath,
            usecols,
            dtype_mapping,
            rename_map=info.get("rename"),
            large_file=Large_file_memory
        )
        print("Have read tsv")
       # Convert columns to the specified types
        for col, expected_type in info["types"].items():
            if expected_type == float:
                if Large_file_memory:
                    df[col] = dd.to_numeric(df[col], errors='coerce')
                    # Handle NA values
                    df[col] = df[col].fillna(-1)  # Fill with -1 or another value as necessary                    
                    # na_count = df[col].isna().sum().compute()  # Evaluate the count
                    # print(f"NA count in '{col}': {na_count}")
                # df[col] = df[col].astype('Int64')  # Use 'Int64' for nullable integers
            elif expected_type == str:
                df[col] = df[col].fillna('')  # Fill NaN with empty string for string columns

        
        # desired_number_of_partitions = 4
        # df=df.repartition(npartitions=desired_number_of_partitions)
        
        # Get the infos on the DataFrame
        dis.infos_on_data(df) if Get_file_sys_mem==True else None
                
        # Log the time taken to apply filters
        df = apply_filter(df, info["filters"])
        log_performance(f"Read {file}", file_start_time)
                
        # Add the DataFrame to the list
        dataframes.append(df)
            
    print()
    print("Time taken to load all dataframe: {:.2f} seconds".format(time.time() - start_time))        
    print()

    # Log the time taken to merge DataFrames
    merge_start_time = time.time()    
    # Merge Dask DataFrames on 'tconst' to create a single unified DataFrame
    if len(dataframes) > 1:
        i = 0
        merged_df = dataframes[i].compute()
        print()
        print("Time taken to compute dataframe "+str(i)+": {:.2f} seconds".format(time.time() - start_time))
        print()
        for df in dataframes[1:]:
            i+=1
            df = df.compute()
            
            if "category" in df.columns:
                # Group by 'tconst' and 'nconst' and join the 'category' values
                df = df.groupby(['tconst', 'nconst'], as_index=False).agg({
                    'category': ', '.join,  # Combine categories
                    'characters': 'first'   # Keep the first non-empty value from characters (if any)
                })
            
            merged_df = dd.merge(merged_df, df, on='tconst', how='inner')
            print()
            print("Time taken to merge dataframe "+str(i)+": {:.2f} seconds".format(time.time() - start_time))
            print()
            # print(df.head(50))
    else:
        merged_df = dataframes[0]
    log_performance("Merging DataFrames", merge_start_time)
    
    # Print the final merged DataFrame (head only, to avoid loading too much data)
    print("\nFinal Merged DataFrame:")
    print(merged_df.head(100))
    print(merged_df)
    print()
    print("Time taken to merge all dataframe: {:.2f} seconds".format(time.time() - start_time))
    print()
    print("      --- end open_dataframe ---")
    print()
    log_performance("Complete open_data", start_time)
    
    return merged_df.compute()

it seems that when it starts to read the tsv file the callback of update_graph_tab2 starts
as shown by the print
------------ callback update_stored_df1 ------------
Active Tab: tab-2
Checkbox Values: [['startYear'], [None], [], [], [], [], [], [], [], []]
X Dropdown Value: startYear
Y Dropdown Value: None
Selected Columns: ['startYear']
      ----- open_dataframe -----
Files to open: ['title.basics.tsv']
Common columns across all selected files: {'tconst', 'startYear'}
Columns, filters, and types in each selected file:
title.basics.tsv:
  Columns: {'tconst', 'startYear'}
  Filters: {'startYear': None}
  Types: {'tconst': <class 'str'>, 'startYear': <class 'float'>}
Will read tsv

---------- callback update_y_dropdown_tab1 ----------
startYear tab-2
Stored DF1 is not ready yet.

------------ callback update_graph_tab2 ------------
[]
Stored DF1 is not ready yet.
Have read tsv
Apply filter.
startYear None

Read title.basics.tsv took 0.02 seconds

Time taken to load all dataframe: 0.02 seconds

Merging DataFrames took 0.00 seconds

Final Merged DataFrame:
       tconst  startYear
0   tt0000001     1894.0
1   tt0000002     1892.0
2   tt0000003     1892.0
3   tt0000004     1892.0
4   tt0000005     1893.0
..        ...        ...
95  tt0000097     1896.0
96  tt0000098     1896.0
97  tt0000099     1896.0
98  tt0000100     1896.0
99  tt0000101     1896.0

[100 rows x 2 columns]
Dask DataFrame Structure:
               tconst startYear
npartitions=1                  
               object   float64
      ...
Dask Name: assign, 10 graph layers

Time taken to merge all dataframe: 0.05 seconds

      --- end open_dataframe ---

Complete open_data took 0.05 seconds