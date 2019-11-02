# pip3 install snorkel pandas
import pandas
from snorkel.labeling import labeling_function, LabelModel, PandasLFApplier

ABSTAIN = -1
LESS_WEIRD = 0
WEIRD = 1

df_train = pandas.read_csv("all_tweets/replies.csv")
print(df_train.head())

profanity = ['asshole', 'shit', 'maga', 'illegals']
conspiracy = ['qanon', 'wwg1wga', 'actress']
nice = ['good fight', 'smart', 'thank']

@labeling_function()
def lf_tweet_profane(x):
    for swear in profanity:
        if swear in str(x.body).lower():
            return WEIRD
    return ABSTAIN

@labeling_function()
def lf_screenname_profane(x):
    for swear in profanity:
        if swear in str(x.screenname).lower():
            return WEIRD
    return ABSTAIN

@labeling_function()
def lf_printname_profane(x):
    for swear in profanity:
        if swear in str(x.printname).lower():
            return WEIRD
    return ABSTAIN

@labeling_function()
def lf_tweet_conspiracy(x):
    for con in conspiracy:
        if con in str(x.body).lower():
            return WEIRD
    return ABSTAIN

@labeling_function()
def lf_printname_conspiracy(x):
    for con in conspiracy:
        if con in str(x.printname).lower():
            return WEIRD
    return ABSTAIN

@labeling_function()
def lf_screenname_conspiracy(x):
    for con in conspiracy:
        if con in str(x.screenname).lower():
            return WEIRD
    return ABSTAIN

@labeling_function()
def lf_nice(x):
    for friend in nice:
        if friend in str(x.body).lower():
            return LESS_WEIRD
    return ABSTAIN

lfs = [
    lf_tweet_profane, lf_printname_profane, lf_screenname_profane,
    lf_tweet_conspiracy, lf_printname_conspiracy, lf_screenname_conspiracy
]
applier = PandasLFApplier(lfs)
L_train = applier.apply(df_train)
label_model = LabelModel(cardinality=2, verbose=True)
label_model.fit(L_train, n_epochs=500, log_freq=50, seed=123)

df_train["label"] = label_model.predict(L=L_train, tie_break_policy="abstain")
df_train = df_train[df_train.label != ABSTAIN]
print(str(df_train["label"]) + "\t" + str(df_train["body"]))
