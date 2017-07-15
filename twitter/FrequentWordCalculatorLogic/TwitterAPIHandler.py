from twython import Twython
import json


class TwitterAPIHandler:
    def __init__(self, settings_file):
        with open(settings_file) as settings_json:
            settings = json.load(settings_json)['TWITTER']
        self.twitter = Twython(settings['APP_KEY'], settings['APP_SECRET'], oauth_version=2,
                               access_token=settings['ACCESS_TOKEN'])

    def query_new_tweets(self, topic, query_type='recent'):
        tweets = self.twitter.search(q=topic, result_type=query_type, count=100, lang='en')
        return tweets['statuses']