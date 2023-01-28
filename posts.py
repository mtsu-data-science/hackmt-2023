import praw as praw
import os
from dotenv import load_dotenv
import re
import transformers
from transformers import pipeline
import pandas as pd
import emoji
import warnings

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
    # Get subreddit from user input
    # subreddit = input("Enter the subreddit name: ")

    # Get number of hottest posts to look at from user input
    num_posts = int(input("Enter the number of subreddit posts to look at: "))

    txt_df = pd.read_csv("first100 (2).csv")

    for subreddit in txt_df["subreddit"]:
        print(subreddit)
        # call the grab_posts function
        grab_posts(subreddit,num_posts)



# this function grabs a number of posts from a subreddit
def grab_posts(subreddit,num_posts):
    # counter
    counter = 0

    # grab "x" number of posts in a subreddit and store them in a variable
    # the reasoning is because if you loop in reddit.subreddit(subreddit).hot(limit=num_posts), it returns a generator object, and the generator is being exhausted after the first iteration. This would result in empty post text after the first iterration
    # It WILL SKIP posts with ONLY IMAGES
    posts = list(reddit.subreddit(subreddit).hot(limit=num_posts))

    # dataframe
    data = {'post_title': [],'post_post': [], 'upvotes': [], 'downvotes': [], 'confidence_title':[],' confidence_text':[]}
    df = pd.DataFrame(data)

    # loop through each post
    for post in posts:
        # reset variables
        post_title = post.title
        post_text = post.selftext
        model = ""
        title_scores = ""
        post_scores = ""
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

        # run model on the title
        title_scores = model(stripped_title)
        # print('THIS IS THE MODEL AFTER',model)

        # if the post text contains words
        if stripped_post != "":
            # reset model
            model = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis", top_k=None)

            # run model on the text of the post
            post_scores = model(stripped_post[:128])
       
        # Append the data to the dataframe
        df = df.append({'post_title': post_title, 'post_text': stripped_post, 'upvotes': upvotes, 'downvotes': downvotes, 'confidence_score_title': title_scores,'confidence_score_text':post_scores}, ignore_index=True)

        # counter increment
        counter += 1
        # print counter
        print(counter)

    # Write the dataframe to a CSV file
    # This will create a file called posts.csv in the current working directory, and store the posts(post), their upvotes and downvotes in it.
    filename = subreddit + '.csv'
    df.to_csv(filename, index=False)

main()
