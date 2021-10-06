import os
import requests

error_output = {
    "status": 404,
    "message": "tweets not found"
}

base_url="https://api.twitter.com/1.1/"

query={}
bearer_token = os.environ['BEARER_TOKEN']

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


# outputs 10 latest tweets by the user screen name
def get_tweets_by_username(username):

    example="GET https://api.twitter.com/1.1/statuses/lookup.json?id=20,1050118621198921728"
    endpoint = f"{base_url}statuses/user_timeline.json?screen_name={username}&count=10"
    
    resp = requests.request("GET",endpoint,auth= bearer_oauth)

    if resp.status_code in (200,202):

        tweets = []     # list of dictionary
        twitter_data = resp.json()

        ## store tweets
        for tweet_data in twitter_data:
            tweets.append({
                    "created_at": tweet_data["created_at"],
                    "text": tweet_data["text"] 
            })

        return {
            "user_name": twitter_data[0]['user']['name'],
            "user_screen_name": twitter_data[0]['user']['screen_name'],
            "followers_count": twitter_data[0]['user']['followers_count'],
            "friends_count": twitter_data[0]['user']['friends_count'],
            "tweets": tweets
        }
    else:
        return error_output,404

####################################################################
