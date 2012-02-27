import json
import tweepy
import StringIO
import urllib
import urllib2
from server import views

def tedglobe_full(request, api_method_wrapper):
    view = getattr(views, api_method_wrapper.view)

    if 'users' not in request.form:
        return view(None)

    users = request.form['users'].split('|')

    CONSUMER_KEY = 'OjXvfklyIok5Y5ykvp31w'
    CONSUMER_SECRET = '78I5kuX9xpOSGNHB4hvnFv93LSvL75g9SBBaAbuO84'
    ACCESS_KEY = '17284436-0orsmx08jZvf6qJ3ZcB5Zw7I04IX5EZDe2p1HAs'
    ACCESS_SECRET = '3tbHft6QmW6zLTJUpSJWfLYjwD2joFDVhBewnLeU'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    return_data = []
    for user in users:
        u = api.get_user(user)
        location = u.location
        post_data = urllib.urlencode({'text':location})
        response = json.loads(urllib2.urlopen('http://api.metalayer.com/s/tedglobe/1/locations', data=post_data).read())
        return_data.append({
            'user':user,
            'location':response['datalayer']['locations'][0]
        })
    return view(return_data)