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

	twitter_handle = ""


	def __init__(self, twitter_handle):
		self.twitter_handle = twitter_handle

	def getTweets(self):
		tweet_dict = {}
		timeline = api.user_timeline(screen_name = self.twitter_handle, count = 25, include_rts = False)
		for tweet in timeline:
			if tweet.text[0] == "@":
				#exclude tweets from the latest 10 tweets part
				pass
			else:
				tweet_dict[tweet.text] = round(TextBlob(tweet.text).sentiment.polarity,2)


		#only return latest 10 tweets
		#tweet_list_trim = tweet_list[:10]

		return tweet_dict


	def getLikes(self):

		likes_list = []
		likes_dict = {}
		#for i in range(1,1):
		likes_per_page = api.favorites(self.twitter_handle,page=1)
		#pages_of_likes.append(likes_per_page)
		for like in likes_per_page:
			likes_list.append(like.text)

		likes_list_trim = likes_list[:10]

		for like in likes_list_trim:
			likes_dict[like] = round(TextBlob(like).sentiment.polarity,2)

		return likes_dict


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

	def getSentimentStock(self):

		self.dates = []
		self.tweet_stock = []
		self.tweet_ma = []
		self.daily_tweet_sentiment = []
		self.daily_like_sentiment = []

		timeline = api.user_timeline(screen_name = self.twitter_handle, count = 100, include_rts = True)

		#analysis on tweets liked
		pages_of_likes = []
		#collecting the first five pages which should be about 100 likes
		for i in range(1,2):
		    likes_per_page = api.favorites(self.twitter_handle,page=i)
		    pages_of_likes.append(likes_per_page)

		tweets = {}
		retweets = {}
		replies = {}
		tweet_ids = {}
		tweet_detail = {}

		#to get tweet id per date
		for tweet in timeline:
		    date = tweet.created_at.strftime('%m/%d/%y')
		    if date in tweet_ids:
		        tweet_ids[date].append(tweet.id)
		    else:
		        
		        tweet_ids[date] = []
		        tweet_ids[date].append(tweet.id)
		        
		#to get tweet text per tweet id
		for tweet in timeline:
		    tweet_id = tweet.id
		    if tweet_id in tweet_detail:
		        tweet_detail[tweet_id] = tweet.text
		    else:     
		        tweet_detail[tweet_id] = tweet.text

		#for tweet sentiment per each date for tweets, retweets and replies
		for tweet in timeline:
		    date = tweet.created_at.strftime('%m/%d/%y')
		    if tweet.retweeted == True:
		        if date in retweets:
		            retweets[date] += TextBlob(tweet.text).sentiment.polarity
		        else:
		            retweets[date] = TextBlob(tweet.text).sentiment.polarity
		    elif tweet.in_reply_to_status_id != None:
		        if date in replies:
		            replies[date] += TextBlob(tweet.text).sentiment.polarity
		        else:
		            replies[date] = TextBlob(tweet.text).sentiment.polarity
		    else:
		        if date in tweets:
		            tweets[date] += TextBlob(tweet.text).sentiment.polarity
		        else:
		            tweets[date] = TextBlob(tweet.text).sentiment.polarity
		    
		#consolidating the sentiment for each day for tweets,retweets and replies
		tweet_sentiment = {}
		for k, v in retweets.items():
		    if k in tweet_sentiment:
		        tweet_sentiment[k] += v
		    else:
		        tweet_sentiment[k] = v
		        
		for k, v in tweets.items():
		    if k in tweet_sentiment:
		        tweet_sentiment[k] += v
		    else:
		        tweet_sentiment[k] = v
		        
		for k, v in replies.items():
		    if k in tweet_sentiment:
		        tweet_sentiment[k] += v
		    else:
		        tweet_sentiment[k] = v

		#starting Like data collection
		likes = {}
		like_ids = {}   #date: ID
		like_detail = {}   #ID: Text
		like_sentiment = {} #date: sentiment

		#this is to create the like_ids for each tweet
		for page in pages_of_likes:
		    for like in page:
		        date = like.created_at.strftime('%m/%d/%y')
		        if date in like_ids:
		            like_ids[date].append(like.id)
		        else:
		            like_ids[date] = []
		            like_ids[date].append(like.id)
		        
		#to get tweet text per tweet id
		for page in pages_of_likes:
		    for like in page:
		        like_id = like.id
		        if like_id in like_detail:
		            like_detail[like_id] = like.text
		        else:     
		            like_detail[like_id] = like.text

		            
		            
		#this is to get the sentiment of each tweet
		for page in pages_of_likes:
		    for like in page:
		        date = like.created_at.strftime('%m/%d/%y')

		        if date in like_sentiment:
		            like_sentiment[date] += TextBlob(like.text).sentiment.polarity
		        else:
		            like_sentiment[date] = TextBlob(like.text).sentiment.polarity

		#creating dataframe of sentiment
		like_sentiment_df = pd.DataFrame.from_dict(like_sentiment, orient='index')
		like_sentiment_df.columns = ['like_sentiment']
		like_sentiment_df['date'] = like_sentiment_df.index
		tweet_sentiment_df = pd.DataFrame.from_dict(tweet_sentiment, orient='index')
		tweet_sentiment_df.columns = ['tweet_sentiment']
		tweet_sentiment_df['date'] = tweet_sentiment_df.index

		#joined dataframes on the date column (first column index 0)
		sentiment_df = like_sentiment_df.join(tweet_sentiment_df, on='date', how="outer", lsuffix='like', rsuffix='tweet')
		sentiment_df = sentiment_df.drop(['datelike','datetweet'], axis=1)
		sentiment_df['tweet_sentiment'] = sentiment_df['tweet_sentiment'].fillna(0)
		sentiment_df['like_sentiment'] = sentiment_df['like_sentiment'].fillna(0)
		sentiment_df['daily_sentiment'] = sentiment_df['like_sentiment'] + sentiment_df['tweet_sentiment']
		sentiment_df['date'] =pd.to_datetime(sentiment_df.date)
		sentiment_df = sentiment_df.sort_values(by=['date'])
		sentiment_df['MA'] = sentiment_df['daily_sentiment'].rolling(window=5).mean()
		sentiment_df = sentiment_df.sort_values(by=['date'])
		sentiment_df['date'] = sentiment_df['date'].dt.strftime('%m/%d/%y')
		#calculating sentiment stock (how sentiment is trending over time)
		sentiment_df['tweet_stock'] = sentiment_df.tweet_sentiment.cumsum()
		sentiment_df['like_stock'] = sentiment_df.like_sentiment.cumsum()
		sentiment_df['sentiment_stock'] = sentiment_df.daily_sentiment.cumsum()
		#sentiment_df['SS_MA'] = sentiment_df['sentiment_stock'].rolling(window=10).mean()
		sentiment_df['tweet_ma'] = sentiment_df['tweet_stock'].rolling(window=10).mean().fillna(0)
		#sentiment_df['like_ma'] = sentiment_df['like_stock'].rolling(window=10).mean()

		self.dates = sentiment_df['date'].tolist()
		self.tweet_stock = sentiment_df['tweet_stock'].tolist()
		self.tweet_ma = sentiment_df['tweet_ma'].tolist()
		self.daily_tweet_sentiment = sentiment_df['tweet_sentiment']
		self.daily_like_sentiment = sentiment_df['like_sentiment']

		return self.dates, self.tweet_stock, self.tweet_ma, self.daily_tweet_sentiment, self.daily_like_sentiment