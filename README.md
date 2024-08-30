# Spotify-Million-Playlist-Dataset-Analysis-and-Visualization

Here's a brief written report summarizing your findings and design choices for your Spotify analysis project.

---

# Project Report: Spotify Playlist Analysis

## Overview
This project aims to analyze a dataset from Spotify containing playlists and their associated tracks. The dataset consists of 250,000 playlists and 16,596,692 tracks, which were processed using PySpark for data cleaning and analysis, followed by visualization in a Streamlit dashboard.

## Data Preparation
1. **Data Loading**: 
   - Utilized PySpark to load JSON files from the Spotify dataset. This approach allows efficient handling of large datasets.
   - Exploded nested arrays (playlists and tracks) to create a flat structure for easier analysis.

2. **Data Cleaning**:
   - Filtered out any unnecessary or corrupted data entries.
   - Ensured consistent data types across columns for seamless processing and analysis.

3. **Data Conversion**:
   - Converted Spark DataFrames to Pandas DataFrames to leverage Pandas' robust visualization capabilities.
   - Used libraries like Matplotlib and Seaborn for data visualization, allowing for effective representation of trends and insights.

## Visualization and Dashboard
- Developed a Streamlit dashboard to present the analysis results interactively.
- Key visualizations include:
  - Distribution of tracks per playlist.
  - Trends in playlist characteristics over time (e.g., number of followers, number of tracks).
  - Insights into artist contributions and collaborations within playlists.

## Tools and Technologies
- **PySpark**: For scalable data processing and manipulation.
- **Pandas**: For data analysis and visualization.
- **Streamlit**: To create a user-friendly interface for presenting the analysis results.
- **Colab and Kaggle**: Used for running notebooks and managing datasets effectively.

## Findings
- The dataset reveals interesting trends in playlist composition, including the average number of tracks, the diversity of artists, and the collaborative nature of playlists.
- Insights generated from the visualizations can inform content creators and marketers about popular trends in music consumption.
