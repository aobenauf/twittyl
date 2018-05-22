import tweepy
from textblob import TextBlob
import pandas as pd
from datetime import datetime as dt
import config




consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# Creating a class for the data to be housed
class Friend:



	def __init__(self, twitter_handle):
		self.twitter_handle = twitter_handle

	def getTweets(self):
		tweet_list = []
		timeline = api.user_timeline(screen_name = self.twitter_handle, count = 10, include_rts = False)
		for tweet in timeline:
			tweet_list.append(tweet.text)

		return tweet_list


	def getLikes(self):
		likes_list = []
		#for i in range(1,1):
		likes_per_page = api.favorites(self.twitter_handle,page=1)
		#pages_of_likes.append(likes_per_page)
		for like in likes_per_page:
			likes_list.append(like.text)

		return likes_list


	def getSentiments(self):
		self.pos_sent =  0
		self.nut_sent =  0
		self.neg_sent =  0

		self.tweets = self.getTweets()
		self.likes = self.getLikes()

		#calculating sentiment of tweets and likes
		for tweet in self.tweets:
			if TextBlob(tweet).sentiment.polarity > 0:
				self.pos_sent += 1
			elif TextBlob(tweet).sentiment.polarity < 0:
				self.neg_sent += 1
			else:
				self.nut_sent += 1

		for like in self.likes:
			if TextBlob(like).sentiment.polarity > 0:
				self.pos_sent += 1
			elif TextBlob(like).sentiment.polarity < 0:
				self.neg_sent += 1
			else:
				self.nut_sent += 1

		#this creates a tuple, and I can assign based on these values
		return self.pos_sent, self.neg_sent, self.nut_sent, self.tweets, self.likes
