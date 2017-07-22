from rest_framework import serializers
from twitter.models import Word, Topic


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('word', 'count', 'topic')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('topic_text', 'num_of_words')
