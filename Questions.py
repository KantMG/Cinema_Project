
I have data_for_plot:

    startYear  averageRating     error
0        1892       5.818432  0.011458
1        1893       6.000000  0.000000
2        1894       5.180647  0.005904
3        1895       5.591333  0.004534
4        1896       5.706276  0.004609
5        1897       5.436463  0.010913
6        1898       5.939964  0.008605
7        1899       5.476064  0.008092
8        1900       5.140976  0.006978
9        1901       5.978362  0.009196
10       1902       7.823060  0.005002
11       1903       6.512520  0.005191
12       1904       6.439614  0.015324
13       1905       5.439133  0.015305
14       1906       5.859683  0.012217
15       1907       5.323980  0.015654
16       1908       5.248399  0.007751
17       1909       5.297414  0.005975
18       1910       5.428454  0.006951
19       1911       5.775913  0.007010
20       1912       5.715040  0.006042
21       1913       5.800771  0.005338
22       1914       5.433745  0.003697
23       1915       5.821350  0.003680
24       1916       6.261883  0.003978
25       1917       6.237488  0.004570
26       1918       6.106951  0.004549
27       1919       6.264246  0.006335
28       1920       5.532468  0.131590
29       1921       5.000000  0.000000
30       1922       6.000000  0.000000
31       1925       5.256757  0.041100
32       1936       4.000000  0.000000
33       1990       5.000000  0.000000


plotly_fig = px.line(
    data_for_plot,
    x=x_axis,
    y=y_column,
    title='Weighted Average Rating Over the Years',
    error_y=dict(
        type='data',
        array=data_for_plot['error'],
        visible=True,
        color='red'
    )
                )  


but it doesnt work, I got

28    5.532468
29    5.000000
30    6.000000
31    5.256757
32    4.000000
33    5.000000
Name: averageRating, dtype: float64}
        length = 34
        argument = {'type': 'data', 'array': array([0.01145798, 0.        , 0.00590382, 0.00453423, 0.00460943,
       0.01091279, 0.00860535, 0.00809241, 0.00697773, 0.00919593,
       0.00500212, 0.00519091, 0.01532437, 0.01530493, 0.01221728,
       0.01565403, 0.00775082, 0.00597518, 0.00695143, 0.00701007,
       0.0060416 , 0.00533808, 0.00369659, 0.00368049, 0.00397791,
       0.00457018, 0.00454946, 0.00633495, 0.13159034, 0.        ,
       0.        , 0.04109975, 0.        , 0.        ]), 'visible': True, 'color': 'red'}
        field = 'error_y'
        len(argument) = 4
   1275             "All arguments should have the same length. "
   1276             "The length of argument `%s` is %d, whereas the "
   1277             "length of  previously-processed arguments %s is %d"
   1278             % (field, len(argument), str(list(df_output.keys())), length)
   1279         )
   1280     df_output[str(col_name)] = to_unindexed_series(argument, str(col_name))
   1282 # Finally, update argument with column name now that column exists

ValueError: All arguments should have the same length. The length of argument `error_y` is 4, whereas the length of  previously-processed arguments ['startYear', 'averageRating'] is 34
