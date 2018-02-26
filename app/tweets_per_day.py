import pandas as pd
import sys

from pandas_highcharts.core import serialize
from collections import namedtuple,defaultdict
from random import randint
from textblob import TextBlob

from app import app, db
from app.models import User, Tweet


def get_date(column):
    column = str(column)
    return pd.to_datetime(column.split()[0])

chart = namedtuple('chart', 'data name statistics')

def get_highchart(data):
    # print(data.head())
    # print(data.columns) 
    data['date'] = data['created_at'].apply(get_date)
    # print(data.head())
    # print(data.tail())
    tweets_per_day = data.groupby('date').count()['id_str']
    print(tweets_per_day.describe())
    statistics = str(tweets_per_day.describe())

    return chart(serialize(pd.DataFrame(tweets_per_day), render_to='my-chart', \
                output_type='json', title='Tweets Per Day', \
                parse_dates='date', kind='bar', zoom='xy'), 'my-chart', statistics)




def sentiment_analysis(polarity):
    if polarity < 0:
        return "negative"
    elif polarity == 0:
        return "neutral"
    else:
        return "positive"
    

def get_sentiment(tweets):
    sentiments = defaultdict(set)
    print(type(tweets))

    for tweet in tweets:
        text = tweet.text
        blob = TextBlob(text)
        sent = sentiment_analysis(blob.sentiment.polarity)
        sentiments[sent].add(text)
    
    total = sum(len(i) for i in sentiments.values())

    perc_pos = len(sentiments["positive"]) / total * 100
    perc_neg = len(sentiments["negative"]) / total * 100
    perc_neu = len(sentiments["neutral"]) / total * 100

    print("Analyzed {} tweets".format(total))
    print("Positive: {:.2f}%".format(perc_pos))
    print("Negative: {:.2f}%".format(perc_neg))
    print("Neutral: {:.2f}%".format(perc_neu))

    return ["Positive: {:.2f}%".format(perc_pos), "Negative: {:.2f}%".format(perc_neg), "Neutral: {:.2f}%".format(perc_neu)]
    