import praw as praw
import os
from dotenv import load_dotenv
import re
import transformers
from transformers import pipeline
import pandas as pd
import emoji
import warnings
import csv
import shutil

warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()

# authenticating with reddit and setting up an object for interacting with the API

reddit = praw.Reddit(
    client_id=os.environ["reddit_client_id"],
    client_secret=os.environ["reddit_client_secret"],
    user_agent=os.environ["reddit_user_agent"],
)

# Create a regular expression pattern to match URLs
url_pattern = re.compile(r'https?://[^\s]+')

def main():
    # Get number of hottest posts to look at from user input
    num_posts = int(input("Enter the number of subreddit posts to look at: "))

    data = pd.read_csv("Top100.csv")
    txt_df = pd.DataFrame(data)

    count = 0 
    for subreddit in txt_df["subreddit"]:
        # call the grab_posts function
        grab_posts(subreddit,num_posts)
        print(subreddit)
    
    # call move files function that moves all csv files to a folder named Parsed-Subreddits
    move_files()

# this function grabs a number of posts from a subreddit
def grab_posts(subreddit,num_posts):
    # counter
    counter = 0

    # grab "x" number of posts in a subreddit and store them in a variable
    # the reasoning is because if you loop in reddit.subreddit(subreddit).top(limit=num_posts,time_filter="month"), it returns a generator object, and the generator is being exhausted after the first iteration. This would result in empty post text after the first iterration
    # It WILL SKIP posts with ONLY IMAGES
    posts = list(reddit.subreddit(subreddit).top(limit=num_posts,time_filter="month"))

    # dataframe
    data = {}
    df = pd.DataFrame(data)

    # loop through each post
    for post in posts:
        # reset variables
        post_title = post.title
        post_text = post.selftext
        model = ""
        post_title_label = ""
        post_title_neutral_score = ""
        post_title_negative_score = ""
        post_title_positive_score = ""
        post_text_label = ""
        post_text_neutral_score = ""
        post_text_negative_score = ""
        post_text_positive_score = ""

        upvotes = 0
        downvotes = 0

        # Use the sub method to remove all URLs from the post title
        stripped_title = url_pattern.sub('', post_title)

        # Use the sub method to remove all URLs from the post text
        stripped_post = url_pattern.sub('', post_text)

        # total upvotes for post
        upvotes = int(post.ups)

        # total downvotes for post
        downvotes = int(post.downs)

        # reset model
        model = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis", top_k=None)
        # print('THIS IS THE MODEL',model)

        # run model on the title and grab the the scores for neg,pos, and neu 
        # after the for loop the scores for the titlename will be finalized
        for i in range(3):
            post_title_label = model(stripped_title[:128])[0][i].get('label')
            if post_title_label == 'NEG':
                post_title_negative_score = model(stripped_title[:128])[0][i].get('score')
            elif post_title_label == 'POS':
                post_title_positive_score = model(stripped_title[:128])[0][i].get('score')
            else:
                post_title_neutral_score = model(stripped_title[:128])[0][i].get('score')

        # if the post text contains words
        if stripped_post != "":
            # reset model
            model = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis", top_k=None)

            # run model on the title and grab the the scores for neg,pos, and neu 
            # after the for loop the scores for the text from the post will be finalized
            for i in range(3):
                post_text_label = model(stripped_post[:128])[0][i].get('label')
                if post_text_label == 'NEG':
                    post_text_negative_score = model(stripped_post[:128])[0][i].get('score')
                elif post_text_label == 'POS':
                    post_text_positive_score = model(stripped_post[:128])[0][i].get('score')
                else:
                    post_text_neutral_score = model(stripped_post[:128])[0][i].get('score')

       
        # Append the data to the dataframe
        df = df.append({'post_title': post_title, 'post_text': stripped_post, 'upvotes': upvotes, 'downvotes': downvotes,'post_title_neutral':post_title_neutral_score,'post_title_positive':post_title_positive_score,'post_title_negative':post_title_negative_score,'post_text_neutral':post_text_neutral_score,'post_text_positive':post_text_positive_score,'post_text_negative':post_text_negative_score}, ignore_index=True)

        # counter increment
        counter += 1
        # print counter
        print(counter)

    # Write the dataframe to a CSV file
    # This will create a file called posts.csv in the current working directory, and store the posts(post), their upvotes and downvotes in it.
    filename = subreddit + '.csv'
    df.to_csv(filename, index=False)

# move the files into a folder and zip it function
def move_files():
    # path to the folder containing the csvs
    folder_path = os.getcwd() + '/'

    # path to the folder where the parsed csvs will be stored
    parsed_folder_path = 'Parsed-Subreddits/'

    # remove the file you are were reading from
    os.remove("Top100.csv")

    # check if the parsed folder already exists, if not create it
    if not os.path.exists(parsed_folder_path):
        os.makedirs(parsed_folder_path)

    # loop through all the files in the folder
    for filename in os.listdir(folder_path):
        # check if the file is a csv
        if filename.endswith(".csv"):
            # move the csv file to the parsed folder
            shutil.move(folder_path + filename, parsed_folder_path + filename)
            print(f'{filename} moved to {parsed_folder_path}')
        else:
            print(f'{filename} is not a csv')

    

    # zip the file for upload script
    shutil.make_archive('Parsed-Subreddits', 'zip', 'Parsed-Subreddits')

main()
