
# Check the top n rows based on count
top_n_rows = data.nlargest(n, count_column)
print(top_n_rows)

# Now check the unique genres in this result
top_n_genres = top_n_rows[col].unique()
print(top_n_genres)

it gives me that 

     startYear genres_split  count
188       1909        Short    180
240       1912        Short    164
302       1915        Short    154
336       1917        Drama    150
315       1916        Drama    145
294       1915        Drama    140
357       1918        Drama    139
291       1915       Comedy    137
260       1913        Short    133
222       1911        Short    131
['Short' 'Drama' 'Comedy']

so I guess I need first to regroup the genre_split first