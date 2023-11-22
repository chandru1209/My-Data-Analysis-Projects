import pandas as pd

# loading the file
member_data = pd.read_csv("casual_data.csv")

# getting to know columns
column_names = member_data.columns
print(column_names)

print(member_data.head(10))
print(member_data.describe())

# List of columns to drop
columns_to_drop = ['member_casual']

# Drop the specified columns
casual_data_cleaned = member_data.drop(columns=columns_to_drop)

# Convert 'started_at' and 'ended_at' columns to datetime
casual_data_cleaned['started_at'] = pd.to_datetime(casual_data_cleaned['started_at'])
casual_data_cleaned['ended_at'] = pd.to_datetime(casual_data_cleaned['ended_at'])

# Create a new column 'ride_duration' by subtracting 'started_at' from 'ended_at'
casual_data_cleaned['ride_duration'] = (casual_data_cleaned['ended_at'] -
                                        casual_data_cleaned['started_at']).dt.total_seconds()

casual_data_cleaned = casual_data_cleaned[(casual_data_cleaned['ride_duration'] > 0)
                                          & (casual_data_cleaned['ride_duration'] <= 3600)]

columns_to_drop_02 = ['ended_at']

casual_data_cleaned_02 = casual_data_cleaned.drop(columns=columns_to_drop_02)

casual_cleaned_data_2 = casual_data_cleaned_02.dropna()

casual_data_cleaned_02.to_csv('casual_data_cleaned_02.csv', index=False)
