import tweepy
from dotenv import load_dotenv
from flask import Flask, render_template,  redirect


import os
import logging
import time
from typing import List
import random

app = Flask(__name__)



load_dotenv()
logging.basicConfig(level=logging.DEBUG, filename="msg.log", filemode='w',
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")


auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)

client = tweepy.Client(BEARER_TOKEN)

#* Create API object
api = tweepy.API(auth,wait_on_rate_limit=True)

#* Authenticate to Twitter
def authenticate():
    if not api.verify_credentials():
        logging.error("Authentication Failed",exc_info=True)
        return False
    else:
        logging.info("Authentication Success!")
        return True

def getUserID(users:List):
    users_id = []
    for t_user in users:
        user = api.get_user(screen_name=t_user)
        users_id.append(user.id_str)
    # print(users_id)
    return users_id[0]

# users = ['yussufSadat','ing_tagoe,'pythontrending']
users = ['yussufSadat']

# fileName
FILE_NAME = 'last.txt'

def read_last_seen(FILE_NAME):
    # print('reading file...')
    file_read = open(FILE_NAME, 'r') #open the file in read mode
    last_seen_id = file_read.read().strip() #read the Tweet ID as an integer
    if last_seen_id == '':
        # print('None')
        # print('reading done...')
        return None
    last_seen_id = int(last_seen_id)  #read the Tweet ID as an integer
    file_read.close() #close file reader
    # print('reading done...')
    return last_seen_id #return the result

def store_last_seen(FILE_NAME, last_seen_id):
    # print('writing file...')
    file_write = open(FILE_NAME, 'w') #open the file in write mode
    file_write.write(str(last_seen_id)) #write the ID as a string
    file_write.close() #close file writer
    # print('writing done...')
    return #return void

def retrieve_tweet_id():
    user_id = getUserID(users)

    if  read_last_seen(FILE_NAME) is None:
        resp =  client.get_users_tweets(id=user_id,max_results=5)
        recent_tweet_id = resp.data[0].id
        print(recent_tweet_id)
        store_last_seen(FILE_NAME, recent_tweet_id)

    if  read_last_seen(FILE_NAME) is not None:
        recent_tweet_id = read_last_seen(FILE_NAME)
        new_tweet =  client.get_users_tweets(id=user_id,since_id = recent_tweet_id)
        if new_tweet.data is None:
            print('*'*20)
            print('Nothing to retrieve')

        if new_tweet.data is not None:
            print(f' ID => {new_tweet.data[0].id}, TEXT => {new_tweet.data[0].text}')
            recent_tweet_id = new_tweet.data[0].id
            store_last_seen(FILE_NAME, recent_tweet_id)
            return recent_tweet_id 

def like_and_retweet_tweet():
    id = retrieve_tweet_id()
    # print(id)
    if id is not None:
    # client.like(id)
        api.create_favorite(id)
        api.retweet(id)
        print('Liked and Retweeted!!')

def retweet_tweet():
    id = retrieve_tweet_id()
    if id is not None:
        api.retweet(id)
        print('Retweeted!!')

time_intervals = [5,15,25]

@app.route('/')
def main_flask_app():
    return render_template('index.html')

@app.route('/tweet')
def main():
    if authenticate():
        print('Authentication is True')
        while True:
            print('listening to a tweet.....')
            like_and_retweet_tweet()

            random_time = random.choice(time_intervals)
            time.sleep(random_time)
    return redirect('/')


# main()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)