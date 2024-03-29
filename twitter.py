import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = '#####'
		consumer_secret = '#####'
		access_token = '#####'
		access_token_secret = '#####'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret,access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
			print("ALL GOOD")
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))		
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query1, query2, count=10):
		'''
		Main function to fetch tweets and parse them.
		'''
		tweets = []
		print(query1, query2)	
		print(type(query1), type(query2))

		# "'Apple''Semiconductor'-filter:retweets AND -filter:replies AND -filter:links"
		# search_query = f"{query1}{query2}-filter:retweets AND -filter:replies AND -filter:links"
		search_query = "'Apple''Semiconductor'-filter:retweets AND -filter:replies AND -filter:links"

		no_of_tweets = 100
		print(search_query, type(search_query))

		try:
			#The number of tweets we want to retrieved from the search
			fetched_tweets = self.api.search_tweets(q=search_query, lang="en", count=10, tweet_mode ='extended', until='2024-03-07')
			print("NOTHING HERE")

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}
				# saving text of tweet
				print("2\n")
				parsed_tweet['text'] = tweet.full_text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)
				print("3\n")

				# appending parsed tweet to tweets list
				tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets			

			# #Pulling Some attributes from the tweet
			# attributes_container = [[tweet.user.name, tweet.created_at, tweet.favorite_count, tweet.source, tweet.full_text] for tweet in tweets]

			# #Creation of column list to rename the columns in the dataframe
			# columns = ["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"]

			# #Creation of Dataframe
			# tweets_df = pd.DataFrame(attributes_container, columns=columns)
		except BaseException as e:
			print('Status Failed On,',str(e))

		# try:
		# 	# call twitter api to fetch tweets
		# 	fetched_tweets1 = self.api.search_tweets(q=query1+"#"+query1+"-filer:retweets AND -filter:replies AND -filter:links", lang="en", tweet_mode=extended, count=count)
		# 	fetched_tweets2 = self.api.search_tweets(q=query2+"#"+query2+"-filer:retweets AND -filter:replies AND -filter:links", lang="en", tweet_mode=extended, count=count)
		# 	fetched_tweets = fetched_tweets1 + fetched_tweets2
		# 	print("1")

		# 	if fetched_tweets:
		# 		# parsing tweets one by one
		# 		for tweet in fetched_tweets:
		# 			# empty dictionary to store required params of a tweet
		# 			parsed_tweet = {}

		# 			# saving text of tweet
		# 			parsed_tweet['text'] = tweet.statuses.text
		# 			# saving sentiment of tweet
		# 			parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.statuses.text)
		# 			print("2")

		# 			# appending parsed tweet to tweets list
		# 			if tweet.retweet_count > 0:
		# 				# if tweet has retweets, ensure that it is appended only once
		# 				if parsed_tweet not in tweets:
		# 					tweets.append(parsed_tweet)
		# 					print("3")
		# 			else:
		# 				tweets.append(parsed_tweet)

		# 			# return parsed tweets
		# 			print("4")
		# 			return tweets

		# except Exception as e:
		# 	# Handle the exception
		# 	print("Error3 : " + str(e))
