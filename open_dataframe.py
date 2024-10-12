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
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl

"""#=============================================================================
   #=============================================================================
   #============================================================================="""


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
    


