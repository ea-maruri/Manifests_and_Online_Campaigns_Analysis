import psycopg2
import datetime


def dr_establishConn(server, db, user, password):
    try:
        conn = psycopg2.connect(
            "dbname='"+db+"' user='"+user+"' host='"+server+"' password='"+password+"'")
        #print("Me conecté sin problemas")#Pamela
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(str(e))
        return None


def dr_insert_candidate(conn, id, nombre, apellido, ciudad, tipo, twitter_id, twitter_screen_name, twitter_date, candidate_status, errorpath):
    cur = conn.cursor()
    try:
        query = "INSERT INTO public.candidatos(" + \
                "            id, nombre, apellidos, ciudad, tipo, twitter_id,twitter_screen_name, twitter_date, candidate_status)" + \
                "    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (id, nombre, apellido, ciudad, tipo, twitter_id,
                            twitter_screen_name, twitter_date, candidate_status))
        return_value = True
    except psycopg2.Error as e:
        f = open(errorpath, 'a')
        f.write('WARNING - Unable to insert user: ' + str(twitter_id) + '\n')
        f.write('MSG: ' + str(e) + '\n')
        f.write('Time: ' + str(datetime.datetime.now()) + '\n')
        f.write('----------------------------------------------------------\n')
        f.close()
        conn.rollback()
        return_value = False
    else:
        conn.commit()

    return return_value


def getMax(conn):
    cur = conn.cursor()
    cur.execute("SELECT MAX (id) from candidatos")
    max = str(cur.fetchone()[0])
    if(max != "None"):
        return int(max)+1
    else:
        return 1
# def dr_insert_tweet(conn, tweet_id, tweet_parent_id, tweet_date,
#                     tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag, tweet_manual_tag, errorpath):
#     cur = conn.cursor()
#     try:
#         query = "INSERT INTO public.tweets(" + \
#                 "            tweet_id, tweet_parent_id, tweet_date,tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag,tweet_manual_tag)" + \
#                 "    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#         cur.execute(query, (
#         tweet_id, tweet_parent_id, tweet_date, tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag, tweet_manual_tag))
#         return_value = True
#     except psycopg2.Error as e:
#         f = open(errorpath, 'a')
#         f.write('WARNING - Unable to insert tweet: ' + str(tweet_id) + '\n')
#         f.write('MSG: ' + str(e) + '\n')
#         f.write('Time: ' + str(datetime.datetime.now()) + '\n')
#         f.write('----------------------------------------------------------\n')
#         f.close()
#         conn.rollback()
#         return_value = False
#     else:
#         conn.commit()
#
#     return return_value


# def dr_insert_tweet(conn, tweet_id, tweet_parent_id, tweet_date,
#                     tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag, tweet_manual_tag, tweet_status, errorpath):
#     cur = conn.cursor()
#     try:
#         query = "INSERT INTO public.tweets(" + \
#                 "            tweet_id, tweet_parent_id, tweet_date,tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag,tweet_manual_tag, tweet_status)" + \
#                 "    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         cur.execute(query, (
#         tweet_id, tweet_parent_id, tweet_date, tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag, tweet_manual_tag,tweet_status))
#         return_value = True
#     except psycopg2.Error as e:
#         f = open(errorpath, 'a')
#         f.write('WARNING - Unable to insert tweet: ' + str(tweet_id) + '\n')
#         f.write('MSG: ' + str(e) + '\n')
#         f.write('Time: ' + str(datetime.datetime.now()) + '\n')
#         f.write('----------------------------------------------------------\n')
#         f.close()
#         conn.rollback()
#         return_value = False
#     else:
#         conn.commit()
#
#     return return_value
'''
def dr_insert_tweet(conn, tweet_id, tweet_date,
                    tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag, tweet_manual_tag, errorpath):
    cur = conn.cursor()
    try:
        query = "INSERT INTO public.tweets(" + \
                "            tweet_id, tweet_date,tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag,tweet_manual_tag)" + \
                "    VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (
        tweet_id, tweet_date, tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag, tweet_manual_tag))
        return_value = True
    except psycopg2.Error as e:
        f = open(errorpath, 'a')
        f.write('WARNING - Unable to insert tweet: ' + str(tweet_id) + '\n')
        f.write('MSG: ' + str(e) + '\n')
        f.write('Time: ' + str(datetime.datetime.now()) + '\n')
        f.write('----------------------------------------------------------\n')
        f.close()
        conn.rollback()
        return_value = False
    else:
        conn.commit()

    return return_value
'''


def dr_insert_tweet(conn, candidates_id, tweet_id, tweet_parent_id, tweet_date,
                    tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag, tweet_manual_tag, tweet_status, errorpath):
    cur = conn.cursor()
    try:
        query = "INSERT INTO public.tweets(" + \
                "            candidates_id, tweet_id, tweet_parent_id, tweet_date,tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag,tweet_manual_tag, tweet_status)" + \
                "    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (
            candidates_id, tweet_id, tweet_parent_id, tweet_date, tweet_text, tweet_screen_name, tweet_json, tweet_automatic_tag, tweet_manual_tag, tweet_status))
        return_value = True
    except psycopg2.Error as e:
        f = open(errorpath, 'a')
        f.write('WARNING - Unable to insert tweet: ' + str(tweet_id) + '\n')
        f.write('MSG: ' + str(e) + '\n')
        f.write('Time: ' + str(datetime.datetime.now()) + '\n')
        f.write('----------------------------------------------------------\n')
        f.close()
        conn.rollback()
        return_value = False
    else:
        conn.commit()

    return return_value


def dr_get_candidatos(conn, errorpath):
    cur = conn.cursor()
    try:
        query = "select id, twitter_screen_name from candidatos"
        cur.execute(query)
        value = cur.fetchall()
        return_value = value
    except psycopg2.Error as e:
        f = open(errorpath, 'a')
        f.write('WARNING - Unable to execute query on tweets_tfb_user.\n')
        f.write('MSG: ' + str(e) + '\n')
        f.write('Time: ' + str(datetime.datetime.now()) + '\n')
        f.write('----------------------------------------------------------\n')
        f.close()
        conn.rollback()
        return_value = None
    else:
        conn.commit()
    cur.close()
    return return_value


def pa_getCandidateId(conn, screen_name, errorpath):
    cur = conn.cursor()
    #print(type(screen_name))
    try:
        query = "select id from candidatos where twitter_screen_name= %s"
        cur.execute(query, (screen_name,))
        value = cur.fetchone()
        return_value = value
    except psycopg2.Error as e:
        f = open(errorpath, 'a')
        f.write('WARNING - Unable to get candidate id' + '\n')
        f.write('MSG: ' + str(e) + '\n')
        f.write('Time: ' + str(datetime.datetime.now()) + '\n')
        f.write('----------------------------------------------------------\n')
        f.close()
        conn.rollback()
        return_value = False
    else:
        conn.commit()

    return return_value


def pa_getMaxTweeId(conn, screen_name, errorpath):
    cur = conn.cursor()
    #print(type(screen_name))
    try:
        query = "select max(cast(tweet_id as BigInt)) from tweets, candidatos where tweets.candidates_id = candidatos.id and twitter_screen_name=%s"
        cur.execute(query, (screen_name,))
        value = cur.fetchone()
        return_value = value
    except psycopg2.Error as e:
        f = open(errorpath, 'a')
        f.write('WARNING - Unable to get candidate id' + '\n')
        f.write('MSG: ' + str(e) + '\n')
        f.write('Time: ' + str(datetime.datetime.now()) + '\n')
        f.write('----------------------------------------------------------\n')
        f.close()
        conn.rollback()
        return_value = False
    else:
        conn.commit()

    return return_value


def pa_updateTweetStatusR(conn, screen_name, tweet_id, errorpath):
    cur = conn.cursor()
    # print(type(screen_name))
    try:
        query = "UPDATE tweets SET tweet_status = 'R' FROM candidatos WHERE tweets.candidates_id = candidatos.id AND candidatos.twitter_screen_name = %s AND tweets.tweet_id = %s;"
        cur.execute(query, (screen_name, tweet_id,))
        return_value = True
    except psycopg2.Error as e:
        f = open(errorpath, 'a')
        f.write('WARNING - Unable to get candidate id' + '\n')
        f.write('MSG: ' + str(e) + '\n')
        f.write('Time: ' + str(datetime.datetime.now()) + '\n')
        f.write('----------------------------------------------------------\n')
        f.close()
        conn.rollback()
        return_value = False
    else:
        conn.commit()

    return return_value


def pa_getAllTweetIds(conn, screen_name, errorpath):
    cur = conn.cursor()
    sinceDate = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
    untilDate = (datetime.datetime.now()).date()
    print(sinceDate, untilDate)
    # print(type(screen_name))
    try:
        query = "select cast(tweet_id as BigInt) from tweets, candidatos where tweets.candidates_id = candidatos.id and twitter_screen_name=%s and tweet_date between %s and %s order by tweet_date"
        cur.execute(query, (screen_name, sinceDate, untilDate))
        value = cur.fetchall()
        return_value = value
    except psycopg2.Error as e:
        f = open(errorpath, 'a')
        f.write('WARNING - Unable to get all tweets ids from candidate' + '\n')
        f.write('MSG: ' + str(e) + '\n')
        f.write('Time: ' + str(datetime.datetime.now()) + '\n')
        f.write('----------------------------------------------------------\n')
        f.close()
        conn.rollback()
        return_value = False
    else:
        conn.commit()

    return return_value
