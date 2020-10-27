import datetime
import threading
from threading import Thread
import time
import tweepy
import json


# # PAMEALMEIDAS / Twitter Credentials
# # Access Token for Twitter App
# access_token = "57173854-fmeivcjvIWtNbHH0AqXnRteGzxWMGgkr88HVxVfEG"
# access_token_secret = "LIHkXdvM1ihAYjPCSWhRXBCpWZseDnmeLX7pdvXitJpiI"
# # Consumer Keys
# consumer_key = "Fvi32GeHQwZZ8rxnX5T4xdvUq"
# consumer_secret = "xRAfWVs0D3UM0Va3548Fdto6YgTbAtrKIsIYvNSreAFkJDV0mY"

# DANIEL RIOFRIO / Twitter Credentials
# Access Token for Twitter App
access_token = "37859688-isXNFc4dFvOa0uHlc14jnuqcKqQKLjExJHKx6EWqu"
access_token_secret = "TiJ4VLrXIq0OxGo90QJEP8RG0FxPoLrXZ7HynTqClv4kx"
# Consumer Keys
consumer_key = "7v5mgmO1TjCexxCmVH2uocG7D"
consumer_secret = "Po5Jii1Ab5oze6IR5fTuqXYZ6sm2o8tuXS8lfVKjRTSzBsIgh0"


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
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
errorpath = './error/error.log'


# def pa_setserverconn():
#     server = "localhost"
#     db = "elecciones2019"
#     user = "elect2019"
#     password = "elecciones2019"
#     conn = dr_establishConn(server, db, user, password)
#     return conn


# def getTimeline2019(n, screen_name):
#     counter429 = 0
#     conn = pa_setserverconn()
#     try:
#         print("X")
#         candidates_id = pa_getCandidateId(conn, screen_name, errorpath)
#         #print(candidates_id)
#         maxTweetId = pa_getMaxTweeId(conn, screen_name, errorpath)[0]
#         #print(maxTweetId)
#         if (maxTweetId == None):
#             print("U1: " + screen_name)
#             for status in api.user_timeline(screen_name, tweet_mode='extended', since='2019-01-01', count=200):
#                 print("Insertando por primera vez... " + screen_name)
#                 dr_insert_tweet(conn, candidates_id[0], status.id, None, status.created_at.strftime(
#                     "%Y-%m-%d"), status.full_text, status.user.screen_name, json.dumps(status._json), "N", "N", "N", errorpath)
#         else:
#             print("U2: " + screen_name)
#             for status in api.user_timeline(screen_name, tweet_mode='extended', since_id=maxTweetId, count=200):
#                 print("Segunda ronda... " + screen_name)
#                 dr_insert_tweet(conn, candidates_id[0], status.id, None, status.created_at.strftime(
#                     "%Y-%m-%d"), status.full_text, status.user.screen_name, json.dumps(status._json), "N", "N", "N", errorpath)
#     except tweepy.TweepError as e:
#         if (e.status == "Twitter error response: status code = 429"):
#             counter429 += 1
#             print("Dormire mucho")
#             time.sleep(n + 180)  # n + 840 o 420
#             print("Intentare de nuevo")
#         else:
#             print(e.reason)


from StudyCasesManage.models import Post, SocialMediaAccount, Timeline

DATE_FORMAT = '%Y-%m-%d'


def ea_get_max_post_id(screen_name):
    the_query = """SELECT "StudyCasesManage_post"."id", MAX(CAST(public."StudyCasesManage_post"."post_id" as BigInt))
	                FROM public."StudyCasesManage_post"
	                INNER JOIN public."StudyCasesManage_timeline"
		                ON (public."StudyCasesManage_timeline"."id" 
			                = public."StudyCasesManage_post"."timeline_id_id")
	                INNER JOIN public."StudyCasesManage_socialmediaaccount"
		                ON (public."StudyCasesManage_socialmediaaccount"."id"
			                = public."StudyCasesManage_timeline"."social_media_id_id")
	                WHERE "StudyCasesManage_socialmediaaccount"."screen_name" = """ + "'" + screen_name + "'" + 'GROUP BY "StudyCasesManage_post"."id"'

    result = Post.objects.raw(the_query)
    posts_ids = list()
    if len(result) > 0:
        for val in result:
            posts_ids.append(val.post_id)  # is an int, val is a Post

        return max(posts_ids)
    else:
        return None


def get_timeline(n: int, screen_name: str, count_limit: int, since_date: str, timeline: Timeline):
    # Create a new Timeline given the id (a social media account)
    # datetime.datetime.strptime(until, DATE_FORMAT)
    # timeline = Timeline(
    #     social_media_id = SocialMediaAccount.objects.get(screen_name=screen_name),
    #     collect_date = datetime.datetime.strptime(since_date, DATE_FORMAT).date(),
    #     end_date = datetime.datetime.strptime(until_date, DATE_FORMAT).date()
    # )

    # print('Timeline to create:', timeline)
    # timeline.save()  # in db

    counter429 = 0
    try:
        max_post_id = ea_get_max_post_id(screen_name)
        print("Max post id:", max_post_id)
        
        # In the case the user in the given timeline does not have posts
        if (max_post_id == None):
            print("U1: " + screen_name)
            #for status in api.user_timeline(screen_name, tweet_mode='extended', since='2020-10-16', count=200):
            for status in api.user_timeline(screen_name, tweet_mode='extended', since=since_date, count=count_limit):
                print("Insertando por primera vez... " + screen_name)
                post = Post(
                    post_id = status.id,
                    timeline_id = timeline,
                    post_date = status.created_at.strftime("%Y-%m-%d"),
                    post_text = status.full_text,
                    post_as_json = json.dumps(status._json)
                )

                post.save()
                # dr_insert_tweet(conn, candidates_id[0], status.id, None, 
                # status.created_at.strftime("%Y-%m-%d"), status.full_text, status.user.screen_name, json.dumps(status._json), "N", "N", "N", errorpath)
        
        #  In the case that a post still exists
        else:
            print("U2: " + screen_name)
            #for status in api.user_timeline(screen_name, tweet_mode='extended', since_id='2020-10-16', count=count_limit):
            for status in api.user_timeline(screen_name, tweet_mode='extended', since_id=max_post_id, count=count_limit):
                print("Segunda ronda... " + screen_name)
                post = Post(
                    post_id = status.id,
                    timeline_id=timeline,
                    post_date=status.created_at.strftime("%Y-%m-%d"),
                    post_text=status.full_text,
                    post_as_json=json.dumps(status._json)
                )
                
                post.save()
                # dr_insert_tweet(conn, candidates_id[0], status.id, None, 
                # status.created_at.strftime("%Y-%m-%d"), status.full_text, status.user.screen_name, json.dumps(status._json), "N", "N", "N", errorpath)
    
    except tweepy.TweepError as e:
        if (e.status == "Twitter error response: status code = 429"):
            counter429 += 1
            print("I'll sleep a lot", Thread.name, 'at:', str(datetime.datetime.now()))
            time.sleep(n + 180)  # n + 840 o 420
            print("I'll try again", Thread.name, 'at:', str(datetime.datetime.now()))
        else:
            print(e.reason)


def execute_collection(screen_names: list, count: int, since: str, until: str):
    print("Start collection...")

    since_date = datetime.datetime.strptime(since, DATE_FORMAT)
    until_date = datetime.datetime.strptime(until, DATE_FORMAT)
    print('Since Date:', since_date.date())    
    print('Until Date:', until_date.date())

    if since_date < until_date:
        print('since is less than until...')

        timelines_to_create = list()
        for screen_name in screen_names:
            timeline = Timeline(
                social_media_id=SocialMediaAccount.objects.get(
                    screen_name=screen_name),
                collect_date=since_date.date(),
                end_date=until_date.date()
            )

            print('Timeline to create:', timeline)
            timeline.save()  # in db
            timelines_to_create.append(timeline)


        # get_timeline(50, screen_names[0], count, since, until)
        while since_date <= until_date:  # while True:
            thread_num = 0
            iteration = 0
            for screen_name in screen_names:
                t = threading.Thread(
                    target=get_timeline,
                    name=('thread' + str(thread_num) + '-' + screen_name),
                    args=(60, screen_name, count, since, timelines_to_create[iteration])
                )

                t.start()
                t.join()

                thread_num += 1
                iteration += 1

            print('About to sleep 10 minutes', Thread.name, 'at:', str(datetime.datetime.now()))
            time.sleep(10*60)


def main(screen_names: list, count: int, until: str, since: str = str(datetime.date.today)):
    # Create a thread to control the others
    main_thread = threading.Thread(
        target=execute_collection,
        name=('Collector: ' + since + '-' + until),
        args=(screen_names, count, since, until)
    )
    main_thread.start()
    main_thread.join()

    #execute_collection(screen_names, count, since)

