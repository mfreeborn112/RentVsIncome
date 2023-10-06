# Rent vs. Income Dataset (2000 & 2020) with CPI Adjustments

## Description
This project generates a dataset comparing rent prices with income for the years 2000 and 2020 across most US counties. Additionally, a Consumer Price Index (CPI) dataset is provided to adjust for inflation. The resultant datasets are useful for analysis in tools like Tableau to assess the changing dynamics of rent against income, while accounting for inflation.

## Getting Started

### Prerequisites
- You will need to obtain API keys for the following services:
  * [BEA (Bureau of Economic Analysis) API](https://apps.bea.gov/API/signup/index.cfm)
  * [BLS (Bureau of Labor Statistics) API](https://www.bls.gov/developers/home.htm)
  
- Ensure you have the following Python libraries installed:
pip install pandas requests lxml


### Files Included
- **FMR_All_1983_2024.csv**: A CSV file containing Fair Market Rents from 1983 to 2024. This file is available in the repository.

### Setting Up
1. Clone the repository to your local machine.
2. Replace the placeholders in the scripts with your obtained API keys.
3. Run the script to generate the desired datasets.

## Running the Script
1. To create the rent vs. income dataset:
   - python rentvsincome.py

2. To create the CPI dataset:
   - python cpi.py


## Using the Datasets
- Once the datasets are generated, you can load them into Tableau.
- Join the datasets using "State" as the link.
- Analyze the rent vs. income dynamics between 2000 to 2020, and adjust for inflation using the CPI data.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
