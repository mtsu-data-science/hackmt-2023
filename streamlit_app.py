import streamlit as st
from src.data_pipeline import read_subreddit_data_from_s3

st.title("Reddit Sentiment Analysis")

df = read_subreddit_data_from_s3("test", "test-file-name")

st.dataframe(df)

# df = pd.read_csv("reddit_sentiment_analysis.csv")
subreddit_title = st.text_input('Subreddit title', 'Enter a title!')
st.write("Subreddit title is ", subreddit_title)

st.write(df.loc[df['Title'] == subreddit_title])
