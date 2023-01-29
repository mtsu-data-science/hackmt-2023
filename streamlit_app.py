import streamlit as st
import streamlit_results
from src.data_pipeline import read_subreddit_data_from_s3

st.set_page_config(page_title="Home")

st.title("Reddit Sentiment Analysis")
st.button("About Us")
st.sidebar.success("Results")
st.markdown("""---""")
df = read_subreddit_data_from_s3("test", "test-file-name")

st.dataframe(df)

#results = {"streamlit_results": streamlit_results}

#st.button.selectbox("Enter", on_click=results)
