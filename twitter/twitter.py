import os
import requests

error_output = {
    "status": 404,
    "message": "tweets not found"
}

base_url="https://api.twitter.com/1.1/"

query={}
bearer_token = os.environ['BEARER_TOKEN']

## authentication function
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


######################################################################################
# outputs 10 latest tweets by the user screen name
def get_tweets_by_username(username):

    endpoint = f"{base_url}statuses/user_timeline.json?screen_name={username}&count=10"
    
    resp = requests.request("GET",endpoint,auth= bearer_oauth,verify=False)

    if resp.status_code in (200,202):

        tweets = []     # list of dictionary
        twitter_data = resp.json()

        if not twitter_data:
            return error_output,404

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
        },200
    else:
        return error_output,404


####################################################################
## search tweet by hashtags ##
def tweets_hashtag(hashtag):
    
    endpoint = f"{base_url}/search/tweets.json?q=%23{hashtag}&count=10&result_type=recent"
    resp = requests.request("GET",endpoint,auth= bearer_oauth,verify=False)
    
    print(resp.status_code)
    if resp.status_code in (200,202):

        data = resp.json()
        output = []

        for tweet in data["statuses"]:
            output.append({
                "text":tweet["text"],
                "user_screen_name":tweet["user"]["screen_name"],
                "retweet_count":tweet["retweet_count"],
            })
        
        return output,200
    else:
        return error_output,404

#####################################################################
## show tweets in given radius of lat,lon ##
def geoloc(lat,lon,radius):

    endpoint = f"{base_url}/search/tweets.json?geocode={lat},{lon},{radius}&count=10&result_type=recent"
    resp = requests.request("GET",endpoint,auth= bearer_oauth,verify=False)

    if resp.status_code in (200,202):

        data = resp.json()
        output = []

        for tweet in data["statuses"]:
            output.append({
                "text": tweet["text"],
                "user_screen_name": tweet["user"]["screen_name"]
            })
        
        return output,200
    else:
        return error_output,404

##################################################################