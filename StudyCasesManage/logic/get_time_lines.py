import threading
import time
import tweepy
import sys
import json
from .dr_dbfuncitons import *


# PAMEALMEIDAS / Twitter Credentials
# Access Token for Twitter App
access_token = "57173854-fmeivcjvIWtNbHH0AqXnRteGzxWMGgkr88HVxVfEG"
access_token_secret = "LIHkXdvM1ihAYjPCSWhRXBCpWZseDnmeLX7pdvXitJpiI"
# Consumer Keys
consumer_key = "Fvi32GeHQwZZ8rxnX5T4xdvUq"
consumer_secret = "xRAfWVs0D3UM0Va3548Fdto6YgTbAtrKIsIYvNSreAFkJDV0mY"

"""
# DANIEL RIOFRIO / Twitter Credentials
# Access Token for Twitter App
access_token = "37859688-isXNFc4dFvOa0uHlc14jnuqcKqQKLjExJHKx6EWqu"
access_token_secret = "TiJ4VLrXIq0OxGo90QJEP8RG0FxPoLrXZ7HynTqClv4kx"
# Consumer Keys
consumer_key = "7v5mgmO1TjCexxCmVH2uocG7D"
consumer_secret = "Po5Jii1Ab5oze6IR5fTuqXYZ6sm2o8tuXS8lfVKjRTSzBsIgh0"
"""

# CS UNM OTF / Twitter Credentials
# Access Token for Twitter App
# access_key = "769272401284694016-9WzG7sGQTzKWJCIvNtSunp5XvofTV5h"
# access_secret = "n6SvQQCBqnjRCoUKehTyvRE7JWWXFv4uyrjafqVHJVQKZ"
# Consumer Keys
# consumer_key = "3q3B5oXfkuIeuRCK6AY4JRNbo"
# consumer_secret = "A4bDHhILUaLXpZKxHC2u2Na084wkrFklL9PXYLNlTSVsA0dOD2"

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# creation of the actual interface, using authentication
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True, compression=True)
errorpath = './error/error.log'


def pa_setserverconn():
    server = "localhost"
    db = "elecciones2019"
    user = "elect2019"
    password = "elecciones2019"
    conn = dr_establishConn(server, db, user, password)
    return conn


def getTimeline2019(n, screen_name):
    counter429 = 0
    conn = pa_setserverconn()
    try:
        print("X")
        candidates_id = pa_getCandidateId(conn, screen_name, errorpath)
        #print(candidates_id)
        maxTweetId = pa_getMaxTweeId(conn, screen_name, errorpath)[0]
        #print(maxTweetId)
        if (maxTweetId == None):
            print("U1: " + screen_name)
            for status in api.user_timeline(screen_name, tweet_mode='extended', since='2019-01-01', count=200):
                print("Insertando por primera vez... " + screen_name)
                dr_insert_tweet(conn, candidates_id[0], status.id, None, status.created_at.strftime(
                    "%Y-%m-%d"), status.full_text, status.user.screen_name, json.dumps(status._json), "N", "N", "N", errorpath)
        else:
            print("U2: " + screen_name)
            for status in api.user_timeline(screen_name, tweet_mode='extended', since_id=maxTweetId, count=200):
                print("Segunda ronda... " + screen_name)
                dr_insert_tweet(conn, candidates_id[0], status.id, None, status.created_at.strftime(
                    "%Y-%m-%d"), status.full_text, status.user.screen_name, json.dumps(status._json), "N", "N", "N", errorpath)
    except tweepy.TweepError as e:
        if (e.status == "Twitter error response: status code = 429"):
            counter429 += 1
            print("Dormire mucho")
            time.sleep(n + 180)  # n + 840 o 420
            print("Intentare de nuevo")
        else:
            print(e.reason)


if __name__ == '__main__':
    conn = pa_setserverconn()

    values = dr_get_candidatos(conn, errorpath)

    print(values)

    while True:

        for row in values:
            id = row[0]
            screen_name = row[1]
            t = threading.Thread(target=getTimeline2019, name=(
                'thread1'), args=(60, screen_name))
            t.start()
            t.join()

        print('About to sleep 20 minutes')
        time.sleep(20*60)
