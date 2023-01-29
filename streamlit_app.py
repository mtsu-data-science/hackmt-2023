import streamlit as st
from streamlit.components.v1 import html
import pages.streamlit_results as streamlit_results
from src.data_pipeline import read_subreddit_data_from_s3

#st.set_page_config(page_title="Home")

st.title("Reddit Sentiment Analysis")


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

st.sidebar.success("Resultsss")
st.markdown("""---""")
df = read_subreddit_data_from_s3("test", "test-file-name")

#st.dataframe(df)

#if st.button("< Prev"):
 #   nav_page("about us")
#if st.button("Next >"):
#    nav_page("results")

#results = {"streamlit_results": streamlit_results}

#st.button.selectbox("Enter", on_click=results)
