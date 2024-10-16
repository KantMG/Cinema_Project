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

def dask_interface(Project_path, Large_file_memory, Get_file_sys_mem):
    

    # Start the timer
    start_time = time.time()    
    
    look_by_name = True
    if look_by_name :

        List_col = ["nconst", "primaryName", "birthYear", "deathYear"]
        
        List_filter = [None, "William K.L. Dickson*", None, None]

        name_info = od.open_data_name(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
        
        if name_info['nconst'].count() > 1:
            print("The DataFrame has more than one row.")
            return None, None
        else:
            # Code to execute if the DataFrame has zero or one row
            print("The DataFrame has one or zero rows.")
            Name_to_look_for = str(name_info['nconst'].iloc[0])
            print(Name_to_look_for)
            print()
        

    List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters", "title", "isOriginalTitle"]
    
    List_filter = [None, None, None, None, None, None, None, None, Name_to_look_for, None, None, None, True]
    
    df = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)
    exclude_col = ["tconst", "isAdult", "nconst", "isOriginalTitle"]
    df = df.drop(columns=exclude_col)
    
    od.log_performance("Full research", start_time)
    od.plot_performance_logs()



    # Initialize the Dash app with the dark theme (background, table, dropdown, etc)
    app, dark_dropdown_style, uniform_style = wis.web_interface_style()
    
    # Create the table with the appropriate dropdowns for each column
    dropdowns_with_labels, data_table = tds.dropdown_table(df, dark_dropdown_style, uniform_style)

    # Create the figure with the appropriate dropdowns for each axis
    dropdowns_with_labels_for_fig = fds.dropdown_figure(app, df, dark_dropdown_style, uniform_style, Large_file_memory)



    @app.callback(
        Output('y-dropdown', 'options'),
        Input('x-dropdown', 'value'),
        Input('tabs', 'value')  # Include tab value to conditionally trigger callback
    )
    def update_y_dropdown(selected_x, selected_tab):
        if selected_tab == 'tab-2':  # Only execute if in the Data Visualization tab
            return [{'label': 'None', 'value': 'None'}] + [{'label': col, 'value': col} for col in df.columns if col != selected_x]
        return []  # Return empty if not in the right tab

    # Define the callback to update the Filter input based on the selected value in the y dropdown
    @app.callback(
        Output('Filter-dropdown-container', 'children'),  # Output for the Filter container
        Input('y-dropdown', 'value')  # Input from y dropdown
    )
    def update_filter_input(y_value):
        print(f"Selected y_value: {y_value}")  # Debugging print
    
        if y_value is None or y_value == 'None':
            return html.Div([
                html.Label('Select Filter on y'),  # Label for the input
                html.Div(" Select an y column.", style={"color": "red"})
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and input vertically
        
        # if y_value not in list_col_num:  # If a valid column is selected
        dtype = df[y_value].dtype
        if dtype != "float64":
            # unique_values = sorted(df[y_value].dropna().unique())  # Sort unique values and drop NaNs
            unique_values = sorted(set(val.strip() for sublist in df[y_value].dropna().str.split(',') for val in sublist))
            print("Filter 1 - Unique Values:", unique_values)  # Debugging print
            return html.Div([
                html.Label(f'Select Filter on y'),  # Label for the dropdown
                dcc.Dropdown(
                    id='Filter-dropdown',  # Ensure this ID is correct
                    options=[{'label': val, 'value': val} for val in unique_values],  # Populate with unique values
                    multi=True,  # Enable multiple selection
                    placeholder='Select values',  # Placeholder text
                    style={**dark_dropdown_style, **uniform_style}  # Apply dark theme style
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and dropdown vertically
        else:  # Default behavior for 'None' or 'All'
            print("Filter 2")  # Debugging print
            return html.Div([
                html.Label(f'Select Filter on y'),  # Label for the input
                dcc.Input(
                    id='Filter-dropdown',  # Ensure this ID is correct
                    type='text',
                    placeholder='Condition (e.g., 100-200)',
                    debounce=True,  # Apply changes when pressing Enter or losing focus
                    style={**dark_dropdown_style, **uniform_style}  # Apply dark theme style
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})  # Align label and input vertically


    # Callback to update the figure based on the dropdown selections
    @app.callback(
        Output('graph-output', 'figure'),
        [Input('x-dropdown', 'value'),
         Input('y-dropdown', 'value'),
         Input('Func-dropdown', 'value'),
         # Input('Filter-dropdown', 'value'),
         Input('Graph-dropdown', 'value')],
        Input('tabs', 'value')  # Include tab value to conditionally trigger callback
    )
    def update_graph(x_column, y_column, func_column, graph_type, selected_tab):
        if selected_tab == 'tab-2':  # Only execute if in the Data Visualization tab
            print()
            print("Start with all data")
            filtered_data = df.copy()  # Make sure to work with a copy of the original DataFrame

            # Get the `Filter-dropdown` value only if it exists
            filter_value = None
            triggered = [p['prop_id'] for p in callback_context.triggered]
        
            # Check if the `Filter-dropdown` exists before trying to use its value
            if 'Filter-dropdown.value' in triggered or any('Filter-dropdown-container' in trigger for trigger in triggered):
                filter_value = callback_context.inputs.get('Filter-dropdown.value', None)
            
            print(filter_value)
            # Only apply filtering if y_column is valid
            if y_column is not None and y_column != 'None' and filter_value:
                filtered_data, error_msg = filter_data_by_value(filtered_data, x_column, y_column, filter_value)        
 
            # Create the figure based on filtered data
            fig = fds.create_figure(filtered_data, x_column, y_column, func_column, filter_value, graph_type, Large_file_memory)
            
            return fig
        else:
            return go.Figure()  # Return a blank figure if not in the right tab




    # Create a list of Input objects for each dropdown
    dropdown_inputs = [Input(f'{col}-dropdown', 'value') for col in df.columns]   
    @app.callback(
        Output('data-table', 'data'),
        dropdown_inputs
    )
    
    def update_output(*selected_values):
        # Start with the original DataFrame
        filtered_df = df.copy()
        # Filter the DataFrame based on selections
        for i, selected_value in enumerate(selected_values):
            col_name = df.columns[i]
            filtered_df = filter_data_by_value_array(filtered_df, col_name, selected_value)
        # Return the updated options for all dropdowns and the filtered data for the table
        return filtered_df.to_dict('records')



    # =============================================================================
    # Main
    # =============================================================================
    # Define the layout with Tabs
    app.layout = html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='IMDB Data Table', value='tab-1'),
            dcc.Tab(label='Data Visualization', value='tab-2'),
            dcc.Tab(label='Summary Statistics', value='tab-3')
        ]),
        html.Div(id='tabs-content')  # This Div will hold the content of each tab
    ])


    # Callback to update the content based on the selected tab
    @app.callback(Output('tabs-content', 'children'),
                  [Input('tabs', 'value')])
    def render_content(tab):
        if tab == 'tab-1':
            # Tab 1: IMDB Data Table
            return layout_for_tab1(dropdowns_with_labels, data_table)
        elif tab == 'tab-2':
            # Tab 2: Data Visualization
            return layout_for_tab2(dropdowns_with_labels_for_fig)
        elif tab == 'tab-3':
            # Tab 3: Summary Statistics
            return layout_for_tab3(df)
    # =============================================================================
    # End Main
    # =============================================================================

    
    app.run_server(debug=True, port=8051)
    
    # Specify the URL you want to open
    url = "http://127.0.0.1:8051/"
    
    # Open the URL in the default web browser
    # webbrowser.open(url)
    
    
    return 0, df


def layout_for_tab1(dropdowns_with_labels, data_table):
    return html.Div([
        html.Div([
            html.P(f'This interface is dedicated to the research on specific artist.'),
        ]),
        html.Div(style={'display': 'flex', 'margin-top': '10px', 'flex-wrap': 'wrap'}, children=[
            html.Div(dropdowns_with_labels, style={'display': 'flex', 'justify-content': 'flex-start', 'gap': '5px'})
        ]),
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div(data_table, style={'width': '100%'})  # Adjusted to take full width
        ])
    ], style={'padding': '20px'})


def layout_for_tab2(dropdowns_with_labels_for_fig):
    return html.Div([
        html.H1("IMDB DataFrame Interface", style={"color": "#FFD700"}, className="text-light"),
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div(dropdowns_with_labels_for_fig, style={'display': 'flex', 'margin-left': '50px', 'justify-content': 'flex-start', 'gap': '5px'})
        ]),
        html.Div(style={'display': 'flex', 'margin-top': '10px'}, children=[
            html.Div([dcc.Graph(id='graph-output', style={'width': '100%', 'height': '600px'})], style={'margin-left': '20px', 'width': '50%'})
        ])
    ], style={'padding': '20px'})


def layout_for_tab3(df):
    return html.Div([
        html.H1("IMDB DataFrame Interface", style={"color": "#FFD700"}, className="text-light"),
        html.Div([
                html.H3('Summary Statistics'),
                html.Div([
                    html.P(f'Total Rows: {len(df)}'),
                    html.P(f'Number of Unique Genres: {df["genres"].nunique()}'),
                    # Add more statistics as needed
                ])
            ])
    ], style={'padding': '20px'})





def filter_data_by_value(df, x_column, y_column, filter_value):

    """
    Filters the DataFrame based on the provided x and y columns, and the filter value.
    
    Parameters:
    - df: DataFrame to filter.
    - x_column: Selected x column.
    - y_column: Selected y column.
    - filter_value: The value or range to filter on.
    
    Returns:
    - df: Filtered DataFrame.
    - error_msg: Any error message that occurred during filtering (None if no error).
    """    
    
    error_msg = None  # Initialize error message

    if x_column is not None and y_column is not None:
        # if y_column in list_col_num:
        dtype = df[y_column].dtype
        if dtype != "float64":
            print(f"{y_column} is numeric data")
            
            # Ensure the y_column is numeric and drop NaNs
            df[y_column] = pd.to_numeric(df[y_column], errors='coerce')
            df = df.dropna(subset=[y_column])
            
            # Handle numeric filtering
            if filter_value:
                try:
                    if isinstance(filter_value, str):
                        lower, upper = map(int, filter_value.split('-'))
                        if lower > upper:
                            error_msg = f"Invalid range: {lower} is greater than {upper}."
                            print(error_msg)
                        else:
                            df = df[(df[y_column] >= lower) & (df[y_column] <= upper)]
                except ValueError:
                    error_msg = f"Invalid filter format: {filter_value}. Please enter in 'lower-upper' format."
                    print(f"Filter value error: {error_msg}")
        else:
            print(f"{y_column} is string data")

            # Handle string filtering for non-numeric columns
            df[y_column] = df[y_column].astype(str)  # Ensure string type
            if filter_value and isinstance(filter_value, str):
                # Check if the filter value exists in the data
                unique_values = df[y_column].unique()
                if filter_value in unique_values:
                    df = df[df[y_column].str.contains(filter_value, case=False, na=False)]
                else:
                    error_msg = f"Filter value '{filter_value}' not found in column '{y_column}'."
                    print(error_msg)
                        
    
    return df, error_msg



def filter_data_by_value_array(df, y_column, filter_value):

    """
    Filters the DataFrame based on the provided x and y columns, and the filter value.
    
    Parameters:
    - df: DataFrame to filter.
    - y_column: Selected y column.
    - filter_value: The value or range to filter on.
    
    Returns:
    - df: Filtered DataFrame.
    - error_msg: Any error message that occurred during filtering (None if no error).
    """    
    
    error_msg = None  # Initialize error message
    print(y_column)
    if y_column is not None:
        # if y_column in list_col_num:
        dtype = df[y_column].dtype
        if dtype == "float64":
            print(f"{y_column} is numeric data")
            
            # Ensure the y_column is numeric and drop NaNs
            df[y_column] = pd.to_numeric(df[y_column], errors='coerce')
            df = df.dropna(subset=[y_column])
            
            # Handle numeric filtering
            if filter_value:
                try:
                    if isinstance(filter_value, str):
                        lower, upper = map(int, filter_value.split('-'))
                        if lower > upper:
                            error_msg = f"Invalid range: {lower} is greater than {upper}."
                            print(error_msg)
                        else:
                            df = df[(df[y_column] >= lower) & (df[y_column] <= upper)]
                except ValueError:
                    error_msg = f"Invalid filter format: {filter_value}. Please enter in 'lower-upper' format."
                    print(f"Filter value error: {error_msg}")
        else:
            
            print(f"{y_column} is string data")

            # Handle string filtering for non-numeric columns
            df[y_column] = df[y_column].astype(str)  # Ensure string type
            if filter_value and isinstance(filter_value, str):
                # Check if the filter value exists in the data
                unique_values = df[y_column].unique()
                if filter_value in unique_values:
                    df = df[df[y_column].str.contains(filter_value, case=False, na=False)]
                elif filter_value == 'All':
                    df = df
                else:
                    error_msg = f"Filter value '{filter_value}' not found in column '{y_column}'."
                    print(error_msg)
                        
    return df



"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def open_data_name(requested_columns, requested_filters, Project_path, Large_file_memory, Get_file_sys_mem):
    """
    Goal: 
    - Read and rename the DataFrame.
    
    Parameters:
    - requested_columns: List of columns to extract from the DataFrame located in several file.
    - requested_filters: List of filter to apply on each column.
    - Project_path: Path of the tsv file.
    - Large_file_memory: Estimate if the file is too large to be open with panda and use dask instead.
    - Get_file_sys_mem: Estimate the memory consuming by the files.
    
    Returns:
    - df: DataFrame
    """
    
    
    # Define the mapping of files to their columns and their types
    file_columns_mapping = {
        'name.basics.tsv': {
            "columns": ["nconst", "primaryName", "birthYear", "deathYear", "primaryProfession", "knownForTitles"],
            "types": {
                "nconst": str,
                "primaryName": str,
                "birthYear": float,
                "deathYear": float,
                "primaryProfession": str,
                "knownForTitles": str
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
    for file, info in columns_in_files.items():
        # Define the columns to read from the file
        usecols = list(info["columns"])

        # Create a dictionary to define the dtypes for the DataFrame
        dtype_mapping = {col: info["types"][col] for col in usecols if col in info["types"]}       
        
        file_start_time = time.time()    
        # Read the file into a DataFrame
        filepath = f"{Project_path}/{file}"
        # Log the time taken for each file reading
        df = read_and_rename(
            filepath,
            usecols,
            dtype_mapping,
            rename_map=None,
            large_file=Large_file_memory
        )
             
       # Convert columns to the specified types
        for col, expected_type in info["types"].items():
            if expected_type == float:
                if Large_file_memory:
                    df[col] = dd.to_numeric(df[col], errors='coerce')
                    # Handle NA values
                    df[col] = df[col].fillna(-1)  # Fill with -1 or another value as necessary                    
            elif expected_type == str:
                df[col] = df[col].fillna('')  # Fill NaN with empty string for string columns


        # df=df.repartition(npartitions=desired_number_of_partitions)
        
        # Get the infos on the DataFrame
        dis.infos_on_data(df) if Get_file_sys_mem==True else None

        # Apply the filter to the DataFrame
        df = apply_filter(df, usecols, info["filters"])
        df = df[df['birthYear'] != -1]
        
        log_performance(f"Reading {file}", file_start_time)    
    
    df = df.compute()
            
    # Print the final merged DataFrame (head only, to avoid loading too much data)
    print("\nFinal Merged DataFrame:")
    print(df.head(100))
    # print(merged_df.compute())

    return df




I now want to create an input to enter "primaryName" which can "William K.L. Dickson*" or anything else.
Depending of this input it must returns
        if name_info['nconst'].count() > 1:
            print("The DataFrame has more than one row.")
            return None, None
        else:
            # Code to execute if the DataFrame has zero or one row
            print("The DataFrame has one or zero rows.")
            Name_to_look_for = str(name_info['nconst'].iloc[0])
            print(Name_to_look_for)
            print()
