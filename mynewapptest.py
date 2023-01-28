import streamlit as st
import pandas as pd
import numpy as np

# Se
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable selectbox widget", key="disabled")
    st.radio(
        "Set selectbox label visibility 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )

with col2:
    option = st.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )

#title
st.title('"title"')

#progress bar (does not dissapear after completed)
import time

#change color of progress bar
st.markdown(
    """
    <style>
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #b700ff , #b700ff);
        }
    </style>""",
    unsafe_allow_html=True,
)

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)




for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Loading {i+1}')
  bar.progress(i + 1)
  time.sleep(0.05)
  #make it dissapear after finishes running
  bar.empty()
  latest_iteration.empty()
  

#spinning progress
import time
import streamlit as st

with st.spinner('Wait for it...'):
    time.sleep(5)
#st.success('Done!') --if want it to display message after loading