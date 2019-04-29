# basic analysis, first steps

import os, json

totalcount = 0
tweets = os.listdir('./all_tweets')
for tweet in tweets:
    if '.json' in tweet:
        d = json.loads(open('./all_tweets/' + tweet, 'r').read())
        totalcount += len(d['replies'])
print(totalcount)
