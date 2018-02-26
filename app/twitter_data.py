import tweepy
from collections import namedtuple
from datetime import datetime

#Twitter API credentials
from app.twitter_access import CONSUMER_KEY, CONSUMER_SECRET 
from app.twitter_access import ACCESS_TOKEN, ACCESS_TOKEN_SECRET

USER = namedtuple('User', 'id_str name url profile_image')
TWEET = namedtuple('Tweet', 'id_str created_at text')

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def get_user(handle):
    # gather user details
    user = api.get_user(handle)
    return USER(user.id_str, user.screen_name, user.url, user.profile_image_url_https)


def get_all_tweets(handle, date=None):
    all_tweets = []
    
    new_tweets = api.user_timeline(handle,count=200)

    #save most recent tweets
    all_tweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
    # todo only collect the max tweets of user

    while len(new_tweets) > 0:
        # only download latest tweets
        if date is not None:
            if all_tweets[-1].created_at < date:
                print("Falsing")
                break

        print("getting tweets before {}".format(oldest))
        
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(handle,count=200,max_id=oldest)
        
        # save most recent tweets
        all_tweets.extend(new_tweets)
        
        # update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1
        
        print("...{} tweets downloaded so far".format(len(all_tweets)))
        print(all_tweets[-1].created_at)       

    user_tweets = [TWEET(tweet.id_str, tweet.created_at, tweet.text) for tweet in all_tweets]
    return user_tweets

    



