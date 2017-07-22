from twitter.models import Tweet, Topic, Word
import datetime
from twitter.FrequentWordCalculatorLogic.TwitterAPIHandler import TwitterAPIHandler
from twitter.FrequentWordCalculatorLogic.FrequentWordCalculator import FrequentWordCalculator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from twitter.serializers import WordSerializer, TopicSerializer
frequentWordCalculator = FrequentWordCalculator("twitter/FrequentWordCalculatorLogic/settings.json")


@csrf_exempt
def index(request):
    topics = ""
    for topic in Topic.objects.all():
        topics += str(topic) + "\n"
    return HttpResponse(topics)


@csrf_exempt
def topics(request):
    if request.method == 'GET':
        all_topics = Topic.objects.all()
        serializer = TopicSerializer(all_topics, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def topic_data(request, topic):
    if request.method == 'GET':
        try:
            topic = Topic.objects.get(pk=topic)
        except Topic.DoesNotExist:
            return HttpResponse(status=404)

        serializer = TopicSerializer(topic)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def monitor(request, topic):
    return HttpResponse(frequentWordCalculator.monitor_topic(topic, 1800))


@csrf_exempt
def printer(request, topic):
    z = ""
    twitter = TwitterAPIHandler("twitter/FrequentWordCalculatorLogic/settings.json")
    tweets = twitter.query_new_tweets(topic)
    for t in tweets:
        date = datetime.datetime.strptime(t['created_at'], "%a %b %d %H:%M:%S %z %Y")
        topic = Topic.objects.get(pk=topic)
        if topic.tweet_set.filter(tweet_text=t['text'], tweet_creation_time=date).count() == 0:
            Topic.objects.get(pk="dota").tweet_set.create(tweet_text=t['text'], tweet_creation_time=date)


@csrf_exempt
def words(request, topic):
    # z = ""
    # sql = """
    # SELECT id, ct FROM (
    #     SELECT case topic_id when '{}'
    #         then unnest(string_to_array(tweet_text, ' '))
    #         else null end AS id,
    #     count(case topic_id when '{}' then 1 else null end) AS ct
    #     FROM   public.twitter_tweet
    #     GROUP  BY 1
    #     ORDER  BY 2 DESC
    #     ) words
    #     WHERE id ~ '^[\w,@,#]+$'
    #     LIMIT 50
    # """.format(topic, topic)
    # for word in Tweet.objects.raw(sql):
    #     z += word.id + " " + str(word.ct) + "\n\n"
    if request.method == 'GET':
        topic_words = Word.objects.filter(topic=topic)
        serializer = WordSerializer(topic_words, many=True)
        return JsonResponse(serializer.data, safe=False)

    # return HttpResponse(frequentWordCalculator.most_frequent_words(topic))
