import pandas as pd

# Load the 'casual_data_cleaned_02.csv' file into a DataFrame
visualize_02 = pd.read_csv('casual_data_cleaned_02.csv')

# Round latitude and longitude to two decimals
visualize_02['start_lat'] = visualize_02['start_lat'].round(2)
visualize_02['start_lng'] = visualize_02['start_lng'].round(2)
visualize_02['end_lat'] = visualize_02['end_lat'].round(2)
visualize_02['end_lng'] = visualize_02['end_lng'].round(2)

# Create 'start_coordinate' and 'start_frequency' columns
visualize_02['start_coordinate'] = list(zip(visualize_02['start_lat'], visualize_02['start_lng']))
start_frequency = visualize_02.groupby('start_coordinate').size().reset_index(name='start_frequency')
visualize_02 = pd.merge(visualize_02, start_frequency, on='start_coordinate', how='left')
unique_visualize_02 = visualize_02[~visualize_02.duplicated(subset='start_frequency', keep='first')]
unique_visualize_02 = unique_visualize_02.drop(['start_coordinate', 'end_lng', 'end_lat'], axis=1)
unique_visualize_02.to_csv('casual_data_coordinates_01.csv', index=False)

# Create 'end_coordinate' and 'end_frequency' columns
visualize_02['end_coordinate'] = list(zip(visualize_02['end_lat'], visualize_02['end_lng']))
end_frequency = visualize_02.groupby('end_coordinate').size().reset_index(name='end_frequency')
visualize_02 = pd.merge(visualize_02, end_frequency, on='end_coordinate', how='left')
unique_visualize_02 = visualize_02[~visualize_02.duplicated(subset='end_frequency', keep='first')]
unique_visualize_02 = unique_visualize_02.drop(['end_coordinate', 'start_lat', 'start_lng'], axis=1)
unique_visualize_02.to_csv('casual_data_coordinates_02.csv', index=False)
