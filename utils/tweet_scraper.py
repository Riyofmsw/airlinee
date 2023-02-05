import snscrape.modules.twitter as sntwitter
from db import DB
from clean_text import clean_text
from classify import Classify
db = DB()
airlines = {
        'flynas':'Fly Nas',
        'flyadeal':'Fly Adeal',
        'flydubai':'Fly Dubai',
        'airarabiagroup': 'Air Arabia',
        'JazeeraAirways':'Ajazerah Airways',
    }
def tweet_scraper(query):
    query = f"(from:{query})"
    tweets = []
    limit = 100
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if  len(tweets) == limit:
            break
        elif db.is_tweet_exists(tweet.rawContent) :
            pass
        else:
            data=dict()
            cleaned_text = clean_text(tweet.rawContent)
            clean_text = clean_text.strip()
            if cleaned_text !='':
                data['tweet']=tweet.rawContent
                data['cleaned_tweet']=cleaned_text
                data['airline']=airlines[tweet.user.username]
                classify = Classify(cleaned_text)
                data['class']= classify.get_result() 
                db.insert(data)
                tweets.append(data)
    return tweets

"""
for airline in airlines.keys():
    #query = 'JazeeraAirways'
    tweet_scraper(airline)
"""
txt = clean_text('Cozy up in a Yurt nomadic house in Almaty or throw snowballs in Bishkek. Fly to a winter destination today! Book now. https://t.co/aBwYwgqT6r')
print(txt=='')