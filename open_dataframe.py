#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 16:06:54 2024

@author: quentin
"""


"""#=============================================================================
   #=============================================================================
   #=============================================================================

    Dictionnary of functions to open/merge the dataframes

#=============================================================================
   #=============================================================================
   #============================================================================="""

import time
import pandas as pd
import dask.dataframe as dd
import re

# Initialize a list to store execution times
performance_logs = []

def log_performance(stage, start_time):
    """Log the performance metric."""
    end_time = time.time()
    duration = end_time - start_time
    performance_logs.append((stage, duration))
    print(f"{stage} took {duration:.2f} seconds")


# # After data processing is complete, you can plot the performance logs
# def plot_performance_logs():
#     # Create a DataFrame from performance logs
#     logs_df = pd.DataFrame(performance_logs, columns=["Stage", "Duration"])

#     figname="Performance Logs of Data Processing"
#     fig, ax = plt.subplots(figsize=(22,12))
#     ax.set_title(figname)
    
#     ax.set_xlabel("Processing Stages", fontsize=35)
#     ax.set_ylabel("Processing time (seconds)", fontsize=35)
#     ax.set_yscale('log')
#     plt.xticks(rotation=45, ha='right')
    
#     p = ax.bar(logs_df['Stage'], logs_df['Duration'], color = 'olivedrab') # , color=mcolors.CSS4_COLORS[colors[i]]
        
#     ax.tick_params(axis='both', labelsize=20)
        
#     plt.tight_layout()
    
#     plt.show()


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def file_columns_dtype():
        
    # Define the mapping of files to their columns and their types
    file_columns_mapping = {
        'title.akas.tsv': {
            "columns": ["titleId", "ordering", "title", "region", "language", "types", "attributes", "isOriginalTitle"],
            "types": {
                "titleId": str,
                "ordering": int,
                "title": str,
                "region": str,
                "language": str,
                "types": str,
                "attributes": str,
                "isOriginalTitle": bool
            },
            "rename": {"titleId": "tconst"}  # Define a renaming rule for this file
        },
        'title.basics.tsv': {
            "columns": ["tconst", "titleType", "primaryTitle", "originalTitle", "startYear", "endYear", "runtimeMinutes", "genres", "isAdult"],
            "types": {
                "tconst": str,
                "titleType": str,
                "primaryTitle": str,
                "originalTitle": str,
                "startYear": float,
                "endYear": float,
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
                "averageRating": "float64",
                "numVotes": "float64"
            }
        },
        'title.principals.tsv': {
            "columns": ["tconst", "ordering", "nconst", "category", "job", "characters"],
            "types": {
                "tconst": str,
                "ordering": int,
                "nconst": str,
                "category": str,
                "job": str,
                "characters": str
            }
        },
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
    return file_columns_mapping


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def open_dataframe(requested_columns, requested_filters, Project_path, Large_file_memory, Get_file_sys_mem):

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
    
    print("      ----- open_dataframe -----")
    print(Project_path)
    start_time = time.time()  
        
    # Define the mapping of files to their columns and their types
    file_columns_mapping_dtype = file_columns_dtype()
    file_columns_mapping = {k: v for k, v in file_columns_mapping_dtype.items() if k != 'name.basics.tsv'}
    
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

            # Handle renaming if it's the 'title.akas.tsv' file
            if file == 'title.akas.tsv' and "titleId" in common_columns:
                common_columns.discard("titleId")  # Remove 'titleId'
                common_columns.add("tconst")  # Add 'tconst' instead

            # Track the columns that should be used from this file, always including 'tconst' if present
            if "tconst" in columns or (file == 'title.akas.tsv' and "titleId" in columns):
                common_columns.add("tconst")

            columns_in_files[file] = {
                "columns": common_columns,
                "types": {("tconst" if col == "titleId" else col): types[col] for col in common_columns if col in types},
                "filters": {("tconst" if col == "titleId" else col): column_filter_mapping[col] for col in common_columns if col in column_filter_mapping},
                "rename": info.get("rename", {})
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
        # Ensure 'titleId' is used instead of 'tconst' in the akas file
        if 'tconst' in usecols and file == 'title.akas.tsv':
            usecols.remove('tconst')
            usecols.append('titleId')

        # Create a dictionary to define the dtypes for the DataFrame
        dtype_mapping = {col: info["types"][col] for col in usecols if col in info["types"]}       
                
        # Read the file into a DataFrame
        filepath = f"{Project_path}/{file}"
        # Log the time taken for each file reading
        file_start_time = time.time()
        df = read_and_rename(
            filepath,
            usecols,
            dtype_mapping,
            rename_map=info.get("rename"),
            large_file=Large_file_memory
        )
       # Convert columns to the specified types
        for col, expected_type in info["types"].items():
            print(col, expected_type)
            if expected_type in [float, "float64"]:
                if Large_file_memory:
                    df[col] = dd.to_numeric(df[col], errors='coerce')
                    # Handle NA values
                    df[col] = df[col].fillna(-1)  # Fill with -1 or another value as necessary  
                else:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    # Handle NA values
                    df[col] = df[col].fillna(-1)  # Fill with -1 or another value as necessary     
                   
            elif expected_type == str:
                df[col] = df[col].fillna('')  # Fill NaN with empty string for string columns

        # desired_number_of_partitions = 4
        # df=df.repartition(npartitions=desired_number_of_partitions)
        
        # Get the infos on the DataFrame
        dis.infos_on_data(df) if Get_file_sys_mem==True else None
                
        # # Log the time taken to apply filters
        # df = apply_filter(df, info["filters"])
        log_performance(f"Read {file}", file_start_time)
        print()
        
        # Add the DataFrame to the list
        dataframes.append(df)
            
    print("Time taken to load all dataframe: {:.2f} seconds".format(time.time() - start_time))        
    print()

    # Log the time taken to merge DataFrames
    merge_start_time = time.time()    
    # Merge Dask DataFrames on 'tconst' to create a single unified DataFrame
    if len(dataframes) > 1:
        i = 0
        if Large_file_memory:
            merged_df = dataframes[i].compute()
        else:
            merged_df = dataframes[i]    
        print()
        print("Time taken to compute dataframe "+str(i)+": {:.2f} seconds".format(time.time() - start_time))
        print()
        for df in dataframes[1:]:
            i+=1

            if Large_file_memory:        
                df = df.compute()
            
            if "category" in df.columns:
                # Group by 'tconst' and 'nconst' and join the 'category' values
                df = df.groupby(['tconst', 'nconst'], as_index=False).agg({
                    'category': ', '.join,  # Combine categories
                    'characters': 'first'   # Keep the first non-empty value from characters (if any)
                })
            
            if Large_file_memory:
                merged_df = dd.merge(merged_df, df, on='tconst', how='inner')
            else:
                merged_df = pd.merge(merged_df, df, on='tconst', how='inner')
                
            print("Time taken to merge dataframe "+str(i)+": {:.2f} seconds".format(time.time() - start_time))
            print()
        # merged_df = dd.from_pandas(merged_df, npartitions=2)
        
    else:
        merged_df = dataframes[0]
    log_performance("Merging DataFrames", merge_start_time)
    
    # Print the final merged DataFrame (head only, to avoid loading too much data)
    print("\nFinal Merged DataFrame:")
    print(merged_df.head(100))
    print(merged_df)
    print()
    print("Time taken to merge all dataframe: {:.2f} seconds".format(time.time() - start_time))
    print()
    print("      --- end open_dataframe ---")
    print()
    log_performance("Complete open_data", start_time)
    
    return merged_df


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def read_and_rename(filepath, usecols=None, dtype_mapping=None, rename_map=None, large_file=True):
    
    """
    Goal: 
    - Read and rename the DataFrame.
    
    Parameters:
    - filepath: Path of the tsv file.
    - usecols: List of columns present in the DataFrame.
    - dtype_mapping: Mapping for the dtype of the columns in the dataframe.
    - rename_map: List of columns to rename.
    - large_file: Estimate if the file is too large to be open with panda and use dask instead.
    
    Returns:
    - df: DataFrame
    """    
    
    if large_file:
        df = dd.read_csv(
            filepath,
            sep='\t',
            usecols=usecols,
            encoding='utf-8',
            na_values='\\N',
            on_bad_lines='skip',
            quotechar='"',
            dtype=dtype_mapping
        )
    else:
        df = pd.read_csv(
            filepath,
            sep='\t',
            usecols=usecols,
            encoding='utf-8',
            on_bad_lines='skip',
            quotechar='"'
        )

    if rename_map:
        df = df.rename(columns=rename_map)

    return df


"""#=============================================================================
   #=============================================================================
   #============================================================================="""


def apply_filter(df, filters):
    
    """
    Goal: 
    - Apply the given filters to the DataFrame.
    
    Parameters:
    - df: DataFrame to filter
    - filters: Dictionary where keys are columns and values are filter conditions
    
    Returns:
    - df: Filtered DataFrame
    """    
    
    print("Apply filter.")
    if not filters:
        return df
    else:
        print(filters)
        for col, filter_value in filters.items():
            print(col, filter_value)
            if filter_value is not None and filter_value != 'All':  
                if isinstance(filter_value, bool):
                    # Handle boolean filters directly
                    df = df[df[col] == filter_value]
                elif ">=" in str(filter_value):
                    # Handle greater than or equal filters (e.g., ">=7.0")
                    threshold = float(filter_value.split(">=")[1])
                    df = df[df[col] >= threshold]
                elif "<=" in str(filter_value):
                    # Handle less than or equal filters (e.g., "<=5.0")
                    threshold = float(filter_value.split("<=")[1])
                    df = df[df[col] <= threshold]
                elif "=" in str(filter_value):
                    # Handle equality filters (e.g., "=nm0005690")
                    value = filter_value.split("=")[1]
                    df = df[df[col] == value]
                elif isinstance(filter_value, str) and filter_value.endswith('*'):
                    # Remove the asterisk and apply an exact match filter
                    exact_value = filter_value[:-1]
                    df = df[df[col] == exact_value]
                else:
                    if 'All' in filter_value:
                        return df
                    else:
                        # Check if 'value' is a list and apply the filter accordingly
                        if isinstance(filter_value, list):
                            # Use regex pattern to match any of the values in the list
                            pattern = '|'.join(map(re.escape, filter_value))  # Escape special characters to avoid regex issues
                            df = df[df[col].str.contains(pattern, na=False)]
                        else:
                            # Single value case, handle as before
                            df = df[df[col].str.contains(str(filter_value), na=False)]
                print(df[col])
    print()
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
                else:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    # Handle NA values
                    df[col] = df[col].fillna(-1)  # Fill with -1 or another value as necessary   
            
            elif expected_type == str:
                df[col] = df[col].fillna('')  # Fill NaN with empty string for string columns


        # df=df.repartition(npartitions=desired_number_of_partitions)
        
        # Get the infos on the DataFrame
        dis.infos_on_data(df) if Get_file_sys_mem==True else None

        # Apply the filter to the DataFrame
        # df = apply_filter(df, info["filters"])
        df = df[df['birthYear'] != -1]
        
        log_performance(f"Reading {file}", file_start_time)    
        
    if Large_file_memory:
        df = df.compute()
            
    # Print the final merged DataFrame (head only, to avoid loading too much data)
    # print("\nFinal Merged DataFrame:")
    # print(df.head(100))
    # print(merged_df.compute())

    return df
