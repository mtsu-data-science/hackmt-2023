import streamlit as st
from src.data_pipeline import read_subreddit_data_from_s3

st.title("Reddit Sentiment Analysis")
st.button("About Us")

df = read_subreddit_data_from_s3("test", "test-file-name")

st.dataframe(df)
