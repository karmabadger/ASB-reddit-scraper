import praw
import os


from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"), client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                     user_agent=os.getenv("REDDIT_USER_AGENT"), username=os.getenv("REDDIT_USER"), password=os.getenv("REDDIT_PWD"))


def get_posts(subreddit, limit):
    posts = []
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        posts.append(submission)
    return posts