import streamlit as st
import streamlit_app
from src.data_pipeline import read_subreddit_data_from_s3

st.title("Results")
st.write(st.session_state.rselection)
streamlit_app.get_selection()
#st.button("Reset")

#df = read_subreddit_data_from_s3("test", "test-file-name")

#subreddit_title = st.selectbox("Enter a subreddit title to analyze:", df)
#with subreddit_title:
 #   st.write("Subreddit title is ", subreddit_title)