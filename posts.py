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

    # Get number of top posts to look at from user input
    num_posts = int(input("Enter the number of subreddit posts to look at: "))

    grab_posts(subreddit,num_posts)


def grab_posts(subreddit,num_posts):

    # grab "x" number of posts in a subreddit and store them in a variable
    # the reasoning is because if you loop in reddit.subreddit(subreddit).hot(limit=num_posts), it returns a generator object, and the generator is being exhausted after the first iteration. This would result in empty submission text after the first iterration
    # It WILL SKIP posts with ONLY IMAGES
    posts = list(reddit.subreddit(subreddit).hot(limit=num_posts))

     # dataframe
    data = {'submission(post)': [], 'upvotes': [], 'downvotes': []}
    # data = {'submission(post)': [], 'upvotes': [], 'downvotes': [], 'scoring': []}
    df = pd.DataFrame(data)

    for submission in posts:
        # reset variables
        submission_text = submission.selftext
        stripped_submission = ""
        upvotes = 0
        downvotes = 0

        # Use the sub method to remove all URLs from the submission text
        stripped_submission = url_pattern.sub('', submission_text)

        if stripped_submission != "":
            print('this is the submission text: ',stripped_submission) 

            # total upvotes for submission
            upvotes = int(submission.ups)
            print(upvotes)

            # total downvotes for submission
            downvotes = int(submission.downs)
            print(downvotes)

            # # loop through each comment and grab the text, upvotes, and downvotes
            # for comment in submission.comments.top(limit = 1):
            #     # Use the sub method to remove all URLs from the comment body
            #     stripped_comment = url_pattern.sub('', comment.body)
            #     print(stripped_comment)
            #     print(comment.ups)
            #     print(comment.downs)

            # # Append the data to the dataframe
            # df = df.append({'submission(post)': stripped_submission, 'upvotes': upvotes, 'downvotes': downvotes, 'scoring':scoring}, ignore_index=True)
            df = df.append({'submission(post)': stripped_submission, 'upvotes': upvotes, 'downvotes': downvotes}, ignore_index=True)

            # Write the dataframe to a CSV file
            # This will create a file called posts.csv in the current working directory, and store the submissions(post), their upvotes and downvotes in it.
            df.to_csv('posts.csv', index=False)

main()
