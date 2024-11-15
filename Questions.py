I have the function

def button_dropdown_function(text_button, id_button, id_created_func_name, id_created_func, id_submit_button, id_modal, id_output_div, dark_dropdown_style, uniform_style):

    return html.Div([
    dbc.Button(text_button, id=id_button, n_clicks=0, className='button'),
    dbc.Modal(
        [
            dbc.ModalHeader("Create Function"),
            dbc.ModalBody(
                [
                    dcc.Input(id=id_created_func_name, type="text", style=uniform_style, className='dash-input dynamic-width', placeholder="Enter function name"),
                    html.Span(":", style={'margin': '0 10px'}),
                    dcc.Input(id=id_created_func, type="text", style=uniform_style, className='dash-input dynamic-width', placeholder="Enter operation (e.g., A + B)"),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button("Submit", id=id_submit_button, n_clicks=0, style=uniform_style, className='button')
            ),
        ],
        id=id_modal,
        is_open=False,  # Initially closed
        # size="lg",
    ),
    html.Div(id=id_output_div)
    ])


the modal doesnt appear in a nice window at the top, can it be due to my css file