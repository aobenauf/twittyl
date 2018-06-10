from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from . import friend
from rest_framework.views import APIView
from rest_framework.response import Response

buddy_name = ""

def home(request):
	#refresh the user and data?
	return render(request, 'home.html')


def tweets(request):
 
	#get the handle from the input field
	person = friend.Friend(request.GET['twitter_handle'])

	pos_sent, neg_sent, nut_sent, tweets, likes = person.getSentiments()
	buddy_name = person
	print(buddy_name.twitter_handle)

	return render(request, 'tweets.html',{'username':person.twitter_handle,'tweets': tweets, 'likes': likes, 'positives': pos_sent,'negatives': neg_sent, 'neutrals': nut_sent})


def analysis(request):
	# Send buffer in a http response the the browser with the mime type image/png set
	#picture = HttpResponse(buffer.getvalue(), content_type="image/png")
	return render(request, 'analysis.html')


class ChartData(APIView):
	authentication_classes = []
	permission_classes = []


	def get(self, request, format=None):
		buddy = friend.Friend(buddy_name)
		print("Buddy's Handle: ")
		dates, tweet_stock_data, tweet_ma_data, daily_tweet_sentiment, daily_like_sentiment = buddy.getSentimentStock()
		#print(len(dates),len(tweet_stock_data),len(tweet_ma_data))
		data = {
			"labels": dates,
			"tweet_stock": tweet_stock_data,
			"tweet_ma": tweet_ma_data,
			"daily_tweet_sentiment": daily_tweet_sentiment,
			"daily_like_sentiment": daily_like_sentiment,
		}
		
		return Response(data)