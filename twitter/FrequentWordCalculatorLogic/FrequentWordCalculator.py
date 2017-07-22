from twitter.FrequentWordCalculatorLogic.TwitterAPIHandler import TwitterAPIHandler
from twitter.FrequentWordCalculatorLogic.TwitterDBHandler import TwitterDBHandler
import threading


class FrequentWordCalculator:
    def __init__(self, settings_file):
        self.db_handler = TwitterDBHandler()
        self.twitter_handler = TwitterAPIHandler(settings_file)

    def query_topic(self, topic_name, query_type):
        tweets = self.twitter_handler.query_new_tweets(topic_name, query_type)
        self.db_handler.create_tweets_topic(topic_name)
        self.db_handler.add_list_to_table(tweets, topic_name)
        self.db_handler.calc_most_frequent_words(topic_name)
        self.db_handler.delete_tweets(topic_name)

    def monitor_topic(self, topic_name, delay):
        if self.db_handler.topic_exists(topic_name):
            return "Already Monitoring " + topic_name
        self.query_topic(topic_name, 'recent')
        threading.Timer(delay, self.monitor_topic, [topic_name, delay]).start()
        return "Starting monitoring " + topic_name

    def most_frequent_words(self, topic_name):
        if not self.db_handler.topic_exists(topic_name):
            return {"Topic doesnt exist"}

        return list(map(lambda word: {"Word": word[0],
                                      "Count": word[1],
                                      "Precentage": word[1] / self.db_handler.total_number_of_rows(topic_name)},
                        self.db_handler.get_most_frequent_words(topic_name)))
