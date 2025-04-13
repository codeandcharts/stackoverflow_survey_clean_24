# Stack Overflow Developer Survey 2024 Analysis

## Project Overview

This project conducts a comprehensive exploratory data analysis (EDA) of the Stack Overflow Annual Developer Survey 2024 dataset. The analysis examines various facets of the global developer ecosystem, including demographics, technology preferences, work environments, compensation patterns, and geographic trends.

## Table of Contents

- [Project Overview](#project-overview)
- [Data Sources](#data-sources)
- [Installation Requirements](#installation-requirements)
- [Project Structure](#project-structure)
- [Analysis Overview](#analysis-overview)
- [Key Findings](#key-findings)
- [Visualizations](#visualizations)
- [How to Run the Analysis](#how-to-run-the-analysis)
- [Contributing](#contributing)
- [License](#license)

## Data Sources

This analysis relies on the following data sources:

1. **Stack Overflow Annual Developer Survey 2024**
   - Primary dataset containing responses from developers worldwide
   - Available at: [Stack Overflow Insights](https://insights.stackoverflow.com/survey)

2. **Cost of Living Index by Country 2024**
   - Supplementary dataset for cost of living analysis
   - Contains cost of living indexes and purchasing power information

## Installation Requirements

To run this analysis, you'll need the following:

```
Python 3.8+
pandas==1.5.3
numpy==1.24.3
matplotlib==3.7.1
seaborn==0.12.2
```

You can install all required packages using:

```bash
pip install -r requirements.txt
```

## Project Structure

```
stack-overflow-analysis/
├── data/
│   ├── raw/
│   │   ├── survey_results_public.csv       # Stack Overflow Survey raw data
│   │   ├── survey_results_schema.csv       # Schema information for survey
│   │   └── Cost_of_Living_Index_by_Country_2024.csv  # Cost of living data
│   └── processed/                        # Generated during analysis
├── notebooks/
│   └── stack_overflow_eda.ipynb          # Main analysis notebook
├── src/
│   ├── __init__.py
│   ├── data_processing.py                # Data cleaning functions
│   └── visualization.py                  # Visualization helper functions
├── results/
│   └── figures/                          # Generated visualizations
├── requirements.txt                      # Project dependencies
└── README.md                             # This file
```

## Analysis Overview

The analysis is divided into several key sections:

1. **Data Preparation**: Data loading, column selection, handling missing values, and type conversion.

2. **Demographics Analysis**: Examination of age distribution, experience levels, and educational backgrounds.

3. **Technology Landscape**: Analysis of programming languages, frameworks, and databases used by developers.

4. **Work Environment**: Investigation of remote work patterns, job satisfaction, and organization size impacts.

5. **Regional Analysis**: Comparison of developer experiences across countries, including experience levels and technology preferences.

6. **Compensation Analysis**: Exploration of salary differences based on geography, experience, and company type.

7. **Learning and Development**: Analysis of how developers acquire skills and professional development paths.

8. **Industry Analysis**: Comparison of experience and satisfaction across different industry sectors.

9. **Cost of Living Integration**: Analysis of developer compensation relative to local costs and purchasing power.

10. **Future Trends**: Identification of technologies developers plan to adopt in the near future.

## Key Findings

- **Demographics**: The profession is dominated by the 25-34 age bracket, with a significant influx of new developers.

- **Work Arrangements**: Hybrid work has emerged as the dominant arrangement (~23,000 developers), with remote work following closely (~21,000), while in-person arrangements now represent a minority (~11,000).

- **Technology Ecosystem**: JavaScript, HTML/CSS, Python, and SQL form the core technology stack, with PostgreSQL leading database adoption.

- **Geographic Impact**: Location has a greater influence on developer compensation than years of experience, creating stark regional stratification in developer economics.

- **Developer Roles**: Full-stack developers represent the largest segment (~18,000), nearly doubling backend specialists (~10,000).

- **Job Satisfaction**: Remarkably consistent across industries and company sizes, with minimal correlation to compensation levels.

- **Cost of Living**: When adjusted for local costs, unexpected countries emerge as offering the best developer value, with Israel, Saudi Arabia, and Uruguay leading the affordability rankings.

## Visualizations

The analysis includes over 20 visualizations covering:

- Age and experience distributions
- Educational background frequency
- Top programming languages, frameworks, and databases
- Work arrangement preferences by age group
- Correlation matrix for key numeric variables
- Job satisfaction by company size and industry
- Regional comparison of experience and compensation
- Developer type distribution by country
- Compensation vs. cost of living analysis
- Affordability and purchasing power rankings
- Technology adoption intentions

## How to Run the Analysis

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/stack-overflow-analysis.git
   cd stack-overflow-analysis
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the Stack Overflow Survey 2024 data and place it in the `data/raw/` directory.

4. Run the Jupyter notebook:
   ```bash
   jupyter notebook notebooks/stack_overflow_eda.ipynb
   ```

5. Alternatively, run the analysis script:
   ```bash
   python src/main.py
   ```

## Data Processing Functions

The project includes several helper functions for data processing:

```python
# Example: Function to count items in semicolon-separated strings
def count_items(column_series):
    all_responses = column_series.dropna().str.split(';')
    flattened = [item.strip() for sublist in all_responses 
                for item in sublist if item.strip() != '']
    return Counter(flattened)

# Example: Function to explode a multi-response column 
def explode_column(df, column):
    temp_df = df[[column, 'Country']].dropna().copy()
    temp_df[column] = temp_df[column].str.split(';')
    return temp_df.explode(column).assign(
        **{column: lambda x: x[column].str.strip()})
```

## Contributing

Contributions to this analysis are welcome! Please feel free to submit a Pull Request or open an Issue for discussion.

To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-analysis`)
3. Commit your changes (`git commit -m 'Add some amazing analysis'`)
4. Push to the branch (`git push origin feature/amazing-analysis`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Stack Overflow for providing the annual developer survey data
- The global developer community for their participation in the survey
- Contributors to the pandas, matplotlib, and seaborn libraries that made this analysis possible