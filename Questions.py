

print(target_ids)
print(callback_dependencies)
target_callbacks = {cb_name for cb_name, deps in callback_dependencies.items()
                    if any(output_id in target_ids for output_id in deps['outputs'])}

print(target_callbacks)

shows


['tabs', 'tabs-1', 'tabs-2', 'tabs-3', 'stored-df1', 'stored-df2', 'tabs-content']
{'render_content': {'outputs': ["'tabs-content', 'children'"], 'inputs': ["'tabs', 'value'"]}, 'update_stored_df1': {'outputs': ["'stored-df1', 'data'"], 'inputs': ["'tabs', 'value'", "'x-dropdown-tab-2', 'value'", "'y-dropdown-tab-2', 'value'", "'z-dropdown-tab-2', 'value'", "f'checkbox-{col}-tab-2', 'value'", "f'{col}-fig-dropdown-tab-2', 'value'"]}, 'update_z_dropdown_tab2': {'outputs': ["'z-dropdown-tab-2', 'options'"], 'inputs': ["'x-dropdown-tab-2', 'value'", "'y-dropdown-tab-2', 'value'", "'tabs', 'value'"]}, 'update_dim_dropdown_tab2': {'outputs': ["'Dim-dropdown-tab-2', 'options'"], 'inputs': ["'y-dropdown-tab-2', 'value'", "'tabs', 'value'"]}, 'update_filter_dropdown_tab2': {'outputs': ["f'{col}-fig-dropdown-tab-2', 'options'"], 'inputs': ["f'checkbox-{col}-tab-2', 'value'", "'tabs', 'value'", "'stored-df1', 'data'"]}, 'update_ui': {'outputs': ["'dynamic-content', 'children'", "'stored-df2', 'data'"], 'inputs': ["'input-value', 'value'"]}, 'update_y_dropdown_tab3': {'outputs': ["'y-dropdown-tab-3', 'options'"], 'inputs': ["'x-dropdown-tab-3', 'value'", "'tabs', 'value'"]}, 'update_graph_tab2': {'outputs': ["'graph-output-tab-3', 'figure'"], 'inputs': ["'tabs', 'value'", "'x-dropdown-tab-3', 'value'", "'y-dropdown-tab-3', 'value'", "'z-dropdown-tab-3', 'value'", "'Func-dropdown-tab-3', 'value'", "'Graph-dropdown-tab-3', 'value'", "'Dim-dropdown-tab-3', 'value'"]}}
set()

why target_callbacks is empty