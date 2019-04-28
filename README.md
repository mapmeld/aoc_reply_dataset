# AOC Reply Dataset

**AKA: don't read the comments**

### The Problem

Rep. Alexandria Ocasio-Cortez's '@AOC' Twitter replies are a flashpoint for polarized political discussions.

Vitriolic users are often called out for being 'bots'. I tried blocking the worst of the accounts here, but more appear here and in other popular accounts (news articles, other reps who have been featured on Fox News). I can't tell if these accounts represent real users, burner accounts to troll with until they get blocked, or organized opposition.

### Methodology

I thought it would be interesting for a machine learning program to look over many thousands of these replies. Maybe it could help filter out asinine comments everywhere on Twitter.

I don't know which users are 'bots', and I don't want to manually categorize thousands of mean Tweets, so the best route forward is unsupervised learning. Ideally, the algorithm will sum up everything into 15–25 archetypal categories, which I can then never see again.

The Twitter API doesn't support this, so I am using a userscript (GreaseMonkey / TamperMonkey) to scrape replies.

### Contributing

I include a sample JSON of replies in this repo - one JSON file will be generated
for each original AOC Tweet or Retweet. Please let me know how structure can be improved.

### License

Script is MIT-licensed. Please be aware that this doesn't use Twitter's official
API, so is likely to miss Tweets (it seems to get about 254 replies), be broken by changes to Twitter UI, or get you into trouble for breaking Twitter's ToS.
