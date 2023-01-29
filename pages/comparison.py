import streamlit as st
from src.data_pipeline import read_subreddit_data_from_s3
import matplotlib.pyplot as plt
import pandas as pd
examp = pd.read_csv('example.csv')

st.title("Subreddit Comparison")
#st.write("How toxic is your favorite Reddit sub?")

subreddit_title3 = st.text_input('Enter a subreddit title to analyze:', '')
#st.write("Subreddit title is ", subreddit_title)

if subreddit_title3:
    try:
        df = read_subreddit_data_from_s3(subreddit_title3, "parsed-subreddits")
        
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
    


        subreddit_title2 = st.text_input('Enter a subreddit title to analyze:', key = '2')
        #st.write("Subreddit title is ", subreddit_title2)

        if subreddit_title2:
        
            df2 = read_subreddit_data_from_s3(subreddit_title2, "parsed-subreddits")
            
            neu2 = df2["post_title_neutral"]
            neg2 = df2["post_title_negative"]
            pos2 = df2["post_title_positive"]
            neu_avg2 = (neu2.sum())/len(neu2)
            neg_avg2 = (neg2.sum())/len(neg2)
            pos_avg2 = (pos2.sum())/len(pos2)
            #st.write("neu", neu_avg)
            #st.write("neg", neg_avg)
            #st.write("pos", pos_avg)
        
        
            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            labels = ['Neutral', 'Negative', 'Positive']

            sizes = [neu_avg2, neg_avg2, pos_avg2]

            colors = ['#FFA500', '#FF0000', '#00FF00']
            fig2, ax1 = plt.subplots()
            ax1.pie(sizes, explode=(0,0,0), labels=labels, labeldistance=1.2,colors=colors, autopct='%0.1f%%',
                    shadow=True, startangle=30)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            st.pyplot(fig2)

            if pos_avg2 > neg_avg2 and pos_avg2 > neu_avg2:
                st.write("Hooray! The sub you found stays on the bright side!")

            elif neg_avg2 > pos_avg2 and neg_avg2 > neu_avg2:
                st.write("There sure are some pessimistic perspectives on this sub!")

            elif neu_avg2 > pos_avg2 and neu_avg2 > neg_avg2:
                st.write("This sub is even keeled and neutral.")

            else:
                st.write("We can't figure out how this mysterious sub feels.")
        

        # ratios
        st.write('Positive Ratio')
        st.write("Sub 1: ",pos_avg.round(2))
        st.write("Sub 2: ",pos_avg2.round(2))
        pos_rat = pos_avg2 - pos_avg
        st.write("Ratio:")
        st.write(pos_rat.round(2))

    except:
        st.write("This is not a valid subreddit title.")