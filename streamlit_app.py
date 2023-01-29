

# pulls files from s3 
import streamlit as st
from src.data_pipeline import read_subreddit_data_from_s3
import matplotlib.pyplot as plt
import pandas as pd






st.title("Reddit Sentimental Analysis")
st.write("How toxic is your favorite Reddit sub?")

subreddit_title = st.text_input('Enter a subreddit title to analyze:', '')
#st.write("Subreddit title is ", subreddit_title)

# pulls files from s3 
# args are subreddit_name, file_name
#examp = pd.read_csv('example.csv')


#st.write(examp)



if subreddit_title:
    try:
        df = read_subreddit_data_from_s3(subreddit_title, "parsed-subreddits")
        
        neu = df["post_title_neutral"]
        neg = df["post_title_negative"]
        pos = df["post_title_positive"]
        neu_avg = (neu.sum())/len(neu)
        neg_avg = (neg.sum())/len(neg)
        pos_avg = (pos.sum())/len(pos)
        #st.write("neu", neu_avg)
        #st.write("neg", neg_avg)
        #st.write("pos", pos_avg)
    
    
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = ['Neutral', 'Negative', 'Positive']

        sizes = [neu_avg, neg_avg, pos_avg]

        colors = ['#FFA500', '#FF0000', '#00FF00']
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=(0,0,0), labels=labels, labeldistance=1.2,colors=colors, autopct='%0.1f%%',
                shadow=True, startangle=30)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)

        if pos_avg > neg_avg and pos_avg > neu_avg:
            st.write("Hooray! The sub you found stays on the bright side!")

        elif neg_avg > pos_avg and neg_avg > neu_avg:
            st.write("There sure are some pessimistic perspectives on this sub!")

        elif neu_avg > pos_avg and neu_avg > neg_avg:
            st.write("This sub is even keeled and neutral.")

        else:
            st.write("We can't figure out how this mysterious sub feels.")

        st.write(df[['post_title','upvotes','post_title_neutral','post_title_positive','post_title_negative']])
    except:
        st.write("This is not a valid subreddit title.")
