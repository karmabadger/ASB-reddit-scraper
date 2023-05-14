from configs.db import get_mongo_client, query_str

import json

# from src.mongo.schemas import post_schema

from src.mongo.controllers.reddit_posts_controller import RedditPostsController
from src.mongo.services.reddit_posts_service import RedditASBPostService

client = get_mongo_client()

print(query_str)

import jsonschema
from src.mongo.schemas.posts.reddit_post import post_schema

# db.createCollection('asb_posts',
#     validator={
#         '$jsonSchema': post_schema
#     }
# )



reddit_service = RedditASBPostService(client, client.get_database("reddit_posts"), 'asb_posts')

reddit_controller = RedditPostsController(reddit_service)

mock_data_file_path = 'mock_data/reddit_post1.json'

mock_data = json.load(open(mock_data_file_path))

print(mock_data)

mock_data['author'] = 'fren2'


def push_to_mongo(post_id, data):
    res = reddit_service.find_one_and_replace({"post_id": post_id}, data)

    if not res:
        res = reddit_service.insert_one(data)

res = reddit_service.find_one_and_replace({"post_id": "ggbmnvm"}, mock_data)

if not res:
    print("inserted")
    res = reddit_service.insert_one(mock_data)
else:
    print("updated")
    # res = reddit_service.find_one_and_replace({"post_id": "ggbmnvm"}, mock_data)

print(res)


# unique = 
print(len(client['reddit_posts']['asb_posts'].distinct('post_id')))

# schema = {
#     "type": "object",
#     "properties": post_schema
# }

# print("res", jsonschema.validate(instance=mock_data, schema=schema))
# print("res", jsonschema.validate(instance={"fdsfds": "fdsfds"}, schema=schema))

# reddit_service.insert_one(mock_data)




# from src.reddit.getposts import *


# print(reddit)

# subreddit = reddit.subreddit("altstreetbets")


