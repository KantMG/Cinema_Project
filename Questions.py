#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 15:56:01 2024

@author: quentin
"""


I am working with a dataframe df with all these columns
['tconst', 'startYear', 'runtimeMinutes', 'genres', 'isAdult', 'averageRating', 'numVotes']
the size is 
Dask DataFrame size: 3297.73 MB (3.22 GB)

the number of partition is npartitions

the 
Dask DataFrame Structure:
                tconst isAdult startYear runtimeMinutes  genres directors writers averageRating numVotes
npartitions=20                                                                                          
                object  object    object         object  object    object  object       float64  float64
    ...       ...            ...     ...       ...     ...           ...      ...
               ...     ...       ...            ...     ...       ...     ...           ...      ...
    ...       ...            ...     ...       ...     ...           ...      ...
    ...       ...            ...     ...       ...     ...           ...      ...
Dask Name: repartition, 14 graph layers


inside directors and writers columns there is indices as nm0769144 which correspond to the id 
from the first column from another tsv file.
I want to replace the indice by the full name of the directors, writers which are in the column of the other file
What is the fastest way to do that with dask



####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################



I am working with a dataframe df with all these columns
['tconst', 'startYear', 'runtimeMinutes', 'genres', 'isAdult', 'averageRating', 'numVotes']
the size is 
Dask DataFrame size: 3297.73 MB (3.22 GB)

the number of partition is npartitions

the 
Dask DataFrame Structure:
                tconst isAdult startYear runtimeMinutes  genres directors writers averageRating numVotes
npartitions=20                                                                                          
                object  object    object         object  object    object  object       float64  float64
    ...       ...            ...     ...       ...     ...           ...      ...
               ...     ...       ...            ...     ...       ...     ...           ...      ...
    ...       ...            ...     ...       ...     ...           ...      ...
    ...       ...            ...     ...       ...     ...           ...      ...
Dask Name: repartition, 14 graph layers


inside directors and writers columns there is indices as nm0769144 which correspond to the id 
from the first column from another tsv file named name_file.
I want to write an indice and get all the rows from the first dask dataframe where this indice appear
What is the fastest way to do that with dask



####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################

I am working with a dataframe df with all these columns
['tconst', 'startYear', 'runtimeMinutes', 'genres', 'isAdult', 'averageRating', 'numVotes']
the size is 
Dask DataFrame size: 3297.73 MB (3.22 GB)

the number of partition is npartitions

the 
Dask DataFrame Structure:
                tconst isAdult startYear runtimeMinutes  genres directors writers averageRating numVotes
npartitions=20                                                                                          
                object  object    object         object  object    object  object       float64  float64
    ...       ...            ...     ...       ...     ...           ...      ...
               ...     ...       ...            ...     ...       ...     ...           ...      ...
    ...       ...            ...     ...       ...     ...           ...      ...
    ...       ...            ...     ...       ...     ...           ...      ...
Dask Name: repartition, 14 graph layers


I know that in the at least on row contains
          # tconst  isAdult  ...  directors                        writers
# 19995  tt0010152      NaN  ...  nm0769144  nm0399203,nm0458691,nm0853130


# The ID we want to search for
search_id = "nm0769144"
    
# Filter only the directors first
filtered_directors = df[df['directors'].fillna('').str.contains(search_id)]
filtered_directors = filtered_directors.persist()

# Now filter only the writers from the original DataFrame
filtered_writers = df[df['writers'].fillna('').str.contains(search_id)]
filtered_writers = filtered_writers.persist()

# Finally, combine the two filtered results
filtered_df = dd.concat([filtered_directors, filtered_writers]).drop_duplicates()


print(filtered_df)

Dask DataFrame Structure:
               tconst isAdult startYear runtimeMinutes  genres directors writers averageRating numVotes
npartitions=1                                                                                          
               object  object    object         object  object    object  object       float64  float64
                  ...     ...       ...            ...     ...       ...     ...           ...      ...
Dask Name: drop-duplicates-agg, 5 graph layers

# # Now compute or inspect the filtered result
result = filtered_df.compute()
print(result)

but I get 

Empty DataFrame
Columns: [tconst, isAdult, startYear, runtimeMinutes, genres, directors, writers, averageRating, numVotes]
Index: []



####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################



List_file=['title.basics.tsv', 'title.crew.tsv', 'title.ratings.tsv']
# Use glob to find all the CSV files
for file in List_file:
    if file =='title.basics.tsv':
        usecol=["tconst", "startYear", "runtimeMinutes", "genres", "isAdult"]
    if file =='title.crew.tsv':
        usecol=["tconst", "directors", "writers"]
    if file =='title.ratings.tsv':
        usecol=["tconst", "averageRating", "numVotes"]
    if file =='title.principals.tsv':
        usecol=["tconst", "nconst", "category", "characters"]
        
    if Large_file_memory==False:
        df = pd.read_csv(Project_path+file, sep=';', usecols=usecol, encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    else:
        df = dd.read_csv(
            Project_path+file,
            sep='\t',
            usecols=usecol,
            encoding='utf-8',
            on_bad_lines='skip',
            quotechar='"',
            dtype={
                'runtimeMinutes': 'object',   # Read as object to handle invalid values
                'startYear': 'object',        # Read as object to handle invalid values
                'isAdult': 'object'           # Read as object to handle invalid values
            }
        )
        df = df.replace('\\N', np.nan)
    
    dis.infos_on_data(df) if Get_file_sys_mem==True else None
    
    # df = pd.read_csv(Project_path+file, sep=';', usecols=usecol, encoding='utf-8', on_bad_lines='skip', quotechar='"')
    df_list.append(df)  # Append the DataFrame to the list
        


# Concatenate the Dask dataframes along rows (axis=0)
concatenated_df = dd.concat(df_list, axis=0, join='outer', ignore_index=True)
print("Concatenation is done")

print(concatenated_df.isnull().sum())

# Drop duplicates based on the common_column
result_df = concatenated_df.drop_duplicates(subset=common_column)
print("Drop duplicates is done")

# Repartition the Dask DataFrame to increase parallelism
df = result_df.repartition(npartitions=desired_number_of_partitions)
print(df)

but all the value in the column rating are Nan in the new df



if file =='title.ratings.tsv':
    print(df.head(1000))
        tconst  averageRating  numVotes
0    tt0000001            5.7      2081
1    tt0000002            5.6       280
2    tt0000003            6.5      2078
3    tt0000004            5.4       181
4    tt0000005            6.2      2816
..         ...            ...       ...
995  tt0002020            4.7       159
996  tt0002022            6.0        12
997  tt0002026            4.5        16
998  tt0002029            6.0        72
999  tt0002031            4.5        25













merged_df = dd.map_partitions(custom_merge, merged_df, df)

Traceback (most recent call last):

  File ~/.local/lib/python3.10/site-packages/spyder_kernels/customize/utils.py:209 in exec_encapsulate_locals
    exec_fun(compile(code_ast, filename, "exec"), globals)

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/Main.py:133
    Para, y = main()

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/Main.py:122 in main
    Para, y = adg3.movie_making_over_year(Project_path,Large_file_memory, desired_number_of_partitions, Get_file_sys_mem)

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/analysation_dataframe_goal3.py:139 in movie_making_over_year
    merged_df = dd.map_partitions(custom_merge, merged_df, df)

  File ~/.local/lib/python3.10/site-packages/dask/dataframe/core.py:7025 in map_partitions
    raise ValueError(

ValueError: Not all divisions are known, can't align partitions. Please use `set_index` to set the index.. If you don't want the partitions to be aligned, and are calling `map_partitions` directly, pass `align_dataframes=False`.

####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################





title.basics.tsv ['tconst', 'startYear', 'runtimeMinutes', 'genres', 'isAdult']
      tconst isAdult startYear runtimeMinutes                    genres
0  tt0000001       0      1894              1         Documentary,Short
1  tt0000002       0      1892              5           Animation,Short
2  tt0000003       0      1892              5  Animation,Comedy,Romance
3  tt0000004       0      1892             12           Animation,Short
4  tt0000005       0      1893              1              Comedy,Short
title.crew.tsv ['tconst', 'directors', 'writers']
      tconst  ...                                            writers
0  tt0848510  ...                                                NaN
1  tt0848520  ...                                          nm1757238
2  tt0848537  ...  nm0366337,nm0431622,nm0792092,nm0040022,nm0256...
3  tt0848545  ...                                          nm2315992
4  tt0848585  ...                                          nm1765797

[5 rows x 7 columns]
title.ratings.tsv ['tconst', 'averageRating', 'numVotes']
      tconst isAdult  ... averageRating numVotes
0  tt6440358       0  ...           9.9       99
1  tt6440396       0  ...           7.6       16
2  tt6440632       0  ...           1.0       14
3  tt6440774       0  ...           6.9       33
4  tt6441046       0  ...           9.8        5

[5 rows x 9 columns]
Time taken to load df: 86.59 seconds



####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################


List_file=['title.basics.tsv', 'title.crew.tsv', 'title.ratings.tsv']

# List to store DataFrames
df_list = []

common_column = 'tconst'  # Replace with the actual common variable (e.g., 'ID', 'Date')

# Use glob to find all the CSV files
for file in List_file:
    if file =='title.basics.tsv':
        usecol=["tconst", "startYear"]
    if file =='title.crew.tsv':
        usecol=["tconst", "directors", "writers"]
    if file =='title.ratings.tsv':
        usecol=["tconst", "averageRating", "numVotes"]
    if file =='title.principals.tsv':
        usecol=["tconst", "nconst", "category", "characters"]
    
    print(file,usecol)
    
    if Large_file_memory==False:
        df = pd.read_csv(Project_path+file, sep=';', usecols=usecol, encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
    else:
        df = dd.read_csv(
            Project_path+file,
            sep='\t',
            usecols=usecol,
            encoding='utf-8',
            on_bad_lines='skip',
            quotechar='"',
            dtype={
                'runtimeMinutes': 'object',   # Read as object to handle invalid values
                'startYear': 'object',        # Read as object to handle invalid values
                'isAdult': 'object'           # Read as object to handle invalid values
            }
        )
        df = df.replace('\\N', np.nan)
        # df=df.repartition(npartitions=desired_number_of_partitions)
        
    print(df.head())  # Check if ratings are preserved after merging
    
    df_list.append(df)  # Append the DataFrame to the list

print("Time taken to load df: {:.2f} seconds".format(time.time() - start_time))        

# # Concatenate the Dask dataframes along rows (axis=0)
concatenated_df = dd.concat(df_list, axis=0, join='outer', ignore_index=True)
print("Concatenation is done")
# Drop duplicates based on the common_column
result_df = concatenated_df.drop_duplicates(subset=common_column)
print("Drop duplicates is done")
print(result_df.head())


output is:

title.basics.tsv ['tconst', 'startYear']
      tconst startYear
0  tt0000001      1894
1  tt0000002      1892
2  tt0000003      1892
3  tt0000004      1892
4  tt0000005      1893
title.crew.tsv ['tconst', 'directors', 'writers']
      tconst  directors writers
0  tt0000001  nm0005690     NaN
1  tt0000002  nm0721526     NaN
2  tt0000003  nm0721526     NaN
3  tt0000004  nm0721526     NaN
4  tt0000005  nm0005690     NaN
title.ratings.tsv ['tconst', 'averageRating', 'numVotes']
      tconst  averageRating  numVotes
0  tt0000001            5.7      2081
1  tt0000002            5.6       280
2  tt0000003            6.5      2078
3  tt0000004            5.4       181
4  tt0000005            6.2      2816
Time taken to load df: 3.90 seconds
Concatenation is done
Drop duplicates is done
      tconst startYear directors writers  averageRating  numVotes
0  tt0000001      1894       NaN     NaN            NaN       NaN
1  tt0000002      1892       NaN     NaN            NaN       NaN
2  tt0000003      1892       NaN     NaN            NaN       NaN
3  tt0000004      1892       NaN     NaN            NaN       NaN
4  tt0000005      1893       NaN     NaN            NaN       NaN

after the concatenation operation of the list df_list the value in  directors writers  averageRating  numVotes are Nan


####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################


List_col = ["directors", "writers", "averageRating", "numVotes"]

List_filter = ["nm0005690", None, ">=5.6", None]



df = open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)


def open_dataframe(requested_columns, requested_filters, Project_path, Large_file_memory, Get_file_sys_mem):

    # Start the timer
    start_time = time.time()  
    
    # Define the mapping of files to their columns and their types
    file_columns_mapping = {
        'title.basics.tsv': {
            "columns": ["tconst", "startYear", "runtimeMinutes", "genres", "isAdult"],
            "types": {
                "tconst": str,
                "startYear": float,
                "runtimeMinutes": str,
                "genres": str,
                "isAdult": float
            }
        },
        'title.crew.tsv': {
            "columns": ["tconst", "directors", "writers"],
            "types": {
                "tconst": str,
                "directors": str,
                "writers": str
            }
        },
        'title.ratings.tsv': {
            "columns": ["tconst", "averageRating", "numVotes"],
            "types": {
                "tconst": str,
                "averageRating": float,
                "numVotes": float
            }
        },
        'title.principals.tsv': {
            "columns": ["tconst", "nconst", "category", "characters"],
            "types": {
                "tconst": str,
                "nconst": str,
                "category": str,
                "characters": str
            }
        }
    }
    
    # Create a dictionary to map each requested column to its filter
    column_filter_mapping = dict(zip(requested_columns, requested_filters))
    
    # Determine which files need to be opened
    files_to_open = []
    columns_in_files = {}
    
    # Iterate through each file and check if it has any of the requested columns
    for file, info in file_columns_mapping.items():
        columns = info["columns"]
        types = info["types"]
        
        # Find the intersection of requested columns and columns in the current file
        common_columns = set(requested_columns).intersection(columns)
        if common_columns:  # Only consider files that have at least one requested column
            files_to_open.append(file)
            # Track the columns that should be used from this file, always including 'tconst' if present
            if "tconst" in columns:
                common_columns.add("tconst")
            columns_in_files[file] = {
                "columns": common_columns,
                "types": {col: types[col] for col in common_columns if col in types},  # Map each column to its type
                "filters": {col: column_filter_mapping[col] for col in common_columns if col in column_filter_mapping}
            }
    
    # Identify common columns between files to be opened
    if len(files_to_open) > 1:
        # Find common columns among all files using set intersection
        common_columns_all_files = set.intersection(*(columns_in_files[file]["columns"] for file in files_to_open))
    else:
        common_columns_all_files = set(columns_in_files[files_to_open[0]]["columns"])
    
    # Ensure 'tconst' is added as a common column if at least two files are being opened and 'tconst' exists in those files
    tconst_in_files = all("tconst" in file_columns_mapping[file]["columns"] for file in files_to_open)
    if len(files_to_open) > 1 and tconst_in_files:
        common_columns_all_files.add("tconst")
    
    # Print the results
    print("Files to open:", files_to_open)
    print("Common columns across all selected files:", common_columns_all_files)
    
    print("Columns, filters, and types in each selected file:")
    for file, info in columns_in_files.items():
        print(f"{file}:")
        print("  Columns:", info["columns"])
        print("  Filters:", info["filters"])
        print("  Types:", info["types"])


    # Create DataFrames based on the files, columns, and filters
    dataframes = []
    for file, info in columns_in_files.items():
        # Define the columns to read from the file
        usecols = list(info["columns"])

        # Create a dictionary to define the dtypes for the DataFrame
        dtype_mapping = {col: info["types"][col] for col in usecols if col in info["types"]}       
        
        # Read the file into a DataFrame
        if Large_file_memory==False:
            df = pd.read_csv(Project_path+file, sep=';', usecols=usecols, encoding='utf-8', on_bad_lines='skip', quotechar='"')  #, index_col=0      
        else:
            df = dd.read_csv(
                Project_path+file,
                sep='\t',
                usecols=usecols,
                encoding='utf-8',
                na_values='\\N',  # Specify \\N as NaN
                on_bad_lines='skip',
                quotechar='"',
                dtype=dtype_mapping
            )
        print("Data types after loading:")
        print(df.dtypes)            

       # Convert columns to the specified types
        for col, expected_type in info["types"].items():
            if expected_type == float:
                if Large_file_memory:
                    print(col)
                    df[col] = dd.to_numeric(df[col], errors='coerce')
                    na_count = df[col].isna().sum().compute()  # Evaluate the count
                    print(f"NA count in '{col}': {na_count}")
    
                    # Handle NA values
                    df[col] = df[col].fillna(-1)  # Fill with -1 or another value as necessary
    
                df[col] = df[col].astype('float64')  # Use 'Int64' for nullable integers
                
            elif expected_type == str:
                df[col] = df[col].fillna('')  # Fill NaN with empty string for string columns


        # df=df.repartition(npartitions=desired_number_of_partitions)
        
        # Get the infos on the DataFrame
        dis.infos_on_data(df) if Get_file_sys_mem==True else None
        
        # Apply the filter to the DataFrame
        df = apply_filter(df, usecols, info["filters"])
                
        # Add the DataFrame to the list
        dataframes.append(df)
    
    # Print a preview of each loaded and filtered DataFrame
    for idx, df in enumerate(dataframes):
        print(f"\nDataFrame {idx + 1} from {files_to_open[idx]}:")
        print(df.head(10))
        print()
            
    
    print("Time taken to load all dataframe: {:.2f} seconds".format(time.time() - start_time))        
    print("")
    
    # Merge Dask DataFrames on 'tconst' to create a single unified DataFrame
    if len(dataframes) > 1:
        merged_df = dataframes[0].compute()
        print(merged_df.dtypes)
        print(merged_df.head(10))
        for df in dataframes[1:]:
            print(df.dtypes)
            print(df.head(10))
            merged_df = dd.merge(merged_df, df.compute(), on='tconst', how='inner')
    else:
        merged_df = dataframes[0]
    
    # Print the final merged DataFrame (head only, to avoid loading too much data)
    print("\nFinal Merged DataFrame:")
    print(merged_df.head(100))
    # print(merged_df.compute())
    print()
    print("Time taken to merge all dataframe: {:.2f} seconds".format(time.time() - start_time))

    return merged_df


def apply_filter(df, col, filters):
    
    for col, filter_value in filters.items():
                
        if filter_value != None:
            if ">=" in filter_value:
                # Handle greater than or equal filters (e.g., ">=7.0")
                threshold = float(filter_value.split(">=")[1])
                df = df[df[col] >= threshold]
            elif "<=" in filter_value:
                # Handle less than or equal filters (e.g., "<=5.0")
                threshold = float(filter_value.split("<=")[1])
                df = df[df[col] <= threshold]
            elif "=" in filter_value:
                # Handle equality filters (e.g., "=nm0005690")
                value = filter_value.split("=")[1]
                df = df[df[col] == value]
            else:
                # Handle other string-based filters (e.g., "actor")
                df = df[df[col].str.contains(filter_value, na=False)]    
        
    return df


it returns 

Files to open: ['title.crew.tsv', 'title.ratings.tsv']
Common columns across all selected files: {'tconst'}
Columns, filters, and types in each selected file:
title.crew.tsv:
  Columns: {'tconst', 'writers', 'directors'}
  Filters: {'writers': None, 'directors': 'nm0005690'}
  Types: {'tconst': <class 'str'>, 'writers': <class 'str'>, 'directors': <class 'str'>}
title.ratings.tsv:
  Columns: {'tconst', 'averageRating', 'numVotes'}
  Filters: {'averageRating': '>=5.6', 'numVotes': None}
  Types: {'tconst': <class 'str'>, 'averageRating': <class 'float'>, 'numVotes': <class 'float'>}
Data types after loading:
tconst       object
directors    object
writers      object
dtype: object
Data types after loading:
tconst            object
averageRating    float64
numVotes         float64
dtype: object
averageRating
NA count in 'averageRating': 0
numVotes
Traceback (most recent call last):

  File ~/.local/lib/python3.10/site-packages/pandas/core/arrays/integer.py:53 in _safe_cast
    return values.astype(dtype, casting="safe", copy=copy)

TypeError: Cannot cast array data from dtype('float64') to dtype('int64') according to the rule 'safe'


The above exception was the direct cause of the following exception:

Traceback (most recent call last):

  File ~/.local/lib/python3.10/site-packages/spyder_kernels/customize/utils.py:209 in exec_encapsulate_locals
    exec_fun(compile(code_ast, filename, "exec"), globals)

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/Main.py:133
    Para, y = main()

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/Main.py:122 in main
    Para, y = adg3.movie_making_over_year(Project_path,Large_file_memory, desired_number_of_partitions, Get_file_sys_mem)

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/analysation_dataframe_goal3.py:109 in movie_making_over_year
    df = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/open_dataframe.py:158 in open_dataframe
    na_count = df[col].isna().sum().compute()  # Evaluate the count

  File ~/.local/lib/python3.10/site-packages/dask/base.py:372 in compute
    (result,) = compute(self, traverse=False, **kwargs)

  File ~/.local/lib/python3.10/site-packages/dask/base.py:660 in compute
    results = schedule(dsk, keys, **kwargs)

  File ~/.local/lib/python3.10/site-packages/pandas/core/arrays/integer.py:59 in _safe_cast
    raise TypeError(

TypeError: cannot safely cast non-equivalent float64 to int64




print(name_info.head())

print(name_info['nconst'].compute())

      nconst   primaryName  birthYear  deathYear
0  nm0000001  Fred Astaire     1899.0     1987.0

0          nm0000001
383145    nm10313850
363499    nm12584561
560026     nm3013608
Name: nconst, dtype: object





####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################

Here is my code.



Project_path='/home/quentin/Documents/Work/Data_analytics/Datasets/Cinema_Project/'
Large_file_memory = True
Get_file_sys_mem = False
desired_number_of_partitions = 10
Test_data = True

if Test_data == True:
    Project_path=Project_path+'Test_data/'

List_col = ["nconst", "primaryName", "birthYear", "deathYear"]

List_filter = [None, None, None, None]

df1 = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)

print(df1)


# Initialize the Dash app with suppress_callback_exceptions set to True
app, dark_dropdown_style, uniform_style = wis.web_interface_style()

app.layout = html.Div([
    # Tabs Component
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Tab 1', value='tab-1'),
        dcc.Tab(label='Tab 2', value='tab-2'),
        dcc.Tab(label='Tab 3', value='tab-3'),
    ]),

    # Hidden store to hold df2 data
    dcc.Store(id='stored-df2', data=None),
    
    # Content Div for Tabs
    html.Div(id='tabs-content')
])

# Callback to manage tab content
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-example', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        # This is the content for Tab 1 - the existing layout we created
        return html.Div([
            html.Div([
                html.P(f'This interface is dedicated to the research on specific artist.'),
            ]),
            dcc.Input(id='input-value', type='text', placeholder='Enter a value...', style={**dark_dropdown_style, **uniform_style}),
            html.Div(id='dynamic-content')
        ])
    elif tab == 'tab-2':
        # Placeholder for Tab 2 content
        return html.Div([
            html.H3('Tab 2 Content'),
            html.P('This is a placeholder for Tab 2. You can add any content you like here.')
        ])
    elif tab == 'tab-3':
        # Placeholder for Tab 3 content
        return html.Div([
            html.H3('Tab 3 Content'),
            html.P('This is a placeholder for Tab 3. You can add any content you like here.')
        ])

# Callback to update UI based on input value in Tab 1
@app.callback(
    [Output('dynamic-content', 'children'), Output('stored-df2', 'data')],
    Input('input-value', 'value')
)
def update_ui(input_value):
    if not input_value:  # Return nothing if input is empty or None
        return '', None
    
    # Check if the input value exists in the 'nconst' column of df1
    if input_value in df1['primaryName'].values:
        # Create dropdown options based on df2
        # dropdown_options = [
        #     {'label': row['directors'], 'value': row['directors']} for index, row in df2.iterrows()
        # ]

        nconst_value = df1[df1['primaryName'] == input_value]['nconst'].iloc[0]
        
        # Display the found nconst value (for debugging purposes)
        print(f"Matched nconst: {nconst_value}")
                        
        List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters", "title", "isOriginalTitle"]
        
        List_filter = [None, None, None, None, None, None, None, None, nconst_value, None, None, None, True]
        
        df2 = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        exclude_col = ["tconst", "isAdult", "nconst", "isOriginalTitle"]
        df2 = df2.drop(columns=exclude_col)

        
        if df2.empty: 
            return html.Div([
                html.Div([
                    html.P(f'The artist '+input_value+' doesnt have referenced movies.'),
                ])
                ], style={'padding': '20px'}), df2.to_dict('records')        
        else:
            # Create the table with the appropriate dropdowns for each column
            dropdowns_with_labels, data_table = tds.dropdown_table(df2, 'table-df2', dark_dropdown_style, uniform_style)
    
            return html.Div([
                html.Div(style={'display': 'flex', 'margin-top': '10px', 'flex-wrap': 'wrap'}, children=[
                    html.Div(dropdowns_with_labels, style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'})
                ]),
                html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
                    html.Div(data_table, style={'width': '100%'})  # Adjusted to take full width
                ])
            ], style={'padding': '20px'}), df2.to_dict('records')
        
    
    # If the input does not correspond to any primaryName, filter df1
    filtered_df = df1[df1['primaryName'].str.contains(input_value, case=False, na=False)]

    # Default case: show table based on df1    
    # Calculate widths, ensuring 'title' is handled specifically
    column_widths = {col: tds.get_max_width(df1[col], col) for col in df1.columns}
    return dash_table.DataTable(
        id='table-df1',
        data=filtered_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df1.columns],
        fixed_rows={'headers': True},
        style_table={
            'minWidth': str(int(len(df1.columns) * 170)) + 'px',  # Minimum width calculation
            'overflowX': 'auto',  # Allow horizontal scrolling
            'paddingLeft': '2px',  # Add padding to prevent it from being cut off
            'paddingRight': '20px',
            'marginLeft': '8px'  # Ensure some margin on the left side
        },
        style_cell={
            'backgroundColor': '#1e1e1e',
            'color': '#f8f9fa',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'whiteSpace': 'nowrap',
            'textAlign': 'center',
            'height': '40px',
            'lineHeight': '40px'
        },
        fixed_columns={'headers': True, 'data': 0},
        style_data_conditional=[
            {
                'if': {'column_id': col},
                'width': f'{column_widths[col]}px'
            } for col in df1.columns
        ],
        style_header={
            'backgroundColor': '#343a40',
            'color': 'white',
            'whiteSpace': 'nowrap',
            'textAlign': 'center',
            'height': '40px'
        },
        style_data={
            'whiteSpace': 'nowrap',
            'textAlign': 'center',
            'backgroundColor': '#1e1e1e',
        }
    ), None


# Create a list of Input objects for each dropdown
List_col = ["startYear", "runtimeMinutes", "genres", "directors", "writers", "averageRating", "numVotes", "category", "characters", "title"]
dropdown_inputs = [Input(f'{col}-dropdown', 'value') for col in List_col]

@app.callback(
    Output('table-df2', 'data'),
    dropdown_inputs,
    State('stored-df2', 'data')  # Ensure this is included as State
)
def filter_df2(*selected_values, stored_df2):
    
    print(f"Stored Data (stored_df2): {stored_df2}")
    
    if stored_df2 is None:  # Check if stored_df2 is None or empty
        return []
    
    # Convert the stored data back to a DataFrame
    df2 = pd.DataFrame(stored_df2)

    # Apply filtering from selected dropdown values
    for i, selected_value in enumerate(selected_values):
        if selected_value:
            col_name = df2.columns[i]
            df2 = df2[df2[col_name] == selected_value]

    return df2.to_dict('records')


Request:  I got the error below when I do select in the input a name which allow the creation of df2


Callback error updating table-df2.data
7:33:10 PM
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
TypeError: filter_df2() missing 1 required keyword-only argument: 'stored_df2'




####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################

Here is my code.



app, dark_dropdown_style, uniform_style = web_interface_style()

def web_interface_style():

    # Initialize the Dash app with the dark theme
    app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])  # Use the DARKLY theme from Bootstrap

    # Define dark theme styles
    dark_dropdown_style = {
        'backgroundColor': '#1e1e1e',  # Dark background for dropdown
        'color': '#f8f9fa',  # White text color
        'border': '1px solid #555',  # Border for dropdown
        'borderRadius': '5px',
        'width': '160px',
    }


    # Define a consistent style for both input and dropdown elements
    uniform_style = {
        'width': '160px',  # Set a consistent width
        'height': '40px',  # Set a consistent width
        'borderRadius': '5px',  # Optional: Add rounded corners
    }

    # CSS to style the dropdown's options menu (this will apply globally)
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Dash Dark Theme</title>
            <style>
                body {
                    background-color: #343a40; /* Ensure dark background */
                    color: white; /* Ensure white text */
                }
                
                /* Dark theme for dropdown options */
                .Select-menu-outer {
                    background-color: #333 !important;  /* Dark background for the options menu */
                    color: white !important;  /* White text for the options */
                }
                
                .Select-option {
                    background-color: #333 !important;  /* Dark background for individual options */
                    color: white !important;  /* White text */
                }
                
                .Select-option.is-focused {
                    background-color: #444 !important;  /* Highlight option on hover */
                    color: white !important;  /* Ensure the text stays white */
                }
                
                .Select-control {
                    background-color: #1e1e1e !important;  /* Dark background for the dropdown control */
                    color: white !important;  /* White text */
                    border: 1px solid #555 !important;  /* Dark border */
                }
                
                /* Ensuring selected text in the dropdown remains white */
                .Select-value-label {
                    color: white !important;
                }
            </style>
        </head>
        <body>
            <div id="react-entry-point">
                {%app_entry%}
            </div>
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''
    
    return app, dark_dropdown_style, uniform_style


app.layout = html.Div([
    # Tabs Component
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='🏠 Home', value='tab-1', className='tab-3d', selected_className='tab-3d-selected'),
        dcc.Tab(label='📈 Analytics', value='tab-2', className='tab-3d', selected_className='tab-3d-selected'),
        dcc.Tab(label='Tab 3', value='tab-3', className='tab-3d', selected_className='tab-3d-selected'),
    ]),

    # Hidden store to hold df2 data
    dcc.Store(id='stored-df2', data=None),
    
    # Content Div for Tabs
    html.Div(id='tabs-content')
])

and my style.css file is
/* General style for the tabs container */
.tab-3d {
    background-color: #1e1e1e; /* Dark background for the tabs */
    color: white; /* Text color */
    border: none; /* Remove default border */
}

/* Style for the selected tab */
.tab-3d-selected {
    background-color: #333; /* Slightly lighter background for selected tab */
    color: white; /* Text color */
    border-bottom: 3px solid white; /* White line effect */
}

/* Style for the tab content */
#tabs-content {
    background-color: #2a2a2a; /* Darker background for the content area */
    color: white; /* White text for content */
    padding: 20px; /* Padding for content */
    border-radius: 5px; /* Rounded corners for the content area */
}

/* Optional: Add hover effect for tabs */
.tab-3d:hover {
    background-color: #444; /* Slightly lighter on hover */
}

/* Optional: Style for tab text */
.tab-3d {
    font-weight: bold; /* Make tab text bold */
}

/* Additional styles for the footer if needed */
footer {
    background-color: #1e1e1e; /* Match the dark theme */
    color: white; /* White text */
}

but the tabs are not in dark black as you can see on the picture


####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################

Here is my code.



app.layout = html.Div([
    # Tabs Component
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(id='tabs-1', label='🏠 Home', value='tab-1', 
                 style={
                     'backgroundColor': '#000000',  # Dark black background
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                     'position': 'relative'  # Relative position for pseudo-element
                 },
                 selected_style={
                     'backgroundColor': '#222222',  # Slightly lighter for selected tab
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                 }),
        dcc.Tab(id='tabs-2', label='📈 Analytics', value='tab-2', 
                 style={
                     'backgroundColor': '#000000',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                     'position': 'relative'
                 },
                 selected_style={
                     'backgroundColor': '#222222',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                 }),
        dcc.Tab(id='tabs-3', label='🎥 Movies & Artists', value='tab-3', 
                 style={
                     'backgroundColor': '#000000',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                     'position': 'relative'
                 },
                 selected_style={
                     'backgroundColor': '#222222',
                     'color': 'white',
                     'border': 'none',
                     'borderBottom': '2px solid white',
                     'borderRight': '2px solid white',
                 }),
    ]),
    
    # Hidden store to hold df1 data
    dcc.Store(id='stored-df1', data=None),
    
    # Hidden store to hold df2 data
    dcc.Store(id='stored-df2', data=None),
        
    # Content Div for Tabs
    html.Div(id='tabs-content')
])

# Callback to manage tab content
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'),
    State('stored-df1', 'data')
)
def render_content(tab, stored_df1):
    if tab == 'tab-1':
        # Placeholder for Tab 3 content
        return html.Div([
            html.H1("IMDB database analysis.", style={"color": "#FFD700"}, className="text-light"),
            tab1_content()
        ])
    elif tab == 'tab-2':
        # Placeholder for Tab 2 content
        return html.Div([
            html.H1("Graphic interface dedicated to the dataframe related to the overall IMDB database.", style={"color": "#FFD700"}, className="text-light"),
            tab2_content(stored_df1)
        ])
    elif tab == 'tab-3':
        # This is the content for Tab 1 - the existing layout we created
        return html.Div([
            html.Div([
                html.H1("Research on an artist or a movie.", style={"color": "#FFD700"}, className="text-light"),
            ]),
            dcc.Input(id='input-value', type='text', placeholder='Enter a value...', style={**dark_dropdown_style, **uniform_style}),
            html.Div(id='dynamic-content')
        ])



# =============================================================================
# =============================================================================
# =============================================================================
# Tab-1
# =============================================================================
# =============================================================================
# =============================================================================

def tab1_content():
    
    Text = f"The IMDB is large ...."
    
    
    return html.Div([
        html.Div([
            html.P(Text),
        ])
        ], style={'padding': '20px'})


# =============================================================================
# =============================================================================
# =============================================================================
# Tab-2
# =============================================================================
# =============================================================================
# =============================================================================


def tab2_content(stored_df1):
    # If df1 has already been processed, use it
    if stored_df1:
        df1 = pd.read_json(stored_df1, orient='split')
    else:
        # Load data and process when tab 2 is active

        List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters", "title", "isOriginalTitle"]
        
        List_filter = [None, None, None, None, None, None, None, None, None, None, None, None, True]
        
        df1 = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        exclude_col = ["tconst", "isAdult", "nconst", "isOriginalTitle"]
        df1 = df1.drop(columns=exclude_col)
    
        # Step 1: Split the strings into individual elements and flatten the list
        all_elements = df1['category'].str.split(',').explode().str.strip()
        primaryProfession = all_elements.value_counts()
        primaryProfession = primaryProfession[primaryProfession > 1].index.tolist()
    
        exclude_col = ["title", "characters"]
        df1_filter = df1.drop(columns=exclude_col)            
        dropdowns_with_labels_for_fig_tab2 = fds.dropdown_figure(df1_filter, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style, Large_file_memory)
        dropdowns_with_labels_for_fig_filter_tab2 = fds.dropdown_figure_filter(df1_filter, 'graph-df1', 'tab-2', dark_dropdown_style, uniform_style)
        
        return html.Div([
    
            html.Div([
                
                fds.figure_position_dash('graph-output-tab-2', dropdowns_with_labels_for_fig_tab2, dropdowns_with_labels_for_fig_filter_tab2)
                
            ], style={'padding': '20px'})
                            
        ], style={'padding': '20px'})



# =============================================================================
# Callback for df1 in tab-2
# =============================================================================

# Callback to store df1 in dcc.Store
@app.callback(
    Output('stored-df1', 'data'),
    Input('tabs', 'value'),
    prevent_initial_call=True
)
def update_stored_df1(tab):
    if tab == 'tab-2':
        # Reload df1 when the second tab is selected
        
        List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters", "title", "isOriginalTitle"]
        List_filter = [None, None, None, None, None, None, None, None, None, None, None, None, True]
        
        df1 = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        exclude_col = ["tconst", "isAdult", "nconst", "isOriginalTitle"]
        df1 = df1.drop(columns=exclude_col)
        
        return df1.to_dict('records')


# =============================================================================
# Callback for graph in tab-2
# =============================================================================

tab = 'tab-2'
# Create a list of Input objects for each dropdown
List_col_fig = ["startYear", "runtimeMinutes", "genres", "directors", "writers", "averageRating", "numVotes", "category"]
dropdown_inputs_fig = [Input(f'{col}-fig-dropdown-'+tab, 'value') for col in List_col_fig]

@app.callback(
    Output('y-dropdown-tab-2', 'options'),
    Input('x-dropdown-tab-2', 'value'),
    Input('tabs', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df1', 'data')  # Use the correct state data for each tab
)
def update_y_dropdown_tab1(selected_x, selected_tab, stored_df1):
    if selected_tab == 'tab-2':  # Only execute if in the correct tab
        exclude_cols = ["title", "characters"]
        return update_y_dropdown_utility(selected_x, stored_df1, exclude_cols)
    return []  # Return empty if not in the right tab

@app.callback(
    Output('Func-dropdown-tab-2', 'options'),
    Input('y-dropdown-tab-2', 'value'),
    Input('tabs', 'value'),  # Include tab value to conditionally trigger callback
    State('stored-df1', 'data')
)
def update_func_dropdown_tab1(selected_y, selected_tab, stored_df1):
    df_col_numeric = ["startYear", "runtimeMinutes", "averageRating", "numVotes"]
    if selected_tab == 'tab-2':
        return update_func_dropdown_utility(selected_y, df_col_numeric)
    return []

@app.callback(
    Output('graph-output-tab-2', 'figure'),
    [Input('x-dropdown-tab-2', 'value'),
     Input('y-dropdown-tab-2', 'value'),
     Input('Func-dropdown-tab-2', 'value'),
     Input('Graph-dropdown-tab-2', 'value'),
     Input('tabs', 'value')] + dropdown_inputs_fig,  # Include tab value to conditionally trigger callback
    State('stored-df1', 'data')
)
def update_graph_tab1(*args):
    x_column, y_column, func_column, graph_type, selected_tab = args[0], args[1], args[2], args[3], args[4]
    selected_values = {col: args[i+5] for i, col in enumerate(List_col_fig)}
    stored_df1 = args[-1]
    
    if selected_tab == 'tab-2':  # Only execute if in the correct tab
        return update_graph_utility(x_column, y_column, func_column, graph_type, selected_values, stored_df1, Large_file_memory)
    return go.Figure()  # Return a blank figure if not in the right tab


In tab2_content and update_stored_df1 I open all the dataframe with the function open_dataframe
in order to do the graph, but I only want to open the col which are selected in the input and dropdown
which mean that when I go to tab-2, I do not open anything, and when I select an input or dropdown on the graph i open put the selected input dropdown in the List_col
