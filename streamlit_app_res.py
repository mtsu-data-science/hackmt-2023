import streamlit as st
from src.data_pipeline import read_subreddit_data_from_s3

st.title("Reddit Sentiment Analysis")

df = read_subreddit_data_from_s3("test", "test-file-name")

st.dataframe(df)

subreddit_title = st.text_input('Subreddit title', 'Enter a subreddit title!')
st.write("Subreddit title is ", subreddit_title)

# st.write(df.loc[df['Submission'] == subreddit_title])

import pandas as pd
import streamlit as st

# Cache the dataframe so it's only loaded once
@st.experimental_memo
def load_data():
    return pd.DataFrame(
        {
            "Results": ['Upvotes'],
            "Title": [5],
            "Body": [8],
        }
    )

# Boolean to resize the dataframe, stored as a session state variable
st.checkbox("Use container width", value=False, key="use_container_width")

df = load_data()

# Display the dataframe and allow the user to stretch the dataframe
# across the full width of the container, based on the checkbox value
st.dataframe(df, use_container_width=st.session_state.use_container_width)

# import pandas as pd
# df = pd.DataFrame([['Upvotes', '5', '8']], index=[''], columns=['Results', 'Title', 'Body'])
# st.write(df)

import streamlit as st

st.header('Score Breakdown')

import streamlit as st

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Title", "upper", "  10")
col2.metric(" ", "lower", "8")
col3.metric(' ', '', ' ')
col4.metric("  Body", "upper ", "  -5")
col5.metric(" ", "lower", "2")

