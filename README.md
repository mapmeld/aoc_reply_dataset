# AOC Reply Dataset

**AKA: don't read the comments**

### The Problem

Rep. Alexandria Ocasio-Cortez's '@AOC' Twitter replies are a flashpoint for  political discussions.

Vitriolic users are often called out for being 'bots'. I tried blocking the worst of the accounts here, but more appear here and in other popular accounts (news articles, other reps who have been featured on Fox News). I can't tell if these accounts represent real users, burner accounts to troll with until they get blocked, or organized opposition.

### Dataset

I include a sample JSON of replies in replies_by_tweet and the full dataset in
all_tweets/ - one JSON file is generated for each original AOC Tweet or Retweet. Please let me know how structure can be improved.

The Twitter API doesn't support scraping replies, so I am using a userscript (scan.js) for the GreaseMonkey / TamperMonkey browser extension.

### Methodology

I thought it would be interesting for a machine learning program to look over many thousands of these replies. Maybe it could help filter out asinine comments everywhere on Twitter.

I don't know which users are 'bots', and I don't want to manually categorize thousands of mean Tweets. I chose two supervised learning methods (Option A and B)
and two unsupervised learning / clustering methods (Option C and D)

- basic-analysis.py counts Tweets by thread
- basic-etl.py combines all of the thread JSON files into two CSVs, has SQL comments for username = bad faith users approach
- option-b-ml.py runs SQL queries for profane text = bad faith users approach
- option-c-clusters.py uses word2vec and k-means clustering
- option-d-hierarchy.py sets up categories for hierarchical / agglomerative clustering
- environment-tweet-charts.py collects environment and name-calling topic tweets and timestamps for visualizations

### License

Script is MIT-licensed. Please be aware that this doesn't use Twitter's official
API, so is likely to get you into trouble for breaking Twitter's ToS.
It may also miss Tweets (it seems to get about 254 replies), and be broken by changes to the Twitter UI.
