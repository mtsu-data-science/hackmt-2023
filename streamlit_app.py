import streamlit as st
from src.data_pipeline import example_func, read_subreddit_data_from_s3

st.title("Reddit Sentiment Analysis")

example_func()

df = read_subreddit_data_from_s3("test", "test-file-name")

st.dataframe(df)