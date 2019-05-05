import json

import psycopg2
#import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
#import scipy.cluster.hierarchy as shc

interestingTerms = open('./profanity.txt', 'r').read().split('\n')
interestingTerms.append('trump')
interestingTerms.append('maga')
interestingTerms.append('nationalis')
interestingTerms.append('anon')
interestingClusters = [
['drug', 'crossing', 'asylum', 'weapons', 'roads', 'opioids', 'governments', 'ports', 'firearms', 'legal', 'criminals', 'southern', 'drugs', 'police', 'secure', 'labor', 'immigration', 'hospitals', 'fentanyl', 'armed', 'dhs', 'buildings', 'universities', 'prisons', 'patrol', 'regulations', 'illegals', 'heroin', 'enter', 'immigrants', 'murder', 'agents', 'profits', 'entry', 'systems', 'services', 'treatment', 'forces', 'homes', 'border', 'cities', 'corporations', 'individuals', 'businesses', 'illegal', 'schools', 'cross', 'protection', 'mass', 'agencies'],
['beliefs', 'allies', 'ideals', 'pockets', 'efforts', 'backs', 'values', 'hearts', 'actions', 'opinions', 'character', 'views', 'neighbors', 'colleagues', 'minds', 'soul', 'interests', 'concerns', 'arrogance', 'defense', 'behalf', 'freedoms', 'customers', 'hands', 'asses', 'feelings', 'success', 'duty', 'stance', 'existence', 'faces', 'base', 'platform', 'dreams', 'strength', 'culture', 'arguments', 'principles', 'voices', 'positions', 'hopes', 'heads', 'ancestors', 'races', 'enemies', 'body', 'brothers', 'priorities', 'intelligence', 'sisters'],
['plants', 'farms', 'methane', 'powered', 'vehicles', 'pipelines', 'panels', 'electricity', 'wind', 'solar', 'burning', 'gas', 'trucks', 'development', 'coal', 'subsidies', 'renewables', 'buildings', 'greenhouse', 'pollution', 'reducing', 'agriculture', 'grid', 'cattle', 'batteries', 'carbon', 'trains', 'vehicle', 'industries', 'inflation', 'emissions', 'supply', 'prices', 'repair', 'oil', 'oceans', 'transportation', 'renewable', 'manufacturing', 'rail', 'eliminating', 'supplies', 'industry', 'fuel', 'farm', 'homelessness', 'increasing', 'roads', 'existing', 'production'],
['misogyny', 'bigoted', 'nonsensical', 'vile', 'blatant', 'islamophobia', 'divisive', 'bigots', 'condemning', 'sexism', 'marxist', 'shameful', 'fascist', 'incompetent', 'biased', 'neo', 'sexist', 'targeting', 'bogus', 'remarks', 'classic', 'jerk', 'elitist', 'deflection', 'trope', 'childish', 'pure', 'actively', 'bias', 'tokenism', 'deplorable', 'incorrect', 'targeted', 'partisan', 'factual', 'outright', 'hamas', 'nazi', 'hack', 'gotcha', 'destructive', 'theories', 'hysterical', 'pos'],
['rates', 'pensions', 'salaries', 'subsidies', 'wages', 'employees', 'businesses', 'revenue', 'benefits', 'mortgages', 'tuition', 'financing', 'income', 'medicaid', 'private', 'fees', 'costs', 'profits', 'retirement', 'sector', 'housing', 'services', 'rent', 'prices', 'debt', 'property', 'minimum', 'increase', 'workers', 'homes', 'funding', 'sales', 'bankruptcy', 'payment', 'treatment', 'roads', 'budget', 'hospitals', 'prisons', 'expenses', 'labor', 'employment', 'industry', 'local', 'transportation', 'regulations', 'companies', 'supplies', 'cuts', 'additional'],
['minorities', 'folks', 'ppl', 'politicians', 'women', 'men', 'americans', 'idiots', 'fools', 'liberals', 'groups', 'moderates', 'victims', 'babies', 'ones', 'girls', 'others', 'people', 'leftists', 'blacks', 'muslims', 'congressmen', 'whites', 'latinos', 'billionaires', 'progressives', 'families', 'types', 'poc', 'males', 'individuals', 'places', 'christians', 'whom', 'conservatives', 'radicals', 'communities', 'sheep', 'freshmen', 'criminals', 'terrorists', 'socialists', 'ladies', 'numbers', 'students', 'voters', 'repubs', 'those', 'jews', 'incumbents'],
['primaries', 'primary', 'dem', 'senate', 'caucus', 'candidate', 'democrat', 'establishment', 'elections', 'democratic', 'governor', 'candidates', 'blue', 'republican', 'senators', 'voters', 'kkk', 'party', 'presidential', 'progressive', 'red', 'virginia', 'incumbents', 'iowa', 'swing', 'general', 'state', 'registered', 'seats', 'opposition', 'districts', 'votes', 'present', 'voting', 'minnesota', 'representatives', 'house', 'election', 'reps', 'michigan', 'congressional', 'district', 'dems', 'democrats', 'repubs', 'dnc', 'moderate', 'mayor', 'states', 'minority'],
['clown', 'bigot', 'pos', 'asshole', 'loser', 'phony', 'villain', 'commie', 'narcissist', 'activist', 'actor', 'deflection', 'crook', 'hack', 'moron', 'utter', 'tool', 'genius', 'con', 'hypocrite', 'absolute', 'badass', 'liar', 'spoiled', 'actress', 'dictator', 'wit', 'traitor', 'star', 'disgrace', 'annoying', 'jerk', 'supporter', 'lunatic', 'epic', 'dumbass', 'puppet', 'uneducated', 'gotcha', 'embarrassment', 'patriot', 'pompous', 'twit', 'quoting', 'fascist', 'elitist', 'analogy', 'inspiration', 'shameful', 'deplorable']
]

# postgresql
conn = psycopg2.connect("dbname='tweetreplies'")
cur = conn.cursor()
cur.execute('SELECT string_agg(body, \' | \') AS body FROM combined GROUP BY screenname LIMIT 10000')

tweetstats = []
alltweets = []
for tweet in cur.fetchall():
    body = tweet[0]
    if body is not None:
        alltweets.append(body)
        body = body.lower()
        tweetstat = []
        for phrase in interestingTerms:
            if len(phrase) > 0:
                tweetstat.append(body.count(phrase))
        for cluster in interestingClusters:
            clusterCount = 0
            for phrase in cluster:
                clusterCount += body.count(phrase)
            tweetstat.append(clusterCount)
        tweetstats.append(tweetstat)

X = np.array(tweetstats)

cluster = AgglomerativeClustering(n_clusters=30, affinity='euclidean', linkage='ward')
cluster.fit_predict(X)

userorder = 0
grouped_users = []
for clusterer in range(0, 30):
    grouped_users.append([])
for cluster in cluster.labels_:
    usertweets = alltweets[userorder]
    if len(grouped_users[cluster]) < 10:
        grouped_users[cluster].append(usertweets)
    userorder += 1
outclusters = open('hierclusters.json','w')
outclusters.write(json.dumps(grouped_users))
