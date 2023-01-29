import streamlit as st
from src.data_pipeline import read_subreddit_data_from_s3

st.title("Results")
#st.button("Reset")

with subreddit_title:
    st.write("Subreddit title is ", subreddit_title)