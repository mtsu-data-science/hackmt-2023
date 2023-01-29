import streamlit as st
import numpy as np
import pandas as pd

#Container located at top of UI.
con = st.container()


#Load CSV Function - Returns csv as numpy a ndarray
def load_csv():
    return np.loadtxt("TeamInformation4.csv", delimiter= ',', dtype = str)

#calls csv as nparray
abt = load_csv()

#Sidebar for Meet the Team - Move to a new page
st.title("Meet the Team")
    
    #st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")

    #picture and caption loop
for i in range(len(abt)-1):
    url = abt[i+1][0]
    st.image(url)
    #name
    caption = abt[i+1][1]
    st.caption(caption)

        





#Side bar area.


abt = st.expander("About the Team")
#about_us = {'Picture': [],'Name': [], 'Major': []}

#st.sidebar.button("Enter", on_click=st.dataframe(df))
#st.text_input()


#def hide_data():
    #return st.button("Show grid", on_click=load_data(df))

#def button_check():
#   print("this button works!")

#btn_chk = button_check()

#test
