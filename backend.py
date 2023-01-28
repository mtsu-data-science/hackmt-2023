import praw as praw
import os
from dotenv import load_dotenv
import re
import transformers
from transformers import pipeline

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
    print(reddit.read_only)

    # Get subreddit from user input
    subreddit = input("Enter the subreddit name: ")

    # Get number of top posts to look at from user input
    num_posts = int(input("Enter the number of subreddit posts to look at: "))

    # Get number of comments from a post to look at from user input
    # num_comments = int(input("Enter the number of comments to look at: "))

    grab_posts(subreddit,num_posts)


def grab_posts(subreddit,num_posts):
    # grab all the posts in a subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=num_posts):
        # print(submission)

        # reset variables
        submission = ""
        upvotes = 0
        downvotes = 0

        # Use the sub method to remove all URLs from the submission text
        stripped_submission = url_pattern.sub('', submission.selftext)
        print('this is the submission text: ',stripped_submission) 

        # # total upvotes for submission
        # upvotes = submission.ups
        # print(upvotes)

        # # total downvotes for submission
        # downvotes = submission.downs
        # print(downvotes)

        # loop through each comment and grab the text, upvotes, and downvotes
        for comment in submission.comments.top(limit = 1):
            # Use the sub method to remove all URLs from the comment body
            stripped_comment = url_pattern.sub('', comment.body)
            print(stripped_comment)
            print(comment.ups)
            print(comment.downs)


        
 
    # # grabbing the comments from a post 
    # for submission in reddit.subreddit(subreddit).hot(limit=5):
    #     print(submission.title)

main()
