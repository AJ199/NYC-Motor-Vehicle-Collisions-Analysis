# NYC Motor Vehicle Collisions Analysis

This project analyzes motor vehicle collision data from New York City to uncover key patterns, trends, and geospatial insights that can inform safer road designs and policies.  
It was developed as part of the **Explorer Transportation Data Science Project (TDSP)**, hosted by the [Northeast Big Data Innovation Hub](https://nebigdatahub.org/about) and the [National Student Data Corps (NSDC)](https://nebigdatahub.org/nsdc).

---

## Project Overview

The project performs end-to-end data analysis on the **NYC Motor Vehicle Collisions** dataset.  
It includes data preprocessing, visualization, time-series trend analysis, and interactive mapping to understand crash behavior across boroughs, times of day, and locations.

---

## Objectives

- Clean and explore the NYC Open Data crash dataset  
- Identify the most common contributing factors and vehicle types involved in crashes  
- Analyze trends over time using time-series and decomposition  
- Visualize borough-wise crash frequency and severity  
- Create interactive maps for crash density and injury severity

---

## Tech Stack
Python, Pandas, Matplotlib, Seaborn, Folium, Statsmodels, NYC Open Data

---

## Key Analyses

1. **Contributing Factors** — Determines the top reasons for crashes such as distracted driving or unsafe speed.  
2. **Vehicle Involvement** — Identifies vehicle types most frequently involved in collisions.  
3. **Injury and Fatality Breakdown** — Analyzes pedestrian, cyclist, and motorist injury and death counts.  
4. **Time-Series Analysis** — Studies hourly and monthly crash trends, including COVID-19 impacts.  
5. **Geospatial Heatmaps** — Visualizes crash density and severity across New York City.  
6. **ZIP Code Analysis** — Highlights areas with the highest number of crashes.

---

## Visual Outputs

Crash Heatmap - `nyc_heatmap.html`
Severity Map - `severity_map.html`
Clustered Crash Map - `nyc_crash_map.html`

---

## References
- [NYC Open Data – Motor Vehicle Collisions](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)  
- [Northeast Big Data Innovation Hub](https://nebigdatahub.org/nsdc/tdsp)  
- [Pandas Documentation](https://pandas.pydata.org/docs)  
- [Folium Documentation](https://python-visualization.github.io/folium/)  
- [Statsmodels Time Series Guide](https://www.statsmodels.org/stable/tsa.html)

