# 2024 Global Developer Landscape Analysis

## Project Overview

This project analyzes the Stack Overflow Developer Survey 2024 data to provide comprehensive insights into the global developer ecosystem. The analysis covers demographics, work preferences, compensation patterns, technology adoption, and geographic influences on the software development profession.

## Table of Contents

- [Project Overview](#project-overview)
- [Data Sources](#data-sources)
- [Key Findings](#key-findings)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Methodology](#methodology)
- [Visualizations](#visualizations)
- [Key Documents](#key-documents)
- [Contributing](#contributing)
- [Contact](#contact)
- [License](#license)

## Data Sources

The analysis uses two primary data sources:
1. **Stack Overflow Annual Developer Survey 2024** - Responses from developers worldwide
2. **Cost of Living Index by Country 2024** - Supplementary data for economic analysis

## Key Findings

1. **Workforce Demographics**: The profession is dominated by the 25-34 age group (37%), with 82% of developers under 45.

2. **Work Arrangements**: Hybrid work (42%) and remote work (38%) dominate, with in-person arrangements (20%) now a minority. Remote work preference increases with age.

3. **Technology Ecosystem**: JavaScript, Python, HTML/CSS, and SQL form the core technology stack, with PostgreSQL leading database adoption.

4. **Regional Variations**: Location significantly impacts developer compensation, with similar experience levels commanding vastly different salaries by region.

5. **Career Economics**: When adjusted for cost of living, countries like Israel, Romania, and Eastern European nations offer excellent compensation value for developers.

6. **Professional Roles**: Full-stack developers represent the largest segment globally (30.7%), with backend specialists as the second largest group (16.7%).

7. **Learning Patterns**: Self-directed learning dominates (20.2%), with formal education increasingly supplemental rather than central to developer training.

8. **Satisfaction Paradox**: Higher compensation doesn't correlate strongly with job satisfaction (r=0.05), with smaller organizations consistently reporting higher satisfaction despite lower pay.

## Project Structure

```
/
├── data/
│   ├── cleaned/          # Processed datasets
│   └── raw/              # Original survey data
├── figures/              # Generated visualizations
├── notebook/
│   └── stack_overflow_analysis.ipynb  # Main analysis notebook
├── .gitignore
├── developer_landscape.md    # Comprehensive report
├── README.md                 # This file
└── story.md                  # Summary of key findings
```

## Installation and Setup

### Requirements

```
Python 3.8+
pandas==1.5.3
numpy==1.24.3
matplotlib==3.7.1
seaborn==0.12.2
```

### Using Conda
```bash
# Create and activate conda environment
conda create -n devsurvey python=3.8
conda activate devsurvey

# Install required packages
conda install pandas=1.5.3 numpy=1.24.3 matplotlib=3.7.1 seaborn=0.12.2
conda install jupyter notebook
```

### Using Python venv
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Running the Analysis
```bash
# Navigate to the notebook directory
cd notebook

# Launch Jupyter Notebook
jupyter notebook stack_overflow_analysis.ipynb
```

## Methodology

The analysis followed a structured approach:
1. **Data Cleaning & Preparation**: Handling missing values and standardizing formats
2. **Exploratory Data Analysis**: Statistical analysis of key variables
3. **Geographic Integration**: Merging survey data with cost of living information
4. **Visualization**: Creating comprehensive charts to highlight patterns
5. **Insight Development**: Synthesizing findings into recommendations

## Visualizations

Key visualizations include:
- Remote work preferences by country
- Developer role distribution
- Compensation by company size
- Job satisfaction by industry
- Programming language adoption rates
- Experience distribution by country
- Affordability and purchasing power maps

## Key Documents

- [Main Analysis Notebook](notebook/stack_overflow_analysis.ipynb) - Complete exploratory data analysis of the developer survey
- [Full Report](./report//story.md) - Narrative summary of key findings and insights

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact
[![LinkedIn](https://img.shields.io/badge/Connect_Professional_Network-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/yourprofile)  
[![Email](https://img.shields.io/badge/Request_Custom_Analysis-4285F4?style=flat&logo=gmail)](mailto:analysis@example.com)
