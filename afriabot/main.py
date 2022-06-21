import tweepy
from dotenv import load_dotenv

import os
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG, filename="msg.log", filemode='w',
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")


auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)


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

authenticate()



