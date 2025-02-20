import streamlit as st  # Import the Streamlit library for creating web applications
import pandas as pd  # Import pandas for data manipulation and analysis
import numpy as np  # Import numpy for numerical operations
import plotly.express as px  # Import Plotly Express for creating visualizations

st.title("Netflix EDA Dashboard")  # Set the title of the Streamlit app

# Load Data
df = pd.read_csv('netflix_titles.csv')  # Read the Netflix dataset from a CSV file into a DataFrame
df.fillna("Unknown", inplace=True)  # Fill missing values in the DataFrame with "Unknown"
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')  # Convert 'date_added' column to datetime format
wrong_ratings = ['74 min', '84 min', '66 min']
df.loc[df['rating'].isin(wrong_ratings), 'rating'] = "Unknown" #Changes the wrong rating to Unknown

# Movies vs TV Shows
st.subheader("Movies vs. TV Shows")  # Create a subheader for the Movies vs TV Shows section
type_counts = df["type"].value_counts()  # Count the occurrences of each type (Movie/TV Show)
fig = px.bar(x=type_counts.index, y=type_counts.values, color=type_counts.index, title="Movies vs. TV Shows")  # Create a bar chart for Movies vs TV Shows
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Top 10 Genres
st.subheader("Top 10 Genres")  # Create a subheader for the Top 10 Genres section
genres = df["listed_in"].str.split(", ").explode().value_counts().head(10)  # Split genres, count occurrences, and get the top 10
fig = px.bar(x=genres.values, y=genres.index, orientation='h', title="Top 10 Genres", color=genres.index)  # Create a horizontal bar chart for top genres
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Release Trend Over Years
st.subheader("Release Trend Over Years")  # Create a subheader for the Release Trend section
fig = px.histogram(df, x="release_year", nbins=15, title="Release Trend Over Years", color_discrete_sequence=['red'])  # Create a histogram for release trends over years
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Top 10 Countries Producing Content
st.subheader("Top 10 Countries Producing Content")  # Create a subheader for the Top 10 Countries section
countries = df["country"].value_counts().head(10)  # Count occurrences of each country and get the top 10
fig = px.bar(x=countries.values, y=countries.index, orientation='h', title="Top 10 Countries Producing Content", color=countries.index)  # Create a horizontal bar chart for top countries
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Content Ratings Distribution
st.subheader("Content Ratings Distribution")  # Create a subheader for the Content Ratings section
rating_counts = df['rating'].value_counts()  # Count occurrences of each content rating
fig = px.bar(x=rating_counts.values, y=rating_counts.index, orientation='h', title="Content Ratings Distribution", color=rating_counts.index)  # Create a horizontal bar chart for content ratings
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Monthly Additions Trend
st.subheader("Monthly Additions Trend")  # Create a subheader for the Monthly Additions section
df['month_added'] = df['date_added'].dt.month_name()  # Extract the month name from 'date_added'
month_counts = df['month_added'].value_counts()[["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]]  # Count occurrences of each month
fig = px.bar(x=month_counts.index, y=month_counts.values, title="Monthly Additions Trend", color=month_counts.index)  # Create a bar chart for monthly additions
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Top 10 Most Frequent Directors
st.subheader("Top 10 Most Frequent Directors")  # Create a subheader for the Top 10 Directors section
top_directors = df[df['director'] != "Unknown"]['director'].value_counts().head(10)  # Count occurrences of directors, excluding "Unknown"
fig = px.bar(x=top_directors.values, y=top_directors.index, orientation='h', title="Top 10 Most Frequent Directors", color=top_directors.index)  # Create a horizontal bar chart for top directors
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Movies vs TV Shows in Top 10 Countries
st.subheader("Movies vs TV Shows in Top 10 Countries")  # Create a subheader for the Movies vs TV Shows in Top 10 Countries section
top_countries = df["country"].value_counts().head(10).index  # Get the top 10 countries
df_filtered = df[df["country"].isin(top_countries)]  # Filter the DataFrame for the top 10 countries
fig = px.histogram(df_filtered, y="country", color="type", title="Movies vs TV Shows in Top 10 Countries", barmode='group')  # Create a grouped histogram for Movies vs TV Shows
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Distribution of Movie Durations
st.subheader("Distribution of Movie Durations")  # Create a subheader for the Movie Durations section
df['duration_minutes'] = df['duration'].str.extract('(\\d+)').astype(float)  # Extract the duration in minutes from the 'duration' column
fig = px.histogram(df[df['type'] == "Movie"], x='duration_minutes', nbins=10, title="Distribution of Movie Durations", color_discrete_sequence=['purple'])  # Create a histogram for movie durations
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Top 5 Longest and Shortest Movies
st.subheader("Top 5 Longest Movies on Netflix")  # Create a subheader for the Top 5 Longest Movies section
longest_movies = df[df['type'] == "Movie"].nlargest(5, 'duration_minutes')  # Get the top 5 longest movies
fig = px.bar(x=longest_movies['duration_minutes'], y=longest_movies['title'], orientation='h', title="Top 5 Longest Movies", color=longest_movies['title'])  # Create a horizontal bar chart for longest movies
st.plotly_chart(fig)  # Display the chart in the Streamlit app

st.subheader("Top 5 Shortest Movies on Netflix")  # Create a subheader for the Top 5 Shortest Movies section
shortest_movies = df[df['type'] == "Movie"].nsmallest(5, 'duration_minutes')  # Get the top 5 shortest movies
fig = px.bar(x=shortest_movies['duration_minutes'], y=shortest_movies['title'], orientation='h', title="Top 5 Shortest Movies", color=shortest_movies['title'])  # Create a horizontal bar chart for shortest movies
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Most Common Number of Seasons in TV Shows
st.subheader("Most Common Number of Seasons in TV Shows")  # Create a subheader for the Most Common Seasons section
tv_shows = df[df['type'] == "TV Show"]  # Filter the DataFrame for TV Shows
tv_shows['season_count'] = tv_shows['duration'].str.extract('(\\d+)').astype(float)  # Extract the number of seasons from the 'duration' column
fig = px.histogram(tv_shows, x='season_count', nbins=15, title="Most Common Number of Seasons", color_discrete_sequence=['purple'])  # Create a histogram for the number of seasons
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Top 10 Actors with Most Appearances
st.subheader("Top 10 Actors with Most Appearances")  # Create a subheader for the Top 10 Actors section
top_celebrities = df[df['cast'] != "Unknown"]['cast'].str.split(", ").explode().value_counts().head(10)  # Count occurrences of actors, excluding "Unknown"
fig = px.bar(x=top_celebrities.values, y=top_celebrities.index, orientation='h', title="Top 10 Actors on Netflix", color=top_celebrities.index)  # Create a horizontal bar chart for top actors
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# TV Shows by Country
st.subheader("Top 10 Countries with Most TV Shows (Excluding Unknown)")  # Create a subheader for the TV Shows by Country section
tv_shows_by_country = df[(df['type'] == "TV Show") & (df['country'] != "Unknown")]['country'].value_counts().head(10)  # Count occurrences of TV Shows by country, excluding "Unknown"
fig = px.bar(x=tv_shows_by_country.values, y=tv_shows_by_country.index, orientation='h', title="Top 10 Countries with Most TV Shows", color=tv_shows_by_country.index)  # Create a horizontal bar chart for top countries with TV Shows
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Movies by Country
st.subheader("Top 10 Countries with the Most Movies on Netflix (Excluding Unknown)")  # Create a subheader for the Movies by Country section
movies_by_country = df[(df['type'] == "Movie") & (df['country'] != "Unknown")]['country'].value_counts().head(10)  # Count occurrences of Movies by country, excluding "Unknown"
fig = px.bar(x=movies_by_country.values, y=movies_by_country.index, orientation='h', title="Top 10 Countries with the Most Movies", color=movies_by_country.index)  # Create a horizontal bar chart for top countries with Movies
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Content Ratings by Type
st.subheader("Distribution of Content Ratings by Type (Movie vs. TV Show)")  # Create a subheader for the Content Ratings by Type section
fig = px.histogram(df, y='rating', color='type', title="Content Ratings by Type", barmode='group')  # Create a grouped histogram for content ratings by type (Movie vs. TV Show)
st.plotly_chart(fig)  # Display the chart in the Streamlit app

# Top 10 Longest TV Shows
st.subheader("Top 10 Longest TV Shows")  # Create a subheader for the Top 10 Longest TV Shows section
longest_tv_shows = tv_shows.nlargest(10, 'season_count')  # Get the top 10 longest TV Shows based on the number of seasons
fig = px.bar(x=longest_tv_shows['season_count'], y=longest_tv_shows['title'], orientation='h', title="Top 10 Longest TV Shows", color=longest_tv_shows['title'])  # Create a horizontal bar chart for the longest TV Shows
st.plotly_chart(fig)  # Display the chart in the Streamlit app
