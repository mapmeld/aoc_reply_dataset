import psycopg2

# postgresql
conn = psycopg2.connect("dbname='tweetreplies'")
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS aset')
cur.execute('CREATE TABLE aset AS (SELECT * FROM combined)')
cur.execute('ALTER TABLE aset ADD COLUMN profane_text BOOLEAN')
cur.execute('UPDATE aset SET profane_text = FALSE WHERE 1 = 1')

badphrases = open('./profanity.txt', 'r').read().split('\n')
for phrase in badphrases:
    if len(phrase) > 1:
        # print(phrase)
        phrase = phrase.lower()
        cur.execute('UPDATE aset SET profane_text = TRUE WHERE screenname IN ( \
          SELECT screenname FROM aset \
          WHERE LOWER(screenname) LIKE \'%' + phrase + '%\' \
          OR LOWER(printname) LIKE \'%' + phrase + '%\' \
          OR LOWER(body) LIKE \'%' + phrase + '%\' \
        )')

cur.execute('DROP TABLE IF EXISTS aset_automl')
cur.execute("""CREATE TABLE aset_automl AS (
    SELECT REPLACE(CONCAT(CONCAT(originbody, ' || '), body), E'\n', ''), profane_text
    FROM aset
)""")

cur.execute('DROP TABLE IF EXISTS aset_automl_2')
cur.execute("""CREATE TABLE aset_automl_2 AS (
    SELECT REPLACE(body, E'\n', ''), profane_text
    FROM aset
)""")
