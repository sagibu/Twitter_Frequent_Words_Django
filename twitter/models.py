from django.db import models


class Topic(models.Model):
    topic_text = models.CharField(primary_key=True, unique=True, max_length=200)

    def __str__(self):
        return self.topic_text


class Tweet(models.Model):
    tweet_creation_time = models.DateTimeField('date created')
    tweet_text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("tweet_creation_time", "tweet_text")

    def __str__(self):
        return self.tweet_text
