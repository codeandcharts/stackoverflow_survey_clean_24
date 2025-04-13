"""
Standalone script to generate and save all visualizations from the
Stack Overflow Survey 2024 analysis into a figures/ folder.

This script does not require separate module imports - all necessary functions
are defined within this single file.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
import sys

# Suppress warnings
warnings.filterwarnings("ignore")


# Define data processing functions
def load_survey_data(
    filepath="./data/raw/survey_results_public.csv", useful_columns=None
):
    """Load the Stack Overflow survey data and select only useful columns if specified."""
    df = pd.read_csv(filepath)
    if useful_columns is not None:
        df = df[useful_columns].copy()
    return df


def load_col_data(filepath="./data/raw/Cost_of_Living_Index_by_Country_2024.csv"):
    """Load the Cost of Living Index by Country data."""
    return pd.read_csv(filepath)


def clean_numeric_columns(df, columns=None):
    """Convert specified columns to numeric type, handling non-numeric values gracefully."""
    if columns is None:
        columns = ["YearsCode", "YearsCodePro", "ConvertedCompYearly", "JobSat"]

    df_cleaned = df.copy()
    for col in columns:
        if col in df.columns:
            df_cleaned[col] = pd.to_numeric(df[col], errors="coerce")
    return df_cleaned


def count_items(series):
    """Count items in semicolon-separated strings."""
    all_responses = series.dropna().str.split(";")
    flattened = [
        item.strip()
        for sublist in all_responses
        for item in sublist
        if item.strip() != ""
    ]
    return Counter(flattened)


def explode_column(df, column, country_col="Country"):
    """Explode a semicolon-delimited column into individual rows, preserving other columns."""
    temp_df = df[[column, country_col]].dropna().copy()
    temp_df[column] = temp_df[column].str.split(";")
    return temp_df.explode(column).assign(**{column: lambda x: x[column].str.strip()})


def categorize_company(org_size):
    """Categorize company size into meaningful groups."""
    if pd.isnull(org_size):
        return "Unknown"

    org_size = str(org_size).lower().strip()
    if any(x in org_size for x in ["1-10", "11-50"]):
        return "Startup"
    elif any(x in org_size for x in ["51-200", "201-500"]):
        return "Mid-sized"
    elif any(x in org_size for x in ["500", "1000", "5000", "5000+"]):
        return "Enterprise"
    else:
        return "Other"


def clean_age_column(df, age_col="Age"):
    """Clean and bin the Age column."""
    df_cleaned = df.copy()

    # Clean age strings, handling non-string values
    df_cleaned["Age_cleaned"] = df_cleaned[age_col].astype(str)
    df_cleaned["Age_cleaned"] = df_cleaned["Age_cleaned"].str.replace(
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
    """Merge survey data with cost of living data."""
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
    """Create regional statistics for compensation, experience, and job satisfaction."""
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


# Set up visualization defaults
def setup_visualization_defaults():
    """Set up default visualization parameters for consistent styling."""
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


# Set up visualization defaults
setup_visualization_defaults()

# Create figures directory if it doesn't exist
os.makedirs("./figures", exist_ok=True)

# Define useful columns from the notebook
useful_columns = [
    # Core Demographics and Background
    "Age",
    "Country",
    "MainBranch",
    "YearsCode",
    "YearsCodePro",
    "EdLevel",
    "DevType",
    "Employment",
    "WorkExp",
    "ResponseId",
    # Work Environment
    "RemoteWork",
    "OrgSize",
    "Industry",
    # Compensation and Economics
    "CompTotal",
    "ConvertedCompYearly",
    "Currency",
    "JobSat",
    # Technology Ecosystem
    "LanguageHaveWorkedWith",
    "LanguageWantToWorkWith",
    "DatabaseHaveWorkedWith",
    "DatabaseWantToWorkWith",
    "WebframeHaveWorkedWith",
    "WebframeWantToWorkWith",
    "PlatformHaveWorkedWith",
    "PlatformWantToWorkWith",
    # Professional Development
    "LearnCode",
    "LearnCodeOnline",
    "BuildvsBuy",
    "PurchaseInfluence",
    "OpSysPersonal use",
    "OpSysProfessional use",
]


# Function to generate and save all visualizations
def generate_all_visualizations(df, col_data):
    print("Generating visualizations...")

    # 1. Demographics Analysis
    # Age Distribution
    plt.figure(figsize=(14, 6))
    sns.histplot(df["Age"].dropna(), bins=30)
    plt.title("Age Distribution of Developers Globally")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.savefig("./figures/01_age_distribution.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("1/23: Age distribution saved")

    # Experience Distribution
    plt.figure(figsize=(14, 6))
    sns.histplot(
        df["YearsCode"].dropna(),
        bins=20,
        palette="dark:b_r",
        label="Total Years Coding",
    )
    sns.histplot(
        df["YearsCodePro"].dropna(),
        bins=20,
        palette="dark:b_r",
        label="Years Coding Professionally",
    )
    plt.title("Experience Distribution of Developers")
    plt.xlabel("Years of Experience")
    plt.ylabel("Count")
    plt.legend()
    plt.savefig(
        "./figures/02_experience_distribution.png", bbox_inches="tight", dpi=300
    )
    plt.close()
    print("2/23: Experience distribution saved")

    # Educational Background
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
    plt.savefig("./figures/03_education_background.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("3/23: Educational background saved")

    # 2. Technology Landscape
    # Programming Languages
    language_counts = count_items(df["LanguageHaveWorkedWith"])
    lang_df = pd.DataFrame(
        language_counts.items(), columns=["Language", "Count"]
    ).sort_values("Count", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Count", y="Language", data=lang_df.head(10), palette="dark:b_r")
    plt.title("Top 10 Programming Languages Used in 2024")
    plt.xlabel("Number of Respondents")
    plt.ylabel("Programming Language")
    plt.savefig("./figures/04_top_languages.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("4/23: Top programming languages saved")

    # Web Frameworks
    framework_counts = count_items(df["WebframeHaveWorkedWith"])
    fw_df = pd.DataFrame(
        framework_counts.items(), columns=["Framework", "Count"]
    ).sort_values("Count", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Count", y="Framework", data=fw_df.head(10), palette="dark:b_r")
    plt.title("Top 10 Frameworks Used in 2024")
    plt.xlabel("Number of Respondents")
    plt.ylabel("Framework")
    plt.savefig("./figures/05_top_frameworks.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("5/23: Top frameworks saved")

    # Databases
    database_counts = count_items(df["DatabaseHaveWorkedWith"])
    database_df = pd.DataFrame(
        database_counts.items(), columns=["Database", "Count"]
    ).sort_values("Count", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Count", y="Database", data=database_df.head(10), palette="dark:b_r")
    plt.title("Top 10 Databases Used in 2024", fontsize=14)
    plt.xlabel("Number of Respondents")
    plt.ylabel("Database")
    plt.tight_layout()
    plt.savefig("./figures/06_top_databases.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("6/23: Top databases saved")

    # 3. Work Environment
    # Remote Work Distribution
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
    plt.savefig(
        "./figures/07_remote_work_distribution.png", bbox_inches="tight", dpi=300
    )
    plt.close()
    print("7/23: Remote work distribution saved")

    # Job Satisfaction by Company Size
    plt.figure(figsize=(14, 8))
    sns.boxplot(
        x="JobSat",
        y="OrgSize",
        data=df,
        order=df["OrgSize"].value_counts().index,
        palette="dark:b_r",
    )
    plt.title("Job Satisfaction by Company Size")
    plt.xlabel("Job Satisfaction Rating")
    plt.ylabel("Company Size")
    plt.savefig(
        "./figures/08_job_satisfaction_by_company_size.png",
        bbox_inches="tight",
        dpi=300,
    )
    plt.close()
    print("8/23: Job satisfaction by company size saved")

    # Correlation Matrix
    numeric_cols = ["ConvertedCompYearly", "JobSat", "YearsCode", "YearsCodePro"]
    corr_df = df[numeric_cols].dropna()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix: Compensation, Satisfaction, Experience")
    plt.savefig("./figures/09_correlation_matrix.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("9/23: Correlation matrix saved")

    # Work Arrangement by Age
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x="AgeBin", hue="RemoteWork", palette="dark:b_r")
    plt.title("Work Arrangement Preferences by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Number of Respondents")
    plt.legend(title="Work Arrangement", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(
        "./figures/10_work_arrangement_by_age.png", bbox_inches="tight", dpi=300
    )
    plt.close()
    print("10/23: Work arrangement by age saved")

    # 4. Regional Analysis
    # Get top countries for regional analysis
    top10_countries = df["Country"].value_counts().head(10).index.tolist()
    df_top10 = df[df["Country"].isin(top10_countries)]

    # Professional Experience by Country
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Country", y="YearsCodePro", data=df_top10, palette="dark:b_r")
    plt.title("Years of Professional Coding Experience by Top 10 Countries")
    plt.xlabel("Country")
    plt.ylabel("Years of Professional Experience")
    plt.xticks(rotation=90)
    plt.savefig("./figures/11_experience_by_country.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("11/23: Experience by country saved")

    # Job Satisfaction by Country
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="JobSat", y="Country", data=df_top10, palette="dark:b_r")
    plt.title("Job Satisfaction by Top 10 Countries")
    plt.xlabel("Job Satisfaction")
    plt.ylabel("Country")
    plt.savefig(
        "./figures/12_job_satisfaction_by_country.png", bbox_inches="tight", dpi=300
    )
    plt.close()
    print("12/23: Job satisfaction by country saved")

    # Developer Type by Country
    try:
        df_devtype = explode_column(df, "DevType")
        devtype_counts = (
            df_devtype.groupby(["Country", "DevType"]).size().reset_index(name="Count")
        )
        devtype_top = devtype_counts[devtype_counts["Country"].isin(top10_countries)]

        # Check if we have data to pivot
        if not devtype_top.empty:
            pivot_devtype = devtype_top.pivot(
                index="Country", columns="DevType", values="Count"
            ).fillna(0)
            plt.figure(figsize=(14, 7))
            sns.heatmap(pivot_devtype, annot=True, fmt=".0f", cmap="YlGnBu")
            plt.title("Concentration of Developer Types by Country (Top 10 Countries)")
            plt.xlabel("Developer Type")
            plt.ylabel("Country")
            plt.savefig(
                "./figures/13_developer_type_by_country.png",
                bbox_inches="tight",
                dpi=300,
            )
            plt.close()
            print("13/23: Developer type by country saved")
        else:
            print("Skipping developer type heatmap - insufficient data")
    except Exception as e:
        print(f"Error generating developer type heatmap: {e}")

    # 5. Compensation Analysis
    # Create regional stats
    regional_stats = create_regional_stats(df)

    # Regional Compensation vs Experience
    try:
        plt.figure(figsize=(14, 6))
        scatter = sns.scatterplot(
            x="MedianExperience",
            y="MedianCompensation",
            size="Count",
            sizes=(50, 100),
            data=regional_stats.head(30),
            palette="dark:b_r",
        )
        plt.title("Regional Influences: Compensation vs Experience")
        plt.xlabel("Median Years of Professional Experience")
        plt.ylabel("Median Yearly Compensation")
        for idx, row in regional_stats.head(30).iterrows():
            plt.text(
                row["MedianExperience"],
                row["MedianCompensation"],
                row["Country"],
                fontsize=9,
            )
        plt.savefig(
            "./figures/14_compensation_vs_experience.png", bbox_inches="tight", dpi=300
        )
        plt.close()
        print("14/23: Compensation vs experience saved")
    except Exception as e:
        print(f"Error generating compensation vs experience plot: {e}")

    # Compensation by Company Category
    plt.figure(figsize=(14, 6))
    sns.boxplot(
        x="CompanyCategory", y="ConvertedCompYearly", data=df, palette="dark:b_r"
    )
    plt.title("Compensation by Company Category")
    plt.xlabel("Company Category")
    plt.ylabel("Yearly Compensation")
    plt.ylim(0, df["ConvertedCompYearly"].quantile(0.95))
    plt.savefig(
        "./figures/15_compensation_by_company_category.png",
        bbox_inches="tight",
        dpi=300,
    )
    plt.close()
    print("15/23: Compensation by company category saved")

    # 6. Learning and Development
    # Learning Methods
    learning_methods_counts = count_items(df["LearnCode"])
    learning_methods_df = pd.DataFrame(
        learning_methods_counts.items(), columns=["Method", "Count"]
    ).sort_values("Count", ascending=False)
    plt.figure(figsize=(14, 8))
    sns.barplot(
        x="Count", y="Method", data=learning_methods_df.head(10), palette="dark:b_r"
    )
    plt.title("Top 10 Learning Methods Preferred by Developers in 2024")
    plt.xlabel("Number of Respondents")
    plt.ylabel("Learning Method")
    plt.savefig("./figures/16_learning_methods.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("16/23: Learning methods saved")

    # Developer Roles
    try:
        dev_roles = df["DevType"].dropna().str.split(";")
        flat_roles = [role.strip() for sublist in dev_roles for role in sublist]
        top_roles = dict(Counter(flat_roles).most_common(10))
        top_roles_df = pd.DataFrame(
            list(top_roles.items()), columns=["DevType", "Count"]
        ).sort_values("Count", ascending=False)
        plt.figure(figsize=(14, 6))
        sns.barplot(data=top_roles_df, y="DevType", x="Count", palette="dark:b_r")
        plt.title("Top 10 Developer Roles in Survey")
        plt.xlabel("Count")
        plt.ylabel("Developer Role")
        plt.tight_layout()
        plt.savefig("./figures/17_developer_roles.png", bbox_inches="tight", dpi=300)
        plt.close()
        print("17/23: Developer roles saved")
    except Exception as e:
        print(f"Error generating developer roles plot: {e}")

    # 7. Industry Analysis
    # Job Satisfaction by Industry
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Industry", y="JobSat", data=df, palette="dark:b_r")
    plt.title("Job Satisfaction by Industry")
    plt.xlabel("Industry")
    plt.ylabel("Job Satisfaction")
    plt.xticks(rotation=90, ha="right")
    plt.savefig(
        "./figures/18_job_satisfaction_by_industry.png", bbox_inches="tight", dpi=300
    )
    plt.close()
    print("18/23: Job satisfaction by industry saved")

    # Professional Coding Experience by Industry
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Industry", y="YearsCodePro", data=df, palette="dark:b_r")
    plt.title("Professional Coding Experience by Industry")
    plt.xlabel("Industry")
    plt.ylabel("Years of Professional Coding Experience")
    plt.xticks(rotation=90, ha="right")
    plt.savefig("./figures/19_experience_by_industry.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("19/23: Experience by industry saved")

    # 8. Cost of Living Integration
    # Merge compensation and cost of living data
    merged_col = merge_comp_col(df, col_data)

    # Compensation vs Cost of Living
    try:
        top_30 = merged_col.head(30)
        plt.figure(figsize=(14, 10))
        scatter = sns.scatterplot(
            data=top_30,
            x="Cost of Living Plus Rent Index",
            y="MedianCompensation",
            size="Local Purchasing Power Index",
            sizes=(50, 300),
            palette="dark:b_r",
        )
        plt.title("Median Compensation vs. Cost of Living Plus Rent Index")
        plt.xlabel("Cost of Living Plus Rent Index")
        plt.ylabel("Median Yearly Compensation")
        for i, row in top_30.iterrows():
            plt.text(
                row["Cost of Living Plus Rent Index"] * 1.01,
                row["MedianCompensation"] * 1.01,
                row["Country"],
                fontsize=8,
            )
        plt.tight_layout()
        plt.savefig(
            "./figures/20_compensation_vs_col.png", bbox_inches="tight", dpi=300
        )
        plt.close()
        print("20/23: Compensation vs cost of living saved")
    except Exception as e:
        print(f"Error generating compensation vs cost of living plot: {e}")

    # Affordability Score Ranking
    try:
        top_affordable = merged_col.sort_values(
            "AffordabilityScore", ascending=False
        ).head(10)
        plt.figure(figsize=(14, 6))
        sns.barplot(
            x="AffordabilityScore", y="Country", data=top_affordable, palette="dark:b_r"
        )
        plt.title("Top 10 Countries by Affordability Score (Compensation / COL Index)")
        plt.xlabel("Affordability Score")
        plt.ylabel("Country")
        plt.savefig(
            "./figures/21_top_affordable_countries.png", bbox_inches="tight", dpi=300
        )
        plt.close()
        print("21/23: Top affordable countries saved")
    except Exception as e:
        print(f"Error generating affordability score ranking plot: {e}")

    # Local Purchasing Power
    try:
        filtered = merged_col[merged_col["Count"] >= 50].copy().head(10)
        filtered = filtered.sort_values("Local Purchasing Power Index", ascending=False)
        plt.figure(figsize=(14, 6))
        sns.barplot(
            x="Local Purchasing Power Index",
            y="Country",
            data=filtered,
            palette="dark:b_r",
        )
        plt.title("Local Purchasing Power Index by Country (≥50 Responses)")
        plt.xlabel("Local Purchasing Power Index")
        plt.ylabel("Country")
        plt.savefig(
            "./figures/22_local_purchasing_power.png", bbox_inches="tight", dpi=300
        )
        plt.close()
        print("22/23: Local purchasing power saved")
    except Exception as e:
        print(f"Error generating local purchasing power plot: {e}")

    # 9. Future Trends
    # Emerging Technologies
    try:
        want_cols = [
            "LanguageWantToWorkWith",
            "WebframeWantToWorkWith",
            "PlatformWantToWorkWith",
            "ToolsTechWantToWorkWith",
        ]
        emerging_counter = Counter()
        for col in want_cols:
            if col in df.columns:
                emerging_counter.update(count_items(df[col]))
        emerging_df = pd.DataFrame(
            emerging_counter.items(), columns=["Technology", "Count"]
        ).sort_values("Count", ascending=False)
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x="Count", y="Technology", data=emerging_df.head(10), palette="dark:b_r"
        )
        plt.title("Top 10 Emerging Technologies Developers Plan to Adopt (2024)")
        plt.xlabel("Number of Respondents")
        plt.ylabel("Technology")
        plt.savefig(
            "./figures/23_emerging_technologies.png", bbox_inches="tight", dpi=300
        )
        plt.close()
        print("23/23: Emerging technologies saved")
    except Exception as e:
        print(f"Error generating emerging technologies plot: {e}")

    print("\nAll visualizations generated and saved to ./figures/ directory!")


# Main execution
if __name__ == "__main__":
    try:
        print("Loading survey data...")

        # Check if data files exist
        data_path = "./data/raw/survey_results_public.csv"
        col_path = "./data/raw/Cost_of_Living_Index_by_Country_2024.csv"

        if not os.path.exists(data_path):
            print(f"Error: Survey data file not found at {data_path}")
            print("Please ensure the survey data file is in the correct location.")
            sys.exit(1)

        if not os.path.exists(col_path):
            print(f"Warning: Cost of living data file not found at {col_path}")
            print("Some visualizations requiring cost of living data will be skipped.")
            col_data = None
        else:
            col_data = load_col_data(col_path)

        # Load and process survey data
        survey_df = load_survey_data(data_path, useful_columns)
        print(
            f"Data loaded successfully: {survey_df.shape[0]} rows, {survey_df.shape[1]} columns"
        )

        # Clean numeric columns
        print("Cleaning data...")
        df = clean_numeric_columns(survey_df)

        # Clean age column
        df = clean_age_column(df)

        # Create company categories
        df["CompanyCategory"] = df["OrgSize"].apply(categorize_company)
        print("Data processing complete")

        # Generate all visualizations
        generate_all_visualizations(df, col_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback

        traceback.print_exc()
