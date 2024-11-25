
I have 

    print("Adding the trace to the plotly figure")
    
    # Ensure the new trace is of a valid type
    if not isinstance(new_trace, go.BaseTraceType):
        print("Invalid trace type returned, expected a trace, got:", type(new_trace))
        return plotly_fig, data_for_plot  # Return as is, do not add invalid trace



and my plotly is updated

pip3 install --upgrade plotly
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: plotly in ./.local/lib/python3.10/site-packages (5.24.1)
Requirement already satisfied: tenacity>=6.2.0 in ./.local/lib/python3.10/site-packages (from plotly) (9.0.0)
Requirement already satisfied: packaging in ./.local/lib/python3.10/site-packages (from plotly) (24.1)

return 


Adding the trace to the plotly figure
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/Main.py:701, in update_graph_tab2(
    selected_tab='tab-2',
    x_dropdown_value='runtimeMinutes',
    y_dropdown_value=None,
    z_dropdown_value=None,
    yfunc_dropdown_value=[],
    zfunc_dropdown_value=[],
    graph_dropdown_value='Histogram',
    dim_dropdown_value='1D',
    reg_dropdown_value=None,
    reg_order_value=None,
    sub_bot_reg_value=0,
    smt_dropdown_value=None,
    smt_order_value=None,
    sub_bot_smt_value=0,
    nb_subplots=2,
    nb_subplots_row=2,
    nb_subplots_col=1,
    hide_drop_fig=0,
    sub_bot_filter_value=0,
    *args=(None, None, None, None, None, None, [1, 0], {'data': [{'alignmentgroup': 'True', 'hovertemplate': 'startYear=%{x}<br>count=%{y}<extra></extra>', 'legendgroup': '', 'marker': {'color': '#636efa', 'pattern': {'shape': ''}}, 'name': '', 'offsetgroup': '', 'orientation': 'v', 'showlegend': False, 'textposition': 'auto', 'type': 'bar', ...}], 'layout': {'autosize': True, 'font': {'color': 'white'}, 'paper_bgcolor': '#101820', 'plot_bgcolor': '#1e1e1e', 'template': {'data': {'bar': [{...}], 'barpolar': [{...}], 'carpet': [{...}], 'choropleth': [{...}], 'contour': [{...}], 'contourcarpet': [{...}], 'heatmap': [{...}], 'heatmapgl': [{...}], 'histogram': [{...}], 'histogram2d': [{...}], ...}, 'layout': {'annotationdefaults': {'arrowcolor': '#2a3f5f', 'arrowhead': 0, 'arrowwidth': 1}, 'autotypenumbers': 'strict', 'coloraxis': {'colorbar': {...}}, 'colorscale': {'diverging': [...], 'sequential': [...], 'sequentialminus': [...]}, 'colorway': ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A', '#19d3f3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52'], 'font': {'color': '#2a3f5f'}, 'geo': {'bgcolor': 'white', 'lakecolor': 'white', 'landcolor': '#E5ECF6', 'showlakes': True, 'showland': True, 'subunitcolor': 'white'}, 'hoverlabel': {'align': 'left'}, 'hovermode': 'closest', 'mapbox': {'style': 'light'}, ...}}, 'xaxis': {'anchor': 'y', 'autorange': True, 'domain': [0, 1], 'range': [1891.5, 1990.5], 'type': 'linear'}, 'xaxis2': {'anchor': 'y2', 'domain': [0, 1]}, 'yaxis': {'anchor': 'x', 'autorange': True, 'domain': [0.575, 1], 'range': [0, 362.10526315789474], 'type': 'linear'}, 'yaxis2': {'anchor': 'x2', 'domain': [0, 0.425]}}}, [{'count': 3, 'startYear': 1892}, {'count': 1, 'startYear': 1893}, {'count': 7, 'startYear': 1894}, {'count': 18, 'startYear': 1895}, {'count': 105, 'startYear': 1896}, {'count': 37, 'startYear': 1897}, {'count': 31, 'startYear': 1898}, {'count': 24, 'startYear': 1899}, {'count': 41, 'startYear': 1900}, {'count': 19, 'startYear': 1901}, {'count': 14, 'startYear': 1902}, {'count': 26, 'startYear': 1903}, {'count': 8, 'startYear': 1904}, {'count': 14, 'startYear': 1905}, {'count': 19, 'startYear': 1906}, {'count': 29, 'startYear': 1907}, {'count': 105, 'startYear': 1908}, {'count': 188, 'startYear': 1909}, {'count': 142, 'startYear': 1910}, {'count': 153, 'startYear': 1911}, ...])
)
    698         print(f"Last clicked subplot button index: {last_clicked_index}")
    699         # Additional logic based on the last clicked button can go here
--> 701     return update_graph_subplot(x_dropdown_value, y_dropdown_value, z_dropdown_value,
        z_dropdown_value = None
        x_dropdown_value = 'runtimeMinutes'
        y_dropdown_value = None
        yfunc_dropdown_value = []
        zfunc_dropdown_value = []
        graph_dropdown_value = 'Histogram'
        dim_dropdown_value = '1D'
        smt_dropdown_value = None
        smt_order_value = None
        sub_bot_smt_value = 0
        last_clicked_index = 0
        nb_subplots = 2
        nb_subplots_row = 2
        nb_subplots_col = 1
        current_fig = {'data': [{'alignmentgroup': 'True', 'hovertemplate': 'startYear=%{x}<br>count=%{y}<extra></extra>', 'legendgroup': '', 'marker': {'color': '#636efa', 'pattern': {'shape': ''}}, 'name': '', 'offsetgroup': '', 'orientation': 'v', 'showlegend': False, 'textposition': 'auto', 'x': [1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1925, 1936, 1990], 'xaxis': 'x', 'y': [3, 1, 7, 18, 105, 37, 31, 24, 41, 19, 14, 26, 8, 14, 19, 29, 105, 188, 142, 153, 195, 191, 274, 344, 286, 325, 296, 110, 3, 2, 1, 2, 1, 1], 'yaxis': 'y', 'type': 'bar'}], 'layout': {'template': {'data': {'histogram2dcontour': [{'type': 'histogram2dcontour', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'choropleth': [{'type': 'choropleth', 'colorbar': {'outlinewidth': 0, 'ticks': ''}}], 'histogram2d': [{'type': 'histogram2d', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'heatmap': [{'type': 'heatmap', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'heatmapgl': [{'type': 'heatmapgl', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'contourcarpet': [{'type': 'contourcarpet', 'colorbar': {'outlinewidth': 0, 'ticks': ''}}], 'contour': [{'type': 'contour', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'surface': [{'type': 'surface', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'mesh3d': [{'type': 'mesh3d', 'colorbar': {'outlinewidth': 0, 'ticks': ''}}], 'scatter': [{'fillpattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}, 'type': 'scatter'}], 'parcoords': [{'type': 'parcoords', 'line': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scatterpolargl': [{'type': 'scatterpolargl', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'bar': [{'error_x': {'color': '#2a3f5f'}, 'error_y': {'color': '#2a3f5f'}, 'marker': {'line': {'color': '#E5ECF6', 'width': 0.5}, 'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}}, 'type': 'bar'}], 'scattergeo': [{'type': 'scattergeo', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scatterpolar': [{'type': 'scatterpolar', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'histogram': [{'marker': {'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}}, 'type': 'histogram'}], 'scattergl': [{'type': 'scattergl', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scatter3d': [{'type': 'scatter3d', 'line': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scattermapbox': [{'type': 'scattermapbox', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scatterternary': [{'type': 'scatterternary', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scattercarpet': [{'type': 'scattercarpet', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'carpet': [{'aaxis': {'endlinecolor': '#2a3f5f', 'gridcolor': 'white', 'linecolor': 'white', 'minorgridcolor': 'white', 'startlinecolor': '#2a3f5f'}, 'baxis': {'endlinecolor': '#2a3f5f', 'gridcolor': 'white', 'linecolor': 'white', 'minorgridcolor': 'white', 'startlinecolor': '#2a3f5f'}, 'type': 'carpet'}], 'table': [{'cells': {'fill': {'color': '#EBF0F8'}, 'line': {'color': 'white'}}, 'header': {'fill': {'color': '#C8D4E3'}, 'line': {'color': 'white'}}, 'type': 'table'}], 'barpolar': [{'marker': {'line': {'color': '#E5ECF6', 'width': 0.5}, 'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}}, 'type': 'barpolar'}], 'pie': [{'automargin': True, 'type': 'pie'}]}, 'layout': {'autotypenumbers': 'strict', 'colorway': ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A', '#19d3f3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52'], 'font': {'color': '#2a3f5f'}, 'hovermode': 'closest', 'hoverlabel': {'align': 'left'}, 'paper_bgcolor': 'white', 'plot_bgcolor': '#E5ECF6', 'polar': {'bgcolor': '#E5ECF6', 'angularaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}, 'radialaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}}, 'ternary': {'bgcolor': '#E5ECF6', 'aaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}, 'baxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}, 'caxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}}, 'coloraxis': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'colorscale': {'sequential': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']], 'sequentialminus': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']], 'diverging': [[0, '#8e0152'], [0.1, '#c51b7d'], [0.2, '#de77ae'], [0.3, '#f1b6da'], [0.4, '#fde0ef'], [0.5, '#f7f7f7'], [0.6, '#e6f5d0'], [0.7, '#b8e186'], [0.8, '#7fbc41'], [0.9, '#4d9221'], [1, '#276419']]}, 'xaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': '', 'title': {'standoff': 15}, 'zerolinecolor': 'white', 'automargin': True, 'zerolinewidth': 2}, 'yaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': '', 'title': {'standoff': 15}, 'zerolinecolor': 'white', 'automargin': True, 'zerolinewidth': 2}, 'scene': {'xaxis': {'backgroundcolor': '#E5ECF6', 'gridcolor': 'white', 'linecolor': 'white', 'showbackground': True, 'ticks': '', 'zerolinecolor': 'white', 'gridwidth': 2}, 'yaxis': {'backgroundcolor': '#E5ECF6', 'gridcolor': 'white', 'linecolor': 'white', 'showbackground': True, 'ticks': '', 'zerolinecolor': 'white', 'gridwidth': 2}, 'zaxis': {'backgroundcolor': '#E5ECF6', 'gridcolor': 'white', 'linecolor': 'white', 'showbackground': True, 'ticks': '', 'zerolinecolor': 'white', 'gridwidth': 2}}, 'shapedefaults': {'line': {'color': '#2a3f5f'}}, 'annotationdefaults': {'arrowcolor': '#2a3f5f', 'arrowhead': 0, 'arrowwidth': 1}, 'geo': {'bgcolor': 'white', 'landcolor': '#E5ECF6', 'subunitcolor': 'white', 'showland': True, 'showlakes': True, 'lakecolor': 'white'}, 'title': {'x': 0.05}, 'mapbox': {'style': 'light'}}}, 'xaxis': {'anchor': 'y', 'domain': [0, 1], 'type': 'linear', 'range': [1891.5, 1990.5], 'autorange': True}, 'yaxis': {'anchor': 'x', 'domain': [0.575, 1], 'type': 'linear', 'range': [0, 362.10526315789474], 'autorange': True}, 'xaxis2': {'anchor': 'y2', 'domain': [0, 1]}, 'yaxis2': {'anchor': 'x2', 'domain': [0, 0.425]}, 'font': {'color': 'white'}, 'plot_bgcolor': '#1e1e1e', 'paper_bgcolor': '#101820', 'autosize': True}}
        data_for_plot = [{'startYear': 1892, 'count': 3}, {'startYear': 1893, 'count': 1}, {'startYear': 1894, 'count': 7}, {'startYear': 1895, 'count': 18}, {'startYear': 1896, 'count': 105}, {'startYear': 1897, 'count': 37}, {'startYear': 1898, 'count': 31}, {'startYear': 1899, 'count': 24}, {'startYear': 1900, 'count': 41}, {'startYear': 1901, 'count': 19}, {'startYear': 1902, 'count': 14}, {'startYear': 1903, 'count': 26}, {'startYear': 1904, 'count': 8}, {'startYear': 1905, 'count': 14}, {'startYear': 1906, 'count': 19}, {'startYear': 1907, 'count': 29}, {'startYear': 1908, 'count': 105}, {'startYear': 1909, 'count': 188}, {'startYear': 1910, 'count': 142}, {'startYear': 1911, 'count': 153}, {'startYear': 1912, 'count': 195}, {'startYear': 1913, 'count': 191}, {'startYear': 1914, 'count': 274}, {'startYear': 1915, 'count': 344}, {'startYear': 1916, 'count': 286}, {'startYear': 1917, 'count': 325}, {'startYear': 1918, 'count': 296}, {'startYear': 1919, 'count': 110}, {'startYear': 1920, 'count': 3}, {'startYear': 1921, 'count': 2}, {'startYear': 1922, 'count': 1}, {'startYear': 1925, 'count': 2}, {'startYear': 1936, 'count': 1}, {'startYear': 1990, 'count': 1}]
        df1_filtered =          tconst  isAdult  ...  averageRating  numVotes
0     tt0000001      0.0  ...            5.7    2081.0
1     tt0000002      0.0  ...            5.6     280.0
2     tt0000003      0.0  ...            6.5    2078.0
3     tt0000004      0.0  ...            5.4     181.0
4     tt0000005      0.0  ...            6.2    2816.0
        ...      ...  ...            ...       ...
3010  tt0010128      0.0  ...            5.6      72.0
3011  tt0010131      0.0  ...            5.3      23.0
3012  tt0010133      0.0  ...            4.2      22.0
3013  tt0010134      0.0  ...            4.3      24.0
3014  tt0010137      0.0  ...            6.0     755.0

[3015 rows x 8 columns]
        Large_file_memory = False
    702                                 yfunc_dropdown_value, zfunc_dropdown_value,
    703                                 graph_dropdown_value, dim_dropdown_value,
    704                                 smt_dropdown_value, smt_order_value, sub_bot_smt_value,
    705                                 last_clicked_index, nb_subplots, nb_subplots_row, nb_subplots_col,
    706                                 df1_filtered, current_fig, data_for_plot, Large_file_memory)
    713 return update_graph_utility(x_dropdown_value, y_dropdown_value, z_dropdown_value, yfunc_dropdown_value, zfunc_dropdown_value, graph_dropdown_value, dim_dropdown_value, smt_dropdown_value, smt_order_value, sub_bot_smt_value, df1_filtered, Large_file_memory)

File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/Main.py:1040, in update_graph_subplot(
    x_column='runtimeMinutes',
    y_column=None,
    z_column=None,
    yfunc_column=[],
    zfunc_column=[],
    graph_type='Histogram',
    dim_type='1D',
    smt_dropdown_value=None,
    smt_order_value=None,
    sub_bot_smt_value=0,
    index_subplot=0,
    nb_subplots=2,
    nb_subplots_row=2,
    nb_subplots_col=1,
    df=         tconst  isAdult  ...  averageRating  nu...           6.0     755.0

[3015 rows x 8 columns],
    current_fig={'data': [{'alignmentgroup': 'True', 'hovertemplate': 'startYear=%{x}<br>count=%{y}<extra></extra>', 'legendgroup': '', 'marker': {'color': '#636efa', 'pattern': {'shape': ''}}, 'name': '', 'offsetgroup': '', 'orientation': 'v', 'showlegend': False, 'textposition': 'auto', 'type': 'bar', ...}], 'layout': {'autosize': True, 'font': {'color': 'white'}, 'paper_bgcolor': '#101820', 'plot_bgcolor': '#1e1e1e', 'template': {'data': {'bar': [{'error_x': {...}, 'error_y': {...}, 'marker': {...}, 'type': 'bar'}], 'barpolar': [{'marker': {...}, 'type': 'barpolar'}], 'carpet': [{'aaxis': {...}, 'baxis': {...}, 'type': 'carpet'}], 'choropleth': [{'colorbar': {...}, 'type': 'choropleth'}], 'contour': [{'colorbar': {...}, 'colorscale': [...], 'type': 'contour'}], 'contourcarpet': [{'colorbar': {...}, 'type': 'contourcarpet'}], 'heatmap': [{'colorbar': {...}, 'colorscale': [...], 'type': 'heatmap'}], 'heatmapgl': [{'colorbar': {...}, 'colorscale': [...], 'type': 'heatmapgl'}], 'histogram': [{'marker': {...}, 'type': 'histogram'}], 'histogram2d': [{'colorbar': {...}, 'colorscale': [...], 'type': 'histogram2d'}], ...}, 'layout': {'annotationdefaults': {'arrowcolor': '#2a3f5f', 'arrowhead': 0, 'arrowwidth': 1}, 'autotypenumbers': 'strict', 'coloraxis': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'colorscale': {'diverging': [[...], [...], [...], [...], [...], [...], [...], [...], [...], [...], [...]], 'sequential': [[...], [...], [...], [...], [...], [...], [...], [...], [...], [...]], 'sequentialminus': [[...], [...], [...], [...], [...], [...], [...], [...], [...], [...]]}, 'colorway': ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A', '#19d3f3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52'], 'font': {'color': '#2a3f5f'}, 'geo': {'bgcolor': 'white', 'lakecolor': 'white', 'landcolor': '#E5ECF6', 'showlakes': True, 'showland': True, 'subunitcolor': 'white'}, 'hoverlabel': {'align': 'left'}, 'hovermode': 'closest', 'mapbox': {'style': 'light'}, ...}}, 'xaxis': {'anchor': 'y', 'autorange': True, 'domain': [0, 1], 'range': [1891.5, 1990.5], 'type': 'linear'}, 'xaxis2': {'anchor': 'y2', 'domain': [0, 1]}, 'yaxis': {'anchor': 'x', 'autorange': True, 'domain': [0.575, 1], 'range': [0, 362.10526315789474], 'type': 'linear'}, 'yaxis2': {'anchor': 'x2', 'domain': [0, 0.425]}}},
    data_for_plot=[{'count': 3, 'startYear': 1892}, {'count': 1, 'startYear': 1893}, {'count': 7, 'startYear': 1894}, {'count': 18, 'startYear': 1895}, {'count': 105, 'startYear': 1896}, {'count': 37, 'startYear': 1897}, {'count': 31, 'startYear': 1898}, {'count': 24, 'startYear': 1899}, {'count': 41, 'startYear': 1900}, {'count': 19, 'startYear': 1901}, {'count': 14, 'startYear': 1902}, {'count': 26, 'startYear': 1903}, {'count': 8, 'startYear': 1904}, {'count': 14, 'startYear': 1905}, {'count': 19, 'startYear': 1906}, {'count': 29, 'startYear': 1907}, {'count': 105, 'startYear': 1908}, {'count': 188, 'startYear': 1909}, {'count': 142, 'startYear': 1910}, {'count': 153, 'startYear': 1911}, ...],
    large_file_memory=False
)
   1036 """
   1037 Utility function to update a graph based on the provided parameters.
   1038 """
   1039 print("update_graph_subplot")
-> 1040 fig, data_for_plot = fc.figure_update_subplot(df, current_fig, data_for_plot, x_column, y_column, z_column,
        data_for_plot = [{'startYear': 1892, 'count': 3}, {'startYear': 1893, 'count': 1}, {'startYear': 1894, 'count': 7}, {'startYear': 1895, 'count': 18}, {'startYear': 1896, 'count': 105}, {'startYear': 1897, 'count': 37}, {'startYear': 1898, 'count': 31}, {'startYear': 1899, 'count': 24}, {'startYear': 1900, 'count': 41}, {'startYear': 1901, 'count': 19}, {'startYear': 1902, 'count': 14}, {'startYear': 1903, 'count': 26}, {'startYear': 1904, 'count': 8}, {'startYear': 1905, 'count': 14}, {'startYear': 1906, 'count': 19}, {'startYear': 1907, 'count': 29}, {'startYear': 1908, 'count': 105}, {'startYear': 1909, 'count': 188}, {'startYear': 1910, 'count': 142}, {'startYear': 1911, 'count': 153}, {'startYear': 1912, 'count': 195}, {'startYear': 1913, 'count': 191}, {'startYear': 1914, 'count': 274}, {'startYear': 1915, 'count': 344}, {'startYear': 1916, 'count': 286}, {'startYear': 1917, 'count': 325}, {'startYear': 1918, 'count': 296}, {'startYear': 1919, 'count': 110}, {'startYear': 1920, 'count': 3}, {'startYear': 1921, 'count': 2}, {'startYear': 1922, 'count': 1}, {'startYear': 1925, 'count': 2}, {'startYear': 1936, 'count': 1}, {'startYear': 1990, 'count': 1}]
        df =          tconst  isAdult  ...  averageRating  numVotes
0     tt0000001      0.0  ...            5.7    2081.0
1     tt0000002      0.0  ...            5.6     280.0
2     tt0000003      0.0  ...            6.5    2078.0
3     tt0000004      0.0  ...            5.4     181.0
4     tt0000005      0.0  ...            6.2    2816.0
        ...      ...  ...            ...       ...
3010  tt0010128      0.0  ...            5.6      72.0
3011  tt0010131      0.0  ...            5.3      23.0
3012  tt0010133      0.0  ...            4.2      22.0
3013  tt0010134      0.0  ...            4.3      24.0
3014  tt0010137      0.0  ...            6.0     755.0

[3015 rows x 8 columns]
        current_fig = {'data': [{'alignmentgroup': 'True', 'hovertemplate': 'startYear=%{x}<br>count=%{y}<extra></extra>', 'legendgroup': '', 'marker': {'color': '#636efa', 'pattern': {'shape': ''}}, 'name': '', 'offsetgroup': '', 'orientation': 'v', 'showlegend': False, 'textposition': 'auto', 'x': [1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1925, 1936, 1990], 'xaxis': 'x', 'y': [3, 1, 7, 18, 105, 37, 31, 24, 41, 19, 14, 26, 8, 14, 19, 29, 105, 188, 142, 153, 195, 191, 274, 344, 286, 325, 296, 110, 3, 2, 1, 2, 1, 1], 'yaxis': 'y', 'type': 'bar'}], 'layout': {'template': {'data': {'histogram2dcontour': [{'type': 'histogram2dcontour', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'choropleth': [{'type': 'choropleth', 'colorbar': {'outlinewidth': 0, 'ticks': ''}}], 'histogram2d': [{'type': 'histogram2d', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'heatmap': [{'type': 'heatmap', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'heatmapgl': [{'type': 'heatmapgl', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'contourcarpet': [{'type': 'contourcarpet', 'colorbar': {'outlinewidth': 0, 'ticks': ''}}], 'contour': [{'type': 'contour', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'surface': [{'type': 'surface', 'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'colorscale': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']]}], 'mesh3d': [{'type': 'mesh3d', 'colorbar': {'outlinewidth': 0, 'ticks': ''}}], 'scatter': [{'fillpattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}, 'type': 'scatter'}], 'parcoords': [{'type': 'parcoords', 'line': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scatterpolargl': [{'type': 'scatterpolargl', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'bar': [{'error_x': {'color': '#2a3f5f'}, 'error_y': {'color': '#2a3f5f'}, 'marker': {'line': {'color': '#E5ECF6', 'width': 0.5}, 'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}}, 'type': 'bar'}], 'scattergeo': [{'type': 'scattergeo', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scatterpolar': [{'type': 'scatterpolar', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'histogram': [{'marker': {'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}}, 'type': 'histogram'}], 'scattergl': [{'type': 'scattergl', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scatter3d': [{'type': 'scatter3d', 'line': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scattermapbox': [{'type': 'scattermapbox', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scatterternary': [{'type': 'scatterternary', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'scattercarpet': [{'type': 'scattercarpet', 'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}}], 'carpet': [{'aaxis': {'endlinecolor': '#2a3f5f', 'gridcolor': 'white', 'linecolor': 'white', 'minorgridcolor': 'white', 'startlinecolor': '#2a3f5f'}, 'baxis': {'endlinecolor': '#2a3f5f', 'gridcolor': 'white', 'linecolor': 'white', 'minorgridcolor': 'white', 'startlinecolor': '#2a3f5f'}, 'type': 'carpet'}], 'table': [{'cells': {'fill': {'color': '#EBF0F8'}, 'line': {'color': 'white'}}, 'header': {'fill': {'color': '#C8D4E3'}, 'line': {'color': 'white'}}, 'type': 'table'}], 'barpolar': [{'marker': {'line': {'color': '#E5ECF6', 'width': 0.5}, 'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}}, 'type': 'barpolar'}], 'pie': [{'automargin': True, 'type': 'pie'}]}, 'layout': {'autotypenumbers': 'strict', 'colorway': ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A', '#19d3f3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52'], 'font': {'color': '#2a3f5f'}, 'hovermode': 'closest', 'hoverlabel': {'align': 'left'}, 'paper_bgcolor': 'white', 'plot_bgcolor': '#E5ECF6', 'polar': {'bgcolor': '#E5ECF6', 'angularaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}, 'radialaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}}, 'ternary': {'bgcolor': '#E5ECF6', 'aaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}, 'baxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}, 'caxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}}, 'coloraxis': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'colorscale': {'sequential': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']], 'sequentialminus': [[0, '#0d0887'], [0.1111111111111111, '#46039f'], [0.2222222222222222, '#7201a8'], [0.3333333333333333, '#9c179e'], [0.4444444444444444, '#bd3786'], [0.5555555555555556, '#d8576b'], [0.6666666666666666, '#ed7953'], [0.7777777777777778, '#fb9f3a'], [0.8888888888888888, '#fdca26'], [1, '#f0f921']], 'diverging': [[0, '#8e0152'], [0.1, '#c51b7d'], [0.2, '#de77ae'], [0.3, '#f1b6da'], [0.4, '#fde0ef'], [0.5, '#f7f7f7'], [0.6, '#e6f5d0'], [0.7, '#b8e186'], [0.8, '#7fbc41'], [0.9, '#4d9221'], [1, '#276419']]}, 'xaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': '', 'title': {'standoff': 15}, 'zerolinecolor': 'white', 'automargin': True, 'zerolinewidth': 2}, 'yaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': '', 'title': {'standoff': 15}, 'zerolinecolor': 'white', 'automargin': True, 'zerolinewidth': 2}, 'scene': {'xaxis': {'backgroundcolor': '#E5ECF6', 'gridcolor': 'white', 'linecolor': 'white', 'showbackground': True, 'ticks': '', 'zerolinecolor': 'white', 'gridwidth': 2}, 'yaxis': {'backgroundcolor': '#E5ECF6', 'gridcolor': 'white', 'linecolor': 'white', 'showbackground': True, 'ticks': '', 'zerolinecolor': 'white', 'gridwidth': 2}, 'zaxis': {'backgroundcolor': '#E5ECF6', 'gridcolor': 'white', 'linecolor': 'white', 'showbackground': True, 'ticks': '', 'zerolinecolor': 'white', 'gridwidth': 2}}, 'shapedefaults': {'line': {'color': '#2a3f5f'}}, 'annotationdefaults': {'arrowcolor': '#2a3f5f', 'arrowhead': 0, 'arrowwidth': 1}, 'geo': {'bgcolor': 'white', 'landcolor': '#E5ECF6', 'subunitcolor': 'white', 'showland': True, 'showlakes': True, 'lakecolor': 'white'}, 'title': {'x': 0.05}, 'mapbox': {'style': 'light'}}}, 'xaxis': {'anchor': 'y', 'domain': [0, 1], 'type': 'linear', 'range': [1891.5, 1990.5], 'autorange': True}, 'yaxis': {'anchor': 'x', 'domain': [0.575, 1], 'type': 'linear', 'range': [0, 362.10526315789474], 'autorange': True}, 'xaxis2': {'anchor': 'y2', 'domain': [0, 1]}, 'yaxis2': {'anchor': 'x2', 'domain': [0, 0.425]}, 'font': {'color': 'white'}, 'plot_bgcolor': '#1e1e1e', 'paper_bgcolor': '#101820', 'autosize': True}}
        x_column = 'runtimeMinutes'
        y_column = None
        z_column = None
        fc = <module 'figure_creation' from '/home/quentin/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/figure_creation.py'>
        yfunc_column = []
        zfunc_column = []
        graph_type = 'Histogram'
        dim_type = '1D'
        smt_dropdown_value = None
        smt_order_value = None
        sub_bot_smt_value = 0
        index_subplot = 0
        nb_subplots = 2
        nb_subplots_row = 2
        nb_subplots_col = 1
        large_file_memory = False
   1041                                               yfunc_column, zfunc_column, graph_type, dim_type, 
   1042                                               smt_dropdown_value, smt_order_value, sub_bot_smt_value,
   1043                                               index_subplot, nb_subplots, nb_subplots_row, nb_subplots_col, large_file_memory)
   1044 return fig, data_for_plot

File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/figure_creation.py:854, in figure_update_subplot(
    df=         tconst  isAdult  ...  averageRating  nu...           6.0     755.0

[3015 rows x 8 columns],
    fig_json_serializable={'data': [{'alignmentgroup': 'True', 'hovertemplate': 'startYear=%{x}<br>count=%{y}<extra></extra>', 'legendgroup': '', 'marker': {'color': '#636efa', 'pattern': {'shape': ''}}, 'name': '', 'offsetgroup': '', 'orientation': 'v', 'showlegend': False, 'textposition': 'auto', 'type': 'bar', ...}], 'layout': {'autosize': True, 'font': {'color': 'white'}, 'paper_bgcolor': '#101820', 'plot_bgcolor': '#1e1e1e', 'template': {'data': {'bar': [{'error_x': {...}, 'error_y': {...}, 'marker': {...}, 'type': 'bar'}], 'barpolar': [{'marker': {...}, 'type': 'barpolar'}], 'carpet': [{'aaxis': {...}, 'baxis': {...}, 'type': 'carpet'}], 'choropleth': [{'colorbar': {...}, 'type': 'choropleth'}], 'contour': [{'colorbar': {...}, 'colorscale': [...], 'type': 'contour'}], 'contourcarpet': [{'colorbar': {...}, 'type': 'contourcarpet'}], 'heatmap': [{'colorbar': {...}, 'colorscale': [...], 'type': 'heatmap'}], 'heatmapgl': [{'colorbar': {...}, 'colorscale': [...], 'type': 'heatmapgl'}], 'histogram': [{'marker': {...}, 'type': 'histogram'}], 'histogram2d': [{'colorbar': {...}, 'colorscale': [...], 'type': 'histogram2d'}], ...}, 'layout': {'annotationdefaults': {'arrowcolor': '#2a3f5f', 'arrowhead': 0, 'arrowwidth': 1}, 'autotypenumbers': 'strict', 'coloraxis': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'colorscale': {'diverging': [[...], [...], [...], [...], [...], [...], [...], [...], [...], [...], [...]], 'sequential': [[...], [...], [...], [...], [...], [...], [...], [...], [...], [...]], 'sequentialminus': [[...], [...], [...], [...], [...], [...], [...], [...], [...], [...]]}, 'colorway': ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A', '#19d3f3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52'], 'font': {'color': '#2a3f5f'}, 'geo': {'bgcolor': 'white', 'lakecolor': 'white', 'landcolor': '#E5ECF6', 'showlakes': True, 'showland': True, 'subunitcolor': 'white'}, 'hoverlabel': {'align': 'left'}, 'hovermode': 'closest', 'mapbox': {'style': 'light'}, ...}}, 'xaxis': {'anchor': 'y', 'autorange': True, 'domain': [0, 1], 'range': [1891.5, 1990.5], 'type': 'linear'}, 'xaxis2': {'anchor': 'y2', 'domain': [0, 1]}, 'yaxis': {'anchor': 'x', 'autorange': True, 'domain': [0.575, 1], 'range': [0, 362.10526315789474], 'type': 'linear'}, 'yaxis2': {'anchor': 'x2', 'domain': [0, 0.425]}}},
    data_for_plot=     runtimeMinutes  count
2                 1  ...33            1428      1

[134 rows x 2 columns],
    x_column='runtimeMinutes',
    y_column=None,
    z_column=None,
    yf_column=[],
    zf_column=[],
    graph_type='Histogram',
    dim_type='1D',
    smt_dropdown_value=None,
    smt_order_value=None,
    sub_bot_smt_value=0,
    index_subplot=0,
    nb_subplots=2,
    nb_subplots_row=2,
    nb_subplots_col=1,
    Large_file_memory=False
)
    851 print("Adding the trace to the plotly figure")
    853 # Ensure the new trace is of a valid type
--> 854 if not isinstance(new_trace, go.BaseTraceType):
        new_trace = Bar({
    'alignmentgroup': 'True',
    'hovertemplate': 'runtimeMinutes=%{x}<br>count=%{y}<extra></extra>',
    'legendgroup': '',
    'marker': {'color': '#636efa', 'pattern': {'shape': ''}},
    'name': '',
    'offsetgroup': '',
    'orientation': 'v',
    'showlegend': False,
    'textposition': 'auto',
    'x': array([   1,    2,    3,    4,    5,    6,    7,    8,    9,   10,   11,   12,
                  13,   14,   15,   16,   17,   18,   19,   20,   21,   22,   23,   24,
                  25,   26,   27,   28,   29,   30,   31,   32,   33,   34,   35,   36,
                  37,   38,   39,   40,   41,   42,   43,   44,   45,   46,   47,   48,
                  49,   50,   51,   52,   53,   54,   55,   56,   57,   58,   59,   60,
                  61,   62,   63,   64,   65,   66,   67,   68,   69,   70,   71,   72,
                  73,   74,   75,   76,   77,   78,   79,   80,   81,   82,   83,   84,
                  85,   86,   87,   88,   90,   92,   93,   95,   96,   97,   99,  100,
                 102,  105,  108,  109,  110,  112,  113,  116,  117,  120,  121,  124,
                 125,  135,  138,  148,  150,  163,  170,  180,  195,  199,  220,  223,
                 300,  310,  330,  350,  360,  374,  400,  410,  418,  421,  440,  450,
                 489, 1428]),
    'xaxis': 'x',
    'y': array([118,  35,  27,  37,  53,  55,  40,  48,  31, 113, 110,  55,  56,  50,
                 44,  56, 145,  25,   6,  57,  11,  11,  16,  20,  18,  10,   6,   9,
                 11,  26,   8,   5,  11,   6,   5,   3,   3,   5,   4,  29,   7,   3,
                  2,   9,  13,   6,   3,  11,   6, 351,   4,  11,   8,   9,  11,   8,
                  5,   9,  14, 102,  10,   9,  11,   6,  17,   5,   8,   9,   7,  51,
                  7,  12,  11,   5,  10,   1,   3,   6,   1,  25,   1,   4,   3,   4,
                  7,   2,   2,   4,  14,   4,   2,   2,   2,   2,   1,  13,   1,   4,
                  1,   2,   3,   3,   1,   1,   1,   3,   1,   1,   1,   1,   1,   2,
                  2,   1,   1,   1,   2,   1,   1,   1,   7,   5,   2,   1,   3,   1,
                  2,   1,   1,   1,   1,   1,   1,   1]),
    'yaxis': 'y'
})
        go = <module 'plotly.graph_objects' from '/home/quentin/.local/lib/python3.10/site-packages/plotly/graph_objects/__init__.py'>
    855     print("Invalid trace type returned, expected a trace, got:", type(new_trace))
    856     return plotly_fig, data_for_plot  # Return as is, do not add invalid trace

File ~/.local/lib/python3.10/site-packages/plotly/graph_objects/__init__.py:311, in __getattr__(import_name='BaseTraceType')
    307         from ..missing_ipywidgets import FigureWidget
    309         return FigureWidget
--> 311 return orig_getattr(import_name)
        import_name = 'BaseTraceType'
        orig_getattr = <function relative_import.<locals>.__getattr__ at 0x7f1dfdbc6050>

File ~/.local/lib/python3.10/site-packages/_plotly_utils/importers.py:39, in relative_import.<locals>.__getattr__(import_name='BaseTraceType')
     36     class_module = importlib.import_module(rel_module, parent_name)
     37     return getattr(class_module, class_name)
---> 39 raise AttributeError(
        import_name = 'BaseTraceType'
        parent_name = 'plotly.graph_objects'
     40     "module {__name__!r} has no attribute {name!r}".format(
     41         name=import_name, __name__=parent_name
     42     )
     43 )

AttributeError: module 'plotly.graph_objects' has no attribute 'BaseTraceType'