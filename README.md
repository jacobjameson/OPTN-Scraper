# OPTN Data Scraper

This repository contains a Python script to scrape organ transplant data from the OPTN website and store the results in a CSV file. The script is set to run automatically every day using GitHub Actions.

## How to Use

1. Clone the repository.
2. Install the required dependencies:

```
pip install -r requirements.txt
```
3. Run the scraper manually:

```
python scraper.py
```


The results will be saved in `state_transplant_data_combined.csv`.

## Automated Updates

The scraper runs automatically every day at midnight (UTC) and updates the CSV file in the repository. 

**Last Updated:** `LAST_UPDATED_PLACEHOLDER`

## Data Sources

Data is sourced from the [OPTN website](https://optn.transplant.hrsa.gov/data/view-data-reports/state-data/).

