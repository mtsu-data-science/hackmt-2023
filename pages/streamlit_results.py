import streamlit as st
import streamlit_app
from src.data_pipeline import read_subreddit_data_from_s3

st.title("Results")
st.button("Reset")