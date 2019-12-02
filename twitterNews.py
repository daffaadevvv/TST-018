from flask import Flask, jsonify
import dotenv
from dotenv import load_dotenv
import json
import twitter
import requests
import os

load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

app = Flask(__name__)
app.config['DEBUG'] = True

api = twitter.Api(consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token_key=ACCESS_TOKEN,
            access_token_secret=ACCESS_SECRET)

# Delete word with @ in the beginning
def cekString(string):
    if string[0] != '@' :
        return True

# Give a new message to another API
def mentionRemove(array):
    message_fix = []
    
    for item in array:
        if cekString(item):
            message_fix.append(item)
    
    return message_fix

def mentionCheck():
    mention = api.GetMentions(count=1)

    return mention

def mentionID(mention = mentionCheck()):
    return mention[0].user.id

def mentionUser(mention = mentionCheck()):
    return mention[0].user.screen_name

def mentionMessage(mention = mentionCheck()):
    message_string = mention[0].text.split( )
    query = mentionRemove(message_string)
    return query[0]

def postTweet(link):
    text = '@' + mentionUser() + ' ' + link

    api.PostUpdate(status=text, in_reply_to_status_id=mentionID())
    
    return text

def callNews(result = mentionMessage()):
    req_link = requests.get('https://news-look.herokuapp.com/resources/news/dalamnegeri/' + result).json()
    
    if req_link['link'] == 'Link tidak ditemukan':
        req_link = requests.get('https://news-look.herokuapp.com/resources/news/internasional/' + result).json()

    link = req_link['link']
    
    tweetMessage = postTweet(link)

    jsonResponse = {
        'code': 200,
        'message': 'request success',
        'data': tweetMessage,
        'to reply query': mentionMessage(),
        'in reply to': mentionUser(),
        'with ID': mentionID()
    }
    
    return jsonResponse

def response_api(data):
    return jsonify(**data)

# ENDPOINT METHOD
@app.route('/twitter/mention', methods=['GET'])
def mention():
    try:
        data = callNews()
        return response_api(data)
    except Exception as e:
        return e

@app.route("/")
def hello():
    return '''<h1> Cara penggunaan Twitter API </h1> 
    <li>/twitter/mention</li>
    <li>/twitter/mention/id</li>
    <li>/twitter/mention/user</li>
    <li>/twitter/mention/message</li>
    '''

# DEBUG METHOD AND ENDPOINT
def jsonMessage(mention = mentionCheck()):
    message_string = mention[0].text.split( )

    jsonResponse = {
        'code': 200,
        'message': 'request success',
        'data': mentionRemove(message_string)[0]
    }
    
    return jsonResponse

def jsonUser(mention = mentionCheck()):
    jsonResponse = {
        'code': 200,
        'message': 'request success',
        'data': (mention[0].user.screen_name)
    }
    return jsonResponse

def jsonTweet():
    api.PostUpdates('BotTwitter Tes')
    
    jsonResponse = {
        'data': 'sukses gan'
    }

    return jsonResponse

def jsonID(mention = mentionCheck()):
    jsonResponse = {
        'code': 200,
        'message': 'request success',
        'data': mention[0].user.id
    }
    return jsonResponse

@app.route('/twitter/mention/message', methods=['GET'])
def message():
    try:
        data = jsonMessage()
        return response_api(data)
    except Exception as e:
        return e

@app.route('/twitter/mention/user', methods=['GET'])
def user():
    try:
        data = jsonUser()
        return response_api(data)
    except Exception as e:
        return e

@app.route('/twitter/mention/id', methods=['GET'])
def id():
    try:
        data = jsonID()
        return response_api(data)
    except Exception as e:
        return e

@app.route('/twitter/post', methods=['GET'])
def update():
    try:
        data = jsonTweet()
        return response_api(data)
    except Exception as e:
        return response_api(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded = True)
