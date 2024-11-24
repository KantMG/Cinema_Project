

I create with the function

button_subplot_tab2 = fds.button_modal_subplot_creation("subplot-"+tab,  "Subplot creation", 
                                                                 "Number of subplot", "Number of rows", "Number of columns",
                                                                 "Configuration of the subplot figure", dark_dropdown_style, uniform_style)

some button like 
def button_modal_subplot_creation(id_subname, text_button, placeholder_input_1, placeholder_input_2, placeholder_input_3,
                               text_modal, dark_dropdown_style, uniform_style):

    """
    Goal: Create a button which give access to a modal.
    The modal contains a dropdown and an input with a submit button.

    Parameters:
    - id_subname: Part of all the id name associated with this button modal.
    - text_button: Text on the button.
    - placeholder_input_1: Text inside the input without content.
    - placeholder_input_2: Text inside the input without content.
    - placeholder_input_3: Text inside the input without content.
    - text_modal: Text at the Head of the modal.
    - dark_dropdown_style: Color style of the dropdown.
    - uniform_style: Color style of the dropdown.

    Returns:
    - The finalized dash button with its modal content. 
    - Creation of all the id:
        - "open-modal-"+id_subname: id of the button.
        - "input_1-"+id_subname: id of the input inside the modal.
        - "input_2-"+id_subname: id of the input inside the modal.
        - "input_3-"+id_subname: id of the input inside the modal.
        - "submit-button-"+id_subname: id of the submit button inside the modal.
        - "modal-"+id_subname: id of the modal.
        - "output-div-"+id_subname: id of the dash output.
        
    """       

    dropdown_style = {'width': f'200px', 'height': '40px', 'boxSizing': 'border-box'}

        
    return html.Div([
    dbc.Button(text_button, id="open-modal-"+id_subname, n_clicks=0, className='button'),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(text_modal)),

            dbc.ModalBody(
                [   
                    dcc.Input(id="input_1-"+id_subname, type="number", style=dropdown_style, className='dash-input dynamic-width', placeholder=placeholder_input_1),
                    html.Span(":", style={'margin': '0 10px'}),
                    dcc.Input(id="input_2-"+id_subname, type="number", style=dropdown_style, className='dash-input dynamic-width', placeholder=placeholder_input_2),
                    html.Span(":", style={'margin': '0 10px'}),
                    dcc.Input(id="input_3-"+id_subname, type="number", style=dropdown_style, className='dash-input dynamic-width', placeholder=placeholder_input_3),

                ]
            ),
            html.Span("", style={'margin': '0 10px'}),
            dbc.ButtonGroup([
            dbc.ModalFooter(
                dbc.Button("Submit", id="submit-button-"+id_subname, n_clicks=0, className='button')
            ),
            dbc.ModalFooter(
                dbc.Button("Reset", id="submit-reset-button-"+id_subname, n_clicks=0, className='button mx-2', style = { 'backgroundColor': '#c0392b', 'color': '#1e1e1e'})
            ),])


        ],
        id="modal-"+id_subname,
        is_open=False,  # Initially closed
        className='top-modal',  # Apply the custom class here
        centered=True,
        size="lg",
    ),
    html.Div(id="output-div-"+id_subname) 
    ])



I use some callback


@app.callback(
    Output("modal-subplot-tab-2", "is_open"),
    [Input("open-modal-subplot-tab-2", "n_clicks"), Input("submit-button-subplot-tab-2", "n_clicks")],
    [State("modal-subplot-tab-2", "is_open")]
)
def toggle_modal(open_clicks, submit_clicks, is_open):
    if open_clicks or submit_clicks:
        return not is_open
    return is_open

@app.callback(
    Output('output-div-subplot-tab-2', 'children'),
    [Input('submit-reset-button-subplot-tab-2', 'n_clicks'), 
     Input('submit-button-subplot-tab-2', 'n_clicks')],
    [State('input_1-subplot-tab-2', 'value'), State('input_2-subplot-tab-2', 'value'), State('input_3-subplot-tab-2', 'value')],
    prevent_initial_call=True
)
def update_output(reset_click, n_clicks, input_1_value, input_2_value, input_3_value):

    print(colored("-------------- callback update_output --------------", "red"))
    print("Submit button clicks:", n_clicks)  # Check for clicks
    print("Inputs Name:", [input_1_value, input_2_value, input_3_value])  # Current function name
    
    global previous_clicks, previous_reset_clicks
    # Reset button clicked
    if reset_click > previous_reset_clicks:
        previous_reset_clicks = reset_click
        previous_clicks = [[]]
        return ""
    
    if n_clicks > 0:
        try:
            # Validate that func_name and input_value are provided
            if not input_1_value or not input_2_value or not input_3_value:
                return dash.no_update
                # return "Error: Function name and input expression are required."
            
            # Create the buttons which will correspond to each subplot.
            buttons_subplot_tab2 = fds.buttons_subplots("Figure-"+tab+"-subplot-", "Subplot ",
                                                        input_1_value, input_2_value, input_3_value, dark_dropdown_style, uniform_style)
            
            previous_clicks = [0] * input_1_value
            return buttons_subplot_tab2
        except Exception as e:
            return f"Error: {str(e)}"
    return ""




@app.callback(
    Output('graph-output-tab-2', 'figure'), Output('figure-store-tab-2', 'data'),
    [Input('tabs', 'value'),
     Input('x-dropdown-tab-2', 'value'),
     Input('y-dropdown-tab-2', 'value'),
     Input('z-dropdown-tab-2', 'value'),
     Input('Func on y-dropdown-tab-2', 'value'),
     Input('Func on z-dropdown-tab-2', 'value'),
     Input('Graph-dropdown-tab-2', 'value'),
     Input('Dim-dropdown-tab-2', 'value'),
     Input("dropdown-regression-tab-2", "value"),
     Input("input-regression-tab-2", "value"),
     Input("submit-button-regression-tab-2", "n_clicks"),
     Input("dropdown-smoothing-tab-2", "value"),
     Input("input-smoothing-tab-2", "value"),
     Input("submit-button-smoothing-tab-2", "n_clicks"),
     Input("input_1-subplot-tab-2", "value"),
     Input("input_2-subplot-tab-2", "value"),
     Input("input_3-subplot-tab-2", "value"),
     Input("submit-button-subplot-tab-2", "n_clicks"),
     Input("hide-dropdowns-tab-2", "n_clicks"),
     Input("submit-button-filter-tab-2", "n_clicks")] +
    [Input(f'fig-dropdown-{col}-tab-2', 'value') for col in List_col_tab2] +
    [Input({'type': 'subplot-button', 'index': ALL}, 'n_clicks')],
    State('graph-output-tab-2', 'figure'),
    State('figure-store-tab-2', 'data')
    )
def update_graph_tab2(selected_tab, x_dropdown_value, y_dropdown_value, z_dropdown_value,
                      yfunc_dropdown_value, zfunc_dropdown_value, graph_dropdown_value, dim_dropdown_value,
                      reg_dropdown_value, reg_order_value, sub_bot_reg_value,
                      smt_dropdown_value, smt_order_value, sub_bot_smt_value,
                      nb_subplots, nb_subplots_row, nb_subplots_col, sub_bot_sub_value,
                      hide_drop_fig, sub_bot_filter_value, *args):

    global previous_clicks, last_clicked_index
    
    print()
    print(colored("------------ callback update_graph_tab2 ------------", "red"))
    current_fig = args[-2]
    data_for_plot = args[-1]
    filter_values = list(args[0:len(List_col_tab2)])
    filter_values = {List_col_tab2[i]: (filter_values[i] if filter_values[i] != '' else None) for i in range(min(len(List_col_tab2), len(filter_values)))}
    subplot_button_clicks = list(args[len(List_col_tab2):-2])
    # Now to get the flat list
    if subplot_button_clicks and isinstance(subplot_button_clicks, list):
        subplot_button_clicks = subplot_button_clicks[0]  # Access the first element
        print("Subplot Button Clicks:", subplot_button_clicks)
    else:
        subplot_button_clicks = []  # Handle cases where subplot_button_clicks might be empty or wrongly structured
        print("No subplot button clicks found.")


when I press the "submit-button-subplot-tab-2"
it send the 

-------------- callback update_output --------------
Submit button clicks: 1
Inputs Name: [2, 2, 1]

------------ callback update_graph_tab2 ------------
Subplot Button Clicks: []
Triggered component: submit-button-subplot-tab-2

------------ callback update_graph_tab2 ------------
Subplot Button Clicks: [0, 0]
Triggered component: {"index":"1","type":"subplot-button"}

why does the Subplot Button Clicks = [] even if I created them in the callback update_output


