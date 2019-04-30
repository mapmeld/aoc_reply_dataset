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

"""
APPROACH A
"""

"""
APPROACH B

SELECT COUNT(*), screenname FROM replies
    WHERE LOWER(screenname) LIKE '%trump%' OR LOWER(printname) LIKE '%trump%'
        OR LOWER(screenname) LIKE '%maga%' OR LOWER(printname) LIKE '%maga%'
        OR LOWER(screenname) LIKE '%anon%' OR LOWER(printname) LIKE '%anon%'
        OR screenname ~ '\d\d\d$' OR printname ~ '\d\d\d\d\d$'
    GROUP BY screenname
    ORDER BY COUNT(*) DESC;

WITH funusers AS (
    SELECT COUNT(*) AS count, screenname FROM replies
        WHERE LOWER(screenname) LIKE '%trump%' OR LOWER(printname) LIKE '%trump%'
            OR LOWER(screenname) LIKE '%maga%' OR LOWER(printname) LIKE '%maga%'
            OR LOWER(screenname) LIKE '%anon%' OR LOWER(printname) LIKE '%anon%'
            OR screenname ~ '\d\d\d$' OR printname ~ '\d\d\d\d\d$'
        GROUP BY screenname
        ORDER BY COUNT(*)
)
SELECT AVG(count) FROM funusers;

SELECT COUNT(*) FROM replies
    WHERE LOWER(screenname) LIKE '%trump%' OR LOWER(printname) LIKE '%trump%'
        OR LOWER(screenname) LIKE '%maga%' OR LOWER(printname) LIKE '%maga%'
        OR LOWER(screenname) LIKE '%anon%' OR LOWER(printname) LIKE '%anon%'
        OR screenname ~ '\d\d\d$' OR printname ~ '\d\d\d\d\d$';

DROP TABLE IF EXISTS bset;
CREATE TABLE bset AS (SELECT * FROM combined);
ALTER TABLE bset ADD COLUMN skeptical_name BOOLEAN;
UPDATE bset SET skeptical_name = FALSE WHERE 1 = 1;
UPDATE bset SET skeptical_name = TRUE WHERE
        LOWER(screenname) LIKE '%trump%' OR LOWER(printname) LIKE '%trump%'
        OR LOWER(screenname) LIKE '%maga%' OR LOWER(printname) LIKE '%maga%'
        OR LOWER(screenname) LIKE '%anon%' OR LOWER(printname) LIKE '%anon%'
        OR screenname ~ '\d\d\d$' OR printname ~ '\d\d\d\d\d$';

DROP TABLE IF EXISTS bset_automl;
CREATE TABLE bset_automl AS (
    SELECT REPLACE(CONCAT(CONCAT(originbody, ' || '), body), E'\n', ''), skeptical_name
    FROM bset
);

DROP TABLE IF EXISTS bset_automl_2;
CREATE TABLE bset_automl_2 AS (
    SELECT REPLACE(body, E'\n', ''), skeptical_name
    FROM bset
);
"""

# sql2csv --db postgres:///tweetreplies --query 'SELECT * FROM bset_automl LIMIT 99000' > all_tweets/bset_automl.csv
# sql2csv --db postgres:///tweetreplies --query 'SELECT * FROM bset_automl_2 WHERE LENGTH(TRIM(replace)) > 0 LIMIT 99000' > all_tweets/bset_automl_2.csv
