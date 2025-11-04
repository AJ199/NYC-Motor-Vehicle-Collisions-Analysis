"""
Explorer Transportation Data Science Project
Author: Anurag Jindal

Project Overview:
This project analyzes NYC motor vehicle collision data to identify
patterns, contributing factors, and spatial trends in crashes.
The analysis includes data preprocessing, visualization, time series
analysis, and geospatial mapping.

Dataset:
NYC OpenData - Motor Vehicle Collisions: https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95

Libraries Used:
pandas, matplotlib, seaborn, folium, statsmodels
"""

# -------------------------------------------------------------------
# Import Libraries
# -------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap, MarkerCluster
from statsmodels.tsa.seasonal import seasonal_decompose

# -------------------------------------------------------------------
# Load Dataset
# -------------------------------------------------------------------

file_path = "Motor_Vehicle_Collisions_-_Crashes_20250127.csv"
data = pd.read_csv(file_path, low_memory=False)

print("Dataset loaded successfully.")
print("Number of records:", len(data))
print("Columns:", list(data.columns))

# -------------------------------------------------------------------
# Basic Data Overview
# -------------------------------------------------------------------

print("\nDataset Summary:")
print(data.describe())

# -------------------------------------------------------------------
# Missing Value Analysis
# -------------------------------------------------------------------

missing_values = data.isnull().sum()
missing_percentage = (missing_values / len(data)) * 100
missing_data = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentage': missing_percentage
}).sort_values(by='Percentage', ascending=False)

print("\nMissing Value Summary:")
print(missing_data.head(10))

# -------------------------------------------------------------------
# Contributing Factors Analysis
# -------------------------------------------------------------------

top_factors = data['CONTRIBUTING FACTOR VEHICLE 1'].value_counts().head(10)

plt.figure(figsize=(12, 7))
sns.barplot(x=top_factors.values, y=top_factors.index, palette="magma")
plt.title('Top 10 Contributing Factors to Crashes')
plt.xlabel('Number of Crashes')
plt.ylabel('Contributing Factor')
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# Vehicle Type Analysis
# -------------------------------------------------------------------

top_vehicle_types = data['VEHICLE TYPE CODE 1'].value_counts().head(10)

plt.figure(figsize=(12, 7))
sns.barplot(x=top_vehicle_types.values, y=top_vehicle_types.index, palette="cividis")
plt.title('Top 10 Vehicle Types Involved in Crashes')
plt.xlabel('Number of Crashes')
plt.ylabel('Vehicle Type')
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# Crash Type Analysis (Injuries & Fatalities)
# -------------------------------------------------------------------

types_of_crashes = {
    'Pedestrian Injuries': data['NUMBER OF PEDESTRIANS INJURED'].sum(),
    'Cyclist Injuries': data['NUMBER OF CYCLIST INJURED'].sum(),
    'Motorist Injuries': data['NUMBER OF MOTORIST INJURED'].sum(),
    'Pedestrian Deaths': data['NUMBER OF PEDESTRIANS KILLED'].sum(),
    'Cyclist Deaths': data['NUMBER OF CYCLIST KILLED'].sum(),
    'Motorist Deaths': data['NUMBER OF MOTORIST KILLED'].sum()
}

crash_types_df = pd.DataFrame(list(types_of_crashes.items()), columns=['Crash Type', 'Count'])

plt.figure(figsize=(12, 7))
sns.barplot(x='Count', y='Crash Type', data=crash_types_df, palette="mako")
plt.title('Types of Crashes and Their Frequencies')
plt.xlabel('Count')
plt.ylabel('Type of Crash')
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# Time Series Analysis - Crashes per Hour
# -------------------------------------------------------------------

data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'])
data['CRASH TIME'] = pd.to_datetime(data['CRASH TIME'], format='%H:%M', errors='coerce')
data['Hour of Day'] = data['CRASH TIME'].dt.hour

crashes_per_hour = data.groupby('Hour of Day').size()

plt.figure(figsize=(12, 6))
sns.barplot(x=crashes_per_hour.index, y=crashes_per_hour.values, color='steelblue')
plt.title('Average Number of Crashes per Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Crashes')
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# Monthly Crash Trend Analysis
# -------------------------------------------------------------------

monthly_crashes = data.groupby(data['CRASH DATE'].dt.to_period("M")).size()

plt.figure(figsize=(15, 7))
monthly_crashes.plot()
plt.title('Number of Crashes per Month')
plt.xlabel('Date')
plt.ylabel('Number of Crashes')
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# Daily Crash Trend and Decomposition
# -------------------------------------------------------------------

daily_crashes = data.groupby('CRASH DATE').size()
decomposition = seasonal_decompose(daily_crashes, model='additive', period=365)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
decomposition.trend.plot(ax=ax1)
ax1.set_title('Trend')
decomposition.seasonal.plot(ax=ax2)
ax2.set_title('Seasonality')
decomposition.resid.plot(ax=ax3)
ax3.set_title('Residuals')
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# Crashes by Borough
# -------------------------------------------------------------------

borough_count = data['BOROUGH'].value_counts()

plt.figure(figsize=(12, 7))
sns.barplot(x=borough_count.index, y=borough_count.values, palette="viridis")
plt.title('Distribution of Crashes by Borough')
plt.xlabel('Borough')
plt.ylabel('Number of Crashes')
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# Geospatial Heatmap of Crash Density
# -------------------------------------------------------------------

data_geo = data.dropna(subset=['LATITUDE', 'LONGITUDE'])
heat_data = [[row['LATITUDE'], row['LONGITUDE']] for _, row in data_geo.iterrows()]

m_heatmap = folium.Map(location=[40.730610, -73.935242], zoom_start=10)
HeatMap(heat_data, radius=8, max_zoom=13).add_to(m_heatmap)
m_heatmap.save("nyc_heatmap.html")

print("Geospatial heatmap saved as 'nyc_heatmap.html'.")

# -------------------------------------------------------------------
# Severity Mapping
# -------------------------------------------------------------------

sample_data = data_geo.sample(n=1000, random_state=42)
m_severity = folium.Map(location=[40.730610, -73.935242], zoom_start=10)

for _, row in sample_data.iterrows():
    if row['NUMBER OF PERSONS KILLED'] > 0:
        folium.features.RegularPolygonMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            number_of_sides=3,
            radius=5,
            color="red",
            fill=True,
            fill_color="red"
        ).add_to(m_severity)
    elif row['NUMBER OF PERSONS INJURED'] > 0:
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=5,
            color="orange",
            fill=True,
            fill_color="orange"
        ).add_to(m_severity)
    else:
        folium.features.RegularPolygonMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            number_of_sides=4,
            radius=5,
            color="green",
            fill=True,
            fill_color="green"
        ).add_to(m_severity)

m_severity.save("severity_map.html")
print("Severity map saved as 'severity_map.html'.")

# -------------------------------------------------------------------
# ZIP Code-Based Crash Analysis
# -------------------------------------------------------------------

zip_code_data = data.groupby('ZIP CODE').agg({
    'NUMBER OF PERSONS INJURED': 'sum',
    'NUMBER OF PERSONS KILLED': 'sum'
}).reset_index()

zip_code_data['CRASH_COUNT'] = (
    zip_code_data['NUMBER OF PERSONS INJURED'] + zip_code_data['NUMBER OF PERSONS KILLED']
)

plt.figure(figsize=(12, 8))
sns.barplot(
    data=zip_code_data.sort_values('CRASH_COUNT', ascending=False).head(10),
    x='ZIP CODE', y='CRASH_COUNT', palette='viridis'
)
plt.title('Top 10 ZIP Codes by Number of Crashes')
plt.xlabel('ZIP Code')
plt.ylabel('Number of Crashes')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# Interactive Map with Marker Clusters
# -------------------------------------------------------------------

data_filtered = data[['LATITUDE', 'LONGITUDE']].dropna()
sample_points = data_filtered.sample(n=5000, random_state=42)

m_cluster = folium.Map(location=[40.730610, -73.935242], zoom_start=10)
marker_cluster = MarkerCluster().add_to(m_cluster)

for _, row in sample_points.iterrows():
    folium.Marker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        popup=f"Lat: {row['LATITUDE']}, Lon: {row['LONGITUDE']}"
    ).add_to(marker_cluster)

m_cluster.save('nyc_crash_map.html')
print("Cluster map saved as 'nyc_crash_map.html'.")

# -------------------------------------------------------------------
# End of Project
# -------------------------------------------------------------------

print("\nAnalysis complete. Generated visualizations and maps are saved as:")
print("- nyc_heatmap.html")
print("- severity_map.html")
print("- nyc_crash_map.html")
