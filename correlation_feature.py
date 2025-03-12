#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 16:48:50 2025

@author: quentin
"""


import numpy as np

import pandas as pd

from sklearn.compose import make_column_selector, make_column_transformer, ColumnTransformer

from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2, SelectFromModel, RFE, RFECV

from scipy.stats import chi2_contingency, f_oneway, zscore



def anova_target(df, tar):

    numerical_features = make_column_selector(dtype_include=np.number)(df)
    categorical_features = make_column_selector(dtype_exclude=np.number)(df)


    # Initialize results list
    anova_results = {}
    
    # Loop through each categorical feature
    for column in categorical_features:
        groups = [df[df[column] == category][tar] for category in df[column].unique()]
        
        # Perform ANOVA
        f_stat, p_value = f_oneway(*groups)
        
        # Store results
        anova_results[column] = {'f_stat': f_stat, 'p_value': p_value}
    
    # Convert results to a DataFrame for easier analysis
    anova_df = pd.DataFrame(anova_results).T
    
    # Sort by p-value
    top_results = anova_df.sort_values(by='p_value')
    
    # Get the top 10 most significant features
    # for i in top_results:
    #     print(top_results[])
    top_50_features = top_results.head(50)
    
    # Display the top 5 features
    print(top_50_features)
    
    
    
    # Initialize list for features to drop
    drop_categorical_features = []
    
    # Calculate the maximum F-statistic
    max_f_stat = top_results['f_stat'].max()
    
    print("max_f_stat=",max_f_stat)
    
    # Loop through each feature's results
    for column, metrics in top_results.iterrows():
        if (metrics['p_value'] > 0.05 or metrics['f_stat'] < max_f_stat / 10 or 
            pd.isna(metrics['f_stat']) or pd.isna(metrics['p_value'])):
            print("metrics['f_stat']=",metrics['f_stat'], "limit max=", max_f_stat / 10)
            drop_categorical_features.append(column)
    
    # Output features considered for dropping
    print("Features to consider dropping:", drop_categorical_features)
    
    remaining_categorical_features = [feature for feature in top_results.index if feature not in drop_categorical_features]
    
    # Output the remaining features
    print("Remaining features after dropping:", remaining_categorical_features)