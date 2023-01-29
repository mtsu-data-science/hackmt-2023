import streamlit as st
from streamlit.components.v1 import html
import pages.streamlit_results as streamlit_results
from src.data_pipeline import read_subreddit_data_from_s3

#Title 
st.title("Reddit Sentiment Analysis")
st.markdown("""---""")

df = read_subreddit_data_from_s3("test", "test-file-name")

#Saving cache from current session
if 'rselection' not in st.session_state:
    st.session_state.rselection = "Enter a subreddit title to analyze:"

#function: get_selection
#Purpose: provide selectbox for user to select from dataframe then update session state with selection.
def get_selection():
    subreddit_title = st.selectbox("Enter a subreddit title to analyze:", df, key="rselection")
    st.write("Subreddit title is: ")
    st.write(st.session_state.rselection)
    return 

#run function
get_selection()
st.markdown("""---""")


#custom navigation applied to app, results and about us pages.
def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

#Navigate to results page when results page button is pressed.
if st.button("streamlit_results"):
    nav_page("streamlit_results")

#Navigate to about page when results page button is pressed.
if st.button("about"):
    nav_page("about")

#Delete cache from current session state
#for rselection in st.session_state.rselection:
#   del st.session_state[rselection]

