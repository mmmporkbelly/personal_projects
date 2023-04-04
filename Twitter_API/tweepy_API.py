#!/usr/bin/env python3
import tweepy

# Reference the API v2 Tweepy Documentation here:
# https://docs.tweepy.org/en/stable/index.html

# ====== #

# Enter Authentication information here:
# NOTE: Consumer Key/Secret is another name for API Key/Secret
client = tweepy.Client(
    bearer_token='',
    consumer_key='',
    consumer_secret='',
    access_token='',
    access_token_secret='')

try:
    me = client.get_me()

    # If authentication worked, you should get your @ name returned here
    print(f"Your Name Is: {me[0]['name']}")
    print("Authentication OK")
    print("\n====\n")
    
except:
    print("Error during authentication")
    
    #Uncomment the below line for detailed error information
    raise

# ====== #

# Tweet With the API
'''ENTER YOUR CODE HERE'''
# Tweet With the API --- Advanced Lab exercise
userWords = input("\nWhat Do you want to say? (Leave Blank To Skip): ")
if userWords != '':
    try:
        client.create_tweet(text=userWords)
    except:
        print("New Tweet Failed")
        # Uncomment the below line for detailed error information
        raise
elif userWords == '':
    print("Skipped...")
    print("\n====\n")
# ====== #

# Read Tweets with the API
try:
    timeLine = client.get_home_timeline(max_results=5)

    i = 1
    for tweet in timeLine[0]:
        print(f"Tweet #{i}:")
        print(tweet)
        print("\n+++++\n")
    i += 1

except:
    print("Timeline Read Failed")
    # Uncomment the below line for detailed error information
    raise
