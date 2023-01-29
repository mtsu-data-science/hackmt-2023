import streamlit as st
from src.data_pipeline import read_subreddit_data_from_s3

#Page title
st.title("Results")

#Store session state into selection variable
selection = st.write(st.session_state.rselection)

#Display session variable value if available
if selection:
    print(selection)
