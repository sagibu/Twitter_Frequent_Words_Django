from django.http import HttpResponse
from random import randint
from twitter.models import Tweet, Topic
import datetime
from django.utils import timezone
from twitter.FrequentWordCalculatorLogic.TwitterAPIHandler import TwitterAPIHandler
from twitter.FrequentWordCalculatorLogic.FrequentWordCalculator import FrequentWordCalculator

frequentWordCalculator = FrequentWordCalculator("twitter/FrequentWordCalculatorLogic/settings.json")


def index(request):
    topics = ""
    for topic in Topic.objects.all():
        topics += str(topic) + "\n"
    return HttpResponse(topics)


def monitor(request, topic):
    frequentWordCalculator.monitor_topic(topic, 1800)
    return HttpResponse("Monitoring topic " + topic)


def printer(request, topic):
    z = ""
    twitter = TwitterAPIHandler("twitter/FrequentWordCalculatorLogic/settings.json")
    tweets = twitter.query_new_tweets(topic)
    for t in tweets:
        date = datetime.datetime.strptime(t['created_at'], "%a %b %d %H:%M:%S %z %Y")
        topic = Topic.objects.get(pk=topic)
        if topic.tweet_set.filter(tweet_text=t['text'], tweet_creation_time=date).count() == 0:
            Topic.objects.get(pk="dota").tweet_set.create(tweet_text=t['text'], tweet_creation_time=date)


def count(request, topic):
    z = ""
    sql = """
    SELECT id, ct FROM (
        SELECT case topic_id when '{}' 
            then unnest(string_to_array(tweet_text, ' '))
            else null end AS id, 
        count(case topic_id when '{}' then 1 else null end) AS ct
        FROM   public.twitter_tweet
        GROUP  BY 1
        ORDER  BY 2 DESC
        ) words
        WHERE id ~ '^[\w,@,#]+$'
        LIMIT 50
    """.format(topic, topic)
    for word in Tweet.objects.raw(sql):
        z += word.id + " " + str(word.ct) + "\n\n"

    return HttpResponse(z)
