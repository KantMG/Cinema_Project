My code is :


# Initialize the Dash app with suppress_callback_exceptions set to True
app, dark_dropdown_style, uniform_style = wis.web_interface_style()

app.layout = html.Div([
    # Tabs Component
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(id='tabs-1', label='🏠 Home', value='tab-1', 
                 style={
                     'backgroundColor': '#000000',  # Dark black background
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                     'position': 'relative'  # Relative position for pseudo-element
                 },
                 selected_style={
                     'backgroundColor': '#222222',  # Slightly lighter for selected tab
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                 }),
        dcc.Tab(id='tabs-2', label='📈 Analytics', value='tab-2', 
                 style={
                     'backgroundColor': '#000000',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                     'position': 'relative'
                 },
                 selected_style={
                     'backgroundColor': '#222222',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                 }),
        dcc.Tab(id='tabs-3', label='🎥 Movies & Artists', value='tab-3', 
                 style={
                     'backgroundColor': '#000000',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                     'position': 'relative'
                 },
                 selected_style={
                     'backgroundColor': '#222222',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                 }),
    ]),
    
    # Hidden store to hold df1 data
    dcc.Store(id='stored-df1', data=None),
    
    # Hidden store to hold df2 data
    dcc.Store(id='stored-df2', data=None),

    # Hidden store for input values
    dcc.Store(id='input-storage', data={}),  # New store to handle input states
            
    # Content Div for Tabs
    html.Div(id='tabs-content')
])

# Callback to manage tab content
@app.callback(
    Output('tabs-content', 'children'),
    Output('input-storage', 'data'),
    Input('tabs', 'value'),
    State('stored-df1', 'data')
)
def render_content(tab, stored_df1):
    if tab == 'tab-1':
        # Placeholder for Tab 3 content
        return html.Div([
            html.H1("THE SEVENTH ART, A STORY OF INFLUENCE", style={"color": "#FFD700"}, className="text-light"),
            tab1_content()
        ]), {}
    elif tab == 'tab-2':
        # Placeholder for Tab 2 content
        return html.Div([
            html.H1("Graphic interface dedicated to the dataframe related to the overall IMDB database.", style={"color": "#FFD700"}, className="text-light"),
            tab2_content()
        ]), {}
    elif tab == 'tab-3':
        return html.Div([
            html.Div([
                html.H1("Research on an artist or a movie.", style={"color": "#FFD700"}, className="text-light"),
            ]),
            dcc.Input(id='input-value', type='text', placeholder='Enter a value...', style={**dark_dropdown_style, **uniform_style}),
            html.Div(id='dynamic-content')
        ]), {}



# =============================================================================
# =============================================================================
# =============================================================================
# Tab-1
# =============================================================================
# =============================================================================
# =============================================================================


def tab1_content():

    # Source for data set : 
    source_data = 'https://developer.imdb.com/non-commercial-datasets/'
    
    # Save the project on github with: !bash ./save_project_on_git.sh
    GitHub_adress= 'https://github.com/KantMG/Cinema_Project'
    
    Text1 = f"THIS PROJECT ENLIGHT THE EVOLUTION OVER THE YEARS OF THE MOVIE AND SERIE MAKING."
    Text2 = f"THE ADAPTATION OF THE WAY OF PRODUCTION AS WELL AS OUR WAY OF CONSOMATION ARE ANALYSED."
    Text3 = f"HOW MUCH THE COUNTRIES ARE INVESTING IN THE FILMS PRODUCTION AND WHICH IS THE LEVEL OF INFLUENCE OF A COUNTRY OVER THE OTHERS."
    
    Text4 = f"The IMDb Non-Commercial Datasets has been used to perform this study, the open source can be find here: "+source_data
    Text5 = f"It corresponds to a multiple variety of tab-separated-values (TSV) formatted files in the UTF-8 character set. "
    Text6 = f"The "
    
    return html.Div([
        html.Div([
            html.P(Text1),
            html.P(Text2),
            html.P(Text3),
        ]),
        html.Div([
            html.P(Text4),
            html.P(Text5),
            html.P(Text6),
        ]),        
        ], style={'padding': '20px'})


# =============================================================================
# =============================================================================
# =============================================================================
# Tab-2
# =============================================================================
# =============================================================================
# =============================================================================

def tab2_content():
    print()
    print("=====================  Tab2_content  =========================")
    # Display dropdowns without loading data initially
    df1_placeholder = fd.df_empty(List_col_tab2, dtypes=List_dtype_tab2)    
    dropdowns_with_labels_for_fig_tab2 = dropdown_figure(df1_placeholder, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style, Large_file_memory)
    dropdowns_with_labels_for_fig_filter_tab2 = dropdown_checkboxes_figure_filter(df1_placeholder, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style)
    for c in dropdowns_with_labels_for_fig_tab2:
        print(c)  # This prints the entire component dictionary to check its structure
        print()
    for d in dropdowns_with_labels_for_fig_filter_tab2:
        print(d)  # This prints the entire component dictionary to check its structure
        print()
    print("==================== End Tab2_content ========================")

    return html.Div([

        html.Div([
            fds.figure_position_dash('graph-output-tab-2',
                                     dropdowns_with_labels_for_fig_tab2,
                                     dropdowns_with_labels_for_fig_filter_tab2)
            
        ], style={'padding': '20px'})
                        
    ], style={'padding': '20px'})

# =============================================================================
# Callback for df1 in tab-2
# =============================================================================

@app.callback(
    Output('stored-df1', 'data'),
    [Input('x-dropdown-tab-2', 'value'),  # x-axis dropdown
     Input('y-dropdown-tab-2', 'value'),  # y-axis dropdown
     Input('z-dropdown-tab-2', 'value')] +  # z-axis dropdown
    [Input(f'checkbox-{col}-tab-2', 'value') for col in List_col_tab2] +  # Each checkbox's value
    [Input(f'{col}-fig-dropdown-tab-2', 'value') for col in List_col_fig_tab2],  # Rest of dropdowns
    Input('tabs', 'value')
)
def update_stored_df1(*args):

    ctx = dash.callback_context
    print("Dash Callback Context:", ctx)
    if not ctx.triggered:  # If nothing has triggered the update, do nothing
        return dash.no_update
    
    print("------------ callback update_stored_df1 ------------")
    # Print out which component triggered the callback for debugging
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Triggered component:", triggered_id)
    print()

    # Get x and y dropdown values
    x_dropdown_value = args[0]  # x-dropdown value
    y_dropdown_value = args[1]  # y-dropdown value
    z_dropdown_value = args[2]  # z-dropdown value

    # Collect values from checkboxes
    checkbox_values = list(args[3:3+len(List_col_tab2)])  # Get the values for checkboxes
    
    # Collect values from the filter  input
    filter_values = list(args[len(List_col_tab2)+3:-1])  # Get the values for checkboxes   
            
    # Get the current active tab
    tab = args[-1]  # Get the current active tab
    
    # Print debug information
    print("Active Tab:", tab)
    print("X Dropdown Value:", x_dropdown_value)
    print("Y Dropdown Value:", y_dropdown_value)
    print("Z Dropdown Value:", z_dropdown_value)
    print("Checkbox Values:", checkbox_values)
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
        # Check if the folder exists
        if os.path.exists(folder_path):
            # Remove the folder and all its contents
            shutil.rmtree(folder_path)
            print(f"Successfully removed the folder: {folder_path}")
        else:
            print(f"The folder does not exist: {folder_path}")
        df1.to_parquet('temp_df1.parquet')  # Store the DataFrame
        return "Data loaded and saved."

    return dash.no_update



def dropdown_figure(df, id_graph, tab, dark_dropdown_style, uniform_style, Large_file_memory):

    """
    Goal: Create the dropdown associated to a figure.

    Parameters:
    - df: dataframe.
    - dark_dropdown_style: Color style of the dropdown.
    - Large_file_memory: Estimate if the file is too large to be open with panda.

    Returns:
    - dropdowns_with_labels: The finalized dropdowns figure. 
    """

    # Get column names
    columns = df.columns
    
    # Get the list of y function
    function_on_y = ["Avg"]
    
    # Get the type of graph
    graph_type = ["Histogram", "Curve", "Scatter"]

    # Get the graph dimension
    dim_type = ["1D", "2D", "3D"]
    
    # Get the list of axis and graph function
    axis = ["x", "y", "z", "Func", "Graph", "Dim"]


    # Define a consistent style for both input and dropdown elements
    uniform_style = {
        'width': '160px',  # Set a consistent width
        'height': '40px',  # Set a consistent width
        'borderRadius': '5px',  # Optional: Add rounded corners
    }

    # Create the dropdowns for each column
    dropdowns_with_labels = []
    for axi in axis:
        if axi == 'Dim':
            # Get unique values and sort them
            dropdown_with_label = html.Div([
                html.Label(f'Select graph {axi}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in dim_type],
                    value='1D',  # Set default to "All", meaning no filtering
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        elif axi == 'Graph':
            # Get unique values and sort them
            dropdown_with_label = html.Div([
                html.Label(f'Select a {axi} type'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in graph_type],
                    value='Histogram',  # Set default to "All", meaning no filtering
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        elif axi == 'Func':
            # Get unique values and sort them
            dropdown_with_label = html.Div([
                html.Label(f'Select {axi} on y'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in function_on_y],
                    # value='All',  # Set default to "All", meaning no filtering
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        elif axi== 'z':
            dropdown_with_label = html.Div([
                html.Label(f'Select {axi}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in columns],  #[{'label': 'None', 'value': 'None'}] + 
                   style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        elif axi== 'y':
            dropdown_with_label = html.Div([
                html.Label(f'Select {axi}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in columns],  #[{'label': 'None', 'value': 'None'}] + 
                   style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        else:
            dropdown_with_label = html.Div([
                html.Label(f'Select {axi}'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in columns],
                    value=None,
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically

        dropdowns_with_labels.append(dropdown_with_label)

        
    return dropdowns_with_labels


The output when I run, it send me to tab-1:
It give me back only in dash interface the error:
A nonexistent object was used in an `Input` of a Dash callback. The id of this object is `x-dropdown-tab-2` and the property is `value`. The string ids in the current layout are: [tabs, tabs-1, tabs-2, tabs-3, stored-df1, stored-df2, input-storage, tabs-content]

Since I create the id x-dropdown-tab-2, y-dropdown-tab-2,etc only in tab2_content() with the function dropdown_figure,
 it seems that on the initial load when tab-1 is active i need to have the id for all these dropdown. Can I just create some fake id and when I go tab-2 it works normally
