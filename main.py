import requests
import os
import json
import psycopg2


def main():
    baseurl = "https://api.twitter.com/2"
    access_token = os.getenv('BearerToken')
    headers = {'Authorization': f'Bearer {access_token}'}

    query_params = {'user.fields': "pinned_tweet_id"}
    username = "BryanJMyers1"

    conn = psycopg2.connect("dbname=twitter_data user=postgres password=test1234")

    try:
        r = requests.get(baseurl + f'/users/by/username/{username}', headers=headers, params=query_params)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(json.dumps(r.json()))

    pinned_tweet = r.json()['data']['pinned_tweet_id']
    ids = {'ids':pinned_tweet}
    try:
        r = requests.get(baseurl + f'/tweets', headers=headers, params=ids)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(json.dumps(r.json()))
    #query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}

    conn.close()

if __name__ == "__main__":
    main()