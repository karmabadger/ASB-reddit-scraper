from src.mongo.services.service import Service

from src.mongo.schemas.posts.reddit_post import post_schema
class RedditASBPostService(Service):
    """
    Service class for the Reddit ASB Post Service
    """

    def __init__(self, mongo_client, mongo_db, mongo_collection):
        """
        Constructor for the Reddit ASB Post Service
        :param reddit_post_service: The Reddit Post Service
        :type reddit_post_service: RedditPostService
        """
        super().__init__(mongo_client, mongo_db, mongo_collection, post_schema)

    

    
