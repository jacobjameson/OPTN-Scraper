# OPTN Kidney Transplant Data Scraper

This repository contains a Python script that automatically scrapes kidney transplant data from the Organ Procurement and Transplantation Network (OPTN) website. The script is set up to run weekly via GitHub Actions, ensuring that the data is always up-to-date.

Data is sourced from the [OPTN website](https://optn.transplant.hrsa.gov/data/view-data-reports/state-data/).

The data was last collected: 2024-06-21 16:11:22

## Overview

The scraper collects data on various donor types for kidney transplants across all U.S. states. The data is saved in Parquet format, which provides efficient storage and fast query performance.

### Data Collection

The script collects data for the following donor types:

- All Donors by Donor Type
- Deceased Donors by Donor Age
- Deceased Donors by Donor Ethnicity
- Deceased Donors by Donor Gender
- Deceased Donors by Circumstance of Death
- Deceased Donors by Mechanism of Death
- Deceased Donors by Cause of Death
- Deceased Donors by DSA
- Living Donors by Donor Age
- Living Donors by Donor Ethnicity
- Living Donors by Donor Gender

Data is collected for each state and combined into a single dataset for each donor type.

### Data Storage

The scraped data is saved in the `data/kidney/` directory.

## Accessing the Data

The data is stored in Parquet format, which can be easily read by various data analysis tools. Here are examples of how to read the data in Python and R:

### Python

To read the data in Python, you can use the `pandas` library:

```python
import pandas as pd

# Read the parquet file
df = pd.read_parquet('data/kidney/All_Donors_by_Donor_Type.parquet')

# Display the first few rows
print(df.head())

# Get basic information about the dataset
print(df.info())
```

### R

To read the data in R, you can use the arrow package:

```R
library(arrow)
library(dplyr)

# Read the parquet file
df <- read_parquet('data/kidney/All_Donors_by_Donor_Type.parquet')

# Display the first few rows
head(df)

# Get basic information about the dataset
glimpse(df)
```

### Automated Updates

This repository is set up with GitHub Actions to run the scraper automatically once a week. The workflow file (.github/workflows/weekly_scraper.yml) defines this automation.
Each time the scraper runs successfully, it updates the data files and commits the changes to the repository. The README is also updated with the latest data collection date.


### Citation

If you use this data in your research, please cite it as:

```
Jameson, J. (2024). OPTN-Scraper (Version X.X.X) [Computer software]. https://doi.org/10.5281/zenodo.XXXXXXX
```


### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Contact

If you have any questions or feedback, please open an issue on this GitHub repository.



