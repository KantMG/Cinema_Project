I have he dataframe data_for_plot

     startYear genres_split  count
0         1892       Comedy      1
1         1892         Long      1
2         1892        Other      3
3         1892      Romance      1
4         1892        Short      2
..         ...          ...    ...
198       1936         Long      1
199       1936        Other      1
200       1936      Western      1
201       1990       Comedy      1
202       1990        Short      1

[203 rows x 3 columns]


x_axis = "startYear"
y_axis = "count"
z_axis = "genres_split"

I want to apply         

window_lenght = len(data_for_plot[x_axis])//5
data_for_plot[y_axis] = signal.savgol_filter(data_for_plot[y_axis],
                       window_lenght, # window size used for filtering
                       smt_order_value)

but I want to do it for each unique vlue of genres_split.

which mean that the signal.savgol_filter must be done on the unique genres_split sepratetly, but all the new filter value must replace the unfilterd value of the data_for_plot 


I have the dataframe

     startYear genres_split  count
0         1892       Comedy      1
1         1892         Long      1
2         1892        Other      3
3         1892      Romance      1
4         1892        Short      2
..         ...          ...    ...
198       1936         Long      1
199       1936        Other      1
200       1936      Western      1
201       1990       Comedy      1
202       1990        Short      1

[203 rows x 3 columns]


 the function 

        # Function to apply savgol_filter
        def apply_savgol_filter(group):
            # Calculate window length based on the size of the group
            window_length = len(group)//5
            
            # Ensure that window_length is odd and less than or equal to the total group length
            if window_length < 3:  # Savitzky-Golay filter needs at least a size of 3
                return group  # Skip filtering for groups too small
            
            if window_length % 2 == 0:
                window_length -= 1  # Make sure window_length is odd
            
            print(group[y_axis])
            print("window_length=",window_length)
            # Apply the savgol_filter
            filtered_values = signal.savgol_filter(group[y_axis], window_length, smt_order_value)

            # Replace the original 'count' with the filtered values
            group[y_axis] = filtered_values
            
            print("filtered_values=",filtered_values)
            
            return group
        
        # Apply the filter to each genre
        data_for_plot_filter = data_for_plot.groupby(z_axis, as_index=False).apply(apply_savgol_filter)

add an index 

       startYear genres_split  count
0 28        1899    Adventure    1.0
  47        1902    Adventure    1.0
  53        1903    Adventure    3.0
  61        1904    Adventure    1.0
  68        1905    Adventure    1.0
         ...          ...    ...
7 160       1916      Western   22.0
  168       1917      Western   30.0
  176       1918      Western   28.0
  184       1919      Western   14.0
  200       1936      Western    1.0

[203 rows x 3 columns]


I dont want to have th new indice




     startYear genres_split  count
0         1892       Comedy      1
1         1892         Long      1
2         1892        Other      3
3         1892      Romance      1
4         1892        Short      2
..         ...          ...    ...
198       1936         Long      1
199       1936        Other      1
200       1936      Western      1
201       1990       Comedy      1
202       1990        Short      1

[203 rows x 3 columns]


