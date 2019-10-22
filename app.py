from __future__ import print_function
from flask import Flask, Response, redirect, request, jsonify
import twitter

CONSUMER_KEY = 'CONSUMER_KEY'
CONSUMER_SECRET = 'CONSUMER_SECRET'
ACCESS_TOKEN = 'ACCESS_TOKEN'
ACCESS_SECRET = 'ACCESS_SECRET'

app = Flask(__name__)
app.config['DEBUG'] = True

def twitterHandler(username):
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                consumer_secret=CONSUMER_SECRET,
                access_token_key=ACCESS_TOKEN,
                access_token_secret=ACCESS_SECRET)

    # Get following data from twitter
    users_following = api.GetFriends()
    db_following = [u.screen_name for u in users_following]

    # Get following data from twitter
    users_followers = api.GetFollowers()
    db_followers = [u.screen_name for u in users_followers]

    # Check the username input
    # following
    following = False
    for x in db_following:
        if x == username:
            following = True

    # followers
    followers = False
    for x in db_followers:
        if x == username:
            followers = True

    if following and followers:
        data = {
            'code': 200,
            'message': 'Request Success',
            'data': {
                'username' : username,
                'condition' : 'You both follow each other'
            }
        }
    elif following and not(followers):
        text = 'Hi @' + username + ' please follow me because you havent follow me yet'
        _ = api.PostUpdate(status=text)
        data = {
            'code': 200,
            'message': 'Request Success',
            'data': {
                'username' : username,
                'condition' : 'You follow him/her but he/she doesnt follow you'
            }
        }
    elif not(following) and followers:
        data = {
            'code': 200,
            'message': 'Request Success',
            'data': {
                'username' : username,
                'condition' : 'You dont follow him/her, but he/she follow you'
            }
        }
    else:
        data = {
            'code': 200,
            'message': 'Request Success',
            'data': {
                'username' : username,
                'condition' : 'You dont follow each other'
            }
        }

    return data

def response_api(data):
    return (
        jsonify(**data),
        data['code']
    )

@app.route('/friendship/<username>', methods=['GET'])
def friendship(username):
    try:
        data = twitterHandler(username)
        return response_api(data)
    except Exception as e:
        return e

if __name__ == "__main__":
    app.run()

