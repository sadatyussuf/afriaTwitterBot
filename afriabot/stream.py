import tweepy
import time
# # print('*******in stream file**********')
# class AfriaListener(tweepy.Stream):
#     def on_status(self, status): 
#         #code to run each time the stream receives a status
#         print('*******start process**********')
#         print(status.text)
#     def on_error(self, status_code):
#         if status_code == 420:
#             #returning False in on_data disconnects the stream
#             print('Error Occurred')
#             return False

class AfriaClientListener(tweepy.StreamingClient):
    tweets = []
    limit = 55
    def on_connect(self):
        # return super().on_connect()
        print('connected')

    def on_tweet(self, tweet): 

        #code to run each time the stream receives a status
        if tweet.referenced_tweets == None:
            # print('*******start process**********')
            print(f'Text = {tweet.text}')
            self.tweets.append(tweet.text)
            if len(self.tweets) == self.limit:
                # self.disconnect()
                pass
            time.sleep(1)
    def on_data(self, raw_data):
        print(raw_data)
        # return super().on_data(raw_data)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            print('Error Occurred')
            return False