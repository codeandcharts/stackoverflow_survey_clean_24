"""
Data processing utilities for Stack Overflow Developer Survey 2024 analysis.
Contains functions for data cleaning, transformation, and preparation.
"""

import pandas as pd
import numpy as np
from collections import Counter
import re


def load_survey_data(
    filepath="./data/raw/survey_results_public.csv", useful_columns=None
):
    """
    Load the Stack Overflow survey data and select only useful columns if specified.

    Parameters:
    -----------
    filepath : str
        Path to the survey data CSV file
    useful_columns : list
        List of column names to keep

    Returns:
    --------
    pandas.DataFrame
        DataFrame containing the survey data
    """
    df = pd.read_csv(filepath)

    if useful_columns is not None:
        df = df[useful_columns].copy()

    return df


def load_col_data(filepath="./data/raw/Cost_of_Living_Index_by_Country_2024.csv"):
    """
    Load the Cost of Living Index by Country data.

    Parameters:
    -----------
    filepath : str
        Path to the Cost of Living CSV file

    Returns:
    --------
    pandas.DataFrame
        DataFrame containing the cost of living data
    """
    return pd.read_csv(filepath)


def clean_numeric_columns(df, columns=None):
    """
    Convert specified columns to numeric type, handling non-numeric values gracefully.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    columns : list
        List of column names to convert to numeric

    Returns:
    --------
    pandas.DataFrame
        DataFrame with converted numeric columns
    """
    if columns is None:
        columns = ["YearsCode", "YearsCodePro", "ConvertedCompYearly", "JobSat"]

    df_cleaned = df.copy()

    for col in columns:
        if col in df.columns:
            df_cleaned[col] = pd.to_numeric(df[col], errors="coerce")

    return df_cleaned


def count_items(series):
    """
    Count items in semicolon-separated strings.

    Parameters:
    -----------
    series : pandas.Series
        Series containing semicolon-separated strings

    Returns:
    --------
    collections.Counter
        Counter of individual items
    """
    all_responses = series.dropna().str.split(";")
    flattened = [
        item.strip()
        for sublist in all_responses
        for item in sublist
        if item.strip() != ""
    ]
    return Counter(flattened)


def explode_column(df, column, country_col="Country"):
    """
    Explode a semicolon-delimited column into individual rows, preserving other columns.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the column to explode
    column : str
        Name of the column to explode
    country_col : str
        Name of the country column to preserve

    Returns:
    --------
    pandas.DataFrame
        DataFrame with exploded column
    """
    temp_df = df[[column, country_col]].dropna().copy()
    temp_df[column] = temp_df[column].str.split(";")
    return temp_df.explode(column).assign(**{column: lambda x: x[column].str.strip()})


def categorize_company(org_size):
    """
    Categorize company size into meaningful groups.

    Parameters:
    -----------
    org_size : str
        Company size string

    Returns:
    --------
    str
        Company category
    """
    if pd.isnull(org_size):
        return "Unknown"

    # Convert org_size to lower-case for matching and remove extra spaces
    org_size = org_size.lower().strip()

    if any(x in org_size for x in ["1-10", "11-50"]):
        return "Startup"
    elif any(x in org_size for x in ["51-200", "201-500"]):
        return "Mid-sized"
    elif any(x in org_size for x in ["500", "1000", "5000", "5000+"]):
        return "Enterprise"
    else:
        return "Other"


def clean_age_column(df, age_col="Age"):
    """
    Clean and bin the Age column.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the Age column
    age_col : str
        Name of the age column

    Returns:
    --------
    pandas.DataFrame
        DataFrame with cleaned Age and new AgeBin column
    """
    df_cleaned = df.copy()

    # Clean age strings
    df_cleaned["Age_cleaned"] = df_cleaned[age_col].str.replace(
        " years old", "", regex=False
    )
    df_cleaned["Age_cleaned"] = df_cleaned["Age_cleaned"].str.replace(
        "Under ", "<", regex=False
    )
    df_cleaned["Age_cleaned"] = df_cleaned["Age_cleaned"].str.strip()

    # Map cleaned age ranges to bins
    age_bin_map = {
        "<18": "<25",
        "18-24": "<25",
        "25-34": "25-34",
        "35-44": "35-44",
        "45-54": "45-54",
        "55-64": "55+",
        "65 or older": "55+",
        "Prefer not to say": None,
    }

    df_cleaned["AgeBin"] = df_cleaned["Age_cleaned"].map(age_bin_map)

    return df_cleaned


def merge_comp_col(survey_df, col_df):
    """
    Merge survey data with cost of living data.

    Parameters:
    -----------
    survey_df : pandas.DataFrame
        DataFrame containing the survey data
    col_df : pandas.DataFrame
        DataFrame containing cost of living data

    Returns:
    --------
    pandas.DataFrame
        Merged DataFrame with compensation and cost of living metrics
    """
    # Group by Country to compute median compensation
    median_comp_by_country = (
        survey_df.groupby("Country")
        .agg(
            MedianCompensation=("ConvertedCompYearly", "median"),
            Count=("ResponseId", "count"),
        )
        .reset_index()
    )

    # Merge with cost of living data
    merged = pd.merge(median_comp_by_country, col_df, on="Country", how="left")

    # Drop rows with missing cost of living data
    merged = merged.dropna(
        subset=["Cost of Living Plus Rent Index", "Local Purchasing Power Index"]
    )

    # Calculate affordability score
    merged["AffordabilityScore"] = (
        merged["MedianCompensation"] / merged["Cost of Living Plus Rent Index"]
    )

    return merged


def create_regional_stats(df, min_count=50):
    """
    Create regional statistics for compensation, experience, and job satisfaction.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    min_count : int
        Minimum number of responses required for inclusion

    Returns:
    --------
    pandas.DataFrame
        DataFrame with regional statistics
    """
    regional_stats = (
        df.groupby("Country")
        .agg(
            MedianCompensation=("ConvertedCompYearly", "median"),
            MedianExperience=("YearsCodePro", "median"),
            Count=("ResponseId", "count"),
            MedianJobSat=("JobSat", "median"),
        )
        .reset_index()
    )

    # Filter for countries with sufficient data
    regional_stats = regional_stats[regional_stats["Count"] >= min_count]

    return regional_stats


def filter_top_countries(df, n=10):
    """
    Filter the dataset to include only the top N countries by response count.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    n : int
        Number of top countries to include

    Returns:
    --------
    pandas.DataFrame
        Filtered DataFrame with only top countries
    """
    top_countries = df["Country"].value_counts().head(n).index.tolist()
    return df[df["Country"].isin(top_countries)]
