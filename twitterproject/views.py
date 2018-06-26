from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from . import friend
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime as dt
import pandas as pd

#initialize a friend with no twitter handle at first
person = friend.Friend("")

def home(request):
	#refresh the user and data?
	return render(request, 'home.html')


def tweets(request):
	#get the handle from the input field, assign it to the class to use in APIview
	person.twitter_handle = request.GET['twitter_handle']
	
	pos_sent, neg_sent, nut_sent, tweets, likes = person.getSentiments()
	buddy_name = person
	#print(buddy_name.twitter_handle)

	return render(request, 'tweets.html',{'username':person.twitter_handle,'tweets': tweets, 'likes': likes}) #, 'positives': pos_sent,'negatives': neg_sent, 'neutrals': nut_sent


def analysis(request):
	#analysis_df = person.friend_df
	tweet_detail_dict = person.tweet_detail
	like_detail_dict = person.like_detail

	start_date = dt.datetime.strptime('6/14/18', '%m/%d/%y')
	end_date = dt.datetime.strptime('6/22/18', '%m/%d/%y')

	#filter the tweets on a date window
	new_tweets = filter_dicts(tweet_detail_dict, start_date, end_date)
	new_likes = filter_dicts(like_detail_dict, start_date, end_date)

	return render(request, 'analysis.html', {'tweets': new_tweets, 'likes': new_likes})


class ChartData(APIView):
	authentication_classes = []
	permission_classes = []


	def get(self, request, format=None):
		#pulling twitter handle that was pulled in "tweets" pull request and stored in the Friend class init 'person'
		buddy = friend.Friend(person.twitter_handle)
		dates, tweet_stock_data, tweet_ma_data, daily_tweet_sentiment, daily_like_sentiment, like_stock, like_ma, likes_dates, tweet_detail, like_detail = buddy.getSentimentStock()
		person.tweet_detail = tweet_detail
		person.like_detail = like_detail
		#print(len(dates),len(tweet_stock_data),len(tweet_ma_data))
		data = {
			"labels": dates,
			"tweet_stock": tweet_stock_data,
			"tweet_ma": tweet_ma_data,
			"daily_tweet_sentiment": daily_tweet_sentiment,
			"daily_like_sentiment": daily_like_sentiment,
			"like_stock": like_stock,
			"like_ma": like_ma,
			"likes_dates": likes_dates
		}
		return Response(data)

def filter_dicts(dictionary_of_tweets, start_date, end_date):

	df= pd.DataFrame.from_dict(dictionary_of_tweets,orient='index')
	df.columns= ['sentiment', 'retweets', 'favorites', 'name', 'twitter_handle', 'profile_image', 'date']
	df['tweet_text'] = df.index
	df_2 = df.set_index(pd.DatetimeIndex(df['date'])).sort_index(ascending=True)


	mask = (df_2.index > start_date) & (df_2.index <= end_date)
	df_3 = df_2.loc[mask]

	print('Original Data: ' + str(len(df_2)))
	print('Filtered Data: ' + str(len(df_3)))

	filtered_tweet_dict = {}
	#load data back into dictionaries
	for index, row in df_3.iterrows():
	    filtered_tweet_dict[row['tweet_text']] = row['sentiment']
	    filtered_tweet_dict[row['tweet_text']] = row['retweets']
	    filtered_tweet_dict[row['tweet_text']] = row['favorites']
	    filtered_tweet_dict[row['tweet_text']] = row['name']
	    filtered_tweet_dict[row['tweet_text']] = row['twitter_handle']
	    filtered_tweet_dict[row['tweet_text']] = row['profile_image']
	    filtered_tweet_dict[row['tweet_text']] = row['date']

	return filtered_tweet_dict