# pip install psycopg2
import json

import psycopg2

# postgresql
conn = psycopg2.connect("dbname='tweetreplies'")
cur = conn.cursor()

envirowords = [
    'temperature',
    'cooling',
    'disasters',
    'weather',
    'natural',
    'warming',
    'flooding',
    'nasa',
    'extinction',
    'greenhouse',
    'emissions',
    'snow',
    'catastrophic',
    'paris accord',
    'climate',
    'climatechange',
    'floods',
    'disaster',
    'rain',
    'predictions',
    'sun',
    'scientific',
    'flood',
    'epidemic',
    'burning',
    'atmosphere',
    'worldwide',
    'hurricanes',
    'methane',
    'cycle',
    'fires',
    'melting',
    'sea',
    'winter',
    'oceans',
    'effects',
    'pollution',
    'science',
    'carbon',
    'green new deal',
    'gnd'
]

badwords = [
    'clown',
    'bigot',
    'asshole',
    'loser',
    'phony',
    'villain',
    'commie',
    'narcissist',
    'actor',
    'crook',
    'moron',
    'hypocrite',
    'liar',
    'spoiled',
    'actress',
    'dictator',
    'traitor',
    'disgrace',
    'annoying',
    'jerk',
    'lunatic',
    'dumbass',
    'puppet',
    'embarrassment',
    'fascist',
    'elitist'
]

tstamps = []
cur.execute('SELECT timestamp FROM combined WHERE LOWER(body) LIKE \'%'
    + '%\' OR LOWER(body) LIKE \'%'.join(envirowords)
    + '%\' ORDER BY timestamp')
for row in cur.fetchall():
    tstamps.append(int(row[0]))
#print(tstamps)

opt = open('visualize-green/all-environment.json', 'w')
opt.write(json.dumps(tstamps))

tstamps2 = []
bysource = {}
badbysource = {}
cur.execute('SELECT origintime, originid FROM origins \
    WHERE originsn = \'AOC\' AND LOWER(originbody) LIKE \'%'
        + '%\' OR LOWER(originbody) LIKE \'%'.join(envirowords)
        + '%\' ORDER BY originid')
for row in cur.fetchall():
    tstamps2.append(row[0])
    bysource[int(row[1])] = []
    badbysource[int(row[1])] = []

opt = open('visualize-green/origin-environment.json', 'w')
opt.write(json.dumps(tstamps2))

for sourceTweet in bysource.keys():
    cur.execute('SELECT timestamp FROM combined \
        WHERE originid = \'' + str(sourceTweet) + '\' \
        AND (LOWER(body) LIKE \'%'
        + '%\' OR LOWER(body) LIKE \'%'.join(envirowords)
        + '%\') ORDER BY timestamp')
    for row in cur.fetchall():
        bysource[sourceTweet].append(int(row[0]))

    cur.execute('SELECT timestamp FROM combined \
        WHERE originid = \'' + str(sourceTweet) + '\' \
        AND (LOWER(body) LIKE \'%'
        + '%\' OR LOWER(body) LIKE \'%'.join(badwords)
        + '%\') ORDER BY timestamp')
    for row in cur.fetchall():
        badbysource[sourceTweet].append(int(row[0]))

opt = open('visualize-green/replies-by-tstamp.json', 'w')
opt.write(json.dumps({ "green": bysource, "bad": badbysource }))
