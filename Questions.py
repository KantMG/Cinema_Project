
I have the following function which create three inputs

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


based on the value of "input_1-"+id_subname

I create some button 

@app.callback(
    Output('output-div-subplot-tab-2', 'children'),
    [Input('submit-button-subplot-tab-2', 'n_clicks')],
    [State('input_1-subplot-tab-2', 'value'), State('input_2-subplot-tab-2', 'value'), State('input_3-subplot-tab-2', 'value')]
)
def update_output(n_clicks, input_1_value, input_2_value, input_3_value):
    print("Submit button clicks:", n_clicks)  # Check for clicks
    print("Inputs Name:", [input_1_value, input_2_value, input_3_value])  # Current function name
    
    if n_clicks > 0:
        try:
            # Validate that func_name and input_value are provided
            if not input_1_value or not input_2_value or not input_3_value:
                return dash.no_update
                # return "Error: Function name and input expression are required."
                
            # Create the buttons which will correspond to each subplot.
            buttons_subplot_tab2 = buttons_subplots("Figure-"+tab+"-subplot-", "Subplot ",
                                                        input_1_value, input_2_value, input_3_value, dark_dropdown_style, uniform_style)

            return buttons_subplot_tab2
        except Exception as e:
            return f"Error: {str(e)}"
    return ""

with the functionbuttons_subplots is

def buttons_subplots(id_subname, text_button, nb_buttons, nb_buttons_row, nb_buttons_column,
                               dark_dropdown_style, uniform_style):

    """
    Goal: Create as many button as asked.

    Parameters:
    - id_subname: Part of all the id name associated with this button modal.
    - text_buttons: Text on the button.
    - nb_buttons: Number of buttons.
    - nb_buttons_row: Number of buttons on a row.
    - nb_buttons_column: Number of buttons on a column.
    - dark_dropdown_style: Color style of the dropdown.
    - uniform_style: Color style of the dropdown.

    Returns:
    - The finalized dash button with its modal content. 
    - Creation of all the id:
        - "open-modal-"+id_subname: id of the button.
        - "dropdown-"+id_subname: id of the dropdown inside the modal.
        - "input-"+id_subname: id of the input inside the modal.
        - "submit-button-"+id_subname: id of the submit button inside the modal.
        - "modal-"+id_subname: id of the modal.
        - "output-div-"+id_subname: id of the dash output.
        
    """       

    dropdown_style = {'width': f'200px', 'height': '40px', 'boxSizing': 'border-box'}
    
    button_list = []
        
    for nb_button in range(1, nb_buttons+1):
                
        button = html.Div(dbc.Button(text_button+str(nb_button), id=id_subname+str(nb_button), value=id_subname+str(nb_button), n_clicks=0, className='dash-input dynamic-width'))

        button_list.append(button)

    return html.Div(children=[
        html.Span("", style={'margin': '0 10px'}),
        html.Div(button_list, style={
                        'display': 'flex',
                        # 'margin-left': '200px',
                        'justify-content': 'flex-start',
                        'gap': '5px',
                        'margin-bottom': '20px'  # Add space below the dropdowns
                    }
                ), html.Div(id='buttons-subplot-content')
        ])


Now I want to use in a callback the id of the buttons, however, they do not exist at first and there name and nuber is given by the value of "input_1-"+id_subname


