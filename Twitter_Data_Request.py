#importing packages
import sys
import datetime
import tweepy
import pandas as pd
import yaml

#access codes
conf = yaml.load(open('config.yml'))
consumer_key = conf['user']['consumer_key']
consumer_secret = conf['user']['consumer_secret']
access_token = conf['user']['access_token']
access_token_secret = conf['user']['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#creating constants
data = []
search_number = 10

#defining class
class CustomStreamListener (tweepy.StreamListener):

    def __init__(self, api = None):
        super(CustomStreamListener, self).__init__()
        self.num_tweets = 0

    def on_status(self, status):
        global twitter_df
        try:
            #getting data
            user = status.user.screen_name
            tweet = status.text
            coordinates = status.place.bounding_box.coordinates
            date_utc = status.created_at
            h_m_s_utc = (str(status.created_at.hour)) + ':' + (str(status.created_at.minute))+ ':' +(str(status.created_at.second))
            date_est = datetime.datetime.now()
            h_m_s_est = (str(date_est.hour)) + ':' + (str(date_est.minute))+ ':' + (str(date.est.second))

            #adding data
            data.append([user, tweet, date_utc, coordinates])

            #print data
            print (user)
            print (tweet)
            print (coordinates)

            self.num_tweets +=1

            #to end data collection 
            if self.num_tweets < search_number:
                return True
            else:
                if self.num_tweets < search_number:
                    return True
                else:
                    return False
        except:
            pass

    #defining errors   
    def on_error (self, status_code):
        print(sys.stderr, 'Encoutered error with status code:', status_code)
        return True
    
    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True

#executing script
listener = tweepy.streaming.Stream(auth, CustomStreamListener())
print("Looking for tweets...")

listener.filter(track=['Raptors'])

#saving data

df = pd.DataFrame(data, columns=["user", "tweet", "date", "coordinates"])
print (df) 
df.to_csv('Test1.csv', encoding ='utf-8')
print("Tweet data frame successfully saved!")


