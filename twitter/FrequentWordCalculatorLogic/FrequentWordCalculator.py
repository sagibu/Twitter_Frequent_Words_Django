from twitter.FrequentWordCalculatorLogic.TwitterAPIHandler import TwitterAPIHandler
from twitter.FrequentWordCalculatorLogic.TwitterDBHandler import TwitterDBHandler
import threading


class FrequentWordCalculator:
    def __init__(self, settings_file):
        self.db_handler = TwitterDBHandler()
        self.twitter_handler = TwitterAPIHandler(settings_file)

    def query_topic(self, topic, query_type):
        tweets = self.twitter_handler.query_new_tweets(topic, query_type)
        self.db_handler.create_tweets_topic(topic)
        self.db_handler.add_list_to_table(tweets, topic)

    def monitor_topic(self, topic, delay):
        self.query_topic(topic, 'recent')
        threading.Timer(delay, self.monitor_topic, [topic, delay]).start()

    def most_frequent_words(self, topic):
        total_words_count = self.db_handler.total_number_of_rows(topic)
        return list(map(lambda word: {"Word": word[0],
                                      "Count": word[1],
                                      "Precentage": word[1] / total_words_count},
                        self.db_handler.most_frequent_words(topic)))
