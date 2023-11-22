import pandas as pd

# loading the file
casual_data = pd.read_csv("casual_data.csv")

# getting to know columns
column_names = casual_data.columns
print(column_names)

print(casual_data.head(10))
print(casual_data.describe())

# List of columns to drop
columns_to_drop = ['start_lat', 'start_lng', 'end_lat', 'end_lng', 'member_casual']

# Drop the specified columns
casual_data_cleaned = casual_data.drop(columns=columns_to_drop)

# Convert 'started_at' and 'ended_at' columns to datetime
casual_data_cleaned['started_at'] = pd.to_datetime(casual_data_cleaned['started_at'])
casual_data_cleaned['ended_at'] = pd.to_datetime(casual_data_cleaned['ended_at'])

# Create a new column 'ride_duration' by subtracting 'started_at' from 'ended_at'
casual_data_cleaned['ride_duration'] = (casual_data_cleaned['ended_at'] -
                                        casual_data_cleaned['started_at']).dt.total_seconds()


member_data_cleaned = casual_data_cleaned[(casual_data_cleaned['ride_duration'] > 0)
                                          & (casual_data_cleaned['ride_duration'] <= 3600)]

member_data_cleaned.to_csv("casual_data_cleaned.csv", index=False)

print('end')
