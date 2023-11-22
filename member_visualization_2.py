import pandas as pd

# Load the 'member_data_cleaned_02.csv' file into a DataFrame
visualize_02 = pd.read_csv('member_data_cleaned_02.csv')

# Round latitude and longitude to two decimals
visualize_02['start_lat'] = visualize_02['start_lat'].round(2)
visualize_02['start_lng'] = visualize_02['start_lng'].round(2)
visualize_02['end_lat'] = visualize_02['end_lat'].round(2)
visualize_02['end_lng'] = visualize_02['end_lng'].round(2)


# Create 'start_coordinate' and 'end_coordinate' columns
visualize_02['start_coordinate'] = list(zip(visualize_02['start_lat'], visualize_02['start_lng']))

# Create 'Start_frequency' column
start_frequency = visualize_02.groupby('start_coordinate').size().reset_index(name='start_frequency')

# Merge frequencies back into the main DataFrame
visualize_02 = pd.merge(visualize_02, start_frequency, on='start_coordinate', how='left')

# Keep only rows where 'Start_frequency' is unique
unique_visualize_02 = visualize_02[~visualize_02.duplicated(subset='start_frequency', keep='first')]

# Drop the 'start_coordinate' column
unique_visualize_02 = unique_visualize_02.drop(['start_coordinate', 'end_lng', 'end_lat'], axis=1)

# Save the resulting DataFrame
unique_visualize_02.to_csv('data_coordinates_01.csv', index=False)


# Create 'start_coordinate' and 'end_coordinate' columns
visualize_02['end_coordinate'] = list(zip(visualize_02['end_lat'], visualize_02['end_lng']))

# Create 'Start_frequency' column
start_frequency = visualize_02.groupby('end_coordinate').size().reset_index(name='end_frequency')

# Merge frequencies back into the main DataFrame
visualize_02 = pd.merge(visualize_02, start_frequency, on='end_coordinate', how='left')

# Keep only rows where 'Start_frequency' is unique
unique_visualize_02 = visualize_02[~visualize_02.duplicated(subset='end_frequency', keep='first')]

# Drop the 'start_coordinate' column
unique_visualize_02 = unique_visualize_02.drop(['start_coordinate', 'start_lat', 'start_lng'], axis=1)

# Save the resulting DataFrame
unique_visualize_02.to_csv('data_coordinates_02.csv', index=False)