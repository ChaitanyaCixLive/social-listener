import tweepy
import logging
from application.twitter.listener import TwitterStreamingListener


class TwitterInterface(object):

    def __init__(self, consumer_key, secret_key, access_token, secret_access_token, hashtags):
        """
        Twitter Interface constructor. This class is used as an interface to the Twitter Listener
        :param consumer_key: Check Out Twitter Documentation
        :param secret_key: Check Out Twitter Documentation
        :param access_token: Check Out Twitter Documentation
        :param secret_access_token: Check Out Twitter Documentation
        :param hashtags: List of Hashtags / Words
        """
        self.auth = tweepy.OAuthHandler(consumer_key, secret_key)
        self.auth.set_access_token(access_token, secret_access_token)
        self.listener = TwitterStreamingListener()
        self.hashtags = hashtags
        self.process_name = "Twitter: " + "-".join(hashtags)
        self.stream = tweepy.streaming.Stream(self.auth, self.listener)

    def test_auth(self):
        """
        Simple Function used to check if authorization object is valid or not
        :return: True / False
        """
        try:
            tweepy.API(self.auth).verify_credentials()
        except Exception as e:
            logging.error("Error trying to connect the object: " + str(self))
            logging.error(e)
            raise Exception(e)

    def start(self, process_manager):
        """
        Create new Twitter Listener Process
        :param process_manager: Process Manager Instance
        :return:
        """
        process_manager.create_process(target=lambda: self.stream.filter(track=self.hashtags),
                                       name=self.process_name)

    def __str__(self):
        """
        String representation
        :return:
        """
        return "Twitter Interface <{hashtags}>".format(auth=self.auth,
                                                       hashtags=self.hashtags)
