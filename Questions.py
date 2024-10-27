
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
        
    # Content Div for Tabs
    html.Div(id='tabs-content')
])

# Callback to manage tab content
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'),
    State('stored-df1', 'data')
)
def render_content(tab, stored_df1):
    if tab == 'tab-1':
        # Placeholder for Tab 3 content
        return html.Div([
            html.H1("THE SEVENTH ART, A STORY OF INFLUENCE", style={"color": "#FFD700"}, className="text-light"),
            tab1_content()
        ])
    elif tab == 'tab-2':
        # Placeholder for Tab 2 content
        return html.Div([
            html.H1("Graphic interface dedicated to the dataframe related to the overall IMDB database.", style={"color": "#FFD700"}, className="text-light"),
            tab2_content()
        ])


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

tab = 'tab-2'
List_col_tab2 = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes"]
List_filter_tab2 = [None, None, None, None, None, None, None, None]
List_dtype_tab2 = [float, float, str, float, str, str, float, float]


def tab2_content():
    print()
    print("=====================  Tab2_content  =========================")
    # Display dropdowns without loading data initially
    df1_placeholder = fd.df_empty(List_col_tab2, dtypes=List_dtype_tab2)    
    dropdowns_with_labels_for_fig_tab2 = fds.dropdown_figure(df1_placeholder, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style, Large_file_memory)
    dropdowns_with_labels_for_fig_filter_tab2 = fds.dropdown_checkboxes_figure_filter(df1_placeholder, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style)
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


# Create a list of Input objects for each dropdown
List_col_fig_tab2 = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes"]
dropdown_inputs_fig_tab2 = [Input(f'{col}-fig-dropdown-'+tab, 'value') for col in List_col_fig_tab2]
df_col_numeric = ["startYear", "runtimeMinutes", "averageRating", "numVotes"]
df_col_string = ["genres", "directors", "writers"]

# =============================================================================
# Callback for df1 in tab-2
# =============================================================================

@app.callback(
    Output('stored-df1', 'data'),
    [Input(f'checkbox-{col}-tab-2', 'value') for col in List_col_tab2] +  # Each checkbox's value
    [Input('x-dropdown-tab-2', 'value'),  # x-axis dropdown
     Input('y-dropdown-tab-2', 'value')] +  # y-axis dropdown
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
    
    # Collect values from checkboxes
    checkbox_values = list(args[:len(List_col_tab2)])  # Get the values for checkboxes
        
    # Get x and y dropdown values
    x_dropdown_value = args[len(List_col_tab2)]  # x-dropdown value
    y_dropdown_value = args[len(List_col_tab2) + 1]  # y-dropdown value

    # Collect values from the filter  input
    filter_values = list(args[len(List_col_tab2)+2:-1])  # Get the values for checkboxes   
            
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


"""#=============================================================================
   #=============================================================================
   #============================================================================="""

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
    graph_type = ["Histogram", "Curve"]
    
    # Get the list of axis and graph function
    axis = ["x", "y", "Func", "Graph"]

    # Define a consistent style for both input and dropdown elements
    uniform_style = {
        'width': '160px',  # Set a consistent width
        'height': '40px',  # Set a consistent width
        'borderRadius': '5px',  # Optional: Add rounded corners
    }

    # Create the dropdowns for each column
    dropdowns_with_labels = []
    for axi in axis:
        if axi == 'Graph':
            # Get unique values and sort them
            dropdown_with_label = html.Div([
                html.Label(f'Select a {axi} type'),  # Label for the dropdown
                dcc.Dropdown(
                    id=f'{axi}-dropdown-'+tab,
                    options=[{'label': val, 'value': val} for val in graph_type],
                    # value='Histogram',  # Set default to "All", meaning no filtering
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
                    style={**dark_dropdown_style, **uniform_style},  # Apply dark theme style
                    className='dash-dropdown'  # Add custom class to target with CSS
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically

        dropdowns_with_labels.append(dropdown_with_label)

        
    return dropdowns_with_labels


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def dropdown_checkboxes_figure_filter(df, id_graph, tab, dark_dropdown_style, uniform_style):
    
    columns = df.columns
    
    # Calculate widths, ensuring 'title' is handled specifically
    column_widths = {col: get_max_width(df[col], col) for col in columns}
    
    # Create dropdowns with checkboxes using calculated widths
    dropdowns_with_labels_and_checkboxes = []
    for col in columns:
        dtype = df[col].dtype
        # dropdown_style = {**dark_dropdown_style, **uniform_style, 'width': f'{column_widths[col]}px'}
        dropdown_style = {**dark_dropdown_style, **uniform_style}
        # Define whether to use dropdown or input based on the data type
        if dtype == "float64":
            input_component = dcc.Input(
                id=f'{col}-fig-dropdown-'+tab,
                type='text',
                debounce=True,
                style=dropdown_style
            )
        else:
            # Collect all unique values, ensuring uniqueness
            all_roles = set()
            for value in df[col].dropna().unique():
                roles = [role.strip() for role in str(value).split(',')]
                all_roles.update(roles)
            unique_values = sorted(all_roles)
            
            input_component = dcc.Dropdown(
                id=f'{col}-fig-dropdown-'+tab,
                options=[{'label': val, 'value': val} for val in unique_values],
                style=dropdown_style,
                className='dash-dropdown',
                multi=True
            )
        
        # Add a div that includes the checkbox and the input component
        dropdown_with_checkbox = html.Div([
            html.Label(f'{col}'),
            dcc.Checklist(
                id=f'checkbox-{col}-'+tab,
                options=[{'label': '', 'value': col}],
                value=[],  # Empty by default
                style={'display': 'inline-block', 'verticalAlign': 'middle'}
            ),
            input_component
        ], style={'display': 'inline-block', 'width': f'{column_widths[col] + 60}px', 'padding': '0 5px'}) # Adjusted width for checkbox
        
        dropdowns_with_labels_and_checkboxes.append(dropdown_with_checkbox)

    return dropdowns_with_labels_and_checkboxes

when I go to tab-2 I got the output

=====================  Tab2_content  =========================
Div(children=[Label('Select x'), Dropdown(options=[{'label': 'startYear', 'value': 'startYear'}, {'label': 'runtimeMinutes', 'value': 'runtimeMinutes'}, {'label': 'genres', 'value': 'genres'}, {'label': 'isAdult', 'value': 'isAdult'}, {'label': 'directors', 'value': 'directors'}, {'label': 'writers', 'value': 'writers'}, {'label': 'averageRating', 'value': 'averageRating'}, {'label': 'numVotes', 'value': 'numVotes'}], style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, className='dash-dropdown', id='x-dropdown-tab-2')], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})

Div(children=[Label('Select y'), Dropdown(options=[{'label': 'startYear', 'value': 'startYear'}, {'label': 'runtimeMinutes', 'value': 'runtimeMinutes'}, {'label': 'genres', 'value': 'genres'}, {'label': 'isAdult', 'value': 'isAdult'}, {'label': 'directors', 'value': 'directors'}, {'label': 'writers', 'value': 'writers'}, {'label': 'averageRating', 'value': 'averageRating'}, {'label': 'numVotes', 'value': 'numVotes'}], style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, className='dash-dropdown', id='y-dropdown-tab-2')], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})

Div(children=[Label('Select Func on y'), Dropdown(options=[{'label': 'Avg', 'value': 'Avg'}], style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, className='dash-dropdown', id='Func-dropdown-tab-2')], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})

Div(children=[Label('Select a Graph type'), Dropdown(options=[{'label': 'Histogram', 'value': 'Histogram'}, {'label': 'Curve', 'value': 'Curve'}], style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, className='dash-dropdown', id='Graph-dropdown-tab-2')], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})

Div(children=[Label('startYear'), Checklist(options=[{'label': '', 'value': 'startYear'}], value=[], style={'display': 'inline-block', 'verticalAlign': 'middle'}, id='checkbox-startYear-tab-2'), Input(type='text', debounce=True, style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, id='startYear-fig-dropdown-tab-2')], style={'display': 'inline-block', 'width': '60px', 'padding': '0 5px'})

Div(children=[Label('runtimeMinutes'), Checklist(options=[{'label': '', 'value': 'runtimeMinutes'}], value=[], style={'display': 'inline-block', 'verticalAlign': 'middle'}, id='checkbox-runtimeMinutes-tab-2'), Input(type='text', debounce=True, style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, id='runtimeMinutes-fig-dropdown-tab-2')], style={'display': 'inline-block', 'width': '60px', 'padding': '0 5px'})

Div(children=[Label('genres'), Checklist(options=[{'label': '', 'value': 'genres'}], value=[], style={'display': 'inline-block', 'verticalAlign': 'middle'}, id='checkbox-genres-tab-2'), Dropdown(options=[], multi=True, style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, className='dash-dropdown', id='genres-fig-dropdown-tab-2')], style={'display': 'inline-block', 'width': '60px', 'padding': '0 5px'})

Div(children=[Label('isAdult'), Checklist(options=[{'label': '', 'value': 'isAdult'}], value=[], style={'display': 'inline-block', 'verticalAlign': 'middle'}, id='checkbox-isAdult-tab-2'), Input(type='text', debounce=True, style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, id='isAdult-fig-dropdown-tab-2')], style={'display': 'inline-block', 'width': '60px', 'padding': '0 5px'})

Div(children=[Label('directors'), Checklist(options=[{'label': '', 'value': 'directors'}], value=[], style={'display': 'inline-block', 'verticalAlign': 'middle'}, id='checkbox-directors-tab-2'), Dropdown(options=[], multi=True, style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, className='dash-dropdown', id='directors-fig-dropdown-tab-2')], style={'display': 'inline-block', 'width': '60px', 'padding': '0 5px'})

Div(children=[Label('writers'), Checklist(options=[{'label': '', 'value': 'writers'}], value=[], style={'display': 'inline-block', 'verticalAlign': 'middle'}, id='checkbox-writers-tab-2'), Dropdown(options=[], multi=True, style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, className='dash-dropdown', id='writers-fig-dropdown-tab-2')], style={'display': 'inline-block', 'width': '60px', 'padding': '0 5px'})

Div(children=[Label('averageRating'), Checklist(options=[{'label': '', 'value': 'averageRating'}], value=[], style={'display': 'inline-block', 'verticalAlign': 'middle'}, id='checkbox-averageRating-tab-2'), Input(type='text', debounce=True, style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, id='averageRating-fig-dropdown-tab-2')], style={'display': 'inline-block', 'width': '60px', 'padding': '0 5px'})

Div(children=[Label('numVotes'), Checklist(options=[{'label': '', 'value': 'numVotes'}], value=[], style={'display': 'inline-block', 'verticalAlign': 'middle'}, id='checkbox-numVotes-tab-2'), Input(type='text', debounce=True, style={'backgroundColor': '#1e1e1e', 'color': '#f8f9fa', 'border': '1px solid #555', 'borderRadius': '5px', 'width': '160px', 'height': '40px'}, id='numVotes-fig-dropdown-tab-2')], style={'display': 'inline-block', 'width': '60px', 'padding': '0 5px'})

==================== End Tab2_content ========================
Dash Callback Context: <dash._callback_context.CallbackContext object at 0x7f75c9b7dcf0>
------------ callback update_stored_df1 ------------
Triggered component: x-dropdown-tab-2

Active Tab: tab-2
Checkbox Values: [[], [], [], [], [], [], [], []]
X Dropdown Value: None
Y Dropdown Value: None
Filter Value: [None, None, None, None, None, None, None, None]
X Dropdown Value is None, returning no update.

-------- callback update_func_dropdown_tab2 --------
Stored DF1 is not ready yet.

---------- callback update_y_dropdown_tab2 ----------
None tab-2
Stored DF1 is not ready yet.

------------ callback update_graph_tab2 ------------
Active Tab: tab-2
Stored DF1 is not ready yet.

--------- callback update_filter_dropdown_tab2 ---------
[[], [], []] tab-2
No filters selected.


it gives me the error when it goes to tab-1
A nonexistent object was used in an `Input` of a Dash callback. The id of this object is `checkbox-startYear-tab-2` and the property is `value`. The string ids in the current layout are: [tabs, tabs-1, tabs-2, tabs-3, stored-df1, stored-df2, tabs-content]
It is true for all the callback, which are all created in tab2_content()

 @app.callback(
    Output('stored-df1', 'data'),
    [Input(f'checkbox-{col}-tab-2', 'value') for col in List_col_tab2] +  # Each checkbox's value
    [Input('x-dropdown-tab-2', 'value'),  # x-axis dropdown
     Input('y-dropdown-tab-2', 'value')] +  # y-axis dropdown
    [Input(f'{col}-fig-dropdown-tab-2', 'value') for col in List_col_fig_tab2],  # Rest of dropdowns
    Input('tabs', 'value')
)

 
except 'tabs'
