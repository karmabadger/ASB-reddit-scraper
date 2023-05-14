
from typing import Counter
from configs.db import get_mongo_client
import requests
import praw
import os

import time

from src.mongo.controllers.reddit_posts_controller import RedditPostsController
from src.mongo.services.reddit_posts_service import RedditASBPostService

from dotenv import load_dotenv
load_dotenv()


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

    # print(pushshift_url)
    r = requests.get(pushshift_url)
    # print(r)

    return r.json()

def get_submission_reddit(praw_client, submission_id):
    submission = praw_client.submission(id=submission_id)

    return submission


def get_all_submissions_into_mongodb(naughty_list, start_after, mongo_client, reddit_service, reddit_controller, reddit_client):

    num_batches = 0

    start_time = time.time()

    cur_start_after = start_after

    next_start_after = start_after
    num_posts = 0
    
    posts_in_batch = 0

    while cur_start_after < start_time:
        print("Batch", num_batches, "Getting submissions after", cur_start_after)
        while True:
            try:
                res = get_submission_pushshift(after=cur_start_after)
            except:
                print("Error getting batch", num_batches, cur_start_after)
                continue
            break
        # print(res['data'][0])
        # print(type(res['data']))
        # print(len(res['data']))

        if (res == None or len(res['data']) == 0):
            break

        
        for post in res['data']:
            breakFor = False
            try:
                real_post = get_submission_reddit(reddit, post['id'])
            except:
                breakFor = True
                print("Error getting post", post['id'])
                continue
            # if breakFor == True:
            #     continue

            if real_post.author == None:
                print("No author for post", post['id'])
                continue

            if real_post.author.name in naughty_list:
                print("Naughty author", real_post.author.name)
                continue

            if (real_post.removed_by_category == None):

                data = {
                    "post_id": post['id'],
                    "author": post['author'],
                    "link": real_post.url,
                    "upvotes": real_post.score,
                    "created_utc": post['created_utc'],
                    "submission_type": "submission"
                }

                mongo_counter = 0
                while mongo_counter < 10:
                    try:
                        print("Trying to push to mongo", data)
                        push_to_mongo(post['id'], data)
                        num_posts += 1
                        posts_in_batch+=1
                    except:
                        print("Error pushing to mongo will try again", data)
                        mongo_counter += 1
                


                # get all the comments
                real_post.comments.replace_more(limit=None)
                for comment in real_post.comments.list():
                    if comment.author == None:
                        print("No author for comment", comment.id)
                        continue

                    if comment.author.name in naughty_list:
                        print("Naughty author", comment.author.name)
                        continue

                    if comment.banned_by == None:
                        data = {
                            "post_id": comment.id,
                            "author": comment.author.name,
                            "link": comment.permalink,
                            "upvotes": comment.score,
                            "created_utc": comment.created_utc,
                            "submission_type": "comment"
                        }

                        # push_to_mongo(post['id'], data)
                        mongo_counter = 0
                        while mongo_counter < 10:
                            try:
                                print("Trying to push to mongo", data)
                                push_to_mongo(post['id'], data)
                                num_posts += 1
                                posts_in_batch+=1
                            except:
                                print("Error pushing to mongo will try again", data)
                                mongo_counter += 1
                        
                        
                        print("Comment", comment.id)
                        num_posts += 1
                        posts_in_batch+=1
                    else:
                        print("Comment Banned by", comment.banned_by)
                        continue
            else:
                print("Post removed by category", real_post.removed_by_category)
                continue 


            next_start_after = post['created_utc']
            cur_time = time.time()
            diff_time = cur_time - start_time
            print("finished post", real_post.id, "in", diff_time, "seconds. Number of posts:",num_posts, ". Average time:", diff_time / num_posts)

            start_time = cur_time

        
            num_posts = 0

        if next_start_after == None:
            print("No more posts")
            break

        if next_start_after == cur_start_after:
            next_start_after = cur_start_after + 1

        cur_start_after = next_start_after
            
        print("finished this batch, next batch starts with time:", cur_start_after, posts_in_batch)
        num_batches += 1
        
        posts_in_batch = 0
        

       

client = get_mongo_client()

reddit_service = RedditASBPostService(client, client.get_database("reddit_posts"), os.environ.get("MONGO_COLLECTION"))

reddit_controller = RedditPostsController(reddit_service)

# this is 2020/12/13 00:00:00 one day before the beginning of the subreddit
# start_time = 1607835600

start_time = 1638375382
get_all_submissions_into_mongodb([], start_time, client, reddit_service, reddit_controller, reddit)
