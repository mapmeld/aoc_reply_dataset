# ETL JSON files into CSV and PostgreSQL

# run once
#   pip install csvkit psycopg2
#   initdb dataaoc
#   postgres -D dataaoc/
#   createdb tweetreplies

import os, csv, json
import psycopg2

tweets = os.listdir('./all_tweets')


with open('./all_tweets/origin_tweets.csv', 'w') as csv1:
    originTweets = csv.writer(csv1)
    originTweets.writerow(['tweetid','timestamp','printname','screenname','verified','body','quotescreenname','quotetext','likes','retweets'])

    with open('./all_tweets/replies.csv', 'w') as csv2:
        replyTweets = csv.writer(csv2)
        replyTweets.writerow(['tweetid','convoid','timestamp','printname','screenname','verified','mentions','cards','body','lang','links','likes','retweets'])

        seenOrigins = {}
        seenReplies = {}

        for tweet in tweets:
            if '.json' in tweet:
                d = json.loads(open('./all_tweets/' + tweet, 'r').read())
                origin = d['origin']
                tweetid = origin[0]
                if tweetid not in seenOrigins:
                    originTweets.writerow(origin)
                    seenOrigins[tweetid] = True

                replies = d['replies']
                for reply in replies:
                    tweetid = reply[0]
                    if tweetid not in seenReplies:
                        replyTweets.writerow(reply)
                        seenReplies[tweetid] = True


os.system('csvsql --insert --overwrite --db postgresql:///tweetreplies ./all_tweets/origin_tweets.csv')
os.system('csvsql --insert --overwrite --db postgresql:///tweetreplies ./all_tweets/replies.csv')

# psql tweetreplies
"""
DROP TABLE IF EXISTS origins;
DROP TABLE IF EXISTS combined;
CREATE TABLE origins AS (
    SELECT tweetid AS originid, timestamp AS origintime, printname AS originname,
    screenname AS originsn, verified AS originverified, body AS originbody,
    quotescreenname, quotetext, likes AS originlikes, retweets AS originretweets
    FROM origin_tweets
);
CREATE TABLE combined AS (
    SELECT * FROM replies
    JOIN origins ON replies.convoid = origins.originid
);
"""
