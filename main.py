import requests
import os
import json
import psycopg2
import tweepy

class TweetPrinter(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)

def get_user_tweets_native(user):
    baseurl = "https://api.twitter.com/2"
    access_token = os.getenv('BearerToken')
    headers = {'Authorization': f'Bearer {access_token}'}

    query_params = {'user.fields': "pinned_tweet_id"}

    try:
        r = requests.get(baseurl + f'/users/by/username/{user}', headers=headers, params=query_params)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    pinned_tweet = r.json()['data']['pinned_tweet_id']
    ids = {'ids':pinned_tweet}
    try:
        r = requests.get(baseurl + f'/tweets', headers=headers, params=ids)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(json.dumps(r.json()))

def get_user_tweets_library(user):
    client = tweepy.Client(bearer_token=os.getenv('BearerToken'))

    response = client.get_user(username=user)

    public_tweets = client.get_users_tweets(response.data.id)
    for tweet in public_tweets.data:
        print(tweet.text)

    return public_tweets.data

def stream_tweets():
    stream_client = TweetPrinter(bearer_token=os.getenv('BearerToken'))
    stream_client.add_rules(tweepy.StreamRule("Tweepy"))
    stream_client.filter()

def create_tables(connection):
    commands = (
        """
        CREATE TABLE IF NOT EXISTS tweets (
            tweet_id BIGINT PRIMARY KEY,
            tweet_text VARCHAR(280) NOT NULL
        )
        """,
    )
   # import pdb; pdb.set_trace()
    cur = connection.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    connection.commit()

def insert_tweet_sql(connection, tweet):
    cur = connection.cursor()
    cur.execute("INSERT INTO tweets (tweet_id, tweet_text) VALUES (%s, %s) ON CONFLICT DO NOTHING", (tweet.id, tweet.text))
    cur.close()
    connection.commit()

def get_tweets_sql(connection):
    cur = connection.cursor()
    cur.execute("SELECT * FROM tweets;")
    tweets = cur.fetchall()
    for tweet in tweets:
        print(tweet)
    cur.close()

if __name__ == "__main__":
    username = "BryanJMyers1"
    #get_user_tweets_native(username)
    tweets = get_user_tweets_library(username)
    print(tweets)

    # Save to Postgres
    conn = psycopg2.connect("dbname=twitter_data user=postgres password=test1234")
    create_tables(conn)
    for tweet in tweets:
        insert_tweet_sql(conn,tweet)
    get_tweets_sql(conn)
    conn.close()

    #stream_tweets()