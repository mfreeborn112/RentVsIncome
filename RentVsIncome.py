# Import necessary libraries
import pandas as pd
import requests
from lxml import etree

# Constants
drop_states = ['AS', 'AK', 'HI', 'VI', 'PR', 'ME', 'MA', 'NH', 'VT', 'CT', 'RI']

# --- Loading and Prepping the FMR Data ---
df = pd.read_csv('FMR_All_1983_2024.csv', encoding='latin1')
df = df[['name', 'fmr20_1', 'fmr00_1', 'pmsaname', 'pop2017']]
df.rename(columns={'name': 'County', 'pop2017': 'Population', 'pmsaname': 'State'}, inplace=True)
df['State'] = df['State'].str.extract(', (\w\w)', expand=False)
df = df[~df['State'].isin(drop_states)]
df.dropna(inplace=True)
df = df[df['County'].str.endswith(('County', 'Parish'))]
df['County'] = df['County'].str.replace(r' (County|Parish)$', '')
fmr_df = df.melt(id_vars=['County', 'State', 'Population'], 
                 value_vars=['fmr20_1', 'fmr00_1'], 
                 var_name='Year', 
                 value_name='Rent')
fmr_df['Year'] = fmr_df['Year'].replace({'fmr20_1': '2020', 'fmr00_1': '2000'})
fmr_df['Rent'] = fmr_df['Rent'].astype(int)
fmr_df.loc[fmr_df['State'] == 'DC', 'State'] = 'VA'
fmr_df['County State'] = fmr_df['County'] + ', ' + fmr_df['State']

# --- Loading and Prepping the Income Data ---
url = "https://apps.bea.gov/api/data/"
params = {
    'UserID': [Your User ID],
    'method': 'GetData',
    'datasetname': 'Regional',
    'TableName': 'CAINC1',
    'LineCode': '3',
    'GeoFIPS': 'COUNTY',
    'ResultFormat': 'XML'
}
data_list = []
for year in [2000, 2020]:
    params['Year'] = str(year)
    response = requests.get(url, params=params)
    root = etree.fromstring(response.content)
    for data in root.xpath("//Data"):
        data_list.append([year, data.get('GeoName'), data.get('DataValue')])
income_df = pd.DataFrame(data_list, columns=['Year', 'County State', 'Income'])
income_df['County State'] = income_df['County State'].str.replace('*', '', regex=False)
income_df = income_df[~income_df['County State'].str.endswith(tuple(drop_states))]
income_df = income_df[~income_df['County State'].str.contains('Independent City')]

# --- Combining Data and Saving as CSV ---
fmr_df['Year'] = fmr_df['Year'].astype(str)
income_df['Year'] = income_df['Year'].astype(str)
merged_df = pd.merge(fmr_df, income_df, on=['County State', 'Year'], how='left')
merged_df_cleaned = merged_df.dropna()
merged_df_cleaned.to_csv('RentVsIncome.csv', index=False)
