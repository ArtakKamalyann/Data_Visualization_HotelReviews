import streamlit as st
import pandas as pd
import plotly.express as px
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from collections import Counter

# Load Data
df = pd.read_csv(r'Hotel_Reviews.csv')

# Convert 'Review_Date' to datetime
df['Review_Date'] = pd.to_datetime(df['Review_Date'])

# Rename 'lng' to 'lon'
df = df.rename(columns={'lng': 'lon'})

# Sidebar
st.sidebar.header('Select Hotel')
hotel_name = st.sidebar.selectbox('Hotel Name', sorted(df['Hotel_Name'].unique()))

# Filter data
mask = df["Hotel_Name"] == hotel_name
df_filtered = df[mask]

# Main
st.header(f'Hotel: {hotel_name}')

# Word Cloud of Review Comments
stopwords_list = set(stopwords.words('english'))

# Combine all review comments for the selected hotel
comments = ' '.join(df_filtered['Negative_Review'].dropna().tolist())

# Tokenize the comments
tokens = word_tokenize(comments)

# Remove stopwords
filtered_tokens = [word for word in tokens if word.lower() not in stopwords_list]

# Create a word cloud
wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(Counter(filtered_tokens))

# Display the word cloud
st.subheader("Word Cloud of Review Comments")
st.image(wordcloud.to_image())

# Map showing hotel location
st.subheader("Hotel Location")
df_filtered = df_filtered.dropna(subset=['lat', 'lon'])
st.map(df_filtered)

# Bar chart for Reviewer Nationalities
st.subheader("Reviewer Nationalities")
fig2 = px.bar(df_filtered['Reviewer_Nationality'].value_counts().head(10))
st.plotly_chart(fig2)

# Histogram of Review Scores
st.subheader("Distribution of Review Scores")
fig4 = px.histogram(df_filtered, x='Reviewer_Score', nbins=20, histnorm='percent')
st.plotly_chart(fig4)
