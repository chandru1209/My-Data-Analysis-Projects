import pandas as pd

# Read the CSV file into the annual_data DataFrame
annual_data = pd.read_csv('yearly_data.csv')

# Create a new DataFrame member_data with rows where 'member_casual' is 'member'
member_data = annual_data[annual_data['member_casual'] == 'member'].copy()

# Save the member_data DataFrame to a new CSV file
member_data.to_csv('member_data.csv', index=False)
