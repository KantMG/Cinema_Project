
I have 

@app.callback(
    Output('stored-df1', 'data'),
    [Input(f'checkbox-{col}-tab-2', 'value') for col in List_col_tab2] +  # Each checkbox's value
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

    # Collect values from checkboxes
    checkbox_values = list(args[:len(List_col_tab2)])  # Get the values for checkboxes
        
    # Get x and y dropdown values
    x_dropdown_value = args[len(List_col_tab2)]  # x-dropdown value
    y_dropdown_value = args[len(List_col_tab2) + 1]  # y-dropdown value

    # Collect values from the filter  input
    filter_values = list(args[len(List_col_tab2)+2:-1])  # Get the values for checkboxes   
        
    # checkbox_values = list([[x_dropdown_value], [y_dropdown_value]]) + checkbox_values
    
    # Get the current active tab
    tab = args[-1]  # Get the current active tab
    
    # Print debug information
    print("Active Tab:", tab)
    print("Checkbox Values:", checkbox_values)
    print("X Dropdown Value:", x_dropdown_value)
    print("Y Dropdown Value:", y_dropdown_value)
    print("Filter Value:", filter_values)

    if tab == 'tab-2':
        if x_dropdown_value is None:
            print("X Dropdown Value is None, returning no update.")
            return dash.no_update  
        
        selected_columns = []
        selected_filter = []
        
        # Add x_dropdown_value if it's not already in checkbox_values
        if x_dropdown_value not in checkbox_values and x_dropdown_value not in selected_columns:
            selected_columns.append(x_dropdown_value)
            # Append None for the filter associated with x_dropdown_value
            selected_filter.append(None)
        
        # Add y_dropdown_value if it's not already in checkbox_values and not already added
        if y_dropdown_value not in checkbox_values and y_dropdown_value not in selected_columns:
            selected_columns.append(y_dropdown_value)
            # Append None for the filter associated with y_dropdown_value
            selected_filter.append(None)
        
        # Add values from checkbox_values that are not empty or duplicates
        for index, value in enumerate(checkbox_values):
            if value and value[0] not in selected_columns:  # Take the first value assuming it's a list with one item
                selected_columns.append(value[0])
                selected_filter.append(filter_values[index])
            
            if value and value[0] == x_dropdown_value :
                selected_filter[0] = filter_values[index]
            if value and value[0] == y_dropdown_value :
                selected_filter[1] = filter_values[index]

        print("Selected Columns:", selected_columns)  # Debugging output for selected columns
        print("Selected Filter:", selected_filter)
        
        # Call your open_dataframe function to get the data
        df1 = od.open_dataframe(selected_columns, selected_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        print(df1)
        df1.to_parquet('temp_store.parquet')  # Store the DataFrame
        return "Data loaded and saved."

    return dash.no_update


@app.callback(
    [Output(f'{col}-fig-dropdown-tab-2', 'options') for col in df_col_string],  # Rest of dropdowns
    [Input(f'checkbox-{col}-tab-2', 'value') for col in df_col_string] +
    [Input('tabs', 'value')],
    State('stored-df1-status', 'data')  # Adding state to check if df1 is loaded
)
def update_filter_dropdown_tab2(*args):
    print()
    print("--------- callback update_filter_dropdown_tab2 ---------")
    selected_boxes = args[:-1]
    selected_tab = args[-1]
    
    print(selected_boxes, selected_tab)
    if selected_tab == 'tab-2':
        if selected_boxes:
            print("No filters selected.")
            return []  # Return an empty options list if the DF is not ready
        print(f"Selected filter: {selected_boxes}")  # Additional debugging
        stored_df1 = dd.read_parquet('temp_store.parquet')
        return update_filter_dropdown_utility(selected_boxes, df_col_string, stored_df1)
    return []  # If not in the right tab




I want the callback update_stored_df1 do be done before update_filter_dropdown_tab2