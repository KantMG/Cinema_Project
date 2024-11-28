I have the function 

def explode_dataframe(df, Para):
    
    """
    Goal: 
    - Count individual elements when multiple elements are stored in a single cell
    - Explode the Dataframe where cells with muliple elements are counted multiple time.

    Parameters:
    - df: Dataframe
    - Para: List of column in the df for which the table should explode the cells with multiple elements.

    Returns:
    - Dataframe which have been explode and the new counts of each elements.
    
    Warning:
    - Can create very large array if many cells contain many elements.
    """
    
    df_temp = df.copy()
    
    # Step 1: Split the elements into lists of elements
    df_temp[Para+'_split'] = df_temp[Para].str.split(',')
    
    # Step 2: Explode the list of elements into individual rows
    df_temp = df_temp.explode(Para+'_split')
        
    # Step 3: Clean up the split elements by stripping whitespace
    df_temp[Para + '_split'] = df_temp[Para + '_split'].str.strip()    
    
    # Step 4: Replace empty cells with 'Unknown' 
    df_temp[Para + '_split'].replace({'': 'Unknown', r'\\N': 'Unknown'}, regex=True, inplace=True)

    # Step 5: Fill NaN values with 'Unknown'
    df_temp[Para + '_split'].fillna('Unknown', inplace=True)

    # Step 6: Count the occurrences of each element
    element_counts = df_temp[Para + '_split'].value_counts()    
    
    # Display the result
    print("Dataframe have been explode base on parameter "+Para)
    print("The new counts of each elements is:")
    print(element_counts)
    print()
    
    return df_temp, element_counts


which is suppose to explode the dataframe.
however it seems that for instance some element has some space , which create two split from the same element
like:
Drama
 Drama
How can I correct that
