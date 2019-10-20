from __future__ import print_function
import twitter

CONSUMER_KEY = 'NtSd91Sg1FTL89OWWG8AKZtbb'
CONSUMER_SECRET = 'vNO3U5p8LwYd5yLzNobM7Pv9pND58mUyRZMmSszq982OT5llTu'
ACCESS_TOKEN = '216299873-JxwWo6jF0CYw2ZSVjGWjumiIrQzl9UVlq3ykhtmy'
ACCESS_SECRET = 'Im00D6v4rw75JC3uY1YNOgy5XCBaLwvwDMnKRdQ0o74zz'

def twitterHandler():
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
        if x == 'leogib':
            following = True

    # followers
    followers = False
    for x in db_followers:
        if x == 'abdul':
            followers = True

    if following and followers:
        print('You both follow each other')
    elif following and not(followers):
        print ('You follow him/her but he/she doesnt follow you')
    elif not(following) and followers:
        print('You dont follow him/her, but he/she follow you')
    else:
        print('You dont follow each other')

if __name__ == "__main__":
    twitterHandler()
