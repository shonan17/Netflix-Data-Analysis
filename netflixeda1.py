import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.title("Netflix EDA Dashboard")

# Load Data
df = pd.read_csv('netflix_titles.csv')
df.fillna("Unknown", inplace=True)
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Movies vs TV Shows
st.subheader("Movies vs. TV Shows")
type_counts = df["type"].value_counts()
fig = px.bar(x=type_counts.index, y=type_counts.values, color=type_counts.index, title="Movies vs. TV Shows")
st.plotly_chart(fig)

# Top 10 Genres
st.subheader("Top 10 Genres")
genres = df["listed_in"].str.split(", ").explode().value_counts().head(10)
fig = px.bar(x=genres.values, y=genres.index, orientation='h', title="Top 10 Genres", color=genres.index)
st.plotly_chart(fig)

# Release Trend Over Years
st.subheader("Release Trend Over Years")
fig = px.histogram(df, x="release_year", nbins=15, title="Release Trend Over Years", color_discrete_sequence=['red'])
st.plotly_chart(fig)

# Top 10 Countries Producing Content
st.subheader("Top 10 Countries Producing Content")
countries = df["country"].value_counts().head(10)
fig = px.bar(x=countries.values, y=countries.index, orientation='h', title="Top 10 Countries Producing Content", color=countries.index)
st.plotly_chart(fig)

# Content Ratings Distribution
st.subheader("Content Ratings Distribution")
rating_counts = df['rating'].value_counts()
fig = px.bar(x=rating_counts.values, y=rating_counts.index, orientation='h', title="Content Ratings Distribution", color=rating_counts.index)
st.plotly_chart(fig)

# Monthly Additions Trend
st.subheader("Monthly Additions Trend")
df['month_added'] = df['date_added'].dt.month_name()
month_counts = df['month_added'].value_counts()[["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]]
fig = px.bar(x=month_counts.index, y=month_counts.values, title="Monthly Additions Trend", color=month_counts.index)
st.plotly_chart(fig)

# Top 10 Most Frequent Directors
st.subheader("Top 10 Most Frequent Directors")
top_directors = df[df['director'] != "Unknown"]['director'].value_counts().head(10)
fig = px.bar(x=top_directors.values, y=top_directors.index, orientation='h', title="Top 10 Most Frequent Directors", color=top_directors.index)
st.plotly_chart(fig)

# Movies vs TV Shows in Top 10 Countries
st.subheader("Movies vs TV Shows in Top 10 Countries")
top_countries = df["country"].value_counts().head(10).index
df_filtered = df[df["country"].isin(top_countries)]
fig = px.histogram(df_filtered, y="country", color="type", title="Movies vs TV Shows in Top 10 Countries", barmode='group')
st.plotly_chart(fig)

# Distribution of Movie Durations
st.subheader("Distribution of Movie Durations")
df['duration_minutes'] = df['duration'].str.extract('(\\d+)').astype(float)
fig = px.histogram(df[df['type'] == "Movie"], x='duration_minutes', nbins=30, title="Distribution of Movie Durations", color_discrete_sequence=['purple'])
st.plotly_chart(fig)

# Top 5 Longest and Shortest Movies
st.subheader("Top 5 Longest Movies on Netflix")
longest_movies = df[df['type'] == "Movie"].nlargest(5, 'duration_minutes')
fig = px.bar(x=longest_movies['duration_minutes'], y=longest_movies['title'], orientation='h', title="Top 5 Longest Movies", color=longest_movies['title'])
st.plotly_chart(fig)

st.subheader("Top 5 Shortest Movies on Netflix")
shortest_movies = df[df['type'] == "Movie"].nsmallest(5, 'duration_minutes')
fig = px.bar(x=shortest_movies['duration_minutes'], y=shortest_movies['title'], orientation='h', title="Top 5 Shortest Movies", color=shortest_movies['title'])
st.plotly_chart(fig)

# Most Common Number of Seasons in TV Shows
st.subheader("Most Common Number of Seasons in TV Shows")
tv_shows = df[df['type'] == "TV Show"]
tv_shows['season_count'] = tv_shows['duration'].str.extract('(\\d+)').astype(float)
fig = px.histogram(tv_shows, x='season_count', nbins=15, title="Most Common Number of Seasons", color_discrete_sequence=['purple'])
st.plotly_chart(fig)

# Top 10 Actors with Most Appearances
st.subheader("Top 10 Actors with Most Appearances")
top_celebrities = df[df['cast'] != "Unknown"]['cast'].str.split(", ").explode().value_counts().head(10)
fig = px.bar(x=top_celebrities.values, y=top_celebrities.index, orientation='h', title="Top 10 Actors on Netflix", color=top_celebrities.index)
st.plotly_chart(fig)

# TV Shows by Country
st.subheader("Top 10 Countries with Most TV Shows (Excluding Unknown)")
tv_shows_by_country = df[(df['type'] == "TV Show") & (df['country'] != "Unknown")]['country'].value_counts().head(10)
fig = px.bar(x=tv_shows_by_country.values, y=tv_shows_by_country.index, orientation='h', title="Top 10 Countries with Most TV Shows", color=tv_shows_by_country.index)
st.plotly_chart(fig)

# Movies by Country
st.subheader("Top 10 Countries with the Most Movies on Netflix (Excluding Unknown)")
movies_by_country = df[(df['type'] == "Movie") & (df['country'] != "Unknown")]['country'].value_counts().head(10)
fig = px.bar(x=movies_by_country.values, y=movies_by_country.index, orientation='h', title="Top 10 Countries with the Most Movies", color=movies_by_country.index)
st.plotly_chart(fig)

# Content Ratings by Type
st.subheader("Distribution of Content Ratings by Type (Movie vs. TV Show)")
fig = px.histogram(df, y='rating', color='type', title="Content Ratings by Type", barmode='group')
st.plotly_chart(fig)

# Top 10 Longest TV Shows
st.subheader("Top 10 Longest TV Shows")
longest_tv_shows = tv_shows.nlargest(10, 'season_count')
fig = px.bar(x=longest_tv_shows['season_count'], y=longest_tv_shows['title'], orientation='h', title="Top 10 Longest TV Shows", color=longest_tv_shows['title'])
st.plotly_chart(fig)
