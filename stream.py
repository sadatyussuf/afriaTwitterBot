import tweepy
import time
import json
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
        if raw_data.referenced_tweets == None:
            print('*********************')
            print(raw_data)
        # return super().on_data(raw_data)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            print('Error Occurred')
            return False


# def delete_Client_rules(stream_tweet):
#     rule_ids = []
#     result = stream_tweet.get_rules()
#     if result is None or result.data is None:
#         return None
#     for rule in result.data:
#         print(f"rule marked to delete: {rule.id} - {rule.value}")
#         rule_ids.append(rule.id)
#     if(len(rule_ids) > 0):
#         stream_tweet.delete_rules(rule_ids)
#         stream_tweet = AfriaClientListener(BEARER_TOKEN)
#     else:
#         print("no rules to delete")

