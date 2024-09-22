
# Project Report: Spotify Playlist Analysis

## Overview
This project aims to analyze a dataset from Spotify containing playlists and their associated tracks. The dataset consists of 250,000 playlists and 16,596,692 tracks, which were processed using PySpark for data cleaning and analysis, followed by visualization in a Streamlit dashboard.

### Summary of Datasets

1. **Spotify Million Playlist Dataset**  
   - **Link**: [Spotify Million Playlist Dataset](https://www.kaggle.com/datasets/himanshuwagh/spotify-million)
   - **Description**: This dataset contains millions of playlists from Spotify, including details like track names, artist names, and playlist metadata. It's suitable for analyzing music trends and user preferences.

2. **Cleaned Spotify Data for Dashboard**  
   - **Link**: [Cleaned Spotify Data](https://www.kaggle.com/datasets/esraaabdelrazek/spotify-data)
   - **Description**: This dataset is a refined subset of the original Spotify Million Playlist dataset. It has been cleaned and structured for easier analysis and visualization. It is used for creating interactive visualizations in the Streamlit dashboard.

### Usage in Project
- The first dataset was used to extract a manageable subset for analysis, focusing on 250,000 playlists and 16,596,692 tracks.
- The cleaned data was then utilized to create a Streamlit dashboard, showcasing visual insights derived from the dataset.


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
    ![image](https://github.com/user-attachments/assets/9e829f42-7286-4852-a4d5-9b4daa7ffce5)
    
    ![image](https://github.com/user-attachments/assets/787efabc-72ae-43a8-9be0-d7f9800044f4)
    
    ![image](https://github.com/user-attachments/assets/51ea1dbd-10cf-44a7-bda7-904ab1177d4a)

    ![image](https://github.com/user-attachments/assets/7ddc7e4f-a4b7-4463-8eb7-f663c0423112)
    
    ![image](https://github.com/user-attachments/assets/ce01d2f6-2f34-4639-a967-5f55d3b3d67e)




## Tools and Technologies
- **PySpark**: For scalable data processing and manipulation.
- **Pandas**: For data analysis and visualization.
- **Streamlit**: To create a user-friendly interface for presenting the analysis results.
- **Colab and Kaggle**: Used for running notebooks and managing datasets effectively.

## Findings
- The dataset reveals interesting trends in playlist composition, including the average number of tracks, the diversity of artists, and the collaborative nature of playlists.
- Insights generated from the visualizations can inform content creators and marketers about popular trends in music consumption.
