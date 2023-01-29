import streamlit as st
from streamlit.components.v1 import html
import pages.streamlit_results as streamlit_results
from src.data_pipeline import read_subreddit_data_from_s3

#st.set_page_config(page_title="Home")

st.title("Reddit Sentiment Analysis")

st.sidebar.success("Results")
st.markdown("""---""")
df = read_subreddit_data_from_s3("test", "test-file-name")

if 'rselection' not in st.session_state:
    st.session_state.rselection = "Enter a subreddit title to analyze:"

st.write(st.session_state.rselection)

def get_selection():
    subreddit_title = st.selectbox("Enter a subreddit title to analyze:", df, key="rselection")
    st.write("Subreddit title is ", subreddit_title)
    st.write(st.session_state.rselection)
    return subreddit_title

get_selection()


#@st.experimental_memo
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

if st.button("streamlit_results"):
    nav_page("streamlit_results")
    st.write.nav_page("entered results page")
    #st.write("entered results page")



if st.button("about"):
    nav_page("about")

#Delete session state
#for rselection in st.session_state.rselection:
    #del st.session_state(rselection)



#st.sidebar.success("Results")
#st.markdown("""---""")
#df = read_subreddit_data_from_s3("test", "test-file-name")

#if 'rselection' not in st.session_state:
#    st.session_state.rselection = 'title'

#st.write(st.session_state.rselection)

#def get_selection():
#    subreddit_title = st.selectbox("Enter a subreddit title to analyze:", df)
#    st.write("Subreddit title is ", subreddit_title)
#    return subreddit_title

#get_selection()

#html("pages\streamlit_results.py")
#subreddit_title = st.selectbox("Enter a subreddit title to analyze:", df)
#with subreddit_title:
#   st.write("Subreddit title is ", subreddit_title)
#st.dataframe(df)

#if st.button("< Prev"):
 #   nav_page("about us")
#if st.button("Next >"):
#    nav_page("results")

#results = {"streamlit_results": streamlit_results}

#st.button.selectbox("Enter", on_click=results)
