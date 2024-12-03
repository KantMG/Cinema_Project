
I have df 


        directors  averageRating   isAdult  ...  firstYear  lastYear  numProductions
0             NaN       6.512198  0.021523  ...     1892.0    2030.0          250036
1             5.0       6.978571  0.000000  ...     1946.0    2008.0              73
2             8.0       7.100000  0.000000  ...     1961.0    1961.0               1
3             9.0       5.400000  0.000000  ...     1967.0    1967.0               1
4            10.0       5.900000  0.000000  ...     1957.0    1957.0               1
          ...            ...       ...  ...        ...       ...             ...
759633  9993679.0       0.000000  0.000000  ...     2017.0    2017.0               1
759634  9993694.0       8.750000  0.000000  ...     2021.0    2022.0               2
759635  9993696.0       0.000000  0.000000  ...     2018.0    2018.0               1
759636  9993708.0       0.000000  0.000000  ...     2015.0    2021.0              11
759637  9993709.0       0.000000  0.000000  ...     2015.0    2021.0              11

[759638 rows x 13 columns]


x_column= "birthYear"
y_column= "deathYear"


def count_alive_directors(df, x_column, y_column, z_column):
    # Create a range for the years from the minimum birthYear to maximum deathYear
    min_x_column = int(df[x_column].min())
    max_y_column = int(df[y_column].max())
    New_x_column = range(min_x_column, max_y_column + 1)
    
    alive_counts = []
    avg_new_z_column = []

    for i_x_col in New_x_column:
        count = df[(df[x_column] <= i_x_col) & (df[y_column] >= i_x_col)].shape[0]
        alive_counts.append({'Year': i_x_col, 'count': count})
        
        if z_column is not None:
            # Calculate the average NewRating for alive directors
            new_z_column = df[(df[x_column] <= i_x_col) & (df[y_column] >= i_x_col)][z_column]
            avg_z_column = new_z_column.mean() if not new_z_column.empty else 0
            avg_new_z_column.append(avg_z_column)

    # Convert to DataFrame
    alive_df = pd.DataFrame(alive_counts)
    if z_column is not None:
        alive_df['avg_'+z_column] = avg_new_z_column  # Add average NewRating

    # Count NaN values in birthYear
    nan_birth = df[x_column].isna().sum()
    nan_death = (df[y_column] == -1).sum()

    # Count those alive (NaN in deathYear) with a valid birthYear
    alive_count_na = df[(df[y_column] == -1) & (df[x_column].notna())].shape[0]

    # Collect New_x_column for individuals that are alive (with NaN in deathYear)
    for index, row in df[(df[y_column] == -1) & (df[x_column].notna())].iterrows():
        birth_year = int(row[x_column])  # Get the birth year of the director
        # Increment count for all New_x_column from birth_year to max_year
        for year in range(birth_year, max_y_column + 1):
            if year in alive_df['Year'].values:
                alive_df.loc[alive_df['Year'] == year, 'count'] += 1
    
    print("nan_birth= ",nan_birth)
    print("nan_death= ",nan_death)
    print("alive_count_na= ", alive_count_na)
    x_column, y_column = 'Year', 'count'
    return alive_df, x_column, y_column, z_column
            
            
but this process is very long, can you make it not time conssuming