# Creating a class for the data to be housed
class Friend(twitter_handle_request):
	twitter_handle = twitter_handle_request

	def getTweets(self, twitter_handle):
		tweet_list = []
		timeline = api.user_timeline(screen_name = twitter_handle, count = 10, include_rts = False)
		for tweet in timeline:
			tweet_list.append(tweet.text)


	def getLikes(self, twitter_handle):
		likes_list = []
		#for i in range(1,1):
		likes_per_page = api.favorites(twitter_handle,page=1)
		#pages_of_likes.append(likes_per_page)
		for like in likes_per_page:
			likes_list.append(like.text)
