import psycopg2
from twitter.models import Tweet, Topic, Word
import json
import datetime
from django.db.models import Max


class TwitterDBHandler:
    def add_tweet_to_table(self, tweet, topic_name):
        date = datetime.datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
        topic = Topic.objects.get(pk=topic_name)
        if topic.tweet_set.filter(tweet_text=tweet['text'], tweet_creation_time=date).count() == 0 \
                and topic.last_tweet_creation_time < date:
            topic.tweet_set.create(tweet_text=tweet['text'], tweet_creation_time=date)
            topic.num_of_words += 1
            topic.save()

    def add_list_to_table(self, tweets_list, topic_name):
        for tweet in tweets_list:
            self.add_tweet_to_table(tweet, topic_name)

        max_date = Tweet.objects.filter(topic_id=topic_name).aggregate(Max('tweet_creation_time'))['tweet_creation_time__max']
        print(max_date)
        topic_object = Topic.objects.get(pk=topic_name)
        topic_object.last_tweet_creation_time = max_date
        topic_object.save()

    def create_tweets_topic(self, topic_name):
        if not self.topic_exists(topic_name):
            new_topic = Topic(topic_text=topic_name, num_of_words=0)
            new_topic.save()

    def get_db_word(self, word, topic_name):
        if not self.word_exists(word, topic_name):
            db_word = Word(word=word, topic=Topic.objects.get(pk=topic_name))
            db_word.save()
            return db_word
        return Word.objects.get(word=word, topic=Topic.objects.get(pk=topic_name))

    def topic_exists(self, topic_name):
        if Topic.objects.filter(pk=topic_name).count() == 0:
            return False
        return True

    def word_exists(self, word, topic_name):
        if Word.objects.filter(word=word, topic=topic_name).count() == 0:
            return False
        return True

    def calc_most_frequent_words(self, topic_name):
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
            """.format(topic_name, topic_name)
        for word in Tweet.objects.raw(sql):
            db_word = self.get_db_word(word.id, topic_name)
            db_word.count += word.ct
            db_word.save()

    def delete_tweets(self, topic_name):
        Tweet.objects.filter(topic_id=topic_name).delete()

    def get_most_frequent_words(self, topic_name):
        return map(lambda word: (word.word, word.count), Word.objects.filter(topic=Topic.objects.get(pk=topic_name)))

    def total_number_of_rows(self, topic_name):
        return Topic.objects.get(pk=topic_name).num_of_words
