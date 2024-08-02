import tweepy
import csv

# Credentials
API_KEY = 'your_api_key'
API_SECRET_KEY = 'your_api_secret_key'
BEARER_TOKEN = 'your_bearer_token'

# Authentication
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Target
username = 'twitter_username'
user = client.get_user(username=username)
user_id = user.data.id
count = 000  # Number of tweets to scrape

# Write to CSV
with open(f'{username}_tweets.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Username', 'Hyperlink', 'Timestamp', 'Full Text', 'Type'])

    # Fetch Tweets
    next_token = None
    fetched_tweets = 0

    while fetched_tweets < count:
        response = client.get_users_tweets(
            id=user_id,
            max_results=min(100, count - fetched_tweets),
            pagination_token=next_token,
            tweet_fields=['created_at', 'referenced_tweets']
        )

        if not response.data:
            break

        for tweet in response.data:
            tweet_type = 'Native Post'
            if tweet.referenced_tweets:
                if tweet.referenced_tweets[0].type == 'replied_to':
                    tweet_type = 'Reply Tweet'
                elif tweet.referenced_tweets[0].type == 'retweeted':
                    tweet_type = 'Retweet'
            
            writer.writerow([username, f'https://twitter.com/{username}/status/{tweet.id}', tweet.created_at, tweet.text, tweet_type])

        fetched_tweets += len(response.data)
        next_token = response.meta.get('next_token')
        if not next_token:
            break

print(f'Successfully saved tweets to {username}_tweets.csv')
