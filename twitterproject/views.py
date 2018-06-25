from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from . import friend
from rest_framework.views import APIView
from rest_framework.response import Response

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

	return render(request, 'analysis.html', {'tweets': tweet_detail_dict, 'likes': like_detail_dict})


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