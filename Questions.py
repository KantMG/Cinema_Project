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

List_col = ["startYear", "runtimeMinutes", "genres", "isAdult", "directors", "writers", "averageRating", "numVotes", "nconst", "category", "characters"]

List_filter = [None, None, None, None, "nm0005690", None, ">=5.6", None, None, None, None]



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
                "runtimeMinutes": float,
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
                "numVotes": int
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
        # dtype_mapping = {col: 'float' if info["types"][col] == int else info["types"][col] for col in usecols if col in info["types"]}
        
        
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
            if expected_type == int:
                if Large_file_memory:
                    na_count = df[col].isna().sum().compute()  # Evaluate the count
                    print(f"NA count in '{col}': {na_count}")
    
                    # Handle NA values
                    df[col] = df[col].fillna(-1)  # Fill with -1 or another value as necessary
    
                df[col] = df[col].astype('Int64')  # Use 'Int64' for nullable integers
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
        print(df.head())
        print()
            
    
    print("Time taken to load all dataframe: {:.2f} seconds".format(time.time() - start_time))        
    print("")
    
    # Merge Dask DataFrames on 'tconst' to create a single unified DataFrame
    if len(dataframes) > 1:
        merged_df = dataframes[0]
        print(merged_df.dtypes)
        for df in dataframes[1:]:
            print(df.dtypes)
            merged_df = dd.merge(merged_df, df, on='tconst', how='inner')
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
        
        print(filter_value)
        
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


Files to open: ['title.basics.tsv', 'title.crew.tsv', 'title.ratings.tsv', 'title.principals.tsv']
Common columns across all selected files: {'tconst'}
Columns, filters, and types in each selected file:
title.basics.tsv:
  Columns: {'tconst', 'runtimeMinutes', 'isAdult', 'genres', 'startYear'}
  Filters: {'runtimeMinutes': None, 'isAdult': None, 'genres': None, 'startYear': None}
  Types: {'tconst': <class 'str'>, 'runtimeMinutes': <class 'float'>, 'isAdult': <class 'float'>, 'genres': <class 'str'>, 'startYear': <class 'float'>}
title.crew.tsv:
  Columns: {'writers', 'directors', 'tconst'}
  Filters: {'writers': None, 'directors': 'nm0005690'}
  Types: {'writers': <class 'str'>, 'directors': <class 'str'>, 'tconst': <class 'str'>}
title.ratings.tsv:
  Columns: {'numVotes', 'tconst', 'averageRating'}
  Filters: {'numVotes': None, 'averageRating': '>=5.6'}
  Types: {'numVotes': <class 'int'>, 'tconst': <class 'str'>, 'averageRating': <class 'float'>}
title.principals.tsv:
  Columns: {'category', 'nconst', 'tconst', 'characters'}
  Filters: {'category': None, 'nconst': None, 'characters': None}
  Types: {'category': <class 'str'>, 'nconst': <class 'str'>, 'tconst': <class 'str'>, 'characters': <class 'str'>}
Data types after loading:
tconst             object
isAdult           float64
startYear         float64
runtimeMinutes    float64
genres             object
dtype: object
None
None
None
None
Data types after loading:
tconst       object
directors    object
writers      object
dtype: object
None
nm0005690
Data types after loading:
tconst            object
averageRating    float64
numVotes           int64
dtype: object
NA count in 'numVotes': 0
None
>=5.6
Data types after loading:
tconst        object
nconst        object
category      object
characters    object
dtype: object
None
None
None

DataFrame 1 from title.basics.tsv:
      tconst  isAdult  startYear  runtimeMinutes                    genres
0  tt0000001      0.0     1894.0             1.0         Documentary,Short
1  tt0000002      0.0     1892.0             5.0           Animation,Short
2  tt0000003      0.0     1892.0             5.0  Animation,Comedy,Romance
3  tt0000004      0.0     1892.0            12.0           Animation,Short
4  tt0000005      0.0     1893.0             1.0              Comedy,Short


DataFrame 2 from title.crew.tsv:
      tconst            directors writers
0  tt0000001            nm0005690        
4  tt0000005            nm0005690        
5  tt0000006            nm0005690        
6  tt0000007  nm0005690,nm0374658        
7  tt0000008            nm0005690        


DataFrame 3 from title.ratings.tsv:
      tconst  averageRating  numVotes
0  tt0000001            5.7      2081
1  tt0000002            5.6       280
2  tt0000003            6.5      2078
4  tt0000005            6.2      2816
9  tt0000010            6.8      7671


DataFrame 4 from title.principals.tsv:
      tconst     nconst         category characters
0  tt0000001  nm1588970             self   ["Self"]
1  tt0000001  nm0005690         director           
2  tt0000001  nm0005690         producer           
3  tt0000001  nm0374658  cinematographer           
4  tt0000002  nm0721526         director           

Time taken to load all dataframe: 6.15 seconds

tconst             object
isAdult           float64
startYear         float64
runtimeMinutes    float64
genres             object
dtype: object
tconst       object
directors    object
writers      object
dtype: object
tconst            object
averageRating    float64
numVotes         float64
dtype: object
tconst        object
nconst        object
category      object
characters    object
dtype: object

Final Merged DataFrame:
Traceback (most recent call last):

  File parsers.pyx:1161 in pandas._libs.parsers.TextReader._convert_tokens

TypeError: Cannot cast array data from dtype('O') to dtype('float64') according to the rule 'safe'


During handling of the above exception, another exception occurred:

Traceback (most recent call last):

  File ~/.local/lib/python3.10/site-packages/spyder_kernels/customize/utils.py:209 in exec_encapsulate_locals
    exec_fun(compile(code_ast, filename, "exec"), globals)

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/Main.py:133
    Para, y = main()

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/Main.py:122 in main
    Para, y = adg3.movie_making_over_year(Project_path,Large_file_memory, desired_number_of_partitions, Get_file_sys_mem)

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/analysation_dataframe_goal3.py:97 in movie_making_over_year
    df = od.open_dataframe(List_col, List_filter, Project_path, Large_file_memory, Get_file_sys_mem)

  File ~/Documents/Work/Data_analytics/Programs/Python/Cinema_Project/open_dataframe.py:200 in open_dataframe
    print(merged_df.head(100))

  File ~/.local/lib/python3.10/site-packages/dask/dataframe/core.py:1557 in head
    return self._head(n=n, npartitions=npartitions, compute=compute, safe=safe)

  File ~/.local/lib/python3.10/site-packages/dask/dataframe/core.py:1591 in _head
    result = result.compute()

  File ~/.local/lib/python3.10/site-packages/dask/base.py:372 in compute
    (result,) = compute(self, traverse=False, **kwargs)

  File ~/.local/lib/python3.10/site-packages/dask/base.py:660 in compute
    results = schedule(dsk, keys, **kwargs)

  File ~/.local/lib/python3.10/site-packages/dask/dataframe/io/csv.py:142 in __call__
    df = pandas_read_text(

  File ~/.local/lib/python3.10/site-packages/dask/dataframe/io/csv.py:195 in pandas_read_text
    df = reader(bio, **kwargs)

  File ~/.local/lib/python3.10/site-packages/pandas/io/parsers/readers.py:1026 in read_csv
    return _read(filepath_or_buffer, kwds)

  File ~/.local/lib/python3.10/site-packages/pandas/io/parsers/readers.py:626 in _read
    return parser.read(nrows)

  File ~/.local/lib/python3.10/site-packages/pandas/io/parsers/readers.py:1923 in read
    ) = self._engine.read(  # type: ignore[attr-defined]

  File ~/.local/lib/python3.10/site-packages/pandas/io/parsers/c_parser_wrapper.py:234 in read
    chunks = self._reader.read_low_memory(nrows)

  File parsers.pyx:838 in pandas._libs.parsers.TextReader.read_low_memory

  File parsers.pyx:921 in pandas._libs.parsers.TextReader._read_rows

  File parsers.pyx:1066 in pandas._libs.parsers.TextReader._convert_column_data

  File parsers.pyx:1167 in pandas._libs.parsers.TextReader._convert_tokens

ValueError: could not convert string to float: 'Comedy,Drama,Horror'











DataFrame 1 from title.crew.tsv:
      tconst            directors
0  tt0000001            nm0005690
4  tt0000005            nm0005690
5  tt0000006            nm0005690
6  tt0000007  nm0005690,nm0374658
7  tt0000008            nm0005690


DataFrame 2 from title.ratings.tsv:
      tconst  averageRating
0  tt0000001            5.7
1  tt0000002            5.6
2  tt0000003            6.5
4  tt0000005            6.2
9  tt0000010            6.8

Time taken to load all dataframe: 2.73 seconds

tconst       object
directors    object
dtype: object
tconst            object
averageRating    float64
dtype: object



Final Merged DataFrame:
       tconst            directors  averageRating
0   tt0000001            nm0005690            5.7
1   tt0000005            nm0005690            6.2
2   tt0000060            nm0005690            7.2
3   tt0000135            nm0005690            6.3
4   tt0000201            nm0005690            6.1
5   tt0154152  nm0005690,nm0374658            6.5
6   tt0177707            nm0005690            6.7
7   tt0203883            nm0005690            5.7
8   tt0205065  nm0005690,nm0374658            5.6
9   tt0219560  nm0005690,nm0374658            5.8
10  tt0219824            nm0005690            5.8
11  tt0227039            nm0005690            5.8
12  tt0229217            nm0005690            5.9
13  tt0229220            nm0005690            6.3
14  tt0229300  nm0005690,nm0374658            5.6
15  tt0241282            nm0005690            6.1
16  tt0277115            nm0005690            5.6
17  tt0390024            nm0005690            5.6