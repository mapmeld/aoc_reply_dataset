import os
import psycopg2

# postgresql
conn = psycopg2.connect("dbname='tweetreplies'")
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS bset')
cur.execute('CREATE TABLE bset AS (SELECT * FROM combined)')
cur.execute('ALTER TABLE bset ADD COLUMN profane_text BOOLEAN')
cur.execute('UPDATE bset SET profane_text = FALSE WHERE 1 = 1')

badphrases = open('./profanity.txt', 'r').read().split('\n')
for phrase in badphrases:
    if len(phrase) > 1:
        # print(phrase)
        phrase = phrase.lower()
        cur.execute('UPDATE bset SET profane_text = TRUE WHERE screenname IN ( \
          SELECT screenname FROM bset \
          WHERE LOWER(screenname) LIKE \'%' + phrase + '%\' \
          OR LOWER(printname) LIKE \'%' + phrase + '%\' \
          OR LOWER(body) LIKE \'%' + phrase + '%\' \
        )')

cur.execute('DROP TABLE IF EXISTS bset_automl')
cur.execute("""CREATE TABLE bset_automl AS (
    SELECT REPLACE(CONCAT(CONCAT(originbody, ' || '), body), E'\n', ''), profane_text
    FROM bset
    WHERE profane_text
)
UNION (
    SELECT REPLACE(CONCAT(CONCAT(originbody, ' || '), body), E'\n', ''), profane_text
    FROM bset
    WHERE profane_text = FALSE
    ORDER BY RANDOM()
    LIMIT 15000
)""")

cur.execute('DROP TABLE IF EXISTS bset_automl_2')
cur.execute("""CREATE TABLE bset_automl_2 AS (
    SELECT REPLACE(body, E'\n', ''), profane_text
    FROM bset
    WHERE profane_text
)
UNION (
    SELECT REPLACE(body, E'\n', ''), profane_text
    FROM bset
    WHERE profane_text = FALSE
    ORDER BY RANDOM()
    LIMIT 15000
)""")
conn.commit()

# sql2csv --no-header-row --db postgres:///tweetreplies --query 'SELECT * FROM bset_automl' > all_tweets/bset_automl.csv
# sql2csv --no-header-row --db postgres:///tweetreplies --query 'SELECT * FROM bset_automl_2 WHERE LENGTH(TRIM(replace)) > 0' > all_tweets/bset_automl_2.csv

cur.execute('DROP TABLE IF EXISTS bset_azure')
cur.execute("""CREATE TABLE bset_azure AS (
    SELECT * FROM bset
    WHERE profane_text
)
UNION (
    SELECT * FROM bset
    WHERE profane_text = FALSE
    ORDER BY RANDOM()
    LIMIT 15000
)""")
conn.commit()
os.system("sql2csv --db postgres:///tweetreplies --query 'SELECT * FROM bset_azure WHERE LENGTH(TRIM(body)) > 0' > all_tweets/bset_azure.csv")
