import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, when, count, row_number
from pyspark.sql.window import Window

# Initialize Spark session
spark = SparkSession.builder \
    .appName("SpotifyMillionPlaylistDataset") \
    .getOrCreate()

# Load data
playlist = spark.read.parquet("playlist.parquet")
tracks = spark.read.parquet("tracks.parquet")

# Streamlit application
st.title('Spotify Playlist Dashboard')

# Sidebar for user input
st.sidebar.header("User Input")

# Step 1: Top Playlists
num_playlists = st.sidebar.slider('Select number of top playlists to display:', min_value=1, max_value=35, value=10)

# Top Playlists Visualization
st.header('Top Playlists by Number of Followers')
top_playlists = playlist.groupBy("playlist_name") \
    .agg({"num_followers": "max"}) \
    .orderBy(col("max(num_followers)").desc()) \
    .limit(num_playlists) \
    .toPandas()

plt.figure(figsize=(10, 6))
sns.barplot(data=top_playlists, x="max(num_followers)", y="playlist_name", palette="viridis")
plt.title(f'Top {num_playlists} Playlists by Number of Followers')
plt.xlabel('Number of Followers')
plt.ylabel('Playlist Name')
st.pyplot(plt)

# Step 2: Average Playlist Duration
max_tracks = playlist.agg({"num_tracks": "max"}).collect()[0][0]
st.sidebar.write(f"Maximum number of tracks in any playlist: {max_tracks}")
num_bins = st.sidebar.slider('Select number of bins for track counts:', min_value=2, max_value=min(max_tracks, 20), value=5)

# Average Playlist Duration Visualization
st.header('Average Playlist Duration by Number of Tracks')
bins = [i * (max_tracks // num_bins) for i in range(num_bins + 1)]
labels = [f"{bins[i]}-{bins[i + 1]}" for i in range(num_bins)]

playlist = playlist.withColumn('track_bins',
                                when(col('num_tracks') <= bins[1], labels[0])
                                .when((col('num_tracks') > bins[1]) & (col('num_tracks') <= bins[2]), labels[1])
                                .when((col('num_tracks') > bins[2]) & (col('num_tracks') <= bins[3]), labels[2])
                                .when((col('num_tracks') > bins[3]) & (col('num_tracks') <= bins[4]), labels[3])
                                .when(col('num_tracks') > bins[4], labels[4]))

avg_duration_bins = playlist.groupBy('track_bins') \
    .agg(avg('playlist_duration_min').alias('avg_duration')) \
    .orderBy('track_bins') \
    .toPandas()

plt.figure(figsize=(10, 6))
sns.lineplot(data=avg_duration_bins, x='track_bins', y='avg_duration', marker='o', palette='coolwarm')
plt.title('Average Playlist Duration by Number of Tracks')
plt.xlabel('Number of Tracks')
plt.ylabel('Average Duration (minutes)')
st.pyplot(plt)

# Step 3: Top Artists
num_artists = st.sidebar.slider('Select number of top artists to display:', min_value=1, max_value=35, value=10)
st.header('Top Artists')
artist_counts = (
    tracks.groupBy('artist_name')
    .agg(count('artist_name').alias('count'))
    .orderBy(col('count').desc())
    .limit(num_artists)
    .toPandas()
)

plt.figure(figsize=(10, 6))
sns.barplot(data=artist_counts, x='artist_name', y='count', palette='magma')
plt.title(f'Top {num_artists} Most Common Artists')
plt.xlabel('Artist Name')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
st.pyplot(plt)

# Step 4: Top Artists per Playlist
top_n = st.sidebar.slider('Select number of top playlists or artists to display', 5, 50, 10)
artist_per_playlist_df = tracks.groupBy("playlist_id", "artist_name").agg(count("track_name").alias("track_count"))

window_spec = Window.partitionBy("playlist_id").orderBy(col("track_count").desc())
artist_rank_df = artist_per_playlist_df.withColumn("rank", row_number().over(window_spec))
top_artists_per_playlist_df = artist_rank_df.filter(col("rank") == 1).orderBy(col("track_count").desc()).limit(top_n)

top_artists_per_playlist_pd = top_artists_per_playlist_df.toPandas()

# Streamlit Interface for Top Artists per Playlist
st.title("Top Artists per Playlist Analysis")
option = st.selectbox('Choose what you want to do:', ('Show DataFrame', 'Plot Bar Graph', 'Plot Pie Chart', 'Plot Heatmap'))

if option == 'Show DataFrame':
    st.subheader('Top Artists per Playlist DataFrame')
    st.dataframe(top_artists_per_playlist_pd)

elif option == 'Plot Bar Graph':
    st.subheader('Top Artists per Playlist - Bar Graph')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_artists_per_playlist_pd, x='playlist_id', y='track_count', hue='artist_name', palette='crest')
    plt.xticks(rotation=90)
    plt.title(f'Top {top_n} Playlists by Track Count - Bar Graph')
    plt.xlabel('Playlist ID')
    plt.ylabel('Number of Tracks')
    st.pyplot(plt)

elif option == 'Plot Pie Chart':
    st.subheader('Top Artists per Playlist - Pie Chart')
    artist_summary = top_artists_per_playlist_pd.groupby('artist_name')['track_count'].sum().reset_index()
    plt.figure(figsize=(8, 8))
    plt.pie(artist_summary['track_count'], labels=artist_summary['artist_name'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title(f'Top {top_n} Artists Contribution Across Playlists')
    st.pyplot(plt)

elif option == 'Plot Heatmap':
    st.subheader('Top Artists per Playlist - Heatmap')
    pivot_df = top_artists_per_playlist_pd.pivot("artist_name", "playlist_id", "track_count").fillna(0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_df, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title(f'Heatmap of Top {top_n} Artists per Playlist')
    plt.xlabel('Playlist ID')
    plt.ylabel('Artist Name')
    st.pyplot(plt)

# Step 5: Artist-Specific Playlist and Track Info
artist_names = tracks.select("artist_name").distinct().toPandas()['artist_name']
selected_artist = st.sidebar.selectbox('Select an Artist:', artist_names)

st.header(f'Playlists and Tracks for {selected_artist}')
artist_playlists = tracks.filter(col("artist_name") == selected_artist) \
    .select("playlist_name", "track_name", "album_name", "track_duration_min").toPandas()

if not artist_playlists.empty:
    st.dataframe(artist_playlists)
else:
    st.write(f"No playlists found for {selected_artist}.")
