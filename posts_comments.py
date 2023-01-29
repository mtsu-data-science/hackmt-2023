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
    subreddit = input("Enter the subreddit name: ")

    # Get number of hottest posts to look at from user input
    num_posts = int(input("Enter the number of subreddit posts to look at: "))

    # grab "x" number of posts in a subreddit and store them in a variable
    # the reasoning is because if you loop in reddit.subreddit(subreddit).hot(limit=num_posts), it returns a generator object, and the generator is being exhausted after the first iteration. This would result in empty post text after the first iterration
    # It WILL SKIP posts with ONLY IMAGES
    posts = list(reddit.subreddit(subreddit).hot(limit=num_posts))

     # dataframe
    data = {'post_title': [],'post_post': [], 'upvotes': [], 'downvotes': [], 'confidence_title':[],' confidence_text':[]}
    # data = {'post(post)': [], 'upvotes': [], 'downvotes': [], 'scoring': []}
    df = pd.DataFrame(data)

    for post in posts:
        # reset variables
        post_title = post.title
        post_text = post.selftext
        model = ""
        title_output = ""
        post_output = ""
        upvotes = 0
        downvotes = 0
        comment_limit = 10

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

        # run model on the title
        title_output = model(stripped_title[:128])

        # if the post text contains words
        if stripped_post != "":
            # reset model
            model = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis", top_k=None)

            # run model on the text of the post
            post_output = model(stripped_post)

        # reset the variables
        comment_counter = 0
        list_comment_scores = []

        # for each post grab all the comments then grab the score in each list and average the neutral,postivive, and negative
        # loop through each comment and grab the text
        for comment in post.comments.list(limit=comment_limit):
            print(comment)
            # reset variables
            post_comment = ""
            comment_scores = ""

            # check if it is a Comment object and only get the comments until it reaches the limit
            if (isinstance(comment, praw.models.Comment) and comment_counter <= comment_limit):

                # reset variables
                stripped_comment = ""

                # Use the sub method to remove all URLs from the comment body
                stripped_comment = url_pattern.sub('', comment.body)

                model = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis", top_k=None)

                # run model on the text of the post
                post_comment = model(stripped_comment[:128])

                list_comment_scores.append(post_comment[0])
                
                comment_counter += 1

                print(comment_counter)
            else:
                break


        # Append the data to the dataframe
        df = df.append({'post_title': post_title, 'post_post': stripped_post, 'upvotes': upvotes, 'downvotes': downvotes, 'confidence_title': title_output,'confidence_text':post_output,'comment_scores':list_comment_scores}, ignore_index=True)

    # Write the dataframe to a CSV file
    # This will create a file called posts.csv in the current working directory, and store the posts(post), their upvotes and downvotes in it.
    df.to_csv('posts.csv', index=False)

main()


# get the negative, neutral, and positive scores

                # negative = None
                # neutral = None
                # positive = None

                # for d in post_comment[0]:
                #     if d['label'] == 'NEG':
                #         negative = d['score']
                #     elif d['label'] == 'NEU':
                #         neutral = d['score']
                #     elif d['label'] == 'POS':
                #         positive = d['score']
                # # negative  = post_comment[0][0]
                # # neutral = post_comment[0][1]
                # # positive = post_comment[0][2]
                # print('negative',negative)
                # print('neutral',neutral)
                # print('positive',positive)
                # print("")