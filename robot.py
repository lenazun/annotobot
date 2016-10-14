
import json
import requests
from TwitterAPI import TwitterAPI
import os

api = TwitterAPI(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
                 consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
                 access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
                 access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))


def hrequest():

    url = 'http://hypothes.is/api/search?limit=10'
    response = requests.get(url)
    response.raise_for_status()

    annotations = json.loads(response.text)

    return annotations


def make_tweets(annotations):

    tweets_list = []

    for i in annotations['rows']:

        try:
            contextlink = i['uri']['incontext']
            print contextlink
        except:
            pass

        try:
            title = i['document']['title']
            title = (title[:75] + '..') if len(title) > 75 else title
        except:
            title = "A document"

        try:
            tags = i['tags']
            hashtags = ""
            for i in tags:
                i = i.replace(" ", "")
                hashtags += " #"+i

        except:
            hashtags = ""

        tweet = 'Annotated: ' + title + ' ' + contextlink + hashtags

        tweets_list.append(tweet)

    return tweets_list

#TODO Fix the backoff so it works nicely and dedups entries
def send(tweets_list, x):

    last_item = tweets_list[x]

    r = api.request('statuses/update', {'status': last_item})
    print (r.status_code)

    if (r.status_code) is not 200:
        try:
            send(tweets_list, (x+1))
        except:
            pass


def main():
    send(make_tweets(hrequest()), 0)


if __name__ == '__main__':
    main()
