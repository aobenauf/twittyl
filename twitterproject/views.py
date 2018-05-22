from django.http import HttpResponse
from django.shortcuts import render
from . import friend

def home(request):
	return render(request, 'home.html')


def tweets(request):
 
	#get the handle from the input field
	person = friend.Friend(request.GET['twitter_handle'])
	####TWEETS#####

	# tweets = person.getTweets()
	# likes = person.getLikes()

	# pos_sent =  0
	# nut_sent =  0
	# neg_sent =  0
	# #calculating sentiment of tweets and likes
	# for tweet in tweets:
	# 	if TextBlob(tweet).sentiment.polarity > 0:
	# 		pos_sent += 1
	# 	elif TextBlob(tweet).sentiment.polarity < 0:
	# 		neg_sent += 1
	# 	else:
	# 		nut_sent += 1

	# for like in likes:
	# 	if TextBlob(like).sentiment.polarity > 0:
	# 		pos_sent += 1
	# 	elif TextBlob(like).sentiment.polarity < 0:
	# 		neg_sent += 1
	# 	else:
	# 		nut_sent += 1

	pos_sent, neg_sent, nut_sent, tweets, likes = person.getSentiments()



	return render(request, 'tweets.html',{'username':person.twitter_handle,'tweets': tweets, 'likes': likes, 'positives': pos_sent,'negatives': neg_sent, 'neutrals': nut_sent})


def analysis(request):
	return render(request, 'analysis.html')