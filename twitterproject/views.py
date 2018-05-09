from django.http import HttpResponse
from django.shortcuts import render
import tweepy
from textblob import TextBlob
import pandas as pd
from datetime import datetime as dt
import config


def home(request):
	return render(request, 'home.html')


def sentiment(request):
	consumer_key = config.consumer_key
	consumer_secret = config.consumer_secret
	access_token = config.access_token
	access_token_secret = config.access_token_secret
	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token,access_token_secret)
	api = tweepy.API(auth)
	print("authentication worked")
	#get the handle from the input field
	twitter_handle = request.GET['twitter_handle']
	####TWEETS#####

	#SUDO UPDATE
	tweet_list = []
	timeline = api.user_timeline(screen_name = twitter_handle, count = 10, include_rts = False)
	for tweet in timeline:
		tweet_list.append(tweet.text)


	return render(request, 'sentiment.html',{'username':twitter_handle,'tweets': tweet_list})