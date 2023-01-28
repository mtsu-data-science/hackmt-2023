import praw as praw
import os
from dotenv import load_dotenv
import re
import transformers
from transformers import pipeline
import pandas as pd

load_dotenv()

# authenticating with reddit and setting up an object for interacting with the API

reddit = praw.Reddit(
    client_id=os.environ["reddit_client_id"],
    client_secret=os.environ["reddit_client_secret"],
    user_agent=os.environ["reddit_user_agent"],
)


def main():
    # Create a regular expression pattern to match URLs
    url_pattern = re.compile(r'https?://[^\s]+')

    print(reddit.read_only)

    # Get input from user
    subreddit = input("Enter the subreddit name: ")

    # dataframe
    data = {'comment': [], 'upvotes': [], 'downvotes': []}
    # data = {'comment': [], 'upvotes': [], 'downvotes': [], 'scoring': []}
    df = pd.DataFrame(data)

    # example for how to get the top "x" submissions in a subreddit inputed by the user
    # currently it is grabbing the hottest post in the subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=1):
        print(submission)

        # Get the comments from each post
        submission.comments.replace_more(limit=None)

        # loop through each comment and grab the text, upvotes, and downvotes
        for comment in submission.comments.list():
            # reset variables
            stripped_comment = ""
            scoring =""
            upvotes = 0
            downvotes = 0

            # Use the sub method to remove all URLs from the comment body
            stripped_comment = url_pattern.sub('', comment.body)

            # total upvotes for comment
            upvotes = int(comment.ups)

            # total downvotes for comment
            downvotes = int(comment.downs)

            # model_checkpoint2= "finiteautomata/bertweet-base-sentiment-analysis"

            # distil_bert_model = pipeline(task="sentiment-analysis", model=model_checkpoint2)
            
            # scoring = distil_bert_model(stripped_comment)

            # # Append the data to the dataframe
            # df = df.append({'comment': stripped_comment, 'upvotes': upvotes, 'downvotes': downvotes, 'scoring':scoring}, ignore_index=True)
            df = df.append({'comment': stripped_comment, 'upvotes': upvotes, 'downvotes': downvotes}, ignore_index=True)

            # Write the dataframe to a CSV file
            # This will create a file called comments.csv in the current working directory, and store the comments, their upvotes and downvotes in it.
            df.to_csv('comments.csv', index=False)


main()