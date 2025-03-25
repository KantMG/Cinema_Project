#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 16:48:50 2025

@author: quentin
"""


import pandas as pd
import numpy as np
import logging
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from termcolor import colored
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

def check_feature_type(df, feature, target, is_target_numeric, is_binary_target):
    """ Check if the feature type is valid based on the target type. """
    if is_binary_target or not is_target_numeric:
        if not pd.api.types.is_numeric_dtype(df[feature]):
            print(colored(f"ERROR: Feature '{feature}' must be numeric for a categorical target. Ignored for ANOVA.", "red"))
            return False
    else:
        if not pd.api.types.is_categorical_dtype(df[feature]) and not pd.api.types.is_object_dtype(df[feature]):
            print(colored(f"ERROR: Feature '{feature}' must be categorical for a numeric target. Ignored for ANOVA.", "red"))
            return False
    return True

def clean_data(df, feature, target):
    """ Remove NaN values from the dataset. """
    df_cleaned = df[[target, feature]].dropna()
    nan_count = df.shape[0] - df_cleaned.shape[0]
    print(f" Removed {nan_count} NaN values for feature {colored(feature, 'yellow')}.")
    return df_cleaned

def test_normality(df_cleaned, feature, target, is_target_numeric, is_binary_target):
    """Perform normality tests depending on the target type."""
    normality_failed = False
    p_values = []

    if is_binary_target or not is_target_numeric:
        groups = [df_cleaned[df_cleaned[target] == val][feature] for val in df_cleaned[target].unique()]
        for i, group in enumerate(groups):
            if len(group) > 3:
                stat, p_value = stats.shapiro(group)
                p_values.append((df_cleaned[target].unique()[i], p_value))
                plot_normal_distribution(df_cleaned, feature)
                if p_value < 0.05:
                    normality_failed = True
    else:
        stat, p_value = stats.shapiro(df_cleaned[target])
        p_values.append(("target", p_value))
        plot_normal_distribution(df_cleaned, target)
        if p_value < 0.05:
            normality_failed = True
    
    if normality_failed:
        for group, p_val in p_values:
            print(colored(f"WARNING: Normality test failed for {group} (p-value = {p_val:.4f}). Switching to Kruskal-Wallis test.", "magenta"))
    
    return not normality_failed

def plot_normal_distribution(df, feature):
    """Plot a histogram of the data along with the fitted normal distribution curve."""
    
    data = df[feature].dropna()
    
    # Compute mean and standard deviation
    mu, sigma = np.mean(data), np.std(data)
    
    # Create a range of values for the normal distribution
    x = np.linspace(min(data), max(data), 100)
    normal_curve = stats.norm.pdf(x, mu, sigma)

    # Plot the histogram and fitted normal curve
    plt.figure(figsize=(8, 5))
    sns.histplot(data, bins=30, kde=True, color='blue', stat='density', label="Actual data")
    plt.plot(x, normal_curve, 'r-', lw=2, label="Fitted normal distribution")
    
    plt.title(f"Comparison of '{feature}' distribution with a normal law")
    plt.xlabel(feature)
    plt.ylabel("Density")
    plt.legend()
    plt.show()

    print(f"Mean of '{feature}': {mu:.4f}")
    print(f"Standard deviation of '{feature}': {sigma:.4f}")
    print("Check if the histogram aligns well with the normal distribution curve.")


def check_outliers(df_cleaned, feature, target, is_target_numeric, is_binary_target):
    """ Detect outliers using Tukey's IQR method. """
    col = feature if is_binary_target or not is_target_numeric else target
    q1, q3 = df_cleaned[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr

    if df_cleaned[col].lt(lower_bound).any() or df_cleaned[col].gt(upper_bound).any():
        print(colored(f"ERROR: Outliers detected in '{col}'.", "red"))
        return False
    return True

def test_variance_homogeneity(df_cleaned, feature, target, is_target_numeric, is_binary_target):
    """ Check variance homogeneity using Levene’s test. """
    if is_binary_target or not is_target_numeric:
        groups = [df_cleaned[df_cleaned[target] == val][feature] for val in df_cleaned[target].unique()]
    else:
        groups = [df_cleaned[df_cleaned[feature] == cat][target] for cat in df_cleaned[feature].unique()]

    stat, p_value = stats.levene(*groups)
    if p_value < 0.05:
        print(colored(f"ERROR: Variance homogeneity is not satisfied for feature '{feature}'.", "red"))
        return False
    return True

def check_class_balance(df_cleaned, feature, target, is_target_numeric, is_binary_target):
    """ Ensure class sizes are sufficient. """
    if is_binary_target or not is_target_numeric:
        if df_cleaned[target].value_counts().min() < 5:
            print(colored(f"ERROR: Insufficient class sizes for feature '{feature}'.", "red"))
            return False
    else:
        if df_cleaned[feature].value_counts().min() < 5:
            print(colored(f"ERROR: Insufficient class sizes for target '{target}'.", "red"))
            return False
    return True

def perform_anova(df_cleaned, feature, target, is_target_numeric, is_binary_target):
    """ Run the ANOVA test if all conditions are met. """
    formula = f'{feature} ~ C({target})' if is_binary_target or not is_target_numeric else f'{target} ~ C({feature})'
    model = ols(formula, data=df_cleaned).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(colored(f"ANOVA result for feature '{feature}':\n", "green"), anova_table)


def perform_kruskal_wallis(df_cleaned, feature, target, is_target_numeric, is_binary_target):
    """Run the Kruskal-Wallis test when normality is not satisfied."""
    if is_binary_target or not is_target_numeric:
        groups = [df_cleaned[df_cleaned[target] == val][feature] for val in df_cleaned[target].unique()]
    else:
        groups = [df_cleaned[df_cleaned[feature] == cat][target] for cat in df_cleaned[feature].unique()]

    stat, p_value = stats.kruskal(*groups)
    print(colored(f"⚠️ Kruskal-Wallis test result for feature '{feature}':\nStatistic = {stat:.4f}, p-value = {p_value:.4f}", "cyan"))


def anova_target(df, target):
    """Main function to test ANOVA conditions and perform either ANOVA or Kruskal-Wallis test."""
    
    features = df.columns.difference([target])
    
    # Determine if target is numeric or categorical
    is_target_numeric = pd.api.types.is_numeric_dtype(df[target])
    target_unique_values = df[target].unique()
    is_binary_target = is_target_numeric and len(target_unique_values) <= 2 and all(isinstance(val, (int, np.integer)) for val in target_unique_values)

    print(f"Target {colored(target, 'green')} is {'binary categorical' if is_binary_target else 'numerical' if is_target_numeric else 'categorical'}. Unique values: {target_unique_values}")

    for feature in features:
        print(f"\n🔍 Checking conditions for ANOVA between {colored(target, 'green')} and {colored(feature, 'yellow')}")

        # Step 1: Validate feature type
        if not check_feature_type(df, feature, target, is_target_numeric, is_binary_target):
            continue

        # Step 2: Clean the data
        df_cleaned = clean_data(df, feature, target)

        # Step 3: Check assumptions for ANOVA
        normality_passed = test_normality(df_cleaned, feature, target, is_target_numeric, is_binary_target)
        if not normality_passed:
            # print(colored(f"⚠️ Kruskal-Wallis test result for feature '{feature}'", "cyan"))
            # perform_kruskal_wallis(df_cleaned, feature, target, is_target_numeric, is_binary_target)
            continue  # Skip ANOVA if Kruskal-Wallis was performed

        if not check_outliers(df_cleaned, feature, target, is_target_numeric, is_binary_target):
            continue
        if not test_variance_homogeneity(df_cleaned, feature, target, is_target_numeric, is_binary_target):
            continue
        if not check_class_balance(df_cleaned, feature, target, is_target_numeric, is_binary_target):
            continue

        # Step 4: Perform ANOVA
        perform_anova(df_cleaned, feature, target, is_target_numeric, is_binary_target)