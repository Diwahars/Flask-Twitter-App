from datetime import datetime
import pandas as pd

from flask import render_template, flash, redirect, url_for

from app import app, db
from app.forms import TwitterSearchForm
from app.models import User, Tweet
from app.twitter_data import get_all_tweets, get_user
from app.tweets_per_day import get_highchart, get_sentiment

@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = TwitterSearchForm()
    if form.validate_on_submit():
        flash('Retrieved Twitter data of {}'.format(form.twitter_handle.data))
        
        # check if user is already in database and then do some stuff      
        user_handle = form.twitter_handle.data.lower()
        user = User.query.filter_by(name=user_handle).first()        

        if user is None:
            new_user = get_user(user_handle)
            new_user = User(id=new_user.id_str, name=new_user.name.lower(), url=new_user.url,
                                profile_image_url_https=new_user.profile_image)
            db.session.add(new_user)
            db.session.commit()
            tweets = get_all_tweets(user_handle)
        else:
            update_user = get_user(user_handle)
            user.profile_image_url_https = update_user.profile_image
            user.url = update_user.url
            db.session.commit()
            last_tweet_date = user.last_tweet().created_at
            tweets = get_all_tweets(user_handle, last_tweet_date)
         
        # save user tweets in database
        for tweet in tweets:
            stored_tweet = Tweet.query.filter_by(id_str=tweet.id_str).first()
            if stored_tweet is None:
                new_tweet = Tweet(id_str=tweet.id_str, created_at=tweet.created_at,
                                        text=tweet.text, user_id=user.id)
                db.session.add(new_tweet)
                db.session.commit()
        
        tweets = Tweet.query.filter_by(user_id=user.id).statement
        tweets = pd.read_sql(tweets, db.engine, parse_dates=True)
        
        user_tweets = user.tweeted_tweets()
        tweets_len = len(user_tweets)
        
        charts = get_highchart(tweets)
        #sentiment = get_sentiment(user_tweets)

        return render_template('index.html', title='Twitter Analytics',
                            form=form, tweets=user_tweets, chart=charts,
                            user=user, tweets_len=tweets_len)

    return render_template('index.html', title='Twitter Analytics',
                            form=form)

                