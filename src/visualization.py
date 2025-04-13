"""
Visualization utilities for Stack Overflow Developer Survey 2024 analysis.
Contains functions for creating standardized visualizations and plots.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter


def setup_visualization_defaults():
    """
    Set up default visualization parameters for consistent styling.
    """
    sns.set_theme(style="ticks", context="talk")

    # Customize Matplotlib parameters for a clean look
    plt.rcParams.update(
        {
            # Fonts and sizes
            "font.family": "sans-serif",
            "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
            "axes.titlesize": 18,
            "axes.labelsize": 16,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "legend.fontsize": 14,
            "figure.titlesize": 20,
            # Grid style
            "grid.color": "lightgray",
            "grid.linestyle": "--",
            # Remove top and right spines for a cleaner look
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def plot_age_distribution(df, save_path=None):
    """
    Plot the age distribution of developers.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=(14, 6))
    sns.histplot(df["Age"].dropna(), bins=30)
    plt.title("Age Distribution of Developers Globally")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.xticks(rotation=45)

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_experience_distribution(df, save_path=None):
    """
    Plot the distribution of coding experience.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=(14, 6))
    sns.histplot(
        df["YearsCode"].dropna(), bins=20, color="blue", label="Total Years Coding"
    )
    sns.histplot(
        df["YearsCodePro"].dropna(),
        bins=20,
        color="orange",
        label="Years Coding Professionally",
    )
    plt.title("Experience Distribution of Developers")
    plt.xlabel("Years of Experience")
    plt.ylabel("Count")
    plt.legend()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_education_background(df, save_path=None):
    """
    Plot the educational background of developers.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=(14, 8))
    sns.countplot(
        y="EdLevel",
        data=df,
        order=df["EdLevel"].value_counts().index,
        palette="dark:b_r",
    )
    plt.title("Educational Background of Developers")
    plt.xlabel("Count")
    plt.ylabel("Education Level")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_top_technologies(df, column, title, n=10, save_path=None):
    """
    Plot the top N technologies from a technology column.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    column : str
        Column name containing semicolon-separated technology lists
    title : str
        Plot title
    n : int
        Number of top technologies to display
    save_path : str, optional
        Path to save the figure
    """
    from collections import Counter

    # Count technologies
    tech_counts = Counter()
    for tech_list in df[column].dropna():
        techs = [t.strip() for t in tech_list.split(";") if t.strip()]
        tech_counts.update(techs)

    # Convert to DataFrame and sort
    tech_df = pd.DataFrame(
        tech_counts.items(), columns=["Technology", "Count"]
    ).sort_values("Count", ascending=False)

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Count", y="Technology", data=tech_df.head(n), palette="dark:b_r")
    plt.title(title)
    plt.xlabel("Number of Respondents")
    plt.ylabel("Technology")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_work_arrangement(df, save_path=None):
    """
    Plot the distribution of work arrangements.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=(14, 6))
    sns.countplot(
        x="RemoteWork",
        data=df,
        order=df["RemoteWork"].value_counts().index,
        palette="dark:b_r",
    )
    plt.title("Work Arrangement Distribution (2024)")
    plt.xlabel("Work Arrangement")
    plt.ylabel("Number of Respondents")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_correlation_matrix(df, columns=None, save_path=None):
    """
    Plot a correlation matrix for specified numeric columns.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    columns : list, optional
        List of column names to include in correlation matrix
    save_path : str, optional
        Path to save the figure
    """
    if columns is None:
        columns = ["ConvertedCompYearly", "JobSat", "YearsCode", "YearsCodePro"]

    corr_df = df[columns].dropna()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix: Key Metrics")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_work_by_age(df, save_path=None):
    """
    Plot work arrangement preferences by age group.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data with AgeBin column
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x="AgeBin", hue="RemoteWork", palette="dark:b_r")
    plt.title("Work Arrangement Preferences by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Number of Respondents")
    plt.legend(title="Work Arrangement", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_boxplot(df, x, y, title, palette="dark:b_r", rotate_x=False, save_path=None):
    """
    Create a boxplot of a variable by group.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    x : str
        Column name for x-axis (grouping variable)
    y : str
        Column name for y-axis (measurement variable)
    title : str
        Plot title
    palette : str, optional
        Color palette to use
    rotate_x : bool, optional
        Whether to rotate x-axis labels
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=(14, 6))
    sns.boxplot(x=x, y=y, data=df, palette=palette)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)

    if rotate_x:
        plt.xticks(rotation=90, ha="right")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_regional_compensation_experience(regional_stats, save_path=None):
    """
    Create a scatter plot of median compensation vs. experience by country.

    Parameters:
    -----------
    regional_stats : pandas.DataFrame
        DataFrame containing regional statistics
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=(14, 6))
    scatter = sns.scatterplot(
        x="MedianExperience",
        y="MedianCompensation",
        hue="MedianJobSat",
        size="Count",
        sizes=(50, 200),
        data=regional_stats,
        palette="dark:b_r",
    )

    plt.title("Regional Influences: Compensation vs Experience")
    plt.xlabel("Median Years of Professional Experience")
    plt.ylabel("Median Yearly Compensation")

    # Add country labels
    for idx, row in regional_stats.iterrows():
        plt.text(
            row["MedianExperience"],
            row["MedianCompensation"],
            row["Country"],
            fontsize=9,
        )

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_comp_col_scatter(merged_data, save_path=None):
    """
    Create a scatter plot of compensation vs. cost of living.

    Parameters:
    -----------
    merged_data : pandas.DataFrame
        DataFrame containing compensation and cost of living data
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=(14, 10))
    scatter = sns.scatterplot(
        data=merged_data,
        x="Cost of Living Plus Rent Index",
        y="MedianCompensation",
        size="Local Purchasing Power Index",
        hue="AffordabilityScore",
        sizes=(50, 300),
        palette="dark:b_r",
    )

    plt.title("Median Compensation vs. Cost of Living Plus Rent Index")
    plt.xlabel("Cost of Living Plus Rent Index")
    plt.ylabel("Median Yearly Compensation")

    # Add country labels
    for i, row in merged_data.iterrows():
        plt.text(
            row["Cost of Living Plus Rent Index"] * 1.01,
            row["MedianCompensation"] * 1.01,
            row["Country"],
            fontsize=8,
        )

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_top_affordable(merged_data, n=10, save_path=None):
    """
    Plot the top N most affordable countries by affordability score.

    Parameters:
    -----------
    merged_data : pandas.DataFrame
        DataFrame containing compensation and cost of living data
    n : int, optional
        Number of countries to display
    save_path : str, optional
        Path to save the figure
    """
    top_affordable = merged_data.sort_values(
        "AffordabilityScore", ascending=False
    ).head(n)

    plt.figure(figsize=(14, 6))
    sns.barplot(
        x="AffordabilityScore", y="Country", data=top_affordable, palette="dark:b_r"
    )
    plt.title(f"Top {n} Countries by Affordability Score (Compensation / COL Index)")
    plt.xlabel("Affordability Score")
    plt.ylabel("Country")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def plot_tech_heatmap(
    df,
    tech_column,
    country_column="Country",
    top_countries=None,
    top_n=10,
    save_path=None,
):
    """
    Create a heatmap of technology usage by country.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the survey data
    tech_column : str
        Column name containing semicolon-separated technology lists
    country_column : str, optional
        Column name for country
    top_countries : list, optional
        List of countries to include
    top_n : int, optional
        Number of top technologies to display
    save_path : str, optional
        Path to save the figure
    """
    from data_processing import explode_column

    # Explode the tech column
    df_tech = explode_column(df, tech_column, country_column)

    # Filter for top countries if specified
    if top_countries is not None:
        df_tech = df_tech[df_tech[country_column].isin(top_countries)]

    # Get counts per country and technology
    tech_counts = (
        df_tech.groupby([country_column, tech_column]).size().reset_index(name="Count")
    )

    # Get top N technologies by total count
    top_techs = (
        tech_counts.groupby(tech_column)["Count"].sum().nlargest(top_n).index.tolist()
    )

    # Filter for top technologies
    tech_counts = tech_counts[tech_counts[tech_column].isin(top_techs)]

    # Pivot table for heatmap
    pivot_tech = tech_counts.pivot(
        index=country_column, columns=tech_column, values="Count"
    ).fillna(0)

    # Plot heatmap
    plt.figure(figsize=(14, 7))
    sns.heatmap(pivot_tech, annot=True, fmt=".0f", cmap="YlGnBu")
    plt.title(f"Concentration of {tech_column} by Country")
    plt.xlabel(tech_column)
    plt.ylabel(country_column)

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)

    plt.show()


def save_all_visualizations(df, output_dir="./results/figures/"):
    """
    Generate and save all standard visualizations to specified directory.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the cleaned survey data
    output_dir : str, optional
        Directory to save the figures
    """
    import os

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate and save all visualizations
    plot_age_distribution(df, save_path=f"{output_dir}age_distribution.png")
    plot_experience_distribution(
        df, save_path=f"{output_dir}experience_distribution.png"
    )
    plot_education_background(df, save_path=f"{output_dir}education_background.png")
    plot_top_technologies(
        df,
        "LanguageHaveWorkedWith",
        "Top 10 Programming Languages Used in 2024",
        save_path=f"{output_dir}top_languages.png",
    )
    plot_work_arrangement(df, save_path=f"{output_dir}work_arrangement.png")
    plot_correlation_matrix(df, save_path=f"{output_dir}correlation_matrix.png")

    # Additional visualizations if data is properly processed
    if "AgeBin" in df.columns:
        plot_work_by_age(df, save_path=f"{output_dir}work_by_age.png")

    print(f"All visualizations saved to {output_dir}")
