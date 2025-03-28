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
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from dash import html
from termcolor import colored

def clean_data(df, feature, target):
    """Cleans data by removing rows with NaN values for the feature and target."""
    return df[[feature, target]].dropna()

def check_outliers_z_score(df, feature):
    """Detects outliers in the specified feature using the Z-score method."""
    z_scores = np.abs(stats.zscore(df[feature]))
    return np.where(z_scores > 3)

def check_outliers_iqr(df, feature):
    """Detects outliers in the specified feature using the IQR method."""
    Q1 = df[feature].quantile(0.25)
    Q3 = df[feature].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
    return outliers, lower_bound, upper_bound

def check_outliers(df, feature):
    """Detects outliers in the specified feature using the IQR method."""
    outliers, lower_bound, upper_bound = check_outliers_iqr(df, feature)
    
    if not outliers.empty:
        return (
            f"❌ Outliers detected in {feature}: "
            f"lower_bound = {lower_bound:.4e}  |  upper_bound = {upper_bound:.4e}\n{outliers}"
        )
    else:
        return f"✅ No outliers detected in {feature}."

def plot_normality(groups, feature, p_values):
    """Creates QQ plots and histograms for each group for normality visualization, returning the figure for Dash."""
    num_groups = len(groups)
    fig = make_subplots(rows=2, cols=num_groups, subplot_titles=[f'Group {i + 1}' for i in range(num_groups)]
                        +[f"p-value: {p_value:.4e}" for i, (group, p_value) in enumerate(zip(groups, p_values))])

    plot_color = 'blue'

    for i, (group, p_value) in enumerate(zip(groups, p_values)):
        # QQ Plot Data
        n = len(group)
        qq_y = np.sort(group)
        qq_x = stats.norm.ppf(np.linspace(0, 1, n, endpoint=False))
        
        print(qq_x.min(), qq_x.max())
        # Create QQ scatter plot
        scatter_fig = px.scatter(x=qq_x, y=qq_y, title=f'QQ Plot for Group {i + 1}', 
                                 labels={'x': 'Theoretical Quantiles', 'y': 'Sample Quantiles'})
        scatter_fig.add_trace(go.Scatter(x=[qq_x.min(), qq_x.max()], y=[qq_x.min(), qq_x.max()], 
                                          mode='lines', line=dict(color='red', width=2),
                                          name='y=x'))

        for trace in scatter_fig.data:
            fig.add_trace(trace, row=1, col=i + 1)

        # Create Histogram Data
        hist_fig = px.histogram(x=group, histnorm='probability density', 
                                 title=f'Histogram for Group {i + 1}', 
                                 labels={'x': feature, 'y': 'Density'})
        
        for trace in hist_fig.data:
            fig.add_trace(trace, row=2, col=i + 1)

    
    # Update layout
    fig.update_layout(title_text=f'Normality Plots for {feature}', height=600)

    # Hide legend for all traces
    # fig.for_each_trace(lambda t: t.update(showlegend=False))
    
    fig.update_layout(
        plot_bgcolor='#1e1e1e',  # Darker background for the plot area
        paper_bgcolor='#101820',  # Dark gray for the paper
        font=dict(color='white'),  # White text color
        # title = figname,
        # title_font=dict(size=20, color='white')
        )

    return fig


# def plot_normality(groups, feature, p_values):
#     """Creates QQ plots and histograms for each group for normality visualization, saving the figure as an image with a dark theme."""
    
#     # Set Seaborn's style to dark
#     sns.set_style("darkgrid", {"axes.facecolor": "#2E2E2E", "figure.facecolor": "#2E2E2E"})
    
#     num_groups = len(groups)
    
#     fig, axes = plt.subplots(nrows=2, ncols=num_groups, figsize=(14, 7))
    
#     for i, (group, p_value) in enumerate(zip(groups, p_values)):
#         # QQ Plot
#         stats.probplot(group, dist="norm", plot=axes[0][i])
#         axes[0][i].set_title(f'QQ Plot for {feature} (Group {i + 1})', color='white')
#         axes[0][i].text(0.2, 0.90, f'p-value: {p_value:.4e}', fontsize=12, 
#                         ha='center', va='center', color='white')  # Moved closer to the top

#         # Histogram with density plot
#         sns.histplot(group, kde=True, ax=axes[1][i], stat='density', color="lightblue")
#         axes[1][i].set_title(f'Histogram & Density for {feature} (Group {i + 1})', color='white')

#         # Set axis labels color
#         axes[0][i].tick_params(axis='x', colors='white')
#         axes[0][i].tick_params(axis='y', colors='white')
#         axes[1][i].tick_params(axis='x', colors='white')
#         axes[1][i].tick_params(axis='y', colors='white')

#         # Change label colors
#         axes[0][i].set_xlabel('Theoretical Quantiles', color='white')
#         axes[0][i].set_ylabel('Sample Quantiles', color='white')
#         axes[1][i].set_xlabel(feature, color='white')
#         axes[1][i].set_ylabel('Density', color='white')

#     # Adjust spacing: reduce space between top and bottom plots
#     plt.subplots_adjust(hspace=0.3)  # Adjust vertical space between rows

#     plt.tight_layout(pad=2.0)  # General tight layout adjustments
    
#     # Save the figure to a BytesIO object
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png', facecolor=fig.get_facecolor())
#     buf.seek(0)
    
#     # Encode it as base64 for Dash
#     image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
#     plt.close(fig)  # Close the figure after saving
#     return f"data:image/png;base64,{image_base64}"



def test_normality(df_cleaned, feature, target):
    """Tests for normality using the Shapiro-Wilk test on the numeric target split by the categorical feature."""
    groups = [group[target].values for name, group in df_cleaned.groupby(feature)]
    groups = [g for g in groups if len(g) >= 3]
    
    # if len(groups) < 2:
    #     return "❌ Not enough groups for normality test."

    p_values = []
    for group in groups:
        _, p_value = stats.shapiro(group)
        p_values.append(p_value)

    fig = plot_normality(groups, feature, p_values)

    overall_p_value = min(p_values)
    if overall_p_value > 0.05:
        return "✅ Normality assumption is satisfied.", fig
    else:
        return f"❌ Normality assumption is not satisfied, overall_p_value = {overall_p_value:.4e} < 0.05", fig

def test_variance_homogeneity(df_cleaned, feature, target):
    """Tests for homogeneity of variances using Levene’s test."""
    groups = [df_cleaned[df_cleaned[feature] == cat][target].values for cat in df_cleaned[feature].unique()]
    
    stat, p_value = stats.levene(*groups)
    
    if p_value > 0.05:
        return "✅ Homogeneity of variances assumption is satisfied."
    else:
        return f"❌ Homogeneity of variances assumption is not satisfied, p-value = {p_value:.4e} < 0.05"

def check_class_balance(df_cleaned, feature, target):
    """Checks balance between classes in the target variable."""
    class_counts = df_cleaned[feature].value_counts()
    min_count = class_counts.min()
    total_count = class_counts.sum()
    
    balance_ratio = min_count / total_count

    if balance_ratio < 0.1:
        return f"❌ Class balance is not acceptable, balance_ratio = {balance_ratio:.4e} < 0.1"
    return "✅ Class balance is acceptable."

def check_expected_frequencies(contingency_table):
    """Check if expected frequencies are sufficient for Chi-squared test."""
    expected = contingency_table.values.sum() * contingency_table.divide(contingency_table.sum(axis=1), axis=0).fillna(0)
    
    if np.any(expected < 5):
        return "❌ Expected frequencies are not adequate for Chi-squared test."
    else:
        return "✅ Expected frequencies are adequate for Chi-squared test."

def perform_t_test(df_cleaned, feature, target):
    """Performs independent t-test."""
    # Check if the feature has exactly two unique categories
    if df_cleaned[feature].nunique() != 2:
        return "🚫 T-test requires exactly two groups for comparison."
    
    # Split the data into two groups based on the feature
    group1 = df_cleaned[df_cleaned[feature] == df_cleaned[feature].unique()[0]][target].values
    group2 = df_cleaned[df_cleaned[feature] == df_cleaned[feature].unique()[1]][target].values
    
    # Perform the t-test
    t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=True)  # Change equal_var=False for Welch's t-test

    if p_value < 0.05:
        return f"⚖️ T-test Result: t-statistic = {t_stat:.4e}, p-value = {p_value:.4e}. ✅ Significance found between groups."
    else:
        return f"⚖️ T-test Result: t-statistic = {t_stat:.4e}, p-value = {p_value:.4e}. ✅ No significant difference found between groups."

def perform_anova(df_cleaned, feature, target):
    """Performs ANOVA test."""
    groups = [df_cleaned[df_cleaned[feature] == cat][target].values for cat in df_cleaned[feature].unique()]
    
    f_stat, p_value = stats.f_oneway(*groups)

    if p_value < 0.05:
        return f"⚖️ ANOVA Test Result: F-statistic = {f_stat:.4e}, p-value = {p_value:.4e}. ✅ Significance found between groups."
    else:
        return f"⚖️ ANOVA Test Result: F-statistic = {f_stat:.4e}, p-value = {p_value:.4e}. ✅ No significant difference found between groups."

def perform_chi_squared_test(df_cleaned, feature, target):
    """Perform Chi-squared test based on the cleaned DataFrame."""
    contingency_table = pd.crosstab(df_cleaned[feature], df_cleaned[target])
    
    expected_freq_message = check_expected_frequencies(contingency_table)
    
    if "❌" in expected_freq_message:
        return expected_freq_message
    
    chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    if p_value < 0.05:
        return f"🔢 Chi-squared Test Result: Chi-squared statistic = {chi2_stat:.4f}, p-value = {p_value:.4e}. ✅ Significance found."
    else:
        return f"🔢 Chi-squared Test Result: Chi-squared statistic = {chi2_stat:.4f}, p-value = {p_value:.4e}. ✅ No significant difference found."

def perform_mann_whitney(df, numerical_feature, ordinal_feature):
    """Performs the Mann-Whitney U Test between a numerical feature and a binary ordinal feature."""
    groups = [df[df[ordinal_feature] == category][numerical_feature].dropna() for category in df[ordinal_feature].unique()]

    if len(groups) != 2:
        return "❌ Mann-Whitney U Test requires exactly two groups."
    
    stat, p_value = stats.mannwhitneyu(groups[0], groups[1], alternative='two-sided')

    if p_value < 0.05:
        return f"⚠️ Mann-Whitney U Test: ✅ Significant difference found between the groups (p-value = {p_value:.4e})."
    else:
        return f"⚠️ Mann-Whitney U Test: ✅ No significant difference found between the groups (p-value = {p_value:.4e})."

def perform_kruskal_wallis(df_cleaned, feature, target):
    """Performs Kruskal-Wallis test."""
    groups = [df_cleaned[df_cleaned[feature] == cat][target].values for cat in df_cleaned[feature].unique()]    
    stat, p_value = stats.kruskal(*groups)

    if len(groups) < 2:
        return "❌ Not enough groups to perform Kruskal-Wallis test."

    if p_value < 0.05:
        return f"⚠️ Kruskal-Wallis test: ✅ Significant differences found between groups (p-value = {p_value:.4e})."
    else:
        return f"⚠️ Kruskal-Wallis test: ❌ No significant differences found (p-value = {p_value:.4e})."

def perform_welch_anova(df_cleaned, feature, target):
    """Performs Welch's ANOVA when homogeneity of variances is not satisfied."""
    groups = [df_cleaned[df_cleaned[feature] == cat][target].dropna().values for cat in df_cleaned[feature].unique() if len(df_cleaned[df_cleaned[feature] == cat]) > 0]
    
    if len(groups) < 2:
        return "❌ Not enough groups to perform Welch's ANOVA."

    f_stat, p_value = stats.f_oneway(*groups)

    if p_value < 0.05:
        return f"⚖️ Welch's ANOVA Test Result: ✅ Significance found between groups (p-value = {p_value:.4e})."
    else:
        return f"⚖️ Welch's ANOVA Test Result: ✅ No significant difference found between groups (p-value = {p_value:.4e})."

def bootstrap_test(df_cleaned, feature, target, n_iterations=1000):
    """Perform bootstrapping to compare group means."""
    groups = [df_cleaned[df_cleaned[feature] == cat][target].values for cat in df_cleaned[feature].unique()]
    means = np.array([np.mean(group) for group in groups])
    observed_diff = means.max() - means.min()

    bootstrap_diffs = []
    
    for _ in range(n_iterations):
        bootstrapped_samples = [np.random.choice(group, size=len(group), replace=True) for group in groups]
        boot_means = np.array([np.mean(sample) for sample in bootstrapped_samples])
        bootstrap_diffs.append(boot_means.max() - boot_means.min())
    
    p_value = np.mean(np.array(bootstrap_diffs) >= observed_diff)
    return f"🔄 Bootstrapping Test Result: Observed difference = {observed_diff}, p-value = {p_value:.4e}"

def Hypothesis_Testing_Methods(df, target, feature, target_type, feature_type):
    """Main function to make an Hypothesis Testing Methods (t-test / ANOVA / chi2)."""
    
    # Step 1: Clean the data
    df_cleaned = clean_data(df, feature, target)

    # Count number of unique groups
    num_groups = df_cleaned[feature].nunique()

    print("teses")
    if target_type == "Numerical" and num_groups==2:
        Hypothesis_test = "t-test"
    elif target_type == "Numerical" and num_groups>2:
        Hypothesis_test = "ANOVA"
    elif (target_type == "Ordinal" or target_type == "Nominal") and (feature_type == "Ordinal" or feature_type == "Nominal"):
        Hypothesis_test = "chi2"
    else:
        messages.append(f"❌ Not enough groups for analysis based on feature '{feature}'.")
        return messages, None
        
    messages = []  # To collect messages
    messages.append(f"\n🔍 Checking conditions for {Hypothesis_test} between {target} and {feature}")

    if target_type != "Nominal":
        # Check for outliers in the target
        outlier_check = check_outliers(df_cleaned, target)
        messages.append(outlier_check)  # Collect outlier check message
    
    print("Hypothesis_test : ", Hypothesis_test)
    
    if Hypothesis_test == "t-test" or Hypothesis_test == "ANOVA":

        # Step 2: Check assumptions
        normality_message, normality_fig = test_normality(df_cleaned, feature, target)
        messages.append(normality_message)
        if "❌" in normality_message:
            if Hypothesis_test == "t-test":
                mann_whitney_message = perform_mann_whitney(df_cleaned, target, feature)
                messages.append(mann_whitney_message)
            else:
                kruskal_message = perform_kruskal_wallis(df_cleaned, feature, target)
                messages.append(kruskal_message)
            return messages, normality_fig
    
        variance_message = test_variance_homogeneity(df_cleaned, feature, target)
        messages.append(variance_message)
        if "❌" in variance_message:               
            welch_message = perform_welch_anova(df_cleaned, feature, target)
            messages.append(welch_message)
            return messages, normality_fig
    
        class_balance_message = check_class_balance(df_cleaned, feature, target)
        messages.append(class_balance_message)
        if "❌" in class_balance_message:
            bootstrap_message = bootstrap_test(df_cleaned, feature, target)
            messages.append(bootstrap_message)
            return messages, normality_fig
        
        # Step 3: Perform test
        if Hypothesis_test == "t-test":
            t_test_message = perform_t_test(df_cleaned, feature, target)
            messages.append(t_test_message)        
        if Hypothesis_test == "t-test":
            anova_message = perform_anova(df_cleaned, feature, target)
            messages.append(anova_message)

    elif Hypothesis_test == "chi2":
        # Step 2: Check expectations and perform Chi-squared test
        chi_squared_message = perform_chi_squared_test(df_cleaned, feature, target)
        messages.append(chi_squared_message)
        normality_fig = None


    return messages, normality_fig