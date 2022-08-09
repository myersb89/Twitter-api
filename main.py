import requests
import os

print("Hello World")

baseurl = "https://api.twitter.com/2"
username = "BryanJMyers1"
access_token = os.getenv('BearerToken')


headers = {'Authorization': f'Bearer {access_token}'}
try:
    r = requests.get(baseurl + f'/users/by/username/{username}', headers=headers)
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

print(r.text)