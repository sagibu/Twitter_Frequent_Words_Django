import psycopg2
from twitter.models import Tweet, Topic
import json
import datetime


class TwitterDBHandler:
    def add_tweet_to_table(self, tweet, topic):
        date = datetime.datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
        topic = Topic.objects.get(pk=topic)
        if topic.tweet_set.filter(tweet_text=tweet['text'], tweet_creation_time=date).count() == 0:
            Topic.objects.get(pk=topic).tweet_set.create(tweet_text=tweet['text'], tweet_creation_time=date)

    def add_list_to_table(self, tweets_list, topic):
        for tweet in tweets_list:
            self.add_tweet_to_table(tweet, topic)

    def create_tweets_topic(self, topic):
        if not self.topic_exists(topic):
            new_topic = Topic(topic_text=topic)
            new_topic.save()

    def topic_exists(self, topic):
        if Topic.objects.filter(pk=topic).count() == 0:
            return False
        return True

    def most_frequent_words(self, topic):
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
        return z

    def total_number_of_rows(self, topic):
        return Topic.objects.filter(pk=topic).count()
