
from configs.db import get_mongo_client, query_str

import json

import requests

import praw

import os

# from src.mongo.schemas import post_schema

from src.mongo.controllers.reddit_posts_controller import RedditPostsController
from src.mongo.services.reddit_posts_service import RedditASBPostService



reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    password=os.environ.get("REDDIT_PWD"),
    user_agent=os.environ.get("REDDIT_USER_AGENT"),
    username=os.environ.get("REDDIT_USER"),
)

def push_to_mongo(post_id, data):
    res = reddit_service.find_one_and_replace({"post_id": post_id}, data)

    if not res:
        res = reddit_service.insert_one(data)


def get_submission_pushshift(after):
    pushshift_url = "https://api.pushshift.io/reddit/submission/search/?after=%s&subreddit=Altstreetbets&size=100&fields=id,author,num_comments,full_link,score,title,created_utc&sort=asc&sort_type=created_utc" % after

    print(pushshift_url)
    r = requests.get(pushshift_url)
    print(r)

    return r.json()

def get_submission_reddit(praw_client, submission_id):
    submission = praw_client.submission(id=submission_id)

    return submission


def check_if_removed(submission):
    if submission.removed:
        return True

    return False

client = get_mongo_client()

reddit_service = RedditASBPostService(client, client.get_database("reddit_posts"), 'asb_posts')

reddit_controller = RedditPostsController(reddit_service)


# res = get_submission_pushshift(after=1575294400)

# print(res['data'][0])
# print(type(res['data']))
# print(len(res['data']))

# for post in res['data']:
    
#     real_post = get_submission_reddit(reddit, post['id'])

#     data = {
#         "post_id": post['id'],
#         "author": post['author'],
#         "link": real_post['full_link'],
#         "upvotes": real_post['score'],
#         "created_utc": post['created_utc'],
#         "submission_type": "submission"
#     }

#     push_to_mongo(post['id'], data)

real_post = reddit.submission(id='qwk95s')

print(real_post.url)
print(real_post.removed_by_category)

# get all the comments
real_post.comments.replace_more(limit=None)
for comment in real_post.comments.list():
    print(comment)
    print(comment.banned_by)
    print(comment.author.name)
    print(comment.score)
    print(comment.created_utc)
    print(comment.id)
    # print(comment.full_link)