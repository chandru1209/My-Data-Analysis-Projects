import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from calendar import day_name, month_name

# Load the 'casual_data_cleaned.csv' file into a DataFrame
casual_cleaned_data_1 = pd.read_csv('casual_data_cleaned.csv')

# Convert 'started_at' to datetime format
casual_cleaned_data_1['started_at'] = pd.to_datetime(casual_cleaned_data_1['started_at'])

# Create a new column for the day of the week
casual_cleaned_data_1['day_of_week'] = casual_cleaned_data_1['started_at'].dt.day_name()

# Convert 'ride_duration' to integers
casual_cleaned_data_1['ride_duration'] = casual_cleaned_data_1['ride_duration'].astype(int)

# Custom function to map period labels to month names
def map_period_to_month(period_label):
    year, month = map(int, str(period_label).split('-'))
    return f"{month_name[month]} {year}"

# Convert the Period object to a string for the 'month' column with custom mapping
casual_cleaned_data_1['month'] = casual_cleaned_data_1['started_at'].dt.to_period('M').apply(map_period_to_month)

# Sort months and days in ascending order
months_order = sorted(casual_cleaned_data_1['month'].unique(),
                      key=lambda x: (int(x.split()[1]), list(month_name).index(x.split()[0]) + 1))
days_order = [day_name[i] for i in range(7)]  # Use a list comprehension to get day names in order

# Monthly usage by ride type using Plotly
monthly_usage = casual_cleaned_data_1.groupby(['month', 'rideable_type']).size().reset_index(name='Count')
fig_monthly = px.bar(monthly_usage, x='month', y='Count', color='rideable_type', barmode='stack',
                     category_orders={'month': months_order},
                     color_discrete_map={'electric_bike': 'skyblue', 'classic_bike': 'coral', 'docked_bike': 'gray'})
fig_monthly.update_layout(title='Monthly Usage by Ride Type')

# Rotate month names to 45 degrees
fig_monthly.update_xaxes(tickangle=45)

fig_monthly.write_html('casual_monthly_usage_by_ride_type.html')

# Day-wise usage by ride type using Plotly
daily_usage = casual_cleaned_data_1.groupby(['day_of_week', 'rideable_type']).size().reset_index(name='Count')
fig_daily = px.bar(daily_usage, x='day_of_week', y='Count', color='rideable_type', barmode='stack',
                   category_orders={'day_of_week': days_order},
                   color_discrete_map={'electric_bike': 'skyblue', 'classic_bike': 'coral', 'docked_bike': 'gray'})
fig_daily.update_layout(title='Day-wise Usage by Ride Type')

# Rotate day names to 45 degrees
fig_daily.update_xaxes(tickangle=45)

fig_daily.write_html('casual_daily_usage_by_ride_type.html')

# Convert 'ride_duration' to integers
casual_cleaned_data_1['ride_duration'] = casual_cleaned_data_1['ride_duration'].astype(int)

# Create bins for ride duration in ascending order
ride_duration_bins = pd.cut(casual_cleaned_data_1['ride_duration'],
                            bins=range(0, casual_cleaned_data_1['ride_duration'].max() + 360, 360),
                            ordered=True)

# Extract lower bound of each bin and convert to string
casual_cleaned_data_1['ride_duration_bins'] = ride_duration_bins.apply(lambda x: f"{x.left}-{x.right}")

# Order ride duration bins in ascending order
ride_duration_bins_order = sorted(casual_cleaned_data_1['ride_duration_bins'].unique(),
                                  key=lambda x: int(x.split('-')[0]))

# Ride duration and ride type relationship (bar plot) using Matplotlib with Bins on X-axis
plt.figure(figsize=(14, 6))
color_map = {'electric_bike': 'skyblue', 'classic_bike': 'coral', 'docked_bike': 'gray'}
for rideable_type, group in casual_cleaned_data_1.groupby('rideable_type'):
    ride_duration_counts = group['ride_duration_bins'].value_counts().sort_index()
    plt.bar(ride_duration_bins_order, ride_duration_counts, label=rideable_type, alpha=0.7,
            color=color_map[rideable_type])

plt.title('Casual Ride Duration Frequency by Rideable Type')
plt.xlabel('Ride Duration Bins')
plt.ylabel('Frequency')

# Rotate ride duration bins to 45 degrees
plt.xticks(rotation=45, ha='right')

plt.legend(title='Rideable Type')
plt.savefig('casual_ride_duration_frequency_by_rideable_type.png')  # Save the bar plot as an image
plt.show()
