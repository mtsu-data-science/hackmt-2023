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

    # Get number of hottest posts to store from user input
    num_posts = int(input("Enter the number of subreddit posts to store: ")
    )

    # Get number of hottest comments from each post to store from user input
    num_comments = int(input("Enter the number of comments from each subreddit that you want store out of {} subreddit posts: ".format(num_posts)))

    grab_posts(subreddit,num_posts,num_comments)

#  this function grabs the number of posts specified by the user 
def grab_posts(subreddit,num_posts,num_comments):

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
        scoring = ""

        # Use the sub method to remove all URLs from the submission text
        stripped_submission = url_pattern.sub('', submission_text)

        if stripped_submission != "":
            # print('this is the submission text: ',stripped_submission) 

            # total upvotes for submission
            upvotes = int(submission.ups)
            # print(upvotes) 

            # total downvotes for submission
            downvotes = int(submission.downs)
            # print(downvotes)

            # # Append the data to the dataframe
            # df = df.append({'submission(post)': stripped_submission, 'upvotes': upvotes, 'downvotes': downvotes, 'scoring':scoring}, ignore_index=True)
            df = df.append({'submission(post)': stripped_submission, 'upvotes': upvotes, 'downvotes': downvotes}, ignore_index=True)

            # Write the dataframe to a CSV file
            # This will create a file called posts.csv in the current working directory, and store the submissions(post), their upvotes and downvotes in it.
            df.to_csv('posts.csv', index=False)

            # print(num_comments,submission)
            # grab the number of comments from the current submission post
            get_comments(num_comments,submission)


def get_comments(num_comments,submission):
    # dataframe
    data = {'comment': [], 'upvotes': [], 'downvotes': []}
    # data = {'comment': [], 'upvotes': [], 'downvotes': [], 'scoring': []}
    df = pd.DataFrame(data)

    # loop through each comment and grab the text, upvotes, and downvotes
    for comment in submission.comments.list():
        print(comment)
        # reset variables
        stripped_comment = ""
        upvotes = 0
        downvotes = 0
        counter = 1
        # scoring = ""

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
        # This will create a file called comments{counter}.csv in the current working directory, and store the comments, their upvotes and downvotes in it.
        df.to_csv('comments{}.csv'.format(counter), index=False)

        counter += 1
        

main()


