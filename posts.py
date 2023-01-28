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

# Create a regular expression pattern to match URLs
url_pattern = re.compile(r'https?://[^\s]+')

def main():
    # Get subreddit from user input
    subreddit = input("Enter the subreddit name: ")

    # Get number of hottest posts to look at from user input
    num_posts = int(input("Enter the number of subreddit posts to look at: "))

    # call the grab_posts function
    grab_posts(subreddit,num_posts)


def grab_posts(subreddit,num_posts):

    # grab "x" number of posts in a subreddit and store them in a variable
    # the reasoning is because if you loop in reddit.subreddit(subreddit).hot(limit=num_posts), it returns a generator object, and the generator is being exhausted after the first iteration. This would result in empty submission text after the first iterration
    # It WILL SKIP posts with ONLY IMAGES
    posts = list(reddit.subreddit(subreddit).hot(limit=num_posts))

     # dataframe
    data = {'submission_title': [],'submission_post': [], 'upvotes': [], 'downvotes': [], 'confidence_title':[],' confidence_text':[]}
    # data = {'submission(post)': [], 'upvotes': [], 'downvotes': [], 'scoring': []}
    df = pd.DataFrame(data)

    for submission in posts:
        # reset variables
        submission_title = submission.title
        submission_text = submission.selftext
        model = ""
        title_output = ""
        post_output = ""
        upvotes = 0
        downvotes = 0

        # Use the sub method to remove all URLs from the submission title
        stripped_title = url_pattern.sub('', submission_title)

        # Use the sub method to remove all URLs from the submission text
        stripped_submission = url_pattern.sub('', submission_text)

        # total upvotes for submission
        upvotes = int(submission.ups)

        # total downvotes for submission
        downvotes = int(submission.downs)

        # reset model
        model = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis", return_all_scores = True)
        print('THIS IS THE MODEL',model)

        # run model on the title
        title_output = model(stripped_title)
        print('THIS IS THE MODEL AFTER',model)

        # if the post text contains words
        if stripped_submission != "":
            # reset model
            model = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis", return_all_scores = True)

            # run model on the text of the post
            post_output = model(stripped_submission)
       
        # Append the data to the dataframe
        df = df.append({'submission_title': submission_title, 'submission_post': stripped_submission, 'upvotes': upvotes, 'downvotes': downvotes, 'confidence_title': title_output,'confidence_text':post_output}, ignore_index=True)

        # Write the dataframe to a CSV file
        # This will create a file called posts.csv in the current working directory, and store the submissions(post), their upvotes and downvotes in it.
        df.to_csv('posts.csv', index=False)

main()
