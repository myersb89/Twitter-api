import requests
import os
import json
import psycopg2
import tweepy

def get_user_tweets_native():
    baseurl = "https://api.twitter.com/2"
    access_token = os.getenv('BearerToken')
    headers = {'Authorization': f'Bearer {access_token}'}

    query_params = {'user.fields': "pinned_tweet_id"}
    username = "BryanJMyers1"


    try:
        r = requests.get(baseurl + f'/users/by/username/{username}', headers=headers, params=query_params)
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

def get_user_tweets_library():
    client = tweepy.Client(bearer_token=os.getenv('BearerToken'))

    response = client.get_user(username="BryanJMyers1")

    public_tweets = client.get_users_tweets(response.data.id)
    for tweet in public_tweets.data:
        print(tweet.text)

if __name__ == "__main__":
    conn = psycopg2.connect("dbname=twitter_data user=postgres password=test1234")
    get_user_tweets_native()
    get_user_tweets_library()
    conn.close()