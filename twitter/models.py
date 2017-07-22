from django.db import models
import datetime


class Topic(models.Model):
    topic_text = models.CharField(primary_key=True, unique=True, max_length=200)
    num_of_words = models.IntegerField(default=0)
    last_tweet_creation_time = models.DateTimeField('last tweet creation time', default=datetime.datetime(2000, 1, 1, 1, 1, 1))

    def __str__(self):
        return self.topic_text


class Word(models.Model):
    word = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("word", "topic")
        ordering = ['-count']


class Tweet(models.Model):
    tweet_creation_time = models.DateTimeField('date created', default=datetime.datetime(2000, 1, 1, 1, 1, 1))
    tweet_text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("tweet_creation_time", "tweet_text", "topic")
        # ordering = ['tweet_creation_time']

    def __str__(self):
        return self.tweet_text
