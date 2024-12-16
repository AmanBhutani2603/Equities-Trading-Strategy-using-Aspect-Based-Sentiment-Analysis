# -*- coding: utf-8 -*-
"""Final DPP with EDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H0FZL3VV5vAaX7O9rvgHjpHtF1vrXhNl

## Libraires And Utilities

## Setting up environment
"""

import pandas as pd
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy

from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/MyDrive/reddit_wsb.csv'

df = pd.read_csv(file_path)
df = df[['title', 'score', 'id', 'url', 'comms_num', 'created', 'body', 'timestamp']]
df.head()

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')

"""## Loading the data and getting Summary of the data"""

data = df

# Displays basic information about the dataset
print("Dataset Info:")
data.info()

data = data.dropna(how="all", axis=0)

# Removes completely empty columns
data = data.dropna(how="all", axis=1)

print(data.columns)

"""## Data Preprocessing Steps:"""

# Handles missing data: Drop rows with missing 'title' and fill missing 'body'
data = data.dropna(subset=['title']).reset_index(drop=True)
data['body'] = data['body'].fillna("No content")

# Text cleaning function
def clean_text(text):
    text = text.lower()  # Converts to lowercase
    text = re.sub(r'@\w+', '', text)  # Removes mentions (e.g., @username)
    text = re.sub(r'http\S+', '', text)  # Removes URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Removes special characters
    text = re.sub(r'\b\w\b', '', text)  # Removes single-character words
    text = re.sub(r'\s+', ' ', text).strip()  # Replaces multiple spaces with a single space
    return text

# Cleans 'title' and 'body'
data['cleaned_title'] = data['title'].apply(clean_text)
data['cleaned_body'] = data['body'].apply(clean_text)

# Converts 'timestamp' to datetime and handle invalid entries
data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')

# Identifies rows with invalid timestamps (now NaT)
invalid_rows = data[data['timestamp'].isna()]

# Option 1: Drop rows with invalid timestamps
data = data.dropna(subset=['timestamp']).reset_index(drop=True)

data['year'] = data['timestamp'].dt.year
data['month'] = data['timestamp'].dt.month
data['day'] = data['timestamp'].dt.day
data['hour'] = data['timestamp'].dt.hour

# Adds word count, stopword count, and average word length
stop_words = set(stopwords.words("english"))

# Display a sample of the preprocessed data
print("Preprocessed Data Sample:")
data.head()

"""## Feature Engineering

### 1. Basic Text Features:
"""

# Loads the spaCy model
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser", "lemmatizer"])

def word_count(text):
    doc = nlp(text)
    return len([token for token in doc if not token.is_space])  # Exclude spaces

def stopword_count(text):
    doc = nlp(text)
    return len([token for token in doc if token.is_stop])  # Use spaCy's `is_stop`

def avg_word_length(text):
    doc = nlp(text)
    words = [token for token in doc if not token.is_stop and not token.is_space]
    return np.mean([len(token.text) for token in words]) if words else 0


data['title_word_count'] = data['cleaned_title'].apply(word_count)
data['body_word_count'] = data['cleaned_body'].apply(word_count)

data['title_stopword_count'] = data['cleaned_title'].apply(stopword_count)
data['body_stopword_count'] = data['cleaned_body'].apply(stopword_count)

data['title_avg_word_length'] = data['cleaned_title'].apply(avg_word_length)
data['body_avg_word_length'] = data['cleaned_body'].apply(avg_word_length)

print("Feature-Enhanced Data Sample:")
print(data[['cleaned_title', 'title_word_count', 'title_stopword_count', 'title_avg_word_length']].head())

"""### 2. Sentiment Analysis:"""

# Initializes the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to calculate sentiment scores
def get_sentiment_scores(text):
    scores = sia.polarity_scores(text)
    return scores['pos'], scores['neu'], scores['neg'], scores['compound']

# Applies sentiment analysis to cleaned_title
data[['title_positive', 'title_neutral', 'title_negative', 'title_compound']] = data['cleaned_title'].apply(
    lambda x: pd.Series(get_sentiment_scores(x))
)

# Applies sentiment analysis to cleaned_body
data[['body_positive', 'body_neutral', 'body_negative', 'body_compound']] = data['cleaned_body'].apply(
    lambda x: pd.Series(get_sentiment_scores(x))
)

# Displays a sample of the sentiment features
print("Sentiment-Enhanced Data Sample:")
data[['cleaned_title', 'title_positive', 'title_negative', 'title_compound']].head()

# Categorizes sentiment based on compound score
def sentiment_category(compound):
    if compound > 0.05:
        return 'Positive'
    elif compound < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

data['title_sentiment_class'] = data['title_compound'].apply(sentiment_category)

# Categorizes sentiment based on compound score
def sentiment_category(compound):
    if compound > 0.05:
        return 'Positive'
    elif compound < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

data['body_sentiment_class'] = data['body_compound'].apply(sentiment_category)

data[['title', 'body', 'title_sentiment_class', 'body_sentiment_class']]

"""## Exploratory Data Analysis (EDA)

### 1. Distribution of Samples Across Sentiment Polarity Classes
"""

# Categorizes sentiment based on compound score
def sentiment_category(compound):
    if compound > 0.05:
        return 'Positive'
    elif compound < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

data['sentiment_class'] = data['title_compound'].apply(sentiment_category)

# Counts the number of samples per class
class_distribution = data['sentiment_class'].value_counts()

# Plot class distribution
plt.figure(figsize=(8, 5))
sns.barplot(x=class_distribution.index, y=class_distribution.values, palette='coolwarm')
plt.title('Distribution of Samples Across Sentiment Classes', fontsize=16)
plt.xlabel('Sentiment Class')
plt.ylabel('Number of Samples')
plt.show()

"""### 2. Visualize Temporal Patterns"""

# Posts per hour
posts_by_hour = data['hour'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
sns.barplot(x=posts_by_hour.index, y=posts_by_hour.values, palette='viridis')
plt.title('Post Activity by Hour', fontsize=16)
plt.xlabel('Hour of Day')
plt.ylabel('Number of Posts')
plt.show()

# Posts per month
posts_by_month = data['month'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.barplot(x=posts_by_month.index, y=posts_by_month.values, palette='magma')
plt.title('Post Activity by Month', fontsize=16)
plt.xlabel('Month')
plt.ylabel('Number of Posts')
plt.show()

# Sentiment trends over time
avg_sentiment_month = data.groupby('month')[['title_positive', 'title_negative', 'title_compound']].mean()
avg_sentiment_month.plot(kind='line', figsize=(12, 8), marker='o')
plt.title('Average Sentiment Trends by Month', fontsize=16)
plt.xlabel('Month')
plt.ylabel('Average Sentiment Score')
plt.grid(True)
plt.show()

"""### 4. Word Cloud for Most Common Words"""

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Combines all text from cleaned_title for word cloud
all_titles = ' '.join(data['cleaned_title'])

# Generates word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=STOPWORDS).generate(all_titles)

# Displays the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Most Common Words in Titles', fontsize=16)
plt.show()