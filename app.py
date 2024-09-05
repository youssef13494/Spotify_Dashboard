import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# Load the data
df = pd.read_csv('spotify_data.csv')

# Convert 'modified_at' to datetime
df['modified_at'] = pd.to_datetime(df['modified_at'])

# Set Streamlit theme for the dashboard
st.set_page_config(layout="wide")


# Function to display matplotlib charts
def plot_to_streamlit(fig):
    st.pyplot(fig)

# Define your dataframe (assuming df is already defined)
# df = ...

# Dashboard title with icon
st.markdown("# 🎵 Spotify Data Dashboard")

# Display the sampled data
st.dataframe(df.head(1000))

# 1st row: Top 10 Artists by Average Track Duration and Top 10 Most Followed Artists
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📊 Average Track Duration by Artist")
    fig, ax = plt.subplots(figsize=(12, 6))
    top_artists = df.groupby('artist_name')['track_duration_sec'].mean().sort_values(ascending=False).head(10)
    ax.bar(top_artists.index, top_artists.values, color='green')
    ax.set_xlabel('Artist Name', color='white')
    ax.set_ylabel('Average Track Duration (seconds)', color='white')
    ax.set_title('Average Track Duration by Artist', color='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('black')
    plot_to_streamlit(fig)

with col2:
    st.markdown("## 👥 Top 10 Most Followed Artists")
    fig, ax = plt.subplots(figsize=(12, 6))
    top_followed_artists = df.groupby('artist_name')['num_followers'].sum().sort_values(ascending=False).head(10)
    ax.bar(top_followed_artists.index, top_followed_artists.values, color='green')
    ax.set_xlabel('Artist Name', color='white')
    ax.set_ylabel('Total Followers', color='white')
    ax.set_title('Top 10 Most Followed Artists', color='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('black')
    plot_to_streamlit(fig)

# 2nd row: Number of Playlists Created Over Time and Average Track Duration by Year
col3, col4 = st.columns(2)

with col3:
    st.markdown("## 🗓️ Number of Playlists Over Time")
    fig, ax = plt.subplots(figsize=(12, 6))
    playlists_over_time = df.groupby(df['modified_at'].dt.to_period('M'))['pid'].count()
    ax.plot(playlists_over_time.index.to_timestamp(), playlists_over_time.values, color='green')
    ax.set_xlabel('Year', color='white')
    ax.set_ylabel('Number of Playlists', color='white')
    ax.set_title('Number of Playlists Created Over Time', color='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('black')
    plot_to_streamlit(fig)

with col4:
    st.markdown("## 📅 Average Track Duration by Year")
    fig, ax = plt.subplots(figsize=(12, 6))
    average_track_duration_by_year = df.groupby(df['modified_at'].dt.year)['track_duration_sec'].mean()
    ax.plot(average_track_duration_by_year.index, average_track_duration_by_year.values, color='green')
    ax.set_xlabel('Year', color='white')
    ax.set_ylabel('Average Track Duration (seconds)', color='white')
    ax.set_title('Average Track Duration by Year', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('black')
    plot_to_streamlit(fig)

# 3rd row: Relationship between Followers and Edits and Correlation between Playlist Duration and Number of Tracks
col5, col6 = st.columns(2)

with col5:
    st.markdown("## 👤 Followers vs. Edits")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['num_followers'], df['num_edits'], color='green')
    ax.set_xlabel('Number of Followers', color='white')
    ax.set_ylabel('Number of Edits', color='white')
    ax.set_title('Relationship between Number of Followers and Number of Edits', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('black')
    plot_to_streamlit(fig)

with col6:
    st.markdown("## 📈Playlist Duration vs num of Tracks")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['num_tracks'], df['duration_sec'], color='green')
    ax.set_xlabel('Number of Tracks', color='white')
    ax.set_ylabel('Playlist Duration (seconds)', color='white')
    ax.set_title('Correlation between Playlist Duration and Number of Tracks', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('black')
    plot_to_streamlit(fig)

# 4th row: Playlist Length Distribution and Track Position Distribution
col7, col8 = st.columns(2)

with col7:
    st.markdown("## 🎧 Playlist Length Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['num_tracks'], bins=20, color='green')
    ax.set_xlabel('Number of Tracks', color='white')
    ax.set_ylabel('Frequency', color='white')
    ax.set_title('Distribution of Playlist Lengths', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('black')
    plot_to_streamlit(fig)

with col8:
    st.markdown("## 🔢 Track Position Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['track_pos'], bins=df['track_pos'].max(), color='green')
    ax.set_xlabel('Track Position', color='white')
    ax.set_ylabel('Frequency', color='white')
    ax.set_title('Distribution of Track Positions within Playlists', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('black')
    plot_to_streamlit(fig)

# 5th row: Word clouds for Most Frequent Album Names and Track Names
col9, col10 = st.columns(2)

with col9:
    st.markdown("## 💿 Most Frequent Album Names")
    album_counts = df['album_name'].value_counts()
    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Greens').generate_from_frequencies(album_counts)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    plot_to_streamlit(fig)

with col10:
    st.markdown("## 🎶 Most Frequent Track Names")
    track_counts = df['track_name'].value_counts()
    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Greens').generate_from_frequencies(track_counts)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    plot_to_streamlit(fig)
