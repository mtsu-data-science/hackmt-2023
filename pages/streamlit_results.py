import streamlit as st
import pandas as pd
import numpy as np
from src.data_pipeline import read_subreddit_data_from_s3

#Page title
st.title("Results")
st.markdown("""---""")

#Store session state into selection variable
selection = st.write(st.session_state.rselection)

df = pd.DataFrame(
   np.random.randn(50, 10),
   columns=('col %d' % i for i in range(10)))

#st.dataframe(df)  # Same as st.write(df)
with st.expander("Scores"):
    st.dataframe(df)

#Display session variable value if available
if selection:
    print(selection)
