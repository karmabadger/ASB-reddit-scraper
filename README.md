# ASB Posts


getting all the posts and comments from r/Altstreetbets into a mongoDB server

## Instructions
1. Please install all of the required packages in requirements.txt using ```pip3 install -r requirements.txt```
2. Please configure your .env file first as indicated from .env.example
3. Run ```python3 main.py``` in the command line. This will run the script and get all the submissions first in batch of 100 sorted by time since the inception of the subreddit, then get the field and the details of the submission from reddit (using PRAW) and then lastly get all the comments of each of the submissions (using PRAW). Each post or comment will be automatically sent to the mongodb server.


Details on which timestamp it is currently at and how long it is taking so far will be pushed to the console.
To log those into a file use ```python3 main.py > log.txt```

