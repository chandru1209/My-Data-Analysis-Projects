import folium
from folium import Popup
from folium.plugins import MarkerCluster
import pandas as pd

# Load the saved DataFrames
casual_data_coordinates_01 = pd.read_csv('casual_data_coordinates_01.csv')
casual_data_coordinates_02 = pd.read_csv('casual_data_coordinates_02.csv')

# Combine the DataFrames
casual_combined_df = pd.concat([casual_data_coordinates_01, casual_data_coordinates_02], ignore_index=True)

# Drop rows with NaN values for start coordinates
casual_start_df = casual_combined_df.dropna(subset=['start_lat', 'start_lng', 'start_frequency'])

# Normalize the frequency values for start coordinates
casual_start_df = casual_start_df.copy()
casual_start_df['normalized_start_frequency'] = (
        casual_start_df['start_frequency'] - casual_start_df['start_frequency'].min()) / (
        casual_start_df['start_frequency'].max() - casual_start_df['start_frequency'].min())

# Drop rows with NaN values for end coordinates
casual_end_df = casual_combined_df.dropna(subset=['end_lat', 'end_lng', 'end_frequency'])

casual_end_df = casual_end_df.copy()
casual_end_df['normalized_end_frequency'] = (
        casual_end_df['end_frequency'] - casual_end_df['end_frequency'].min()) / (
        casual_end_df['end_frequency'].max() - casual_end_df['end_frequency'].min())

# Create clustering columns for start and end
casual_start_df['start_cluster'] = casual_start_df.groupby(['start_lat', 'start_lng']).ngroup()
casual_end_df['end_cluster'] = casual_end_df.groupby(['end_lat', 'end_lng']).ngroup()

# Calculate combined frequency for each start cluster
casual_start_combined_df = casual_start_df.groupby('start_cluster').agg({
    'start_lat': 'mean',
    'start_lng': 'mean',
    'start_frequency': 'sum',
    'normalized_start_frequency': 'mean'
}).reset_index()

# Calculate combined frequency for each end cluster
casual_end_combined_df = casual_end_df.groupby('end_cluster').agg({
    'end_lat': 'mean',
    'end_lng': 'mean',
    'end_frequency': 'sum',
    'normalized_end_frequency': 'mean'
}).reset_index()

# Combine start and end clusters
casual_combined_clusters_df = pd.concat([casual_start_combined_df, casual_end_combined_df], ignore_index=True)
casual_combined_clusters_df = casual_combined_clusters_df.dropna(subset=['start_lat', 'start_lng'])

# Create a map centered around the mean of start coordinates
casual_combined_map = folium.Map(
    location=[casual_combined_df[['start_lat', 'end_lat']].mean().mean(),
              casual_combined_df[['start_lng', 'end_lng']].mean().mean()],
    zoom_start=12)

# Create a MarkerCluster layer for combined clusters
casual_combined_marker_cluster = MarkerCluster(control=False).add_to(casual_combined_map)

# Iterate over unique combined clusters and create circles
for index, row in casual_combined_clusters_df.iterrows():
    cluster_location = [row['start_lat'], row['start_lng']]
    casual_combined_frequency = row['start_frequency'] if 'start_frequency' in row else 0
    casual_combined_frequency += row['end_frequency'] if 'end_frequency' in row else 0

    casual_normalized_frequency = (
            casual_combined_frequency - casual_combined_df['start_frequency'].min()) / (
                                        casual_combined_df['start_frequency'].max() - casual_combined_df[
                                    'start_frequency'].min())

    radius = 50 + (casual_normalized_frequency * 50)
    folium.CircleMarker(location=cluster_location,
                        radius=radius,
                        color='purple',
                        fill=True,
                        fill_color='purple',
                        fill_opacity=0.6,
                        popup=Popup(f"Casual Combined Frequency: {casual_combined_frequency:.2f}")).add_to(
        casual_combined_marker_cluster)

# Add LayerControl to the map
folium.LayerControl().add_to(casual_combined_map)

# Save the casual combined map as an HTML file
casual_combined_map.save('casual_combined_normalized_cluster_plot.html')
