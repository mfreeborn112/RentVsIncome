# Step 1: Import necessary libraries
import requests
import pandas as pd

# Step 2: Define API details and initialize data structures
endpoint = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
start_year = "2000"
end_year = "2022"
api_key = [YOUR API KEY]
series_ids = ["CUUR0000SA0", "CUUR0100SA0", "CUUR0200SA0", "CUUR0300SA0", "CUUR0400SA0"]
df = pd.DataFrame(columns=["Region", "Year", "CPI"])

# Step 3: Make API calls and collect data
for series_id in series_ids:
    url = f"{endpoint}{series_id}?startyear={start_year}&endyear={end_year}&registrationkey={api_key}"
    response = requests.get(url)
    data = response.json()

    # Extract and append the CPI data to the DataFrame
    for series in data['Results']['series']:
        region = series['seriesID']
        for item in series['data']:
            year = item['year']
            value = item['value']
            df = df.append({"Region": region, "Year": year, "CPI": value}, ignore_index=True)

# Step 4: Process and transform the data

# 4.1 Map out the Region ID with the real name
region_map = {
    'CUUR0000SA0': 'U.S. City Average',
    'CUUR0100SA0': 'Northeast',
    'CUUR0200SA0': 'Midwest',
    'CUUR0300SA0': 'South',
    'CUUR0400SA0': 'West'
}
df['Region'] = df['Region'].replace(region_map)

# 4.2 Filter the data and calculate the percent increase
min_2000 = df[df['Year'] == '2000'].groupby('Region')['CPI'].min().reset_index()
max_2019 = df[df['Year'] == '2019'].groupby('Region')['CPI'].max().reset_index()
merged = pd.merge(min_2000, max_2019, on='Region', how='inner', suffixes=('_2000', '_2019'))
final_df = merged.rename(columns={'CPI_2000': 'Min CPI 2000', 'CPI_2019': 'Max CPI 2019'})

# Drop the "U.S. City Average" row, convert the CPIs to floating data types and calculate percent increase
final_df = final_df[final_df['Region'] != 'U.S. City Average']
final_df['Max CPI 2019'] = final_df['Max CPI 2019'].astype(float)
final_df['Min CPI 2000'] = final_df['Min CPI 2000'].astype(float)
final_df['Percent Increase'] = ((final_df['Max CPI 2019'] - final_df['Min CPI 2000']) / final_df['Min CPI 2000']) * 100
final_df = final_df[['Region', 'Percent Increase']].reset_index(drop=True)

# Further transformations
final_df['Percent Increase'] = (final_df['Percent Increase'] / 100) + 1
final_df['Percent Increase'] = final_df['Percent Increase'].round(3)

# Step 5: Map states to regions and export to CSV

# 5.1 Define the state-region mapping
state_region_mapping = {
    'AL': 'South',
    'AK': 'West',
    'AZ': 'West',
    'AR': 'South',
    'CA': 'West',
    'CO': 'West',
    'CT': 'Northeast',
    'DE': 'Northeast',
    'FL': 'South',
    'GA': 'South',
    'HI': 'West',
    'ID': 'West',
    'IL': 'Midwest',
    'IN': 'Midwest',
    'IA': 'Midwest',
    'KS': 'Midwest',
    'KY': 'South',
    'LA': 'South',
    'ME': 'Northeast',
    'MD': 'Northeast',
    'MA': 'Northeast',
    'MI': 'Midwest',
    'MN': 'Midwest',
    'MS': 'South',
    'MO': 'Midwest',
    'MT': 'West',
    'NE': 'Midwest',
    'NV': 'West',
    'NH': 'Northeast',
    'NJ': 'Northeast',
    'NM': 'West',
    'NY': 'Northeast',
    'NC': 'South',
    'ND': 'Midwest',
    'OH': 'Midwest',
    'OK': 'South',
    'OR': 'West',
    'PA': 'Northeast',
    'RI': 'Northeast',
    'SC': 'South',
    'SD': 'Midwest',
    'TN': 'South',
    'TX': 'South',
    'UT': 'West',
    'VT': 'Northeast',
    'VA': 'South',
    'WA': 'West',
    'WV': 'South',
    'WI': 'Midwest',
    'WY': 'West',
    'DC': 'Northeast'
}
# 5.2 Create a DataFrame from the mapping and merge with final_df
states_df = pd.DataFrame(list(state_region_mapping.items()), columns=['State', 'Region'])
result_df = pd.merge(states_df, final_df, left_on='Region', right_on='Region', how='left')

# 5.3 Export to CSV
result_df.to_csv('states_cpi.csv', index=False)
