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

def main():
    # Create a regular expression pattern to match URLs
    url_pattern = re.compile(r'https?://[^\s]+')

    print(reddit.read_only)

    # Get input from user
    subreddit = input("Enter the subreddit name: ")

    # example for how to get the top 10 submissions in a subreddit inputed by the user
    for submission in reddit.subreddit(subreddit).hot(limit=1):
        print(submission)

        # Get the comments from each post
        submission.comments.replace_more(limit=None)

        # loop through each comment and grab the text, upvotes, and downvotes
        for comment in submission.comments.list()[:10]:
            # reset variables
            stripped_comment = ""
            upvotes = 0
            downvotes = 0

            # Use the sub method to remove all URLs from the comment body
            stripped_comment = url_pattern.sub('', comment.body)
            print(stripped_comment) 

            # total upvotes for comment
            upvotes = comment.ups
            # print(upvotes)

            # total downvotes for comment
            downvotes = comment.downs
            # print(downvotes)

            classifier = pipeline("sentiment-analysis", return_all_scores= True)
            res = classifier(stripped_comment)
            print(res)
            print("")

        # # loop through each comment and grab the text, upvotes, and downvotes
        # for comment in submission.comments.top(limit = 1):
        #     # Use the sub method to remove all URLs from the comment body
        #     stripped_comment = url_pattern.sub('', comment.body)
        #     print(stripped_comment)
        #     print(comment.ups)
        #     print(comment.downs)


        
 
    # # grabbing the comments from a post 
    # for submission in reddit.subreddit(subreddit).hot(limit=5):
    #     print(submission.title)

main()
