I have 

                plotly_fig = px.bar(
                   data_for_plot, 
                   x=x_axis, 
                   y=y_axis,
                   color=z_axis if "Movie" not in g_column else None,
                   animation_frame=z_axis if "Movie" in g_column else None,
                   range_y=[data_for_plot[y_axis].min(), data_for_plot[y_axis].max()] if "Movie" in g_column else None
                   )